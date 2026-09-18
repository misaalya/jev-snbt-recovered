# jev-snbt-recovered

[English](README.md) · **Bahasa Indonesia**

Benchmark **TypeSafe Jev** pada **SNBT 2025**, memakai naskah hasil
rekonstruksi komunitas.

159 soal dari ketujuh subtes, masing-masing berdiri sendiri: bacaan dan
transkrip gambarnya ikut menempel di soal itu. Skor run pertama ada di
**[RESULTS.id.md](RESULTS.id.md)** — ringkasnya: 60% di penalaran umum, 90% di
literasi bahasa Indonesia, 29% di pengetahuan kuantitatif.

## Dari mana soalnya

*Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam — rekonstruksi komunitas atas
naskah SNBT 2025 dari apa yang diingat peserta setelah ujian
(`dataset/MMASNBT2025.pdf`, 764 halaman, tidak ikut di-commit di sini).

Dua hal mengikuti dari situ, dan keduanya membentuk seluruh isi repo ini:

- **Kunci jawabannya bukan kunci resmi.** Itu karya penyusun modul sendiri, dan
  hanya untuk tiga subtes: PU, PK, dan PM. Kunci PU bahkan memuat
  disclaimer-nya sendiri, *"bukan jawaban yang pasti"*. PPU, PBM, LBI, dan LBE
  sama sekali tidak punya kunci.
- **Sebagian soal sampai dalam keadaan rusak.** `LBI-d1s1-q21` kehilangan satu
  opsi, dan `PPU-d1s1-teks4` tertulis "kristal udara" padahal jelas maksudnya
  "kristal es". Tidak ada yang diperbaiki diam-diam. Setiap soal seperti itu
  dipertahankan persis seperti tercetak dan membawa `_source_note` yang
  menyebutkan apa yang janggal.

## Apa yang kami ambil, dan apa yang kami lakukan

Kami mengambil **Hari 1, Sesi 1 tiap subtes**. PU tidak terbagi sesi, jadi
untuk PU yang diambil Hari 1.

| Subtes | | Soal | Jawaban dari |
|---|---|---|---|
| PU | Penalaran Umum | 30 | kunci modul |
| PK | Pengetahuan Kuantitatif | 20 | kunci modul |
| PM | Penalaran Matematika | 20 | kunci modul |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | label Claude |
| PBM | Pemahaman Bacaan dan Menulis | 20 | label Claude |
| LBI | Literasi Bahasa Indonesia | 29 | label Claude |
| LBE | Literasi Bahasa Inggris | 20 | label Claude |

`scripts/extract.py` menarik semuanya dari PDF dan menulis JSON. Yang
dikerjakannya di luar sekadar mengambil teks:

- **Tiap soal membawa bacaannya sendiri.** Satu bacaan dicetak sekali di modul
  dan dipakai empat sampai lima soal; di sini bacaan itu disematkan utuh ke
  masing-masing soal. Tidak ada soal yang perlu menengok ke tempat lain.
- **Tebal dan miring tidak hilang.** Ada soal yang menanyakan "kata **bercetak
  tebal**", jadi ekstraksinya membaca XML dari PDF, bukan teks polos.
- **Pergantian paragraf dibangun ulang**, karena ada soal yang merujuk
  "paragraf ketiga". Pemenggalan kata di ujung baris disambung kembali
  (`me-` + `nang` → `menang`).
- **Matematika ditulis ulang sebagai teks biasa**: `x²`, `√29`, `2^(n–1)`,
  `6 5/7`. Seluruh soal PK dan PM diketik ulang dengan tangan dari gambar
  halaman, karena pecahan bertingkat tidak selamat lewat ekstraksi teks.
- **Tidak ada koreksi senyap.** Semua koreksi tinggal di `data/overrides/`, dan
  apa pun yang janggal di sumbernya tetap membawa `_source_note`.

Menjalankan ulang `extract.py` menghasilkan `data/questions/` yang persis sama.

## Bagaimana gambar ditangani

Jev menerima teks, bukan gambar. Jadi seluruh gambar — ada 10: diagram garis,
diagram lingkaran, gambar geometri, definisi operator dalam kurung besar —
**dipotong dari halaman lalu ditranskripsikan menjadi kata-kata oleh Claude**,
kemudian dicocokkan kembali dengan potongannya secara manual. Untuk
`LBI-d1s1-teks2`, itu berarti mengukur kemiringan garis yang digambar, karena
transkrip pertamanya mengklaim dua garis sejajar padahal tidak.

Transkripnya tinggal di `figure_note` dan disematkan ke setiap soal yang
memakai gambar itu. Potongan aslinya tetap disimpan di `data/figures/` supaya
siapa pun bisa memeriksa transkripnya.

Tiap model melihat masukan teks yang sama, dan transkripnya bisa diaudit
alih-alih tersembunyi di dalam model visual.

## Bagaimana jawabannya dibuat

**PU, PK, PM — memakai kunci modul**, persis seperti tercetak.

Kuncinya tetap kami periksa. Seluruh 70 soal dikerjakan ulang dari nol secara
mandiri, lalu tiga instansi Claude yang baru mengerjakannya lagi secara buta —
masing-masing hanya melihat soal tanpa jawaban dan dilarang membuka repo ini.
PK dan PM cocok 20/20 pada kedua ronde. PU cocok 24/30 dan 23/30. Kuncinya
**tidak** diubah; ketidaksepakatannya dicatat di
`data/audit/module_key_audit.json`, dan `PU-d1-q05` serta `PU-d1-q24` ditandai
di `data/audit/disputed_items.json` sebagai kemungkinan kunci keliru, supaya
penilai bisa melaporkan akurasi dengan dan tanpa keduanya.

