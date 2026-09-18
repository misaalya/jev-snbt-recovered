# jev-snbt-recovered

[English](README.md) · **Bahasa Indonesia**

**Run pertama: Jev 1.13.0 memperoleh 47,8% (32/67) terhadap kunci modul — 75% di separuh verbal PU, 30% di separuh hitungannya — dan 85,4% (76/89) di subtes bahasa yang dinilai terhadap label Claude; 69,2% (108/156) untuk keseluruhan dengan acuan campuran. Angka lengkap di [RESULTS.id.md](RESULTS.id.md).**

Benchmark **TypeSafe Jev** (model System One) pada soal **SNBT 2025** hasil
rekonstruksi komunitas.

Status: **ekstraksi dataset selesai untuk Hari 1 / Sesi 1 ketujuh subtes**
(159 soal: 70 berkunci modul, 89 berlabel Claude), harness benchmark jalan,
hasil run pertama tersedia di [RESULTS.id.md](RESULTS.id.md).

## Sumber data

Soal berasal dari *Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam, sebuah
rekonstruksi komunitas atas SNBT 2025 dari ingatan peserta
(`dataset/MMASNBT2025.pdf`, 764 halaman, tidak ikut di-commit). Penataan dan
tata letaknya berlisensi **CC BY-NC 4.0**; isi soalnya sendiri milik
penyelenggara ujian dan direproduksi di sini semata untuk riset non-komersial.

Dua caveat yang mengikuti dari sumbernya:

- Kunci jawaban adalah karya penyusun modul, bukan kunci resmi. Kunci PU mereka
  memuat disclaimer *"bukan jawaban yang pasti"*. Kunci hanya ada untuk
  **PU, PK, dan PM**; PPU, PBM, LBI, dan LBE tidak punya kunci di modul.
- Sebagian soal rusak akibat rekonstruksinya: `LBI-d1s1-q21` hanya punya empat
  opsi, batang soal `LBE-d1s1-q09` tampaknya memuat jawabannya sendiri,
  `LBI-d1s1-q10` menanyakan makanan tetapi opsinya urutan daur hidup,
  `LBE-d1s1-q11` salah mengutip bacaan yang ditanyakannya, dan
  `PPU-d1s1-teks4` tertulis "kristal udara" padahal jelas maksudnya "kristal
  es" — justru itulah yang membuat kalimat (1) menjadi yang tidak logis di
  `PPU-d1s1-q16`. Tidak ada yang diperbaiki diam-diam: setiap soal atau bacaan
  semacam itu dipertahankan apa adanya dan membawa `_source_note`, dan label
  yang terdampak menyebutkannya di rationale.

## Apa yang diekstraksi

Sesuai aturan proyek, **Hari 1 Sesi 1** tiap subtes; bila subtes tidak terbagi
sesi, **Hari 1**.

| Subtes | Bagian | Halaman PDF | Bacaan | Soal | Kunci modul | Label Claude | Gambar | Jenis soal |
|---|---|---|---|---|---|---|---|---|
| PU | Hari 1 | 9–22 | 0 | 30 | 30 | – | 3 | mcq 30 |
| PPU | Hari 1 Sesi 1 | 87–96 | 5 | 20 | – | 20 | 0 | mcq 20 |
| PBM | Hari 1 Sesi 1 | 128–136 | 4 | 20 | – | 20 | 0 | mcq 20 |
| PK | Hari 1 Sesi 1 | 168–173 | 2 | 20 | 20 | – | 3 | fill_in 3, mcq 9, multi_statement 3, quantity_comparison 3, data_sufficiency 2 |
| LBI | Hari 1 Sesi 1 | 224–237 | 7 | 29 | – | 29 | 1 | mcq 29 |
| LBE | Hari 1 Sesi 1 | 306–314 | 5 | 20 | – | 20 | 0 | mcq 20 |
| PM | Hari 1 Sesi 1 | 351–356 | 5 | 20 | 20 | – | 2 | mcq 18, table_yes_no 2 |

