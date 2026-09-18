# jev-snbt-recovered

**English** · [Bahasa Indonesia](README.id.md)

Benchmark of **TypeSafe Jev** on **SNBT 2025**, Indonesia's university entrance
test, using a community reconstruction of the paper.

159 questions across all seven subtests, each one self-contained: its reading
passage and its figure transcription travel with it. First run scores are in
**[RESULTS.md](RESULTS.md)** — short version: 60% on general reasoning, 90% on
Indonesian literacy, 29% on quantitative.

## Where the questions come from

*Modul MMA SNBT 2025* by Tim Mangkuk Mi Ayam — a community reconstruction of
the 2025 paper from what participants remembered afterwards
(`dataset/MMASNBT2025.pdf`, 764 pages, not committed here).

Two things follow from that, and they shape everything else in this repo:

- **The answer keys are not official.** They are the module authors' own work,
  and only for three subtests: PU, PK and PM. The PU key even carries its own
  disclaimer, *"bukan jawaban yang pasti"*. PPU, PBM, LBI and LBE have no key
  at all.
- **Some questions arrived damaged.** `LBI-d1s1-q21` lost an option, and
  `PPU-d1s1-teks4` says "kristal udara" where it plainly means "kristal es".
  Nothing is quietly fixed. Every such item is kept exactly as printed and
  carries a `_source_note` saying what looks wrong.

## What we took, and what we did to it

We took **Day 1, Sesi 1 of every subtest**. PU has no session split, so for PU
we took Day 1.

| Subtest | | Questions | Answers from |
|---|---|---|---|
| PU | Penalaran Umum | 30 | module key |
| PK | Pengetahuan Kuantitatif | 20 | module key |
| PM | Penalaran Matematika | 20 | module key |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | Claude labels |
| PBM | Pemahaman Bacaan dan Menulis | 20 | Claude labels |
| LBI | Literasi Bahasa Indonesia | 29 | Claude labels |
| LBE | Literasi Bahasa Inggris | 20 | Claude labels |

`scripts/extract.py` pulls these out of the PDF and writes JSON. What it does
beyond plain text extraction:

- **Every question carries its own passage.** A reading passage is printed once
  in the module and shared by four or five questions; here it is embedded in
  full into each of them. No item ever needs a lookup somewhere else.
- **Bold and italic survive.** Some questions ask about "kata **bercetak
  tebal**", so extraction reads the PDF's XML rather than flat text.
- **Paragraph breaks are rebuilt**, because some questions refer to "paragraf
  ketiga". Line-ending hyphenation is rejoined (`me-` + `nang` → `menang`).
- **Maths is rewritten as plain text**: `x²`, `√29`, `2^(n–1)`, `6 5/7`. Every
  PK and PM item was retyped by hand from the page image, since stacked
  fractions do not survive text extraction.
- **Nothing is silently corrected.** Corrections live in `data/overrides/` and
  anything odd in the source keeps a `_source_note`.

Re-running `extract.py` reproduces `data/questions/` exactly.

## How figures are handled

Jev takes text, not images. So every figure — 10 of them: line charts, a pie
chart, a geometry diagram, a bracketed operator definition — was **cropped from
the page and transcribed into words by Claude**, then checked against the crop
by hand. For `LBI-d1s1-teks2` that meant measuring the drawn line slopes,
because the first transcription claimed two lines were parallel when they are
not.

The transcription lives in `figure_note` and is embedded into every question
that uses the figure. The original crop stays in `data/figures/` so anyone can
check the transcription against it.

Every model sees the same text-only input, and the transcription is auditable
rather than hidden inside a vision model.

## How the answers were produced

**PU, PK, PM — the module's key**, kept exactly as printed.

We did check it. All 70 items were solved independently from scratch, then
three fresh Claude instances solved them again blind, each seeing only the
questions with the answers stripped out and forbidden from opening this repo.
PK and PM matched 20/20 in both rounds. PU matched 24/30 and 23/30. The keys
were **not** changed; the disagreements are recorded in
`data/audit/module_key_audit.json`, and `PU-d1-q05` and `PU-d1-q24` are flagged
in `data/audit/disputed_items.json` as probable key errors so a scorer can
report accuracy with and without them.

