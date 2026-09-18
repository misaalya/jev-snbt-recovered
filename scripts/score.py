#!/usr/bin/env python3
"""Score a benchmark run against the module's keys.

Reads the result lines written by run_bench.py and reports:

  accuracy        overall and per subtest, on the 67-item headline set
  disputed        the same with PU-d1-q05 and PU-d1-q24 dropped (65 items),
                  because two independent solvers rejected those keys
  tables          PM's two Ya/Tidak items, whole-item and per statement
  calibration     accuracy by confidence band, plus a Brier score on the
                  probability the model put on the correct option
  coverage        accuracy if the least confident answers are left blank
  cost            input tokens x the rate given by --rate-per-mtok
  latency         median and p95 wall clock per request

Nothing here changes a key: disputed items are reported both ways.
"""

import argparse
import json
import os
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _env  # noqa: E402  - local helper, no dependency

_env.load()

ROOT = pathlib.Path(__file__).resolve().parent.parent
THRESHOLD = 0.5


def load_keys(split: str = "with_key") -> dict:
    keys = {}
    for path in sorted((ROOT / "data/questions" / split).glob("*.json")):
        for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
            keys[q["id"]] = q
    return keys


def grade(rec: dict, q: dict) -> tuple[bool, float | None, float | None, list]:
    """-> (correct, confidence, prob on the correct option, per-statement flags)"""
    a = rec["answers"]
    if q["type"] == "mcq":
        got = a.get("jawaban", {})
        pick = str(got.get("choice", "")).lower()
        want = str(q["answer"]).lower()
        probs = got.get("probabilities") or {}
        return pick == want, got.get("confidence"), probs.get(want), []
    if q["type"] == "table_yes_no":
        flags = []
        for i, want in enumerate(q["answer"], 1):
            p = a.get("pernyataan_%d" % i, {}).get("noul")
            flags.append(p is not None and (p >= THRESHOLD) == (want == "Ya"))
        return all(flags), None, None, flags
    raise ValueError(q["type"])


def pct(n: int, d: int) -> str:
    return "%5.1f%% (%d/%d)" % (100.0 * n / d, n, d) if d else "    n/a"