**PPU, PBM, LBI, LBE — dilabeli Claude Opus 5**, karena modulnya tidak punya
kunci untuk keempatnya. Ini bacaan satu model, bukan kebenaran dasar, dan
disimpan di folder terpisah dari jawaban modul supaya keduanya tidak pernah
tertukar. Tiap label membawa alasan dan tingkat keyakinan high / medium / low
(52 / 23 / 14).

Cara labelnya dibuat:

1. Jawab seluruh 89 soal dari teks hasil ekstraksi, satu per satu, dengan
   alasan tertulis.
2. Dua instansi Claude lain menjawab 89 soal yang sama secara **buta**, hanya
   melihat soal, bacaan, dan opsi. Ketiganya sepakat pada 87/89.
3. Audit bias memakai 62 soal lima opsi berkunci modul sebagai kelompok
   kontrol. Distribusi hurufnya wajar, tetapi label memilih opsi terpanjang 28%
   berbanding 21% pada kontrol. Soal yang terkena bias itu diturunkan ulang
   dengan tangan.
4. Dua pass lagi menjawab ulang semuanya dari nol dan mengargumenkan ulang tiap
   perbedaan.

Semua pass tercatat per soal di `data/labels/`, jadi kamu bisa melihat jawaban
tiap ronde alih-alih memercayai huruf akhirnya begitu saja. Ringkasan jujurnya
tetap: **semua penilainya model yang sama, jadi kesepakatan mereka bukti yang
lemah.** `data/questions/without_key/` memuat 89 soal yang sama dengan
`answer: null` kalau kamu lebih suka melabelinya sendiri.

## Bagaimana Jev ditanya

Satu request per soal, dikirim ke `POST https://api.typesafe.ai/v1/systemone`.
`scripts/build_requests.py` menulis payload-nya ke disk sebelum ada yang
dikirim, sehingga request persis di balik sebuah skor bisa diperiksa.

Soal pilihan ganda biasa menjadi satu **Choice**, dengan opsi a–e milik soal
itu sendiri. Tidak ada yang dikarang. Dua kasus butuh penanganan berbeda:

- **Dua soal tabel Ya/Tidak** (PM q06, q14) bukan satu keputusan — masing-masing
  punya tiga pernyataan untuk dicontreng. Tiap tabel menjadi satu request
  berisi tiga penilaian **Noul** (benar/salah) atas bacaan yang sama.
  Penilaiannya utuh: ketiga baris harus benar, kalau tidak soalnya dihitung
  salah. Angka per pernyataan dilaporkan terpisah dan tidak pernah dicampur,
  karena baseline tebakannya 50% berbanding 20% milik soal lima opsi.
- **Tiga soal isian** (PK q01, q02, q18) sama sekali tidak punya opsi, jadi
  tidak bisa menjadi Choice tanpa kami mengarang distraktornya — yang berarti
  mengukur karangan kami sendiri. **Ketiganya dikeluarkan.** Set yang dinilai
  berisi 67 soal, bukan 70.

## Cara menjalankan

```bash
python3 scripts/build_requests.py     # tulis payload request-nya
python3 scripts/run_bench.py --dry-run   # validasi, tanpa mengirim apa pun

cp .env.example .env                  # lalu isi kuncimu di situ
python3 scripts/run_bench.py --limit 5   # uji cepat
python3 scripts/run_bench.py             # 67 soal berkunci
python3 scripts/score.py

# 89 soal sisanya, dinilai terhadap label Claude
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined   # seluruh 156 sekaligus
```

Runner-nya bisa dilanjutkan: id yang sudah ada di berkas keluaran dilewati,
jadi run yang terpotong rate limit tinggal diulang perintahnya. Ia mengulang
408, 429, dan 5xx dengan backoff, dan mencatat kegagalan sebagai baris hasil
alih-alih membatalkan run.

`scripts/score.py` melaporkan akurasi per subtes, akurasi per pita keyakinan,
skor Brier, berapa akurasinya bila jawaban paling ragu dikosongkan, serta biaya
token dan latensi.

## Hasil

| Set | Skor |
|---|---|
| 67 soal, kunci modul | **47,8%** |
| 89 soal, label Claude | **85,4%** |
| Seluruh 156, acuan campuran | **69,2%** |

Bagian menariknya bukan angka totalnya: Jev mendapat 75% di separuh verbal PU
dan 30% di separuh hitungannya, dan keyakinannya mengikuti akurasinya cukup
rapat untuk dipakai sebagai penyaring. Uraian lengkap per subtes, beserta
kalibrasi dan biaya: **[RESULTS.id.md](RESULTS.id.md)**.

## Berkas

```
data/questions/with_key/        PU, PK, PM — jawaban modul
data/questions/claude_labeled/  PPU, PBM, LBI, LBE — label Claude
data/questions/without_key/     89 soal yang sama, answer: null
data/labels/                    tiap pass pelabelan, per soal, dengan alasannya
data/audit/                     audit kunci modul dan daftar soal yang disengketakan
data/overrides/                 koreksi tangan atas hasil ekstraksi otomatis
data/figures/                   potongan gambar aslinya
data/requests/                  payload yang dikirim ke Jev
scripts/                        ekstraksi, crop, bangun request, jalankan, nilai
```

## Atribusi

Soal: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Penataannya CC BY-NC 4.0; isi soalnya
milik penyelenggara ujian dan direproduksi di sini semata untuk riset
non-komersial.
