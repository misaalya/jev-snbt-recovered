#!/usr/bin/env python3
"""Extract SNBT questions from the MMA SNBT 2025 module PDF into JSON.

Uses `pdftohtml -xml` so bold/italic survive as markdown (**bold**, _italic_),
which matters for questions like "kata bercetak tebal" or "the word _may_".

Output: data/questions/<section>.json, one file per section, plus a summary
of items flagged for manual review (math notation, figures, odd option counts).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "dataset" / "MMASNBT2025.pdf"
OUT = ROOT / "data" / "questions"

# (section id, subtest, day, session, first page, last page)
SECTIONS = [
    ("PU_d1", "PU", 1, None, 9, 22),
    ("PPU_d1s1", "PPU", 1, 1, 87, 96),
    ("PBM_d1s1", "PBM", 1, 1, 128, 136),
    ("PK_d1s1", "PK", 1, 1, 168, 173),
    ("LBI_d1s1", "LBI", 1, 1, 224, 237),
    ("LBE_d1s1", "LBE", 1, 1, 306, 314),
    ("PM_d1s1", "PM", 1, 1, 351, 356),
]

MATH_FONT = re.compile(r"LMMath|CMSY|CMMI|CMEX")
FIGURE_WORDS = re.compile(
    r"\b(diagram|grafik|gambar|tabel|bagan|kurva|bangun datar|ilustrasi)\b",
    re.I,
)
LINE_TOL = 8  # px; nodes whose top differs by less are on the same line
PARA_INDENT = 12  # px; a passage line starting this far right of the body margin opens a new paragraph
SHORT_LINE = 60   # px; in justified text a line ending this far short of the margin ends a paragraph
JUSTIFIED = 0.7   # fraction of lines that must reach the right margin before the short-line rule applies


@dataclass
class Node:
    page: int
    top: int
    left: int
    width: int
    height: int
    font: str
    text: str  # already markdown-marked


@dataclass
class Line:
    page: int
    top: int
    left: int
    right: int
    text: str
    math: bool


@dataclass
class Question:
    id: str
    subtest: str
    day: int
    session: int | None
    number: int
    type: str = "mcq"  # mcq | fill_in | table_yes_no
    subtype: str | None = None  # multi_statement | quantity_comparison | data_sufficiency
    passage_ids: list[str] = field(default_factory=list)
    question: str = ""
    options: dict[str, str] = field(default_factory=dict)
    statements: list[str] = field(default_factory=list)  # for yes/no tables
    answer: str | list[str] | None = None  # letter, fill-in value, or per-statement Ya/Tidak list
    answer_source: str | None = None  # "module" (the module's key/pembahasan) | "claude-opus-5" (data/labels/)
    label_confidence: str | None = None  # high | medium | low; only for claude-labeled answers
    has_figure: bool = False
    figure_path: str | None = None  # crop of the original figure, data/figures/<id>.png
    figure_note: str | None = None  # text transcription of the figure
    source_page: int = 0
    _source_note: str | None = None
    needs_review: bool = False
    review_reasons: list[str] = field(default_factory=list)


def run_pdftohtml(first: int, last: int) -> ET.Element:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "out"
        subprocess.run(
            ["pdftohtml", "-xml", "-i", "-q", "-f", str(first), "-l", str(last), str(PDF), str(base)],
            check=True,
        )
        return ET.parse(base.with_suffix(".xml")).getroot()


def node_text(el: ET.Element, is_math_font: bool) -> str:
    """Flatten a <text> node to a string, wrapping <b>/<i> as markdown."""
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        inner = "".join(child.itertext())
        if child.tag == "b" and inner.strip():
            parts.append(f"**{inner}**")
        elif child.tag == "i" and re.search(r"\w", inner) and not is_math_font and len(inner.strip()) > 1:
            parts.append(f"_{inner}_")
        else:
            parts.append(inner)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def extract_lines(root: ET.Element) -> list[Line]:
    lines: list[Line] = []
    fonts: dict[str, str] = {}  # pdftohtml declares each fontspec once, on the first page that uses it
    for page in root.iter("page"):
        pno = int(page.get("number"))
        fonts.update({f.get("id"): f.get("family", "") for f in page.iter("fontspec")})
        nodes = []
        for t in page.iter("text"):
            fam = fonts.get(t.get("font"), "")
            txt = node_text(t, bool(MATH_FONT.search(fam)))
            if not txt.strip():
                continue
            nodes.append(Node(pno, int(t.get("top")), int(t.get("left")), int(t.get("width")), int(t.get("height")), fam, txt))
        nodes.sort(key=lambda n: (n.top, n.left))
        cur: list[Node] = []
        for n in nodes:
            if cur and abs(n.top - cur[0].top) > LINE_TOL:
                lines.append(_merge(cur))
                cur = []
            cur.append(n)
        if cur:
            lines.append(_merge(cur))
    return lines


def _merge(nodes: list[Node]) -> Line:
    nodes.sort(key=lambda n: n.left)
    out = ""
    prev_end = None
    for n in nodes:
        gap = n.left - prev_end if prev_end is not None else 0
        # glue tightly adjacent fragments (kerned words, math tokens); otherwise space
        if out and gap > 3 and not out.endswith(" ") and not n.text.startswith(" "):
            out += " "
        out += n.text
        prev_end = n.left + n.width
    math = any(MATH_FONT.search(n.font) and re.search(r"[^\s.…]", n.text) for n in nodes)
    right = max(n.left + n.width for n in nodes)
    return Line(nodes[0].page, nodes[0].top, nodes[0].left, right, re.sub(r"\s+", " ", out).strip(), math)


RE_Q = re.compile(r"^(\d{1,2})\.\s+(.*)$")
RE_OPT = re.compile(r"\(([a-e])\)\s*")
RE_TEKS = re.compile(r"^(Teks|Text)\s+(\d+)$", re.I)
RE_READ = re.compile(r"^Bacalah .*nomor\s+(\d+)\s+(?:sampai|s\.d\.|hingga)\s+(\d+)", re.I)
RE_TABLE = re.compile(r"Klik pilihan kolom", re.I)
RE_YESNO_HDR = re.compile(r"^(Ya|Benar)\s+(Tidak|Salah)$", re.I)
RE_FRAG = re.compile(r"(?=.*[\d√])[\d√\-–+,.·/ ]{1,12}")


def dehyphen(a: str, b: str) -> str:
    """Join a line-end hyphenated word: 'me-' + 'nang' -> 'menang'."""
    if a.endswith("-") and not a.endswith(" -"):
        last = a.rstrip("-").split()[-1] if a.rstrip("-").split() else ""
        first = re.split(r"[^\w]", b, 1)[0]
        if len(first) >= 3 and last.lower().endswith(first.lower()):  # reduplication: 'sehari-'+'hari', 'pernyataan-'+'pernyataan'
            return a + b
        if b[:1].islower() or last.isupper():  # 'me-'+'nang', 'SA-'+'LAH'
            return a[:-1] + b
        if b[:1].isupper():  # hyphenated proper compound: 'Timor-'+'Timur'
            return a + b
    return a + " " + b


def join_paragraphs(lines: list[tuple[int, int, str]]) -> str:
    """Join passage lines into paragraphs (kept as '\n').

    A paragraph starts either at an indented line, or - in justified text, where the
    module does not indent - right after a line that stops well short of the margin.
    """
    if not lines:
        return ""
    margin = min(left for left, _, _ in lines)
    edge = max(right for _, right, _ in lines)
    justified = sum(right >= edge - 4 for _, right, _ in lines) >= JUSTIFIED * len(lines)
    out = ""
    prev_short = False
    for left, right, t in lines:
        if not out:
            out = t
        elif left > margin + PARA_INDENT or (justified and prev_short):
            out += "\n" + t
        else:
            out = dehyphen(out, t)
        prev_short = right < edge - SHORT_LINE
    return out


def parse_section(sec_id: str, subtest: str, day: int, session: int | None, lines: list[Line]):
    tag = f"{subtest}-d{day}" + (f"s{session}" if session else "")
    passages: dict[str, dict] = {}
    questions: list[Question] = []
    cur_passage: dict | None = None
    group: list[dict] = []  # consecutive Teks headers that share the following questions
    intro: list[tuple[int, int, str]] = []  # (left, right, text) before any Teks header / question (LBE forum thread)
    q: Question | None = None
    cur_opt: str | None = None
    mode = "none"  # none | passage | question | option | statements
    header_re = re.compile(rf"^{subtest} Day {day}(?: Sesi {session})?$")

    for ln in lines:
        t = ln.text
        plain = re.sub(r"\*\*|(?<!\w)_|_(?!\w)", "", t).strip()
        if header_re.match(plain) or plain == str(ln.page):  # section header / page number
            continue
        if RE_FRAG.fullmatch(plain) and q is not None:
            # a lone number/radical on its own line: numerator, denominator or index of stacked notation
            _flag(q, "stacked notation (fraction/root) - rebuild from page image")
            t = f"[frag:{plain}]"
        m_teks = RE_TEKS.fullmatch(plain)
        m_q = RE_Q.match(plain)
        if m_teks:
            pid = f"{tag}-teks{m_teks.group(2)}"
            cur_passage = {"id": pid, "text": "", "_lines": [], "covers": None, "figure_path": None, "figure_note": None, "_source_note": None, "source_page": ln.page, "math": False}
            passages[pid] = cur_passage
            if mode != "passage":
                group = []
            group.append(cur_passage)
            mode = "passage"
            q = None
            continue
        if m_q and (mode in ("none", "passage") or int(m_q.group(1)) == (q.number + 1 if q else 1)):
            n = int(m_q.group(1))
            if not passages and len(" ".join(t for _, _, t in intro)) >= 80:  # real intro text (LBE forum thread), not a stray fragment
                pid = f"{tag}-teks0"
                passages[pid] = {"id": pid, "text": join_paragraphs(intro), "covers": None, "figure_path": None, "figure_note": None, "_source_note": None, "source_page": lines[0].page, "math": False}
                group = [passages[pid]]
            intro = []
            body = re.sub(r"^\**\d{1,2}\.\**\s*", "", t).strip()
            pids = [pg["id"] for pg in group if pg["covers"] is None or pg["covers"][0] <= n <= pg["covers"][1]]
            if body.startswith("(1)"):
                pids = []  # self-contained item carrying its own numbered sentences
            q = Question(
                id=f"{tag}-q{n:02d}", subtest=subtest, day=day, session=session,
                number=n, passage_ids=pids, question=body, source_page=ln.page,
            )
            questions.append(q)
            mode = "question"
            cur_opt = None
            if ln.math:
                _flag(q, "math notation")
            if RE_TABLE.search(t):
                q.type = "table_yes_no"
            continue
        if mode == "none":
            intro.append((ln.left, ln.right, t))
            continue
        if mode == "passage" and cur_passage is not None:
            m_read = RE_READ.match(plain)
            if m_read:  # "Bacalah informasi berikut untuk nomor 1 sampai 4."
                cur_passage["covers"] = [int(m_read.group(1)), int(m_read.group(2))]
                continue
            cur_passage["_lines"].append((ln.left, ln.right, t))
            cur_passage["math"] |= ln.math
            continue
        if q is None:
            continue
        # yes/no table: header line then statements
        if q.type == "table_yes_no":
            if RE_YESNO_HDR.match(plain):
                mode = "statements"
                continue
            if mode == "statements":
                prev = q.statements[-1] if q.statements else ""
                wrapped = prev and (prev.endswith("-") or not re.search(r"[.!?]$", prev) and t[:1].islower())
                if wrapped:
                    q.statements[-1] = dehyphen(prev, t)
                else:
                    q.statements.append(t)
                continue
        # options, possibly several on one line: "(a) 14 (b) 13 (c) 12"
        opts = list(RE_OPT.finditer(t))
        if opts and (mode in ("question", "option")):
            prefix = t[: opts[0].start()].strip()
            if prefix and mode == "question":
                q.question = dehyphen(q.question, prefix)
            elif prefix and cur_opt:
                q.options[cur_opt] = dehyphen(q.options[cur_opt], prefix)
            for i, m in enumerate(opts):
                end = opts[i + 1].start() if i + 1 < len(opts) else len(t)
                q.options[m.group(1)] = t[m.end():end].strip()
                cur_opt = m.group(1)
            mode = "option"
            if ln.math:
                _flag(q, "math notation")
            continue
        if mode == "question":
            q.question = dehyphen(q.question, t)
            if ln.math:
                _flag(q, "math notation")
        elif mode == "option" and cur_opt:
            q.options[cur_opt] = dehyphen(q.options[cur_opt], t)
            if ln.math:
                _flag(q, "math notation")

    for pg in passages.values():
        if "_lines" in pg:
            pg["text"] = join_paragraphs(pg.pop("_lines"))
    for q in questions:
        if q.type == "table_yes_no" and len(q.statements) not in (3, 4):
            _flag(q, f"{len(q.statements)} table rows")
        if q.type == "mcq" and q.subtype is None and len(q.options) != 5:
            _flag(q, f"{len(q.options)} options")
        if FIGURE_WORDS.search(q.question):
            q.has_figure = True
            _flag(q, "may reference figure/table")
        if any(passages[pid]["math"] for pid in q.passage_ids):
            _flag(q, "passage has math notation")
    return passages, questions


def _flag(q: Question, why: str):
    q.needs_review = True
    if why not in q.review_reasons:
        q.review_reasons.append(why)


ANSWER_KEY_PAGES = {"PU": (433, 435)}


def load_answer_key(subtest: str, day: int, session: int | None) -> dict[int, str]:
    """Parse the 'Kunci Jawaban' tables (No Kunci columns) for one Day/Sesi block."""
    if subtest not in ANSWER_KEY_PAGES:
        return {}
    first, last = ANSWER_KEY_PAGES[subtest]
    txt = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), "-layout", str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    key: dict[int, str] = {}
    active = False
    for line in txt.splitlines():
        st = line.strip()
        m = re.fullmatch(r"Day (\d+)(?: Sesi (\d+))?", st)
        if m:
            k_day, k_sess = int(m.group(1)), (int(m.group(2)) if m.group(2) else None)
            active = k_day == day and (session is None or k_sess in (None, session))
            continue
        if active:
            for n, a in re.findall(r"(\d{1,2})\s+([A-E?–-])", st):
                if a in "ABCDE":
                    key[int(n)] = a
    if not key:
        print(f"WARNING: no answer key entries found for {subtest} Day {day} Sesi {session}", file=sys.stderr)
    return key


def load_labels(sec_id: str) -> dict[str, dict]:
    """Model-written labels for sections the module has no key for (data/labels/<sec>.json)."""
    path = ROOT / "data" / "labels" / f"{sec_id}.json"
    if not path.exists():
        return {}
    return {k: v for k, v in json.loads(path.read_text(encoding="utf-8")).items() if not k.startswith("_")}


def apply_overrides(sec_id: str, questions: list[Question], passages: dict[str, dict]):
    path = ROOT / "data" / "overrides" / f"{sec_id}.json"
    if not path.exists():
        return
    ov = json.loads(path.read_text(encoding="utf-8"))
    by_id = {q.id: q for q in questions}
    for key, patch in ov.items():
        if key.startswith("_"):
            continue
        if key in passages:
            passages[key].update(patch)
            continue
        q = by_id[key]
        for k, v in patch.items():
            setattr(q, k, v)
        q.needs_review = False
        q.review_reasons = []


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    total = flagged = 0
    for sec_id, subtest, day, session, first, last in SECTIONS:
        if only and sec_id not in only:
            continue
        root = run_pdftohtml(first, last)
        lines = extract_lines(root)
        passages, questions = parse_section(sec_id, subtest, day, session, lines)
        key = load_answer_key(subtest, day, session)
        for q in questions:
            q.answer = key.get(q.number)
        apply_overrides(sec_id, questions, passages)
        # a passage applies only to the questions it covers; without an explicit range the
        # module just stops using it, so data/overrides/ states the range (see "covers")
        for q in questions:
            q.passage_ids = [
                pid for pid in q.passage_ids
                if passages[pid]["covers"] is None
                or passages[pid]["covers"][0] <= q.number <= passages[pid]["covers"][1]
            ]
        for pid, pg in passages.items():
            used = [q.number for q in questions if pid in q.passage_ids]
            if not used:
                print(f"WARNING: passage {pid} is attached to no question", file=sys.stderr)
        for q in questions:
            if q.answer is not None:
                q.answer_source = "module"
        labels = load_labels(sec_id)
        items = []
        for q in questions:
            if q.answer is None and q.id in labels:
                # keep module keys and model labels apart: the labeled copy goes to claude_labeled/ only
                q.answer, q.answer_source = labels[q.id]["answer"], "claude-opus-5"
                q.label_confidence = labels[q.id]["confidence"]
            item = asdict(q)
            # every item is self-contained: the shared passage(s) it refers to are embedded in full,
            # each with its own figure transcription, so a consumer never has to look anything up
            item["passages"] = [
                {k: passages[pid][k] for k in ("id", "text", "figure_path", "figure_note", "_source_note", "source_page")}
                for pid in q.passage_ids
            ]
            item["has_answer"] = q.answer is not None
            items.append(item)
        splits = {
            "with_key": ("module answer key / pembahasan", [it for it in items if it["answer_source"] == "module"]),
            "claude_labeled": ("labeled by claude-opus-5 (data/labels/), NOT from the source",
                               [it for it in items if it["answer_source"] == "claude-opus-5"]),
            "without_key": ("none in source", [
                dict(it, answer=None, answer_source=None, label_confidence=None, has_answer=False)
                for it in items if it["answer_source"] != "module"
            ]),
        }
        for sub, (answer_key, part) in splits.items():
            path = OUT / sub / f"{sec_id}.json"
            if not part:
                path.unlink(missing_ok=True)
                continue
            doc = {
                "section": sec_id, "subtest": subtest, "day": day, "session": session,
                "pages": [first, last], "source": "MMA SNBT 2025 (Tim Mangkuk Mi Ayam), CC BY-NC 4.0",
                "answer_key": answer_key,
                "questions": part,
            }
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n_flag = sum(q.needs_review for q in questions)
        total += len(questions)
        flagged += n_flag
        cover = ", ".join(
            f"{pid.split('-')[-1]}:q{min(u)}-q{max(u)}"
            for pid, u in ((pid, [q.number for q in questions if pid in q.passage_ids]) for pid in passages)
            if u
        )
        n_key = sum(q.answer_source == "module" for q in questions)
        n_lab = sum(q.answer_source == "claude-opus-5" for q in questions)
        print(f"{sec_id:10s} {len(passages)} passages, {len(questions):2d} questions, {n_key:2d} keyed, {n_lab:2d} labeled, {n_flag:2d} flagged")
        if cover:
            print(f"{'':10s} {cover}")
    print(f"total {total} questions, {flagged} flagged for review")


if __name__ == "__main__":
    main()
