# snbt-jev-bench

**English** · [Bahasa Indonesia](README.id.md)

A benchmark of **TypeSafe Jev** on **SNBT 2025**, the Indonesian university
entrance test, using a community reconstruction of the paper.

The dataset contains 159 questions covering all seven subtests. Each question
is self-contained: its reading passage and the transcription of any figure it
refers to are embedded in the question itself. Results of the first run are
recorded in **[RESULTS.md](RESULTS.md)**, with the raw responses in
`data/results/`.

## Source of the questions

The questions are taken from *Modul MMA SNBT 2025*, compiled by Tim Mangkuk Mi
Ayam. The module is a community reconstruction of the 2025 paper, assembled
from what participants recalled after the examination
(`dataset/MMASNBT2025.pdf`, 764 pages, not included in this repository).

Two properties of that source determine how the rest of this project is
organised.

**The answer keys are not official.** They are the work of the module's
authors, and they exist for three subtests only: PU, PK and PM. The PU key
carries the authors' own disclaimer, *"bukan jawaban yang pasti"*. PPU, PBM,
LBI and LBE have no key.

**Some questions were damaged in reconstruction.** `LBI-d1s1-q21` is missing an
option, and `PPU-d1s1-teks4` reads "kristal udara" where the intended term is
"kristal es". No such defect is corrected without a record: the item is
reproduced as printed and carries a `_source_note` describing the problem.

## Scope and preparation

The dataset covers **Day 1, Sesi 1 of every subtest**. PU is not divided into
sessions, so Day 1 was taken in full.

| Subtest | | Questions | Answers from |
|---|---|---|---|
| PU | Penalaran Umum | 30 | module key |
| PK | Pengetahuan Kuantitatif | 20 | module key |
| PM | Penalaran Matematika | 20 | module key |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | Claude labels |
| PBM | Pemahaman Bacaan dan Menulis | 20 | Claude labels |
| LBI | Literasi Bahasa Indonesia | 29 | Claude labels |
| LBE | Literasi Bahasa Inggris | 20 | Claude labels |

The questions were extracted from the PDF into JSON. Beyond plain text
extraction, the following was applied.

- **Each question carries its own passage.** A reading passage is printed once
  in the module and shared by four or five questions; in the dataset it is
  embedded in full into every question that refers to it, so no item requires
  an external lookup.
- **Bold and italic are preserved.** Several questions ask about "kata
  **bercetak tebal**", so the extraction read the PDF's XML representation
  rather than flat text.
- **Paragraph boundaries are reconstructed**, because some questions refer to a
  specific paragraph. End-of-line hyphenation is rejoined (`me-` + `nang` →
  `menang`).
- **Mathematics is rendered as plain text**: `x²`, `√29`, `2^(n–1)`, `6 5/7`.
  Every PK and PM item was retyped by hand from the page image, since stacked
  fractions do not survive text extraction.
- **No correction was applied silently.** Any irregularity inherited from the
  source is recorded in a `_source_note` on the item or passage it affects.

The extraction itself is not part of this repository: it depends on the source
PDF, which cannot be redistributed here. `data/questions/` is the published
artefact.

## Treatment of figures

Jev accepts text, not images. Each of the ten figures in the dataset — line
charts, a pie chart, a geometry diagram and a bracketed operator definition —
was cropped from the page and **transcribed into text by Claude**, then
verified against the crop by hand. The verification changed one transcription:
for `LBI-d1s1-teks2` the drawn line slopes were measured, which showed that the
first transcription's claim that two lines were parallel was incorrect.

Each transcription is stored in `figure_note` and embedded into every question
that uses the figure. The original crop remains in `data/figures/` so that the
transcription can be audited against it. The model therefore receives the same
text-only input for every question, and the transcription is available for
inspection rather than performed inside a vision model.

## Derivation of the answers

**PU, PK and PM use the module's key**, reproduced exactly as printed.

The key was nevertheless verified. All 70 items were solved independently from
scratch, after which three separate Claude instances solved them again blind,
each receiving only the questions with the answers removed and prohibited from
opening this repository. PK and PM matched the module 20/20 in both rounds; PU
matched on 24 of 30 and 23 of 30. The keys were not altered. The disagreements
are recorded in `data/audit/module_key_audit.json`, and `PU-d1-q05` and
`PU-d1-q24` are listed in `data/audit/disputed_items.json` as probable key
errors so that accuracy can be reported both with and without them.