PU = Penalaran Umum, PPU = Pengetahuan dan Pemahaman Umum, PBM = Pemahaman
Bacaan dan Menulis, PK = Pengetahuan Kuantitatif, LBI = Literasi Bahasa
Indonesia, LBE = Literasi Bahasa Inggris, PM = Penalaran Matematika.

## Asal jawaban

Setiap soal yang punya jawaban mencantumkan asalnya (`answer_source`):

- `module` — kunci modul sendiri (PU) atau pembahasan bertahap (PK, PM). Bukan
  kunci resmi; lihat caveat di atas.
- `claude-opus-5` — untuk empat subtes yang tidak punya kunci di modul (PPU,
  PBM, LBI, LBE), 89 soal dilabeli Claude Opus 5 dari teks hasil ekstraksi pada
  18 September 2026 (`data/labels/<section>.json`, dengan rationale satu baris
  dan `confidence` high / medium / low per soal). Ini bacaan satu model, bukan
  kebenaran dasar; soal berkeyakinan rendah memang ambigu pada teks yang
  terpulihkan. Jumlahnya: high 52, medium 23, low 14.
  Sebagai pemeriksaan, dua instansi Claude Opus 5 lain melabeli 89 soal yang
  sama secara buta, terpisah satu sama lain dan dari label pertama (masing-masing
  hanya melihat soal, bacaan, dan opsi). Ketiganya sepakat pada 87/89. Dua
  ketidaksepakatan yang tersisa (`LBE-d1s1-q05`, `LBE-d1s1-q09`) ditandai low
  dan menyebutkan alternatifnya; `LBI-d1s1-q28` diubah mengikuti kedua penilai
  buta. Tiap berkas label mencatat dua jawaban buta itu sebagai `blind_check`
  dan `blind_check2`, sehingga kesepakatan per soal bisa diaudit. Kesepakatan
  itu sendiri pemeriksaan yang lemah — ketiga penilai model yang sama, jadi
  kesalahannya berkorelasi.
  Audit kedua, yang berorientasi bias, mengukur label terhadap 62 soal lima opsi
  yang kuncinya dari modul sebagai kelompok kontrol: distribusi hurufnya
  konsisten dengan kebetulan (chi-square 1,77, df 4), tetapi label memilih opsi
  terpanjang 28% (kontrol 21%) dan opsi yang paling menggemakan diksi bacaan 31%
  (kontrol 21%). Enam soal yang terkena kedua bias diturunkan ulang dengan
  tangan; satu (`LBI-d1s1-q08`) tidak bertahan utuh dan kini berkeyakinan rendah
  dengan alternatifnya dicatat. Perlakukan label selebihnya sebagai bacaan satu
  model dengan bias pencocokan leksikal yang diketahui dan terukur, bukan
  sebagai kunci.
  Terakhir, seluruh 89 soal dibaca dan dijawab ulang dari nol. Pass itu mengubah
  `PBM-d1s1-q15` (E ke D: "informasi utama" tetap membawa atribut "baru" pada
  objeknya — tiga suara sebelumnya sama-sama memakai heuristik terpendek-adalah-inti)
  dan mengonfirmasi 88 lainnya. Tiap label membawa jawaban itu sebagai `reread`.
  Pass keempat mengulangi latihan yang sama per subtes — jawab buta dulu, lalu
  bandingkan dan argumenkan ulang tiap perbedaan (`review3` pada tiap label).
  Cocok pada 84/89 dan, setelah diargumenkan ulang, mendukung jawaban tersimpan
  pada 4 dari 5 perbedaan, termasuk penurunan ulang perubahan `PBM-d1s1-q15`
  secara mandiri. Satu keberatannya yang bertahan (`LBE-d1s1-q05`, C bukan A)
  bersandar pada cara distraktor tampak dibangun, bukan pada teksnya, dan tidak
  diambil; kedua bacaan tercatat pada soal itu.

### Audit atas kunci modul sendiri

70 soal berkunci modul juga dikerjakan ulang dari nol tanpa melihat kuncinya,
dengan setiap hitungan diperiksa memakai Python; hasilnya lalu dibandingkan
dengan modul (`data/audit/module_key_audit.json`). PK (20/20) dan PM (20/20)
cocok persis. PU cocok pada 24 dari 30. Keenam perbedaannya diargumenkan ulang:

- `PU-d1-q05` — modul A, audit E. Teks hanya menyatakan angka malaria "tidak
  menurun", tidak pernah menyatakan naik, jadi opsi (a) menambahkan klaim yang
  tidak ada di teks, sementara (e) adalah rantai sebab yang dinyatakan terang-
  terangan. Kemungkinan besar kunci keliru.
- `PU-d1-q24` — modul E, audit A. Soalnya meminta pernyataan yang menggambarkan
  *neraca keuangan* 2024, sedangkan (e) adalah prediksi perilaku pedagang.
  Diagramnya tidak punya titik 2024, jadi jawabannya harus tahan ekstrapolasi:
  (a) "mengalami kerugian" hanya menuntut arah tren (H < M pada 2021, 2022, dan
  2023) dan tetap berlaku meski pembacaan skala pindaian meleset sedikit,
  sementara (b) "besarnya kerugian sama dengan tahun sebelumnya" menegaskan
  besaran yang sama untuk tahun tanpa titik data. Kunci tampak keliru; (a)
  pengganti terbaik, (b) runner-up.
- `PU-d1-q11` — modul E, audit D. Betul-betul ambigu: (d) asumsi penghubung, (e)
  bukti pendukung. Kunci bertahan.
- `PU-d1-q10`, `PU-d1-q15`, `PU-d1-q20` — modul yang benar dan jawaban audit
  ditarik; alasannya tercatat di berkas audit.

Ronde kedua yang buta memberikan 70 soal yang sama kepada tiga instansi Claude
Opus 5 terpisah, satu per subtes. Masing-masing hanya menerima salinan soal
tanpa jawaban (di luar repo, dengan gambar disalin di sebelahnya), tanpa
petunjuk apa pun tentang kunci modul maupun temuan di atas, dan dilarang membuka
direktori proyek. PK dan PM kembali 20/20 identik dengan modul. PU kembali
23/30, berbeda pada enam soal yang sama ditambah satu yang baru:

- `PU-d1-q05` — pemecah buta juga menjawab E, secara mandiri. Ini kini kandidat
  terkuat untuk kekeliruan kunci yang sesungguhnya.
- `PU-d1-q24` — pemecah buta juga menolak E, menjawab A ("mengalami kerugian").
  Dua pemecah independen menolak kuncinya; setelah diargumenkan ulang, A
  pengganti yang lebih baik, karena B mematok besaran kerugian pada tahun yang
  tidak digambar di diagram.
- `PU-d1-q18` — baru: pemecah buta menjawab E dan menunjukkan bahwa kuncinya (B)
  secara formal adalah penyangkalan anteseden, karena "jika persatuan memudar,
  konflik meningkat" tidak memberi "jika tradisi dilestarikan, konflik dicegah".
  Dicatat sebagai diperdebatkan; kuncinya tetap bertahan mengingat batang soal
  memakai frasa yang lebih lunak, "PALING MUNGKIN BENAR".
- `PU-d1-q10`, `PU-d1-q11`, `PU-d1-q15`, `PU-d1-q20` — pemecah buta mendarat di
  jawaban audit pass pertama, semuanya berkeyakinan medium dan semuanya
  ditandainya sendiri sebagai ambigu. Kunci modul tetap bacaan yang lebih baik
  pada keempatnya; perlu dicatat ketiga pemecah adalah model yang sama, jadi
  kesepakatan mereka bukan bukti independen.

Ronde itu juga menandai masalah mutu soal yang tidak mengubah jawaban apa pun:
sistem persamaan tak bersolusi tunggal dan salah tulis variabel di
`PK-d1s1-q17`, dua pernyataan tautologis di `PK-d1s1-q19`, dan diagram yang
tidak konsisten secara internal di teks 4 PM (pasokan 69 kuintal berhadapan
dengan 70 kuintal terjual, sehingga stok kumulatif hari Minggu menjadi negatif).

