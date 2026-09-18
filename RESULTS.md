# Jev on recovered SNBT 2025 — first run

**English** · [Bahasa Indonesia](RESULTS.id.md)

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

## Second benchmark: 89 items scored against Claude's labels

Kept separate from the headline on purpose. The module has no key for PPU, PBM,
LBI or LBE, so the reference here is Claude Opus 5's labels — one model's
reading, audited over several passes but not ground truth. Read this as a
second benchmark with a weaker reference, not as accuracy against the exam.

| Subtest | Score | Items |
| --- | --- | --- |
| LBE (literasi bahasa Inggris) | **100.0%** | 20/20 |
| LBI (literasi bahasa Indonesia) | **89.7%** | 26/29 |
| PBM (pemahaman bacaan & menulis) | **75.0%** | 15/20 |
| PPU (pengetahuan & pemahaman umum) | **75.0%** | 15/20 |
| **All** | **85.4%** | 76/89 |

Broken down by how sure the label was: high 90.4% (47/52), medium 87.0%
(20/23), low 64.3% (9/14). The disagreements concentrate where the labels
already said they were unsure, which is what you want to see from both sides.

Calibration on this set is markedly better than on the keyed set:

| Jev confidence | Score |
| --- | --- |
| 0.0–0.5 | 60.0% (9/15) |
| 0.5–0.7 | 81.8% (9/11) |
| 0.7–0.9 | 76.5% (13/17) |
| 0.9–1.0 | **97.8%** (45/46) |

Brier score 0.143, against 0.402 on the keyed set. Coverage: 85.4% at full
coverage, 91.5% at 80%, 91.9% at 70%. Cost 70,754 input tokens ($0.0030),
latency p50 882 ms, p95 1187 ms.

Two readings of the 85.4% are possible and this run cannot separate them: the
language subtests may simply be easier for Jev than the computational ones, or
two models reading the same text may correlate in ways that inflate the figure
above what an official key would give. The kind of item differs too — these are
reading and language questions, while PK and PM are arithmetic.

### The 13 disagreements

Neither column is authoritative, so these are open items rather than errors:

| Item | Label (confidence) | Jev (confidence) |
| --- | --- | --- |
| PPU-d1s1-q11 | E (low) | A (0.98) |
| PBM-d1s1-q15 | D (medium) | B (0.87) |
| LBI-d1s1-q26 | E (medium) | A (0.80) |
| PPU-d1s1-q04 | A (medium) | E (0.80) |
| LBI-d1s1-q13 | C (low) | D (0.70) |
| PBM-d1s1-q03 | A (high) | B (0.56) |
| PBM-d1s1-q04 | C (low) | E (0.54) |
| LBI-d1s1-q09 | E (low) | C (0.46) |
| PBM-d1s1-q16 | E (high) | C (0.44) |
| PPU-d1s1-q20 | A (high) | B (0.40) |
| PPU-d1s1-q17 | D (high) | A (0.27) |
| PPU-d1s1-q16 | A (low) | D (0.12) |
| PBM-d1s1-q10 | B (high) | C (0.10) |

Four are worth a second look because both sides are confident in opposite
directions: `PPU-d1s1-q11` (label low, Jev 0.98), `PBM-d1s1-q15` (Jev 0.87
against a label that an earlier re-read had already changed from E to D),
`LBI-d1s1-q26` and `PPU-d1s1-q04` (both 0.80). The rest are low-confidence on
at least one side, where disagreement is expected.

## Combined: all 156 askable items

Every item the harness can ask, scored against whatever reference it has: 67
against the module's key, 89 against Claude's labels. Broader than either half
— all seven subtests are represented — but the reference is mixed, so this
figure is weaker than the headline and replaces neither.

| Subtest | Score | Reference |
| --- | --- | --- |
| LBE | 100.0% (20/20) | Claude labels |
| LBI | 89.7% (26/29) | Claude labels |
| PBM | 75.0% (15/20) | Claude labels |
| PPU | 75.0% (15/20) | Claude labels |
| PU | 60.0% (18/30) | module key |
| PM | 45.0% (9/20) | module key |
| PK | 29.4% (5/17) | module key |
| **All** | **69.2%** (108/156) | mixed |

Split by reference: 47.8% against the module's keys, 85.4% against Claude's
labels. Those two numbers are what the 69.2% is made of, and the gap between
them is large enough that the combined figure should always be quoted with
them, never on its own. It also tracks the subject split — the module-keyed
subtests are the computational ones and the labeled subtests are the language
ones — so the combined number reflects that mix as much as it reflects Jev.

Calibration over all 156 (154 with a Choice confidence; the two Ya/Tidak items
return per-statement probabilities instead):

| Confidence | Score |
| --- | --- |
| 0.0–0.5 | 34.0% (16/47) |
| 0.5–0.7 | 68.4% (13/19) |
| 0.7–0.9 | 75.0% (21/28) |
| 0.9–1.0 | **96.7%** (58/60) |

Brier 0.253. Coverage: 70.1% at full coverage, 81.3% at 80%, 85.2% at 70%. The
monotone climb holds across the mixed reference, which is the most useful thing
in this section: whatever the score, Jev's own confidence orders its answers
correctly.

Whole run: 156 requests, 106,637 input tokens, **$0.0045**, p50 883 ms, p95
1187 ms.

Reproduce with `python3 scripts/score.py --combined`.

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
