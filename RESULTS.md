# Results

**English** · [Bahasa Indonesia](RESULTS.id.md)

Model `jev-1.13.0` (called as `jev-latest`), run on 18 September 2026. 156
questions, one request each, with figures sent as text. No request needed a
retry.

## Score by subtest

| Subtest | Score | Items | Reference |
|---|---|---|---|
| LBE (Literasi Bahasa Inggris) | 100.0% | 20/20 | Claude labels |
| LBI (Literasi Bahasa Indonesia) | 89.7% | 26/29 | Claude labels |
| PBM (Pemahaman Bacaan dan Menulis) | 75.0% | 15/20 | Claude labels |
| PPU (Pengetahuan dan Pemahaman Umum) | 75.0% | 15/20 | Claude labels |
| PU (Penalaran Umum) | 60.0% | 18/30 | module key |
| PM (Penalaran Matematika) | 45.0% | 9/20 | module key |
| PK (Pengetahuan Kuantitatif) | 29.4% | 5/17 | module key |

## Score by reference

| Set | Score | Items |
|---|---|---|
| Module key | 47.8% | 32/67 |
| Module key, without the two disputed items | 49.2% | 32/65 |
| Claude labels | 85.4% | 76/89 |
| Combined | 69.2% | 108/156 |

The module key only covers PU, PK and PM. The other four subtests are scored
against labels from Claude Opus 5, which are not an official key. For
comparison, random guessing scores 20% with five options, 25% on PK's
four-option comparison questions, and 12.5% on a three-statement Ya/Tidak
table.

## PU by question type

PU mixes verbal and math questions.

| Items | Score |
|---|---|
| q1 to q20, verbal reasoning | 75.0% (15/20) |
| q21 to q30, math and chart reading | 30.0% (3/10) |

## Calibration

Based on the 154 Choice questions. The two Ya/Tidak tables are left out
because they don't return a Choice confidence.

| Confidence | Score | Items |
|---|---|---|
| 0.0 - 0.5 | 34.0% | 16/47 |
| 0.5 - 0.7 | 68.4% | 13/19 |
| 0.7 - 0.9 | 75.0% | 21/28 |
| 0.9 - 1.0 | 96.7% | 58/60 |

The more confident Jev is, the more often it is right.

Brier score: 0.253 across all 154 items, 0.402 on the module-keyed set, and
0.143 on the Claude-labeled set. Lower is better.

Score when the least confident answers are skipped:

| Answered | Combined | Module key | Claude labels |
|---|---|---|---|
| 100% | 69.2% | 49.2% | 85.4% |
| 90% | 77.0% | 53.4% | 88.8% |
| 80% | 81.3% | 59.6% | 91.5% |
| 70% | 85.2% | 63.0% | 91.9% |

## Ya/Tidak tables

| Measure | Score |
|---|---|
| Per item (all three statements correct) | 0/2 |
| Per statement | 4/6 |

The two wrong statements:

- `PM-d1s1-q06` statement 3: reference is "Tidak", Jev returned 0.59.
- `PM-d1s1-q14` statement 1: reference is "Ya", Jev returned 0.33.

## Differences from the Claude labels

Agreement on the 89 labeled items, by label confidence:

| Label confidence | Agreement | Items |
|---|---|---|
| high | 90.4% | 47/52 |
| medium | 87.0% | 20/23 |
| low | 64.3% | 9/14 |

The 13 items where they disagree:

| Item | Label | Label confidence | Jev | Jev confidence |
|---|---|---|---|---|
| PPU-d1s1-q11 | E | low | A | 0.98 |
| PBM-d1s1-q15 | D | medium | B | 0.87 |
| LBI-d1s1-q26 | E | medium | A | 0.80 |
| PPU-d1s1-q04 | A | medium | E | 0.80 |
| LBI-d1s1-q13 | C | low | D | 0.70 |
| PBM-d1s1-q03 | A | high | B | 0.56 |
| PBM-d1s1-q04 | C | low | E | 0.54 |
| LBI-d1s1-q09 | E | low | C | 0.46 |
| PBM-d1s1-q16 | E | high | C | 0.44 |
| PPU-d1s1-q20 | A | high | B | 0.40 |
| PPU-d1s1-q17 | D | high | A | 0.27 |
| PPU-d1s1-q16 | A | low | D | 0.12 |
| PBM-d1s1-q10 | B | high | C | 0.10 |

Neither the labels nor Jev's answers are an official key.

## Disputed module keys

Seven PU items were flagged before this run (see
`data/audit/module_key_audit.json`). Jev's answers are shown for comparison.
The keys were not changed.

| Item | Module key | Audit | Blind solver | Jev | Jev confidence |
|---|---|---|---|---|---|
| PU-d1-q05 | A | E | E | E | 0.90 |
| PU-d1-q24 | E | A | A | A | 0.34 |
| PU-d1-q18 | B | B | E | E | 0.59 |
| PU-d1-q11 | E | D | D | E | 0.54 |
| PU-d1-q10 | B | A | A | B | 0.41 |
| PU-d1-q15 | B | D | D | A | 0.19 |
| PU-d1-q20 | A | B | B | B | 0.39 |

`PU-d1-q05` and `PU-d1-q24` are the two items left out of the 49.2% score.

## Cost and latency

| Run | Requests | Input tokens | Output tokens | Cost | p50 | p95 |
|---|---|---|---|---|---|---|
| Module-keyed set | 67 | 35,883 | 3,558 | $0.0015 | 884 ms | 1083 ms |
| Claude-labeled set | 89 | 70,754 | 4,710 | $0.0030 | 882 ms | 1187 ms |
| Total | 156 | 106,637 | 8,268 | $0.0045 | 883 ms | 1187 ms |

Cost uses $0.042 per million input tokens, with output tokens free. This is
the default rate in `scripts/score.py` (change it with `--rate-per-mtok`). The
TypeSafe docs don't list pricing, so check this rate against current prices.
Four requests ran at a time, with no 429 or 5xx responses.

## Limitations

- The questions are a community reconstruction, and the module key is not
  official. See the [README](README.md).
- Three PK fill-in questions are not scored, leaving 67 of 70 module-keyed
  items.
- Figures were sent as text, not images. No run without transcriptions has
  been done, so their effect on the score is unknown.
- One run on one model version, so there are no error estimates.

All responses are in `data/results/`, one JSON line per question. Recompute
with `python3 scripts/score.py` and `python3 scripts/score.py --combined`. For
a new run, use `python3 scripts/run_bench.py`.