**PPU, PBM, LBI, LBE — labeled by Claude Opus 5**, because the module has no
key for them. These are one model's reading, not ground truth, and they are
kept in a separate folder from the module's answers so the two can never be
confused. Each label carries a rationale and a confidence of high / medium /
low (52 / 23 / 14).

How the labels were made:

1. Answer all 89 from the extracted text, one at a time, with a written reason.
2. Two more Claude instances answer the same 89 **blind**, seeing only question
   plus passage plus options. All three agreed on 87/89.
3. A bias audit against the 62 module-keyed five-option items as a control. The
   letter distribution was fine, but the labels picked the longest option 28%
   of the time against the control's 21%. The items hit by that bias were
   re-derived by hand.
4. Two further passes re-answered everything from scratch and re-argued every
   difference.

Every pass is recorded per item in `data/labels/`, so you can see what each
round answered rather than taking the final letter on trust. The honest summary
is still: **all the graders are the same model, so their agreement is weak
evidence.** `data/questions/without_key/` holds the same 89 questions with
`answer: null` if you would rather label them yourself.

## How Jev is asked

One request per question, posted to `POST https://api.typesafe.ai/v1/systemone`.
`scripts/build_requests.py` writes the payloads to disk before anything is
sent, so the exact request behind any score can be inspected.

A normal multiple-choice question becomes one **Choice**, where the options are
the question's own a–e. Nothing is invented. Two cases need different handling:

- **The two Ya/Tidak tables** (PM q06, q14) are not one decision — each has
  three statements to tick. Each table becomes one request carrying three
  **Noul** (true/false) judgments over the same passage. They are scored whole:
  all three rows right, or the item is wrong. The per-statement figure is
  reported separately, never mixed in, because its guessing baseline is 50%
  against a five-option question's 20%.
- **The three fill-in questions** (PK q01, q02, q18) have no options at all, so
  they cannot be a Choice without us inventing the distractors — which would
  mean measuring our own distractors. **They are excluded.** The scored set is
  67 items, not 70.

## Running it

```bash
python3 scripts/build_requests.py     # write the request payloads
python3 scripts/run_bench.py --dry-run   # validate them, send nothing

cp .env.example .env                  # then put your key in it
python3 scripts/run_bench.py --limit 5   # smoke test
python3 scripts/run_bench.py             # the 67 keyed items
python3 scripts/score.py

# the other 89, scored against Claude's labels
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined   # all 156 together
```

The runner is resumable: it skips ids already in the output file, so a run cut
short by a rate limit continues by repeating the command. It retries 408, 429
and 5xx with backoff and records failures as result lines instead of aborting.

`scripts/score.py` reports accuracy per subtest, accuracy by confidence band, a
Brier score, what accuracy would be if the least confident answers were left
blank, plus token cost and latency.

## Results

| Set | Score |
|---|---|
| 67 items, module's key | **47.8%** |
| 89 items, Claude's labels | **85.4%** |
| All 156, mixed reference | **69.2%** |

The interesting part is not the totals: Jev gets 75% on PU's verbal half and
30% on its arithmetic half, and its confidence tracks its accuracy closely
enough to be useful as a filter. Full write-up, per subtest, with calibration
and cost: **[RESULTS.md](RESULTS.md)**.

## Files

```
data/questions/with_key/        PU, PK, PM — the module's answers
data/questions/claude_labeled/  PPU, PBM, LBI, LBE — Claude's labels
data/questions/without_key/     the same 89, answer: null
data/labels/                    every labeling pass, per item, with reasons
data/audit/                     the module-key audit and the disputed items
data/overrides/                 hand corrections over the automatic extraction
data/figures/                   the original figure crops
data/requests/                  the payloads sent to Jev
scripts/                        extract, crop, build requests, run, score
```

## Attribution

Questions: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Typesetting CC BY-NC 4.0; the question
content belongs to the test organiser and is reproduced here for
non-commercial research only.