**PPU, PBM, LBI and LBE carry labels written by Claude Opus 5**, since the
module provides no key for them. These labels are one model's reading and are
not ground truth. They are stored in a separate directory from the module's
answers so the two are never combined, and every item carries the field
`answer_source` naming which of the two it came from.

Each label records a confidence of high, medium or low (52, 23 and 14 items
respectively), assigned during labeling and reported in RESULTS.md alongside
the rate at which Jev agrees with it. Only the final label is published; the
intermediate drafting passes are working material and are not part of this
repository. One limitation remains stated plainly: the label and its
verification come from the same model family, so their agreement is weak
evidence.

## How Jev is queried

One request is sent per question to `POST
https://api.typesafe.ai/v1/systemone`. `scripts/build_requests.py` writes the
payloads to disk before anything is transmitted, so the exact request behind
any score can be examined.

A standard multiple-choice question becomes a single **Choice**, whose criteria
are the question's own options a–e. Nothing is synthesised. Two categories
require different handling.

**The two Ya/Tidak tables** (PM q06 and q14) are not a single decision: each
presents three statements to be marked individually. Each table is sent as one
request containing three **Noul** judgments over the same passage. Scoring is
applied to the item as a whole — all three statements must be correct — and the
per-statement figure is reported separately, since its guessing baseline of 50%
is not comparable with the 20% of a five-option question.

**The three fill-in questions** (PK q01, q02 and q18) provide no options and
therefore cannot be expressed as a Choice without inventing the distractors,
which would measure the distractors rather than the model. They are excluded.
The scored set consists of 67 items rather than 70.

## Running the benchmark

```bash
python3 scripts/build_requests.py        # write the request payloads
python3 scripts/run_bench.py --dry-run   # validate them without sending

cp .env.example .env                     # then enter the API key
python3 scripts/run_bench.py --limit 5   # smoke test
python3 scripts/run_bench.py             # the 67 module-keyed items
python3 scripts/score.py

# the remaining 89, scored against the Claude labels
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined      # all 156 items together
```

`data/results/` already contains the published run, and the runner skips
identifiers it finds there, so a repeat of the commands above reports every
item as done and scores the committed responses without an API key. To make a
new run, direct it elsewhere with `--out data/results/rerun.jsonl` and pass the
same path to `scripts/score.py --results`.

The runner is resumable: identifiers already present in the output file are
skipped, so a run interrupted by a rate limit continues when the command is
repeated. Responses of 408, 429 and 5xx are retried with exponential backoff
and honour `Retry-After`; failures are recorded as result lines rather than
aborting the run.

`scripts/score.py` reports accuracy per subtest, accuracy by confidence band, a
Brier score, the accuracy obtained when the least confident answers are
withheld, and token cost and latency.

## Summary of results

| Set | Score |
|---|---|
| 67 items, module key | 47.8% |
| 89 items, Claude labels | 85.4% |
| 156 items, mixed reference | 69.2% |

Per-subtest scores, calibration, the differences from the labels, and cost are
given in **[RESULTS.md](RESULTS.md)**.

## Repository layout

```
data/questions/with_key/        PU, PK, PM — the module's answers
data/questions/claude_labeled/  PPU, PBM, LBI, LBE — Claude's labels
data/audit/                     the module-key audit and the disputed items
data/figures/                   the original figure crops
data/results/                   the run reported in RESULTS.md, one line per question
scripts/build_requests.py       questions -> System One request payloads
scripts/run_bench.py            post the payloads, record answers and usage
scripts/score.py                score a run against the module key or the labels
```

`scripts/build_requests.py` writes into `data/requests/`, which is generated
locally and is not tracked. `data/results/` holds the published run exactly as
the runner recorded it, so the figures in RESULTS.md can be recomputed, and a
new run can be compared against it line by line.

## Attribution

Questions: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). The typesetting is licensed CC BY-NC 4.0;
the question content belongs to the examination organiser and is reproduced
here for non-commercial research only.
