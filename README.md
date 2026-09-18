# snbt-jev-bench

**English** · [Bahasa Indonesia](README.id.md)

A benchmark of **TypeSafe Jev** on **SNBT 2025**, Indonesia's state university
entrance test.

> **These are not the official questions.** SNBT papers are never released, so
> these questions were rebuilt by the community from what participants
> remembered. The wording may differ from the real test, a few questions are
> flawed, and the answer keys were written by the module's authors, not the
> exam organiser. Every number here measures Jev against this reconstruction,
> not against the real SNBT.

The dataset has 159 questions across all seven subtests. Each question
includes its own reading passage and figure transcriptions. Results are in
**[RESULTS.md](RESULTS.md)**, and raw responses are in `data/results/`.

## Where the questions come from

The questions come from *Modul MMA SNBT 2025* by Tim Mangkuk Mi Ayam, a
764-page collection of recalled questions (`dataset/MMASNBT2025.pdf`, not
included here).

**The answer keys are not official.** They were written by the module's
authors and only cover PU, PK and PM. For PU, the authors note that the answers
are *"bukan jawaban yang pasti"* (not certain). PPU, PBM, LBI and LBE have no
key.

We use Day 1, Sesi 1 of each subtest. PU has no sessions, so all of PU Day 1 is
used.

| Subtest | | Questions | Answers from |
|---|---|---|---|
| PU | Penalaran Umum | 30 | module key |
| PK | Pengetahuan Kuantitatif | 20 | module key |
| PM | Penalaran Matematika | 20 | module key |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | Claude labels |
| PBM | Pemahaman Bacaan dan Menulis | 20 | Claude labels |
| LBI | Literasi Bahasa Indonesia | 29 | Claude labels |
| LBE | Literasi Bahasa Inggris | 20 | Claude labels |

The questions were converted from PDF to JSON with help from **Claude Code**.

## Questions with figures

Jev only reads text. The dataset has ten figures: line charts, a pie chart, a
geometry diagram and one operator definition. Each was **transcribed into text
by Claude** and checked by hand against the original. One transcription was
corrected this way: in `LBI-d1s1-teks2`, two lines first described as parallel
turned out not to be once their slopes were measured.

## Where the reference answers come from

**PU, PK and PM use the module key.** The key was still re-checked, since its
own authors say it may be wrong.

**PPU, PBM, LBI and LBE use labels from Claude Opus 5**, because the module has
no key for them. These labels come from a single model, so they may be wrong.

## How Jev is queried

Each question is sent as one request to `POST
https://api.typesafe.ai/v1/systemone`. `scripts/build_requests.py` saves every
payload to disk first, so the request behind any score can be checked.

A multiple-choice question is sent as one **Choice** using its own options a
to e. There are two exceptions:

- **Two Ya/Tidak tables** (PM q06 and q14) are sent as three **Noul**
  judgments, one per statement. Each item is scored as a whole. Per-statement
  results are reported separately because the guessing rate there is 50%, not
  20%.
- **Three fill-in questions** (PK q01, q02, q18) have no options. Making up
  options would test those options, not the model, so these are left out. That
  leaves 67 scored items instead of 70.

## Running the benchmark

```bash
python3 scripts/build_requests.py        # write the request payloads
python3 scripts/run_bench.py --dry-run   # check them without sending

cp .env.example .env                     # then add your API key
python3 scripts/run_bench.py --limit 5   # quick test
python3 scripts/run_bench.py             # the 67 module-keyed items
python3 scripts/score.py

# the other 89, scored against the Claude labels
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined      # all 156 items
```

`data/results/` already holds the published run. The runner skips questions
that already have an answer there, so the commands above work without an API
key. For a new run, write to another file with `--out data/results/rerun.jsonl`
and pass the same path to `scripts/score.py --results`.

If a run stops partway, just run the same command again. Responses 408, 429 and
5xx are retried automatically, and failed requests are logged without stopping
the run.

`scripts/score.py` reports accuracy by subtest and by confidence level, a Brier
score, accuracy when the least confident answers are skipped, and cost and
latency.

## Summary of results

| Set | Score |
|---|---|
| 67 items, module key | 47.8% |
| 89 items, Claude labels | 85.4% |
| 156 items, combined | 69.2% |

Full details are in **[RESULTS.md](RESULTS.md)**.

## Repository layout

```
data/questions/with_key/        PU, PK, PM (answers from the module key)
data/questions/claude_labeled/  PPU, PBM, LBI, LBE (answers from Claude labels)
data/audit/                     module key audit and disputed items
data/figures/                   original figure crops
data/results/                   the run in RESULTS.md, one line per question
scripts/build_requests.py       turn questions into request payloads
scripts/run_bench.py            send payloads, record answers and tokens
scripts/score.py                score a run
```

`data/requests/` is generated locally and not tracked by git. `data/results/`
is kept exactly as recorded, so the numbers in RESULTS.md can be recomputed and
compared with new runs.

## Attribution

Questions: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). The typesetting is licensed CC BY-NC 4.0.
The question content belongs to the exam organiser and is used here for
non-commercial research only.
