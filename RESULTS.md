# Results

**English** · [Bahasa Indonesia](RESULTS.id.md)

Model `jev-1.13.0`, requested as `jev-latest`. Run on 18 September 2026.
156 questions, one request per question, sequential scoring, figures supplied
as text transcriptions. No request required a retry.

## Score by subtest

| Subtest | Score | Items | Reference |
|---|---|---|---|
| LBE — Literasi Bahasa Inggris | 100.0% | 20/20 | Claude labels |
| LBI — Literasi Bahasa Indonesia | 89.7% | 26/29 | Claude labels |
| PBM — Pemahaman Bacaan dan Menulis | 75.0% | 15/20 | Claude labels |
| PPU — Pengetahuan dan Pemahaman Umum | 75.0% | 15/20 | Claude labels |
| PU — Penalaran Umum | 60.0% | 18/30 | module key |
| PM — Penalaran Matematika | 45.0% | 9/20 | module key |
| PK — Pengetahuan Kuantitatif | 29.4% | 5/17 | module key |

## Score by reference

| Set | Score | Items |
|---|---|---|
| Module key | 47.8% | 32/67 |
| Module key, excluding the two disputed items | 49.2% | 32/65 |
| Claude labels | 85.4% | 76/89 |
| Combined | 69.2% | 108/156 |

The module's key covers PU, PK and PM. The remaining four subtests have no key
in the module and are scored against Claude Opus 5's labels, which are one
model's reading rather than an official answer key. Random selection among five
options scores 20%; PK's four quantity-comparison items give 25%; a
three-statement Ya/Tidak table scored whole gives 12.5%.

## PU by question type

PU is the only subtest in the set that mixes verbal and computational items.

| Items | Score |
|---|---|
| q1–q20, verbal reasoning | 75.0% (15/20) |
| q21–q30, arithmetic and chart reading | 30.0% (3/10) |

## Calibration

Over the 154 items answered as a Choice. The two Ya/Tidak tables return
per-statement probabilities and carry no Choice confidence.

| Confidence | Score | Items |
|---|---|---|
| 0.0–0.5 | 34.0% | 16/47 |
| 0.5–0.7 | 68.4% | 13/19 |
| 0.7–0.9 | 75.0% | 21/28 |
| 0.9–1.0 | 96.7% | 58/60 |

Brier score on the probability assigned to the reference answer: 0.253 over all
154 items, 0.402 on the module-keyed set, 0.143 on the Claude-labeled set.

Score when the least confident answers are withheld:

| Coverage | Combined | Module key | Claude labels |
|---|---|---|---|
| 100% | 69.2% | 49.2% | 85.4% |
| 90% | 77.0% | 53.4% | 88.8% |
| 80% | 81.3% | 59.6% | 91.5% |
| 70% | 85.2% | 63.0% | 91.9% |

## Ya/Tidak tables

| Measure | Score |
|---|---|
| Whole item, all three statements correct | 0/2 |
| Individual statements | 4/6 |

The two incorrect statements were `PM-d1s1-q06` statement 3, where the
reference is "Tidak" and Jev returned 0.59, and `PM-d1s1-q14` statement 1,
where the reference is "Ya" and Jev returned 0.33.

## Differences from the Claude labels

Agreement on the 89 labeled items, by the confidence recorded on the label:

| Label confidence | Agreement | Items |
|---|---|---|
| high | 90.4% | 47/52 |
| medium | 87.0% | 20/23 |
| low | 64.3% | 9/14 |

The 13 items where the two differ:

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

Neither column is an official key.

## Items where the module's key is disputed

Seven PU items were already flagged before this run, in the audit recorded in
`data/audit/module_key_audit.json`. Jev's answers are listed alongside for
reference. The keys were not changed.

| Item | Module key | Audit | Blind solver | Jev | Jev confidence |
|---|---|---|---|---|---|
| PU-d1-q05 | A | E | E | E | 0.90 |
| PU-d1-q24 | E | A | A | A | 0.34 |
| PU-d1-q18 | B | B | E | E | 0.59 |
| PU-d1-q11 | E | D | D | E | 0.54 |
| PU-d1-q10 | B | A | A | B | 0.41 |
| PU-d1-q15 | B | D | D | A | 0.19 |
| PU-d1-q20 | A | B | B | B | 0.39 |

`PU-d1-q05` and `PU-d1-q24` are the two items excluded in the 49.2% figure
above.

## Cost and latency

| Run | Requests | Input tokens | Output tokens | Cost | p50 | p95 |
|---|---|---|---|---|---|---|
| Module-keyed set | 67 | 35,883 | 3,558 | $0.0015 | 884 ms | 1083 ms |
| Claude-labeled set | 89 | 70,754 | 4,710 | $0.0030 | 882 ms | 1187 ms |
| Total | 156 | 106,637 | 8,268 | $0.0045 | 883 ms | 1187 ms |

Cost is computed at $0.042 per million input tokens with output not charged,
which is the rate `scripts/score.py` uses by default (`--rate-per-mtok`); the
documentation carries no pricing page, so the rate should be checked against
current pricing. Four requests ran concurrently. No 429 or 5xx response was
returned.

## Scope of the measurement

- The questions are a community reconstruction of the 2025 paper from
  participant recollection, and the module's keys are its authors' own work,
  not official. See the [README](README.md).
- Three PK fill-in items are excluded from every figure above, leaving 67 of
  the 70 module-keyed items. They have no answer options in the source.
- Figures were supplied as hand-written text transcriptions; no image was sent
  to the model. A run without the transcriptions was not performed, so their
  contribution to the scores is not isolated.
- One run, one model version, no repetitions. No figure above carries an error
  estimate.

The responses behind every figure above are in `data/results/`, one JSON line
per question with the answer, its probabilities and the token usage. Recompute
with `python3 scripts/score.py` and `python3 scripts/score.py --combined`; a
new run can be produced with `python3 scripts/run_bench.py`.