def agreement(results: str) -> None:
    """The 89 keyless items: Jev against Claude's labels.

    This is not accuracy. Neither side is ground truth, so the only honest
    reading is how often two independent readers land on the same option, and
    whether the disagreements sit where the label was already unsure.
    """
    keys = load_keys("claude_labeled")
    conf_of = {}
    for path in sorted((ROOT / "data/labels").glob("*.json")):
        for qid, lab in json.loads(path.read_text(encoding="utf-8")).items():
            if not qid.startswith("_"):
                conf_of[qid] = lab.get("confidence")

    rows = []
    for line in (ROOT / results).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if "error" in rec:
            continue
        q = keys[rec["id"]]
        got = rec["answers"].get("jawaban", {})
        label = str(q["answer"]).lower()
        rows.append({
            "id": rec["id"], "subtest": q["subtest"],
            "label": label, "jev": str(got.get("choice", "")).lower(),
            "same": str(got.get("choice", "")).lower() == label,
            "jev_conf": got.get("confidence"),
            "p_label": (got.get("probabilities") or {}).get(label),
            "label_conf": q.get("label_confidence") or conf_of.get(rec["id"]),
            "usage": rec.get("usage", {}), "latency": rec.get("latency_ms"),
        })

    print("== kesepakatan Jev vs label Claude (BUKAN akurasi) ==")
    for s_ in sorted({r["subtest"] for r in rows}):
        sub = [r for r in rows if r["subtest"] == s_]
        print("  %-4s %s" % (s_, pct(sum(r["same"] for r in sub), len(sub))))
    print("  %-4s %s" % ("ALL", pct(sum(r["same"] for r in rows), len(rows))))

    print("\n== dipecah menurut keyakinan label Claude ==")
    for c in ("high", "medium", "low", None):
        sub = [r for r in rows if r["label_conf"] == c]
        if sub:
            print("  label %-7s %s" % (c or "(tidak ada)", pct(sum(r["same"] for r in sub), len(sub))))

    print("\n== dipecah menurut keyakinan Jev ==")
    for lo, hi in ((0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)):
        band = [r for r in rows if r["jev_conf"] is not None and lo <= r["jev_conf"] < hi]
        if band:
            print("  conf %.1f-%.1f  %s" % (lo, min(hi, 1.0), pct(sum(r["same"] for r in band), len(band))))

    pt = [r for r in rows if r["p_label"] is not None]
    if pt:
        print("  brier (peluang pada opsi berlabel): %.3f  atas %d soal" % (
            statistics.fmean((1 - r["p_label"]) ** 2 for r in pt), len(pt)))

    conf = [r for r in rows if r["jev_conf"] is not None]
    if conf:
        print("\n== jika soal paling ragu dikosongkan ==")
        ranked = sorted(conf, key=lambda r: -r["jev_conf"])
        for cov in (1.0, 0.9, 0.8, 0.7):
            k = max(1, int(round(cov * len(ranked))))
            print("  cakupan %3d%%  %s" % (round(100 * k / len(ranked)),
                                           pct(sum(r["same"] for r in ranked[:k]), k)))

    toks = sum(r["usage"].get("input_tokens", 0) for r in rows)
    lat = [r["latency"] for r in rows if r["latency"]]
    print("\n== biaya & latensi ==")
    print("  input tokens %d  -> $%.4f" % (toks, toks / 1e6 * 0.042))
    if lat:
        print("  latensi p50 %.0f ms, p95 %.0f ms" % (statistics.median(lat), sorted(lat)[int(0.95 * (len(lat) - 1))]))

    diffs = [r for r in rows if not r["same"]]
    if diffs:
        print("\n== %d ketidaksepakatan ==" % len(diffs))
        for r in sorted(diffs, key=lambda r: -(r["jev_conf"] or 0)):
            print("  %-14s label=%s (%s)  jev=%s (conf %.2f)" % (
                r["id"], r["label"].upper(), r["label_conf"] or "?", r["jev"].upper(), r["jev_conf"] or 0))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="data/results/with_key.jsonl")
    ap.add_argument("--agreement", action="store_true",
                    help="score a claude_labeled run as agreement, not accuracy")
    ap.add_argument("--rate-per-mtok", type=float, default=float(os.environ.get("BENCH_RATE_PER_MTOK", 0.042)),
                    help="USD per 1M input tokens; verify against current pricing")
    args = ap.parse_args()

    if args.agreement:
        agreement(args.results)
        return

    keys = load_keys()
    disputed = set(json.loads((ROOT / "data/audit/disputed_items.json").read_text(encoding="utf-8"))["exclude_candidates"])

    graded, errors = [], []
    for line in (ROOT / args.results).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if "error" in rec:
            errors.append(rec)
            continue
        ids = rec.get("members", [rec["id"]])
        for qid in ids:
            sub = rec if len(ids) == 1 else {**rec, "answers": _slice(rec["answers"], keys[qid])}
            ok, conf, p_true, flags = grade(sub, keys[qid])
            graded.append({"id": qid, "subtest": keys[qid]["subtest"], "type": keys[qid]["type"],
                           "ok": ok, "conf": conf, "p_true": p_true, "flags": flags,
                           "latency": rec.get("latency_ms"), "usage": rec.get("usage", {})})

    print("== akurasi (set headline) ==")
    for s in sorted({g["subtest"] for g in graded}):
        rows = [g for g in graded if g["subtest"] == s]
        print("  %-4s %s" % (s, pct(sum(g["ok"] for g in rows), len(rows))))
    print("  %-4s %s" % ("ALL", pct(sum(g["ok"] for g in graded), len(graded))))

    keep = [g for g in graded if g["id"] not in disputed]
    print("\n== tanpa soal yang kuncinya diragukan (%s) ==" % ", ".join(sorted(disputed)))
    print("  %-4s %s" % ("ALL", pct(sum(g["ok"] for g in keep), len(keep))))

    tables = [g for g in graded if g["type"] == "table_yes_no"]
    if tables:
        st = [f for g in tables for f in g["flags"]]
        print("\n== soal tabel Ya/Tidak ==")
        print("  per nomor      %s" % pct(sum(g["ok"] for g in tables), len(tables)))
        print("  per pernyataan %s   (baseline tebak 50%%, tidak digabung ke headline)" % pct(sum(st), len(st)))

    conf = [g for g in graded if g["conf"] is not None]
    if conf:
        print("\n== kalibrasi ==")
        for lo, hi in ((0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)):
            band = [g for g in conf if lo <= g["conf"] < hi]
            if band:
                print("  conf %.1f-%.1f  %s" % (lo, min(hi, 1.0), pct(sum(g["ok"] for g in band), len(band))))
        pt = [g for g in conf if g["p_true"] is not None]
        if pt:
            brier = statistics.fmean((1 - g["p_true"]) ** 2 for g in pt)
            print("  brier (peluang pada opsi benar): %.3f  atas %d soal" % (brier, len(pt)))

        print("\n== jika soal paling ragu dikosongkan ==")
        ranked = sorted(conf, key=lambda g: -g["conf"])
        for cov in (1.0, 0.9, 0.8, 0.7):
            k = max(1, int(round(cov * len(ranked))))
            top = ranked[:k]
            print("  cakupan %3d%%  %s" % (round(100 * k / len(ranked)), pct(sum(g["ok"] for g in top), len(top))))

    toks = sum(g["usage"].get("input_tokens", 0) for g in graded)
    lat = [g["latency"] for g in graded if g["latency"]]
    print("\n== biaya & latensi ==")
    print("  input tokens %d  -> $%.4f @ $%.3f/1M" % (toks, toks / 1e6 * args.rate_per_mtok, args.rate_per_mtok))
    if lat:
        print("  latensi p50 %.0f ms, p95 %.0f ms" % (statistics.median(lat), sorted(lat)[int(0.95 * (len(lat) - 1))]))
    if errors:
        print("\n%d request gagal: %s" % (len(errors), ", ".join(e["id"] for e in errors[:5])))


def _slice(answers: dict, q: dict) -> dict:
    """Pull one item's answers out of a grouped (batch arm) response."""
    tag = "soal_%d" % q["number"]
    if q["type"] == "mcq":
        return {"jawaban": answers.get(tag, {})}
    return {k.replace(tag + "_", ""): v for k, v in answers.items() if k.startswith(tag + "_")}


if __name__ == "__main__":
    main()