Kunci di `with_key/` dibiarkan persis seperti di modul; auditnya dicatat di
sebelahnya, tidak digabungkan. Untuk penilaian,
`data/audit/disputed_items.json` memuat daftar yang dibutuhkan runner:
`PU-d1-q05` dan `PU-d1-q24` sebagai kandidat pengecualian — keduanya ditolak
dua pemecah independen tanpa ada yang membela kuncinya, sehingga model yang
menjawabnya dengan benar justru akan dihitung salah — ditambah tujuh soal lain
yang ditandai ambigu atau cacat desain tetapi kuncinya dipertahankan. Akurasi
PU sebaiknya dilaporkan dua kali, dengan dan tanpa kedua soal itu.

Keduanya tidak pernah dicampur: `with_key/` hanya memuat jawaban modul,
`claude_labeled/` hanya jawaban Claude, dan `without_key/` adalah 89 soal yang
sama dengan `answer: null` bagi siapa pun yang ingin melabelinya sendiri.

## Tata letak berkas

```
data/questions/with_key/<section>.json        soal yang dijawab modul (PU, PK, PM)
data/questions/claude_labeled/<section>.json  soal tanpa kunci beserta label Claude (PPU, PBM, LBI, LBE)
data/questions/without_key/<section>.json     soal yang sama, answer null
data/labels/<section>.json      label Claude: answer, confidence, rationale per soal
data/overrides/<section>.json   koreksi tangan yang ditimpakan ke hasil ekstraksi otomatis
data/audit/module_key_audit.json  pengerjaan ulang mandiri atas 70 soal berkunci modul
data/audit/blind_<section>.json   jawaban mentah ronde pengerjaan ulang yang buta
data/audit/disputed_items.json    soal yang dikecualikan / ditandai saat penilaian
data/figures/<id>.png           crop tiap gambar/tabel/diagram pada soal yang diekstraksi
data/raw/                       dump pdftotext (tidak di-commit)
data/pages/                     render halaman untuk pemeriksaan (tidak di-commit)
scripts/extract.py              PDF -> JSON (pdftohtml XML, mempertahankan tebal/miring sebagai markdown)
scripts/crop.py                 memotong gambar dari render halaman ke data/figures/
scripts/build_requests.py       soal -> payload request System One (JSONL)
scripts/run_bench.py            mengirim payload, mencatat jawaban/usage/latensi
scripts/score.py                menilai satu run terhadap acuannya
data/requests/<split>.jsonl     payload yang dikirim runner, satu per soal (67 soal berkunci)
data/results/<split>.jsonl      keluaran run mentah (gitignored)
```

`extract.py` bersifat deterministik: `PDF mentah -> parse otomatis -> kunci
jawaban -> overrides -> label`. Menjalankannya ulang menghasilkan
`data/questions/` yang persis sama.

## Menanyakan soal sebagai pertanyaan System One

`scripts/build_requests.py` mengubah dataset menjadi payload persis yang
dikirim runner ke `POST https://api.typesafe.ai/v1/systemone`, sehingga request
di balik sebuah skor tetap bisa diperiksa. Tiga jenis soal butuh tiga bentuk:

- **mcq (154 soal)** — satu Choice, kriterianya opsi soal itu sendiri, `a`–`e`
  (`a`–`d` untuk empat soal perbandingan kuantitas di PK). Tidak ada yang
  disintesis.
- **table_yes_no (PM q06, q14)** — satu request berisi tiga Noul atas state yang
  sama, satu per pernyataan; inilah yang disarankan dokumentasi untuk beberapa
  label ya/tidak independen atas satu masukan.
- **fill_in (PK q01, q02, q18)** — sumbernya tidak memberi opsi, jadi soal ini
  tidak bisa menjadi Choice apa adanya. **Dikeluarkan dari benchmark**: set
  utama adalah 67 soal berkunci sisanya, dan builder melewatinya kecuali diberi
  `--fill-in`. Flag itu ada semata agar keputusannya bisa ditinjau ulang; ia
  menulis berkas terpisah yang tidak pernah digabung ke set utama, memakai
  himpunan kandidat di `data/audit/fill_in_candidates.json` (tiap distraktor
  adalah hasil satu jalur kesalahan yang bisa dituliskan, ditambah opsi
  tidak-ada-yang-cocok). Secara default tidak ada satu pun di `data/requests/`.

