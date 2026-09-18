# jev-snbt-recovered

**First run: Jev 1.13.0 scores 47.8% (32/67) against the module's keys — 75% on PU's verbal half, 30% on its arithmetic half — and 85.4% (76/89) on the language subtests scored against Claude's labels; 69.2% (108/156) over everything, mixed reference. Full numbers in [RESULTS.md](RESULTS.md).**

Benchmark of **TypeSafe Jev** (System One model) on community-recovered
**SNBT 2025** (Indonesian university entrance test) questions.

Status: **dataset extraction done for Day 1 / Sesi 1 of all seven subtests**
(159 questions: 70 with the module's key, 89 labeled by Claude). Benchmark
runner and results: not yet.

## Data source

Questions come from *Modul MMA SNBT 2025* by Tim Mangkuk Mi Ayam, a community
reconstruction of the 2025 SNBT test from participant recollection
(`dataset/MMASNBT2025.pdf`, 764 pages, not committed). Typesetting and layout
are licensed **CC BY-NC 4.0**; the question content itself belongs to the test
organiser and is reproduced here for non-commercial research only.

Two caveats that follow from the source:

- Answer keys are the module authors' own work, not official. Their PU key
  carries the disclaimer *"bukan jawaban yang pasti"*. Keys exist only for
  **PU, PK and PM**; PPU, PBM, LBI and LBE have no key in the module.
- Some items are visibly damaged by the reconstruction: `LBI-d1s1-q21` has four
  options, `LBE-d1s1-q09`'s stem appears to contain its own answer,
  `LBI-d1s1-q10` asks for a food but lists life-cycle sequences, `LBE-d1s1-q11`
  misquotes the passage it asks about, and `PPU-d1s1-teks4` reads "kristal
  udara" where "kristal es" is clearly meant — which is exactly what makes
  sentence (1) the illogical one in `PPU-d1s1-q16`. Nothing is silently
  repaired: every such item or passage is kept verbatim and carries a
  `_source_note`, and the affected labels say so in their rationale.

## What is extracted

Per the project rule, **Day 1 Sesi 1** of each subtest; where a subtest has
no session split, **Day 1**.

| Subtest | Section | PDF pages | Passages | Questions | Module key | Claude label | Figures | Item types |
|---|---|---|---|---|---|---|---|---|
| PU | Day 1 | 9–22 | 0 | 30 | 30 | – | 3 | mcq 30 |
| PPU | Day 1 Sesi 1 | 87–96 | 5 | 20 | – | 20 | 0 | mcq 20 |
| PBM | Day 1 Sesi 1 | 128–136 | 4 | 20 | – | 20 | 0 | mcq 20 |
| PK | Day 1 Sesi 1 | 168–173 | 2 | 20 | 20 | – | 3 | fill_in 3, mcq 9, multi_statement 3, quantity_comparison 3, data_sufficiency 2 |
| LBI | Day 1 Sesi 1 | 224–237 | 7 | 29 | – | 29 | 1 | mcq 29 |
| LBE | Day 1 Sesi 1 | 306–314 | 5 | 20 | – | 20 | 0 | mcq 20 |
| PM | Day 1 Sesi 1 | 351–356 | 5 | 20 | 20 | – | 2 | mcq 18, table_yes_no 2 |

PU = Penalaran Umum, PPU = Pengetahuan dan Pemahaman Umum, PBM = Pemahaman
Bacaan dan Menulis, PK = Pengetahuan Kuantitatif, LBI = Literasi Bahasa
Indonesia, LBE = Literasi Bahasa Inggris, PM = Penalaran Matematika.

## Answer sources

Every answered item says where its answer came from (`answer_source`):

- `module` — the module's own key (PU) or worked solutions (PK, PM). Not
  official; see the caveat above.
- `claude-opus-5` — for the four subtests the module has no key for (PPU, PBM,
  LBI, LBE), the 89 items were labeled by Claude Opus 5 from the extracted
  text on 2026-09-18 (`data/labels/<section>.json`, with a one-line rationale
  and a `confidence` of high / medium / low per item). These are one model's
  reading, not ground truth; low-confidence items are genuinely ambiguous in the
  recovered text. Counts: high 52, medium 23, low 14.
  As a check, two further Claude Opus 5 instances labeled the same 89 items
  blind, independently of each other and of the first labels (each saw only the
  question, passage and options). All three agree on 87/89. The two remaining
  disagreements (`LBE-d1s1-q05`, `LBE-d1s1-q09`) are marked low and name the
  alternative; `LBI-d1s1-q28` was changed to follow both blind graders. Each
  label file records the two blind answers as `blind_check` and `blind_check2`,
  so the per-item agreement is auditable. That agreement is a weak check on its
  own — all three graders are the same model, so their errors correlate.
  A second, bias-oriented audit measures the labels against the 62 five-option
  items whose key comes from the module, used as a control: the letter
  distribution is consistent with chance (chi-square 1.77, df 4), but the labels
  pick the longest option 28% of the time (control 21%) and the option that most
  echoes the passage's wording 31% of the time (control 21%). The six items
  affected by both biases were re-derived by hand; one (`LBI-d1s1-q08`) did not
  survive unchanged and is now low confidence with its alternative recorded.
  Treat the remaining labels as one model's reading with a known, measured
  lexical-matching bias, not as a key.
  Finally, all 89 questions were read and answered again from scratch. That pass
  changed `PBM-d1s1-q15` (E to D: "informasi utama" keeps the object's attribute
  "baru" — the three earlier votes had all applied a shortest-is-core heuristic)
  and confirmed the other 88. Each label carries that answer as `reread`.
  A fourth pass repeated that exercise per subtest — answer blind first, then
  compare and re-argue every difference (`review3` on each label). It matched on
  84/89 and, after re-arguing, endorsed the stored answer in 4 of the 5
  differences, including an independent re-derivation of the `PBM-d1s1-q15`
  change. Its one standing objection (`LBE-d1s1-q05`, C instead of A) rests on
  how the distractors look built rather than on the text, and was not taken;
  both readings are recorded on the item.

### Audit of the module's own key

The 70 module-answered items were also solved from scratch, without looking at
the key, with every computation checked in Python; the results were then diffed
against the module (`data/audit/module_key_audit.json`). PK (20/20) and PM
(20/20) match exactly. PU matches on 24 of 30. Each of the six differences was
re-argued:

- `PU-d1-q05` — module A, audit E. The text says the malaria figure "tidak
  menurun", never that it rose, so option (a) adds a claim the text does not
  make, while (e) is the causal chain stated outright. Most likely a key error.
- `PU-d1-q24` — module E, audit A. The question asks what describes the 2024
  *neraca keuangan*, and (e) is a prediction about the trader's behaviour. The
  diagram has no 2024 point, so the answer has to survive extrapolation: (a)
  "mengalami kerugian" needs only the direction of the trend (H < M in 2021,
  2022 and 2023) and holds even if the scanned scale is read a little off,
  while (b) "besarnya kerugian sama dengan tahun sebelumnya" asserts an equal
  magnitude for a year with no plotted point. Key looks wrong; (a) is the best
  replacement, (b) the runner-up.
- `PU-d1-q11` — module E, audit D. Genuinely ambiguous: (d) is the bridging
  assumption, (e) the supporting evidence. Key stands.
- `PU-d1-q10`, `PU-d1-q15`, `PU-d1-q20` — the module is right and the audit
  answer was withdrawn; the reasons are recorded in the audit file.

A second, blind round put the same 70 items to three separate Claude Opus 5
instances, one per subtest. Each got only an answer-free copy of its questions
(outside the repo, with the figures copied next to it), no hint about the
module's key or about the findings above, and was told not to open the project
directory. PK and PM came back 20/20 identical to the module again. PU came back
23/30, disagreeing on the same six items plus one new one:

- `PU-d1-q05` — the blind solver also answered E, independently. This is now
  the strongest candidate for an actual key error.
- `PU-d1-q24` — the blind solver also rejected E, answering A ("mengalami
  kerugian"). Two independent solvers reject the key; on re-argument A is the
  better replacement, since B pins an exact loss to a year the chart does not
  plot.
- `PU-d1-q18` — new: the blind solver answered E and pointed out that the key
  (B) is formally a denial of the antecedent, since "if unity fades, conflict
  rises" does not yield "if the tradition is kept up, conflict is prevented".
  Recorded as disputed; the key still stands under the item's softer "PALING
  MUNGKIN BENAR" framing.
- `PU-d1-q10`, `PU-d1-q11`, `PU-d1-q15`, `PU-d1-q20` — the blind solver landed
  on the first-pass audit answers, all at medium confidence and all flagged by
  it as ambiguous. The module's key is still the better reading on each; note
  that all three solvers are the same model, so their agreement is not
  independent evidence.

The round also flagged item-quality problems that do not change any answer: a
non-unique system and a variable typo in `PK-d1s1-q17`, two tautological
statements in `PK-d1s1-q19`, and an internally inconsistent chart in PM's teks 4
(69 kuintal supplied against 70 sold, so Sunday's cumulative stock is negative).

The keys in `with_key/` are left exactly as the module has them; the audit is
recorded alongside, not merged in. For scoring, `data/audit/disputed_items.json`
carries the list a runner needs: `PU-d1-q05` and `PU-d1-q24` as exclusion
candidates — both were rejected by two independent solvers with nobody defending
the key, so a model that answers them correctly would be marked wrong — and
seven further items flagged as ambiguous or badly built but keyed as-is. PU
accuracy is best reported twice, with and without the two.

The two are never mixed: `with_key/` holds only module answers,
`claude_labeled/` only Claude's, and `without_key/` is the same 89 items with
`answer: null` for anyone who wants to label them independently.

## Layout

```
data/questions/with_key/<section>.json        items answered by the module (PU, PK, PM)
data/questions/claude_labeled/<section>.json  the keyless items with Claude's labels (PPU, PBM, LBI, LBE)
data/questions/without_key/<section>.json     the same keyless items, answer null
data/labels/<section>.json      Claude's labels: answer, confidence, rationale per item
data/overrides/<section>.json   hand corrections merged over the automatic extraction
data/audit/module_key_audit.json  independent re-solve of the 70 module-answered items
data/audit/blind_<section>.json   raw answers from the blind re-solve round
data/audit/disputed_items.json    items to exclude from / flag in scoring
data/figures/<id>.png           crops of every figure/table/diagram in the extracted items
data/raw/                       pdftotext dumps (not committed)
data/pages/                     page renders used for review (not committed)
scripts/extract.py              PDF -> JSON (pdftohtml XML, keeps bold/italic as markdown)
scripts/crop.py                 crop a figure from a page render into data/figures/
scripts/build_requests.py       questions -> System One request payloads (JSONL)
scripts/run_bench.py            post the payloads, record answers/usage/latency
scripts/score.py                score a run against the module's keys
data/requests/<split>.jsonl     the payloads a runner posts, one per question (67 keyed items)
data/results/<split>.jsonl      raw run output (gitignored)
```

`extract.py` is deterministic: `raw PDF -> automatic parse -> answer key ->
overrides -> labels`. Re-running it regenerates `data/questions/` exactly.

## Asking the items as System One questions

`scripts/build_requests.py` turns the dataset into the exact payloads a runner
posts to `POST https://api.typesafe.ai/v1/systemone`, so the request behind a
score stays inspectable. Three item types need three shapes:

- **mcq (154 items)** — one Choice, criteria are the item's own options, `a`–`e`
  (`a`–`d` for PK's four quantity-comparison items). Nothing is synthesised.
- **table_yes_no (PM q06, q14)** — one request carrying three Nouls over the same
  state, one per statement, which is what the docs recommend for several
  independent yes/no labels on one input.
- **fill_in (PK q01, q02, q18)** — the source gives no options, so these cannot
  be a Choice as they stand. **They are out of the benchmark**: the headline set
  is the remaining 67 keyed items, and the builder skips them unless `--fill-in`
  is passed. That flag exists only so the decision can be revisited; it writes a
  separate file that is never folded into the headline, using the candidate sets
  in `data/audit/fill_in_candidates.json` (each distractor the result of one
  writable error path, plus a no-match option). Nothing in `data/requests/`
  contains them by default.

So the scored set is **67 items**: PU 30, PK 17, PM 20. Drop the two disputed PU
keys and it is 65; report both.

Scoring:

| item | correct when |
| --- | --- |
| mcq | `answers.jawaban.choice` equals the key |
| table_yes_no | every statement satisfies `(noul >= 0.5) == (key == "Ya")` |

A three-statement table scored whole gives a 12.5% guessing baseline, close
enough to a five-option mcq's 20% to sit in the same accuracy figure; the
per-statement number (50% baseline) is reported separately and never mixed in.
PK's four-option items have a 25% baseline, which matters if a hensachi-style
score is reported.

## Running the benchmark

```bash
python3 scripts/build_requests.py                      # 67 payloads, one per item
python3 scripts/build_requests.py --group-by-passage   # + the 48-request batch arm
python3 scripts/run_bench.py --dry-run                 # validate payloads, send nothing

export TYPESAFE_API_KEY=...
python3 scripts/run_bench.py --limit 5                 # smoke test against the live API
python3 scripts/run_bench.py                           # the full headline run
python3 scripts/score.py
```

`run_bench.py` writes one result line per request — answers, token usage,
latency and attempt count — and skips ids already in the output file, so a run
cut short by a rate limit is resumed by repeating the command. Retries follow
the SDK's documented policy: 408, 429 and 5xx back off exponentially with
jitter and honour `Retry-After` / `retry-after-ms`; 400, 401, 403, 404 and 422
stop that item instead of being hammered. Failures are recorded as result lines
with an `error` field rather than aborting the run. Results are gitignored:
they are run artefacts, not data.

`score.py` reports accuracy overall and per subtest, the same figure with the
two disputed PU keys dropped, the Ya/Tidak items whole-item and per statement,
accuracy by confidence band with a Brier score on the probability given to the
correct option, what accuracy would be if the least confident answers were left
blank, and token cost and latency. The cost rate is a flag
(`--rate-per-mtok`, default 0.042) because the docs carry no pricing page —
check it against current pricing before quoting a number.

Both scripts were exercised end to end on synthetic result files before any
live run, including the batch arm's answer-splitting path.

## Question schema

```jsonc
{
  "id": "PK-d1s1-q04",          // <subtest>-d<day>[s<session>]-q<nn>
  "subtest": "PK", "day": 1, "session": 1, "number": 4,
  "type": "mcq",                // mcq | fill_in | table_yes_no
  "subtype": null,              // multi_statement | quantity_comparison | data_sufficiency
  "passage_ids": ["PK-d1s1-teks2"],   // passages the item refers to (may be several, e.g. LBE Text 1 + Text 2)
  "passages": [{"id": "PK-d1s1-teks2", "text": "...", "figure_path": "...", "figure_note": "...",
                "_source_note": null, "source_page": 169}],
                                // the same passages embedded in full: every item is self-contained
  "has_answer": true,
  "question": "...",            // markdown: **bold**, _italic_, \n for line/paragraph breaks
  "options": {"a": "...", "e": "..."},
  "statements": [],             // table_yes_no only
  "answer": "C",                // letter | fill-in value ("64") | ["Ya","Tidak","Tidak"] | null
  "answer_source": "module",    // "module" | "claude-opus-5" | null
  "label_confidence": null,     // high | medium | low, only when answer_source is "claude-opus-5"
  "has_figure": true,
  "figure_path": "data/figures/PK-d1s1-q04.png",   // crop of the original
  "figure_note": "...",         // text transcription of the figure, written by hand
  "source_page": 168,
  "_source_note": null,         // oddities inherited from the source (passages carry one too)
  "needs_review": false, "review_reasons": []
}
```

A shared passage ("Teks 1", a forum thread, a chart) is printed once in the
module but embedded in full into every item that refers to it, together with
its figure transcription, so an item never needs an external lookup. The same
holds for a figure serving several items: `PM-d1s1-teks4`'s chart transcription,
for instance, is carried by each of q13–q16.

Where the module states the range ("Bacalah ... untuk nomor 17 sampai 19") it is
used directly; where it just stops using a passage without printing a new "Teks"
heading, the range is written down in `data/overrides/` as `covers`, because
otherwise the passage would keep attaching to the self-contained items that
follow. `extract.py` prints the resulting coverage per section on every run:

```
PK_d1s1    2 passages, 20 questions, 20 keyed,  0 labeled,  0 flagged
           teks1:q6-q8, teks2:q9-q11
```

Math is written in plain text: `x²`, `√29`, `2^(n–1)`, `a/b`, `6 5/7` (mixed
number). Every PK and PM item, and every item flagged by the extractor
(stacked fractions, figures, odd option counts), was rewritten by hand from the
page render; see `data/overrides/`.

## Extraction notes

- Figures are cropped from a 200-dpi render and transcribed into
  `figure_note`, so that every model receives the same text-only input. The
  original crop is kept so the transcription can be audited.
- Paragraph breaks in passages are recovered from the first-line indent, and in
  justified passages (which the module does not indent) from a line that stops
  short of the right margin, so
  items that say "Text 2 Paragraph 3" can be resolved against `passages[].text`
  (paragraphs are separated by `\n`).
- Bold/italic matter for some items ("kata **bercetak tebal**", "the word
  _may_"), so extraction uses `pdftohtml -xml` rather than `pdftotext`.
- Hyphenation at line ends is rejoined (`me-` + `nang` → `menang`,
  `SA-` + `LAH` → `SALAH`, `Timor-` + `Timur` → `Timor-Timur`).
- Fidelity is re-checked by two automated passes over all 959 question, option,
  statement and passage fields: every field must appear verbatim in an
  independent `pdftotext` dump, and every word and every digit must exist in the
  source. The 38 fields that cannot match that way are the stacked-fraction
  math rewritten by hand; each was re-verified against the page render, and the
  four remaining word-level exceptions are listed in the audit script and carry
  a `_source_note`.
- Figure transcriptions were audited against the crops themselves, including
  measuring the drawn line slopes for `LBI-d1s1-teks2`.

## Attribution

Questions: Modul MMA SNBT 2025, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>), CC BY-NC 4.0 for the typesetting.
