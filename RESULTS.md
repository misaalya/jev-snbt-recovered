# How Jev did on SNBT 2025

**English** · [Bahasa Indonesia](RESULTS.id.md)

`jev-1.13.0`, 18 September 2026. 156 questions, one request each, no retries,
$0.0045 for the whole run.

## The short version

| Subtest | Score | Answer key |
|---|---|---|
| **LBE** Literasi Bahasa Inggris | 100.0% (20/20) | Claude labels |
| **LBI** Literasi Bahasa Indonesia | 89.7% (26/29) | Claude labels |
| **PBM** Pemahaman Bacaan dan Menulis | 75.0% (15/20) | Claude labels |
| **PPU** Pengetahuan dan Pemahaman Umum | 75.0% (15/20) | Claude labels |
| **PU** Penalaran Umum | 60.0% (18/30) | module key |
| **PM** Penalaran Matematika | 45.0% (9/20) | module key |
| **PK** Pengetahuan Kuantitatif | 29.4% (5/17) | module key |

Read the two halves separately. The four language subtests are scored against
Claude's labels, which are one model's reading rather than an official key, so
those rows are a weaker measurement than the three below them. Against the
module's own key Jev scores **47.8%** (32/67); against Claude's labels,
**85.4%** (76/89); over everything, 69.2% (108/156).

## Jev reads Indonesian well and cannot do arithmetic

The clearest result in the run is inside PU, where the same subtest contains
both kinds of question:

| | Score |
|---|---|
| PU q1–q20, verbal reasoning | **75%** (15/20) |
| PU q21–q30, arithmetic and charts | **30%** (3/10) |

That 30% lines up with PK (29.4%) and PM (45.0%), the two computational
subtests, and 75% lines up with the language subtests above. The dividing line
in this benchmark is not language versus English, or easy versus hard — it is
**reading versus calculating**.

It makes sense. Jev returns a typed judgment directly; it does not work through
steps. "Peluang terpilihnya sekretaris perempuan dengan ketua dan bendahara
berjenis kelamin berbeda" needs four or five steps before an answer exists, and
no amount of reading the question gives you the number. Meanwhile "manakah
simpulan yang PALING TEPAT" is a judgment about text, which is what this class
of model is for.

So for Indonesian specifically: on LBI, Jev matched the labels on 26 of 29, and
on PU's verbal items it got 15 of 20 against the module's own key. It handles
Indonesian reading comprehension at a level that is useful. Do not put it in
front of the mathematics section.

## It knows when it does not know

This matters more than the headline if you are building on it. Across all 154
Choice answers:

| Jev's confidence | How often it was right |
|---|---|
| 0.0–0.5 | 34.0% (16/47) |
| 0.5–0.7 | 68.4% (13/19) |
| 0.7–0.9 | 75.0% (21/28) |
| 0.9–1.0 | **96.7%** (58/60) |

The climb is monotone, and it holds on both halves of the benchmark
separately. In practice that means the confidence is usable as a filter:
dropping the least confident third of its answers takes the combined score from
69.2% to 85.2%. On the module-keyed half alone, 49.2% → 63.0%.

Brier score 0.253 overall — 0.402 on the keyed half, 0.143 on the labeled half.

## Where Jev disagreed with our labels

On the 89 questions with no official key, Jev and Claude's labels differ on 13.
Neither side is authoritative, so these are open questions rather than Jev's
mistakes — and the disagreements sit where the labels already admitted doubt:
agreement was 90.4% on high-confidence labels, 87.0% on medium, 64.3% on low.

Four are worth a human look, because both sides are confident and they point in
opposite directions:

| Question | Our label | Jev |
|---|---|---|
| PPU-d1s1-q11 | E (low confidence) | **A (0.98)** |
| PBM-d1s1-q15 | D (medium) | **B (0.87)** |
| LBI-d1s1-q26 | E (medium) | **A (0.80)** |
| PPU-d1s1-q04 | A (medium) | **E (0.80)** |

The other nine are low-confidence on at least one side, where disagreement is
expected. The full list is in the repo.

## Jev found a probable mistake in the answer key

Before this run, an audit had already flagged two PU answers in the module as
likely wrong. Jev is a different model family from the auditors, so its answer
is a third independent reading:

| Question | Module says | Our audit | Blind solver | Jev |
|---|---|---|---|---|
| PU-d1-q05 | A | E | E | **E (0.90)** |
| PU-d1-q24 | E | A | A | **A (0.34)** |
| PU-d1-q18 | B | B | E | **E (0.59)** |

`PU-d1-q05` now has three independent readers choosing E, and it is Jev's
most confident answer among all the disputed items. The question says malaria
cases "tidak menurun" — did not fall — while the keyed option (a) claims they
rose, which the passage never says. Option (e) is the causal chain the passage
states outright.

We did not change the key. It is the module's, and this repo records the
dispute instead of overwriting it. But if you score PU, report it both ways:
47.8% over 67 items, 49.2% over the 65 without these two.

## The Ya/Tidak tables

Jev got 0 of the 2 table questions, and 4 of their 6 individual statements.
Both misses were a single row: one false claim about 2^64 accepted at 0.59, and
one true claim rejected at 0.33. Scoring a table whole is deliberately harsh,
and with only two of them in the paper, this says very little.

## Cost and speed

| Run | Requests | Input tokens | Cost | p50 | p95 |
|---|---|---|---|---|---|
| 67 keyed items | 67 | 35,883 | $0.0015 | 884 ms | 1083 ms |
| 89 labeled items | 89 | 70,754 | $0.0030 | 882 ms | 1187 ms |

At $0.042 per million input tokens, output free — check that rate against
current pricing before quoting it. Nothing needed a retry, and no rate limit
was hit at four concurrent requests.

## What this does not tell you

- The questions are a community reconstruction from memory, and the keys are
  the module authors' own, not official. See the [README](README.md).
- The three PK fill-in questions are excluded — no options to choose from.
- Jev never saw an image. Every figure reached it as a text transcription we
  wrote by hand, so part of what is measured here is the quality of those
  transcriptions. A run without them would separate the two; it has not been
  done.
- One run, one model version, no repeats. None of these numbers has an error
  bar.

Reproduce: `python3 scripts/run_bench.py && python3 scripts/score.py`.