Jadi set yang dinilai adalah **67 soal**: PU 30, PK 17, PM 20. Buang dua soal PU
yang kuncinya disengketakan, menjadi 65; laporkan keduanya.

Penilaian:

| soal | dihitung benar bila |
| --- | --- |
| mcq | `answers.jawaban.choice` sama dengan kunci |
| table_yes_no | setiap pernyataan memenuhi `(noul >= 0.5) == (kunci == "Ya")` |

Tabel tiga pernyataan yang dinilai utuh memberi baseline tebakan 12,5%, cukup
dekat dengan 20% milik mcq lima opsi untuk duduk dalam satu angka akurasi;
angka per pernyataan (baseline 50%) dilaporkan terpisah dan tidak pernah
dicampur. Soal empat opsi di PK punya baseline 25%, yang penting bila skor
bergaya hensachi dilaporkan.

## Menjalankan benchmark

```bash
python3 scripts/build_requests.py                      # 67 payload, satu per soal
python3 scripts/build_requests.py --group-by-passage   # + arm batch berisi 48 request
python3 scripts/run_bench.py --dry-run                 # validasi payload, tanpa mengirim apa pun

export TYPESAFE_API_KEY=...
python3 scripts/run_bench.py --limit 5                 # uji cepat ke API sungguhan
python3 scripts/run_bench.py                           # run set utama
python3 scripts/score.py                               # skor set utama
python3 scripts/score.py --agreement \
    --results data/results/claude_labeled.jsonl        # skor terhadap label Claude
python3 scripts/score.py --combined                    # gabungan 156 soal
```

`run_bench.py` menulis satu baris hasil per request — jawaban, pemakaian token,
latensi, dan jumlah percobaan — serta melewati id yang sudah ada di berkas
keluaran, sehingga run yang terpotong rate limit cukup dilanjutkan dengan
mengulang perintahnya. Retry mengikuti kebijakan yang didokumentasikan SDK:
408, 429, dan 5xx mundur eksponensial dengan jitter serta menghormati
`Retry-After` / `retry-after-ms`; 400, 401, 403, 404, dan 422 menghentikan soal
itu alih-alih digedor. Kegagalan dicatat sebagai baris hasil ber-`error`, bukan
membatalkan run. Hasil masuk gitignore: itu artefak run, bukan data.

`score.py` melaporkan akurasi keseluruhan dan per subtes, angka yang sama tanpa
dua kunci PU yang disengketakan, soal Ya/Tidak secara utuh maupun per
pernyataan, akurasi per pita keyakinan beserta skor Brier atas peluang yang
diberikan pada opsi benar, berapa akurasinya bila jawaban paling ragu
dikosongkan, serta biaya token dan latensi. Tarif biayanya berupa flag
(`--rate-per-mtok`, default 0,042) karena dokumentasinya tidak memuat halaman
harga — periksa terhadap harga terkini sebelum mengutip angka.

Kedua skrip diuji ujung ke ujung memakai berkas hasil sintetis sebelum ada run
sungguhan, termasuk jalur pemecahan jawaban pada arm batch.

## Skema soal

```jsonc
{
  "id": "PK-d1s1-q04",          // <subtes>-d<hari>[s<sesi>]-q<nn>
  "subtest": "PK", "day": 1, "session": 1, "number": 4,
  "type": "mcq",                // mcq | fill_in | table_yes_no
  "subtype": null,              // multi_statement | quantity_comparison | data_sufficiency
  "passage_ids": ["PK-d1s1-teks2"],   // bacaan yang dirujuk soal (bisa lebih dari satu, mis. LBE Teks 1 + Teks 2)
  "passages": [{"id": "PK-d1s1-teks2", "text": "...", "figure_path": "...", "figure_note": "...",
                "_source_note": null, "source_page": 169}],
                                // bacaan yang sama disematkan utuh: tiap soal berdiri sendiri
  "has_answer": true,
  "question": "...",            // markdown: **tebal**, _miring_, \n untuk ganti baris/paragraf
  "options": {"a": "...", "e": "..."},
  "statements": [],             // khusus table_yes_no
  "answer": "C",                // huruf | nilai isian ("64") | ["Ya","Tidak","Tidak"] | null
  "answer_source": "module",    // "module" | "claude-opus-5" | null
  "label_confidence": null,     // high | medium | low, hanya bila answer_source "claude-opus-5"
  "has_figure": true,
  "figure_path": "data/figures/PK-d1s1-q04.png",   // crop dari aslinya
  "figure_note": "...",         // transkrip teks gambar, ditulis tangan
  "source_page": 168,
  "_source_note": null,         // keanehan warisan sumber (bacaan juga membawa field ini)
  "needs_review": false, "review_reasons": []
}
```

