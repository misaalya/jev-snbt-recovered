# Jev on recovered SNBT 2025 — first run

Model `jev-1.13.0` (requested as `jev-latest`), 2026-09-18. One request per
item, no figures (every figure is a text transcription in the state), no
retries needed. Reproduce with:

```bash
python3 scripts/build_requests.py && python3 scripts/run_bench.py && python3 scripts/score.py
```

## Headline: 67 items with the module's own key

| Subtest | Accuracy | Items |
| --- | --- | --- |
| PU (penalaran umum) | **60.0%** | 18/30 |
| PM (penalaran matematika) | **45.0%** | 9/20 |
| PK (pengetahuan kuantitatif) | **29.4%** | 5/17 |
| **All** | **47.8%** | 32/67 |

Dropping the two items whose keys the audit disputes (`PU-d1-q05`,
`PU-d1-q24`): **49.2%** (32/65). Random guessing on five options is 20%.

The split inside PU is the sharpest result in the run:

| | Accuracy |
| --- | --- |
| PU q1–q20, verbal reasoning | **75%** (15/20) |
| PU q21–q30, arithmetic and charts | **30%** (3/10) |

Read together with PK (29.4%) and PM (45.0%), both computational subtests, the
pattern is consistent: this is a model that reads well and calculates poorly.
Nothing here is a reasoning-model comparison — Jev returns a typed judgment
without working anything out step by step, and the arithmetic items need
several steps.

## Calibration

Confidence tracks correctness closely, which matters more than the headline for
anyone building on it:

| Confidence | Accuracy |
| --- | --- |
| 0.0–0.5 | 21.9% (7/32) |
| 0.5–0.7 | 50.0% (4/8) |
| 0.7–0.9 | 72.7% (8/11) |
| 0.9–1.0 | **92.9%** (13/14) |

Brier score on the probability given to the correct option: 0.402. Leaving the
least confident answers blank lifts accuracy as it should: 49.2% at full
coverage, 59.6% at 80%, 63.0% at 71%. The model knows when it does not know.

## The two Ya/Tidak tables

0 of 2 whole items, 4 of 6 statements. Both failures are single rows:
`PM-d1s1-q06` statement 3 (0.59 for a false claim about 2^64 versus 2^63) and
`PM-d1s1-q14` statement 1 (0.33 for a true claim). Whole-item scoring is
unforgiving by design, and with two items it says little on its own.

## Agreement arm: 89 items with no module key

Not accuracy — neither Jev nor Claude's labels are ground truth. This measures
how often two independent readers pick the same option.

| Subtest | Agreement |
| --- | --- |
| LBE | 100.0% (20/20) |
| LBI | 89.7% (26/29) |
| PBM | 75.0% (15/20) |
| PPU | 75.0% (15/20) |
| **All** | **85.4%** (76/89) |

Broken down by how sure the label was: high 90.4%, medium 87.0%, low 64.3%.
The disagreements concentrate exactly where the labels already said they were
unsure, which is the pattern you want to see — it supports both the labels and
Jev's calibration, and it is evidence against the labels being arbitrary.

The gap between 85.4% here and 47.8% on the keyed set is not a contradiction:
the keyless subtests are reading and language items, while PK and PM are
computational, and Jev's weakness is computation.

## The disputed keys

Jev is a different model family from the auditors, so its answers are a third
independent reading of the seven contested PU items:

| Item | Module | Audit | Blind solver | Jev (confidence) |
| --- | --- | --- | --- | --- |
| q05 | A | E | E | **E (0.90)** |
| q24 | E | A | A | **A (0.34)** |
| q18 | B | B | E | **E (0.59)** |
| q11 | E | D | D | E (0.54) |
| q10 | B | A | A | B (0.41) |
| q15 | B | D | D | A (0.19) |
| q20 | A | B | B | B (0.39) |

`PU-d1-q05` now has three independent readers choosing E, one of them at 0.90
confidence — its highest-confidence answer among the contested items. That
strengthens the case that the module's A is a genuine key error. `PU-d1-q24`
gets a third vote for A, though at low confidence. The rest stay unsettled and
the keys stay as the module has them.

## Cost and latency

| Run | Requests | Input tokens | Cost | p50 | p95 |
| --- | --- | --- | --- | --- | --- |
| Keyed (67) | 67 | 35,883 | $0.0015 | 884 ms | 1083 ms |
| Agreement (89) | 89 | 70,754 | $0.0030 | 882 ms | 1187 ms |

At $0.042 per 1M input tokens, output free. Verify the rate against current
pricing before quoting it: the docs carry no pricing page, so `score.py` takes
it as `--rate-per-mtok`. No request needed a retry; no 429 or 5xx was seen at
concurrency 4.

## Caveats

- The questions are a community reconstruction from participant recollection,
  and the keys are the module authors' own, not official. See the README.
- 3 PK fill-in items are excluded: they have no options, so they cannot be
  asked as a Choice without invented distractors.
- Figures reach the model only as text transcriptions written by hand. A
  figures-off arm was not run, so the contribution of those transcriptions to
  the score is not separated out.
- One run, one model version, no repeats: nothing here has error bars.
