# snbt-jev-bench

**English** · [Bahasa Indonesia](README.id.md)

A benchmark of **TypeSafe Jev** on **SNBT 2025**, the Indonesian university
entrance test.

> **These are recovered questions, not the official paper.** SNBT papers are
> not released after the examination. Every item here was reconstructed by the
> community from what participants remembered, so the wording can differ from
> what was actually sat, a few items are demonstrably damaged, and the answer
> keys are the reconstruction's own rather than the organiser's. Every figure
> in this repository is a measurement against that reconstruction, not against
> the examination itself.

The dataset contains 159 questions covering all seven subtests. Each question
is self-contained: its reading passage and the transcription of any figure it
refers to are embedded in the question itself. Results of the first run are
recorded in **[RESULTS.md](RESULTS.md)**, with the raw responses in
`data/results/`.

## Source of the questions

The questions are taken from *Modul MMA SNBT 2025*, compiled by Tim Mangkuk Mi
Ayam: 764 pages of recalled questions, typeset by volunteers
(`dataset/MMASNBT2025.pdf`, not included in this repository).

**The answer keys are not official.** They are the work of the module's
authors, and they exist for three subtests only: PU, PK and PM. The PU key
carries the authors' own disclaimer, *"bukan jawaban yang pasti"*. PPU, PBM,
LBI and LBE have no key.

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

The questions were moved from the PDF into JSON with the help of
**Claude Code**.

## Questions with figures

Jev reads text, not images. The ten figures in the dataset are line charts, a
pie chart, a geometry diagram and a bracketed operator definition. Each was
cropped from its page, then **transcribed into text by Claude** and checked
against the crop by hand. That check changed one transcription: for
`LBI-d1s1-teks2` the drawn line slopes were measured, which contradicted the
first transcription's claim that two of the lines were parallel.

## Where the answers come from

**PU, PK and PM use the module's key.** The key was nevertheless re-examined,
since the source itself states that its answers are not certain.

**PPU, PBM, LBI and LBE carry labels written by Claude Opus 5**, since the
module provides no key for them. These labels come from one model only, so they
are not settled answers.

## How Jev is queried

One request is sent per question to `POST
https://api.typesafe.ai/v1/systemone`. `scripts/build_requests.py` writes the
payloads to disk before anything is transmitted, so the exact request behind
any score can be examined.

A standard multiple-choice question becomes a single **Choice** holding the
item's own options a–e; nothing is invented. Two kinds of question fall outside
that pattern.

- **The two Ya/Tidak tables** (PM q06 and q14) are sent as one request carrying
  three **Noul** judgments, one per statement. Scoring is applied to the item
  as a whole, and the per-statement figure is reported separately because its
  guessing baseline is 50%, not 20%.
- **The three fill-in questions** (PK q01, q02, q18) print no options at all.
  Making them a Choice would mean inventing the distractors, and what gets
  measured then is the distractors rather than the model. They are excluded:
  67 items are scored, not 70.

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

`data/results/` already contains the published run, and the runner skips items
whose answers it finds there. The commands above can therefore be repeated to
score the committed responses without an API key. For a new run, send the
output elsewhere with `--out data/results/rerun.jsonl` and give the same path
to `scripts/score.py --results`.

That skipping is also what makes an interrupted run resumable: simply repeat
the command. Responses of 408, 429 and 5xx are retried automatically with a
growing delay, and failures are recorded as result lines rather than aborting
the run.

`scripts/score.py` reports accuracy per subtest and per confidence band, a
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