Bacaan bersama ("Teks 1", utas forum, sebuah diagram) dicetak sekali saja di
modul, tetapi disematkan utuh ke setiap soal yang merujuknya, berikut transkrip
gambarnya, sehingga sebuah soal tidak pernah perlu pencarian di luar dirinya.
Hal yang sama berlaku untuk gambar yang melayani beberapa soal: transkrip
diagram `PM-d1s1-teks4`, misalnya, dibawa oleh masing-masing q13–q16.

Bila modul menyebutkan rentangnya ("Bacalah ... untuk nomor 17 sampai 19"),
rentang itu dipakai langsung; bila modul sekadar berhenti memakai sebuah bacaan
tanpa mencetak judul "Teks" yang baru, rentangnya dituliskan di
`data/overrides/` sebagai `covers`, karena kalau tidak, bacaan itu akan terus
menempel pada soal-soal mandiri yang menyusul. `extract.py` mencetak cakupan
hasilnya per bagian pada tiap run:

```
PK_d1s1    2 passages, 20 questions, 20 keyed,  0 labeled,  0 flagged
           teks1:q6-q8, teks2:q9-q11
```

Matematika ditulis sebagai teks biasa: `x²`, `√29`, `2^(n–1)`, `a/b`, `6 5/7`
(pecahan campuran). Setiap soal PK dan PM, serta setiap soal yang ditandai
extractor (pecahan bertingkat, gambar, jumlah opsi yang ganjil), ditulis ulang
dengan tangan dari render halaman; lihat `data/overrides/`.

## Catatan ekstraksi

- Gambar dipotong dari render 200 dpi dan ditranskripsikan ke `figure_note`,
  sehingga tiap model menerima masukan berupa teks saja. Crop aslinya disimpan
  agar transkripnya bisa diaudit.
- Pergantian paragraf pada bacaan dipulihkan dari indentasi baris pertama, dan
  pada bacaan rata kanan-kiri (yang tidak diberi indentasi oleh modul) dari
  baris yang berhenti sebelum margin kanan, sehingga soal yang menyebut "Teks 2
  Paragraf 3" bisa ditelusuri pada `passages[].text` (paragraf dipisahkan `\n`).
- Tebal/miring penting bagi sebagian soal ("kata **bercetak tebal**", "the word
  _may_"), jadi ekstraksi memakai `pdftohtml -xml`, bukan `pdftotext`.
- Pemenggalan kata di ujung baris disambung kembali (`me-` + `nang` → `menang`,
  `SA-` + `LAH` → `SALAH`, `Timor-` + `Timur` → `Timor-Timur`).
- Kesetiaan teks diperiksa ulang oleh dua pass otomatis atas seluruh 959 field
  soal, opsi, pernyataan, dan bacaan: tiap field harus muncul apa adanya pada
  dump `pdftotext` yang independen, dan tiap kata serta tiap angka harus ada di
  sumbernya. 38 field yang tidak bisa dicocokkan dengan cara itu adalah
  matematika pecahan bertingkat yang ditulis ulang dengan tangan; masing-masing
  diverifikasi ulang terhadap render halaman, dan empat pengecualian tingkat
  kata yang tersisa terdaftar di skrip audit serta membawa `_source_note`.
- Transkrip gambar diaudit terhadap crop-nya sendiri, termasuk mengukur
  kemiringan garis yang digambar pada `LBI-d1s1-teks2`.

## Atribusi

Soal: Modul MMA SNBT 2025, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>), CC BY-NC 4.0 untuk penataannya.
