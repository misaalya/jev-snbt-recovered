#!/usr/bin/env python3
"""Turn the extracted questions into TypeSafe System One request payloads.

One request per question. Nothing is sent here: this writes JSONL that the
runner posts to https://api.typesafe.ai/v1/systemone, so the exact payload that
produced a score stays inspectable.

Two item types need two different shapes:

  mcq            -> one Choice, criteria = the item's own options (a..e, or
                    a..d for PK's quantity comparisons). Nothing synthesised.
  table_yes_no   -> one request carrying N Noul questions over the same state,
                    one per statement. The docs recommend exactly this for
                    several independent yes/no labels on one input.

PK q01, q02 and q18 print no options in the source. A Choice needs a fixed set
of criteria, so those three would require invented distractors; they are
skipped and reported as skipped.

Scoring rules the runner should apply, kept here so they travel with the
payloads:

  mcq           correct iff answers[q].choice == key
  table_yes_no  per statement: (noul >= 0.5) == (key == "Ya")
                item is correct only if every statement is correct
                (baseline 12.5% for 3 statements, comparable to a 5-option mcq
                at 20%; the per-statement number, baseline 50%, is reported
                separately and never mixed into the headline)
"""

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _env  # noqa: E402  - local helper, no dependency

_env.load()

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = os.environ.get("TYPESAFE_MODEL", "jev-latest")


def build_state(q: dict) -> dict:
    """Everything the model needs to answer, as named fields.

    A table_yes_no stem is pure interface text ("Klik pilihan kolom di sebelah
    kanan ..."), so it is left out: the judgment lives in the statements, and
    the stem would only add noise to the state.
    """
    state: dict = {}
    if q["passages"]:
        state["bacaan"] = [
            {k: v for k, v in (("teks", p["text"]), ("keterangan_gambar", p["figure_note"])) if v}
            for p in q["passages"]
        ]
    if q["figure_note"]:
        state["keterangan_gambar"] = q["figure_note"]
    if q["type"] != "table_yes_no":
        state["soal"] = q["question"]
    return state


def build(q: dict) -> dict | None:
    state = build_state(q)

    if q["type"] == "mcq":
        questions = {
            "jawaban": {
                "type": "choice",
                "instructions": "Pilih satu opsi yang menjawab `soal` dengan benar.",
                "criteria": {k: v for k, v in q["options"].items()},
            }
        }
    elif q["type"] == "table_yes_no":
        questions = {
            "pernyataan_%d" % i: {
                "type": "noul",
                "instructions": {
                    "tanya": "Apakah pernyataan ini benar menurut data yang diberikan?",
                    "pernyataan": s,
                },
                "criteria": {"true": "Pernyataan sesuai dengan data.", "false": "Pernyataan tidak sesuai dengan data."},
            }
            for i, s in enumerate(q["statements"], 1)
        }
    else:
        return None

    return {
        "id": q["id"],
        "subtest": q["subtest"],
        "type": q["type"],
        "answer": q["answer"],
        "payload": {"model": MODEL, "state": state, "questions": questions},
    }


def build_group(qs: list, rows_by_id: dict) -> dict:
    """One request for every question sharing a passage (the batch arm).

    The state is the shared reading plus each question's own stem, and the
    questions map carries one judgment per item. Cheaper, but every item is
    answered while its neighbours' stems are in the same request, which a
    candidate working one number at a time does not get -- so this is an arm,
    never the headline.
    """
    first = qs[0]
    state: dict = {}
    if first["passages"]:
        state["bacaan"] = [
            {k: v for k, v in (("teks", p["text"]), ("keterangan_gambar", p["figure_note"])) if v}
            for p in first["passages"]
        ]
    soal = {}
    questions = {}
    for q in qs:
        key = "soal_%d" % q["number"]
        entry: dict = {"pertanyaan": q["question"]}
        if q["figure_note"]:
            entry["keterangan_gambar"] = q["figure_note"]
        soal[key] = entry
        built = rows_by_id[q["id"]]["payload"]["questions"]
        for sub, defn in built.items():
            qid = key if sub == "jawaban" else "%s_%s" % (key, sub)
            defn = json.loads(json.dumps(defn))
            instr = defn["instructions"]
            ref = "Jawab untuk `soal.%s`." % key
            defn["instructions"] = (ref + " " + instr) if isinstance(instr, str) else dict(instr, untuk=ref)
            questions[qid] = defn
    state["soal"] = soal
    return {
        "id": "+".join(q["id"] for q in qs),
        "subtest": first["subtest"],
        "type": "group",
        "members": [q["id"] for q in qs],
        "answer": {q["id"]: q["answer"] for q in qs},
        "payload": {"model": MODEL, "state": state, "questions": questions},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="with_key", choices=["with_key", "claude_labeled"])
    ap.add_argument("--group-by-passage", action="store_true",
                    help="also build the batch arm: one request per shared passage")
    ap.add_argument("--out", default="data/requests")
    args = ap.parse_args()

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    main_rows, group_rows = [], []
    for path in sorted((ROOT / "data/questions" / args.split).glob("*.json")):
        qs_all = json.loads(path.read_text(encoding="utf-8"))["questions"]
        rows_by_id = {}
        for q in qs_all:
            row = build(q)
            if row is None:
                print("SKIP %s (%s)" % (q["id"], q["type"]), file=sys.stderr)
                continue
            rows_by_id[q["id"]] = row
            main_rows.append(row)
        if args.group_by_passage:
            groups: dict = {}
            for q in qs_all:
                if q["id"] not in rows_by_id:
                    continue
                key = tuple(q["passage_ids"]) or ("solo", q["id"])
                groups.setdefault(key, []).append(q)
            for _, members in groups.items():
                group_rows.append(build_group(members, rows_by_id))

    def write(rows: list, name: str) -> None:
        p = out_dir / name
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        by = {}
        for r in rows:
            by[r["type"]] = by.get(r["type"], 0) + 1
        print("%-28s %3d requests  %s" % (p.relative_to(ROOT), len(rows), by))

    write(main_rows, "%s.jsonl" % args.split)
    if args.group_by_passage:
        write(group_rows, "%s_grouped.jsonl" % args.split)


if __name__ == "__main__":
    main()
