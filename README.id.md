# jev-snbt-recovered

[English](README.md) · **Bahasa Indonesia**

Benchmark **TypeSafe Jev** pada **SNBT 2025**, dengan memakai naskah hasil
rekonstruksi komunitas.

Dataset ini memuat 159 soal yang mencakup ketujuh subtes. Setiap soal berdiri
sendiri: bacaan dan transkrip gambar yang dirujuknya disematkan di dalam soal
itu sendiri. Hasil run pertama tercatat di **[RESULTS.id.md](RESULTS.id.md)**.

## Sumber soal

Soal diambil dari *Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam. Modul
tersebut merupakan rekonstruksi komunitas atas naskah SNBT 2025, disusun dari
apa yang diingat peserta setelah ujian (`dataset/MMASNBT2025.pdf`, 764 halaman,
tidak disertakan dalam repositori ini).

Dua sifat sumber tersebut menentukan bagaimana keseluruhan proyek ini disusun.

**Kunci jawabannya bukan kunci resmi.** Kunci itu karya penyusun modul, dan
hanya tersedia untuk tiga subtes: PU, PK, dan PM. Kunci PU bahkan memuat
disclaimer dari penyusunnya sendiri, *"bukan jawaban yang pasti"*. PPU, PBM,
LBI, dan LBE tidak memiliki kunci.

**Sebagian soal rusak dalam proses rekonstruksi.** `LBI-d1s1-q21` kehilangan
satu opsi, dan `PPU-d1s1-teks4` tertulis "kristal udara" padahal istilah yang
dimaksud adalah "kristal es". Tidak ada cacat semacam itu yang diperbaiki tanpa
catatan: soalnya direproduksi sebagaimana tercetak dan membawa `_source_note`
yang menguraikan masalahnya.

## Cakupan dan penyiapan

Dataset ini mencakup **Hari 1, Sesi 1 tiap subtes**. PU tidak terbagi ke dalam
sesi, sehingga Hari 1 diambil seluruhnya.

| Subtes | | Soal | Jawaban dari |
|---|---|---|---|
| PU | Penalaran Umum | 30 | kunci modul |
| PK | Pengetahuan Kuantitatif | 20 | kunci modul |
| PM | Penalaran Matematika | 20 | kunci modul |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | label Claude |
| PBM | Pemahaman Bacaan dan Menulis | 20 | label Claude |
| LBI | Literasi Bahasa Indonesia | 29 | label Claude |
| LBE | Literasi Bahasa Inggris | 20 | label Claude |

`scripts/extract.py` mengubah PDF menjadi JSON. Di luar pengambilan teks biasa,
skrip ini melakukan hal-hal berikut.

- **Setiap soal membawa bacaannya sendiri.** Satu bacaan dicetak sekali di
  modul dan dipakai bersama oleh empat sampai lima soal; di sini bacaan itu
  disematkan utuh ke setiap soal yang merujuknya, sehingga tidak ada soal yang
  memerlukan rujukan dari luar.
- **Cetak tebal dan miring dipertahankan.** Beberapa soal menanyakan "kata
  **bercetak tebal**", sehingga ekstraksi membaca representasi XML dari PDF,
  bukan teks polos.
- **Batas paragraf direkonstruksi**, karena sebagian soal merujuk paragraf
  tertentu. Pemenggalan kata di ujung baris disambung kembali (`me-` + `nang` →
  `menang`).
- **Matematika ditulis sebagai teks biasa**: `x²`, `√29`, `2^(n–1)`, `6 5/7`.
  Seluruh soal PK dan PM diketik ulang dengan tangan dari gambar halaman,
  karena pecahan bertingkat tidak bertahan melalui ekstraksi teks.
- **Tidak ada koreksi yang diterapkan secara senyap.** Koreksi manual disimpan
  di `data/overrides/`, dan setiap kejanggalan yang diwarisi dari sumbernya
  dicatat dalam `_source_note`.

Menjalankan ulang `extract.py` menghasilkan kembali `data/questions/` secara
persis.

## Penanganan gambar

Jev menerima teks, bukan gambar. Kesepuluh gambar dalam dataset ini — diagram
garis, diagram lingkaran, gambar geometri, dan definisi operator dalam kurung
besar — dipotong dari halamannya lalu **ditranskripsikan menjadi teks oleh
Claude**, kemudian diverifikasi terhadap potongannya secara manual. Verifikasi
itu mengubah satu transkrip: pada `LBI-d1s1-teks2`, kemiringan garis yang
digambar diukur, dan pengukuran itu menunjukkan bahwa klaim transkrip pertama
bahwa dua garis sejajar tidaklah benar.

Setiap transkrip disimpan dalam `figure_note` dan disematkan ke setiap soal
yang memakai gambar tersebut. Potongan aslinya tetap berada di `data/figures/`
sehingga transkripnya dapat diaudit terhadap potongan itu.

Dengan begitu model menerima masukan berupa teks yang sama untuk setiap soal,
dan transkripnya tersedia untuk diperiksa alih-alih dikerjakan di dalam model
visual.

## Penurunan jawaban

**PU, PK, dan PM memakai kunci modul**, direproduksi persis sebagaimana
tercetak.

Kunci tersebut tetap diverifikasi. Seluruh 70 soal dikerjakan secara mandiri
dari nol, setelah itu tiga instansi Claude yang terpisah mengerjakannya kembali
secara buta, masing-masing hanya menerima soal tanpa jawaban dan dilarang
membuka repositori ini. PK dan PM cocok dengan modul 20/20 pada kedua ronde; PU
cocok pada 24 dari 30 dan 23 dari 30. Kuncinya tidak diubah. Ketidaksepakatan
tercatat di `data/audit/module_key_audit.json`, dan `PU-d1-q05` serta
`PU-d1-q24` terdaftar di `data/audit/disputed_items.json` sebagai kemungkinan
kunci keliru, sehingga akurasi dapat dilaporkan dengan maupun tanpa keduanya.

**PPU, PBM, LBI, dan LBE dilabeli Claude Opus 5**, karena modulnya tidak
menyediakan kunci untuk keempatnya. Label ini adalah bacaan satu model dan
bukan kebenaran dasar. Label disimpan terpisah dari jawaban modul sehingga
keduanya tidak pernah tergabung. Setiap label mencatat alasan dan tingkat
keyakinan high, medium, atau low (berturut-turut 52, 23, dan 14 soal).

Label dibuat melalui empat tahap.

1. Seluruh 89 soal dijawab dari teks hasil ekstraksi, satu per satu, masing-
   masing disertai alasan tertulis.
2. Dua instansi Claude lain menjawab 89 soal yang sama secara buta, hanya
   melihat soal, bacaannya, dan opsinya. Ketiganya sepakat pada 87 dari 89.
3. Audit bias membandingkan label terhadap 62 soal lima opsi berkunci modul
   yang dipakai sebagai kelompok kontrol. Sebaran huruf jawabannya konsisten
   dengan kebetulan, tetapi label memilih opsi terpanjang pada 28% kasus
   berbanding 21% pada kontrol. Soal yang terdampak diturunkan ulang dengan
   tangan.
4. Dua tahap berikutnya menjawab ulang seluruh soal dari nol dan
   mengargumenkan kembali setiap perbedaan.

Setiap tahap tercatat per soal di `data/labels/`, sehingga jawaban pada tiap
ronde dapat diperiksa alih-alih diterima begitu saja. Satu keterbatasan perlu
dinyatakan terus terang: seluruh penilainya adalah model yang sama, sehingga
kesepakatan mereka merupakan bukti yang lemah.
`data/questions/without_key/` memuat 89 soal yang sama dengan `answer: null`
bagi siapa pun yang lebih memilih melabelinya secara mandiri.

## Cara Jev ditanya

Satu request dikirim per soal ke `POST https://api.typesafe.ai/v1/systemone`.
`scripts/build_requests.py` menulis payload-nya ke disk sebelum ada yang
dikirimkan, sehingga request persis di balik sebuah skor dapat diperiksa.

Soal pilihan ganda standar menjadi satu **Choice**, yang kriterianya adalah
opsi a–e milik soal itu sendiri. Tidak ada yang disintesis. Dua kategori
memerlukan penanganan berbeda.

**Dua soal tabel Ya/Tidak** (PM q06 dan q14) bukan satu keputusan tunggal:
masing-masing menyajikan tiga pernyataan yang harus ditandai satu per satu.
Setiap tabel dikirim sebagai satu request berisi tiga penilaian **Noul** atas
bacaan yang sama. Penilaian diterapkan pada soal secara utuh — ketiga
pernyataan harus benar — dan angka per pernyataan dilaporkan terpisah, karena
baseline tebakannya sebesar 50% tidak sebanding dengan 20% milik soal lima
opsi.

**Tiga soal isian** (PK q01, q02, dan q18) tidak menyediakan opsi sehingga
tidak dapat dinyatakan sebagai Choice tanpa mengarang distraktornya, dan hal
itu berarti mengukur distraktornya alih-alih modelnya. Ketiganya dikecualikan.
Set yang dinilai terdiri atas 67 soal, bukan 70.

## Menjalankan benchmark

```bash
python3 scripts/build_requests.py        # tulis payload request-nya
python3 scripts/run_bench.py --dry-run   # validasi tanpa mengirim

cp .env.example .env                     # lalu isikan kunci API
python3 scripts/run_bench.py --limit 5   # uji cepat
python3 scripts/run_bench.py             # 67 soal berkunci modul
python3 scripts/score.py

# 89 soal sisanya, dinilai terhadap label Claude
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined      # seluruh 156 soal sekaligus
```

Runner-nya dapat dilanjutkan: identifier yang sudah ada di berkas keluaran akan
dilewati, sehingga run yang terputus oleh rate limit berlanjut ketika
perintahnya diulang. Respons 408, 429, dan 5xx diulang dengan backoff
eksponensial serta menghormati `Retry-After`; kegagalan dicatat sebagai baris
hasil alih-alih membatalkan run.

`scripts/score.py` melaporkan akurasi per subtes, akurasi per pita keyakinan,
skor Brier, akurasi yang diperoleh bila jawaban paling ragu ditahan, serta
biaya token dan latensi.

## Ringkasan hasil

| Set | Skor |
|---|---|
| 67 soal, kunci modul | 47,8% |
| 89 soal, label Claude | 85,4% |
| 156 soal, acuan campuran | 69,2% |

Skor per subtes, kalibrasi, perbedaan terhadap label, dan biaya disajikan di
**[RESULTS.id.md](RESULTS.id.md)**.

## Tata letak repositori

```
data/questions/with_key/        PU, PK, PM — jawaban modul
data/questions/claude_labeled/  PPU, PBM, LBI, LBE — label Claude
data/questions/without_key/     89 soal yang sama, answer: null
data/labels/                    tiap tahap pelabelan, per soal, dengan alasannya
data/audit/                     audit kunci modul dan daftar soal yang disengketakan
data/overrides/                 koreksi manual atas hasil ekstraksi otomatis
data/figures/                   potongan gambar aslinya
data/requests/                  payload yang dikirim ke Jev
scripts/                        ekstraksi, pemotongan, penyusunan request, eksekusi, penilaian
```

## Atribusi

Soal: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Penataannya berlisensi CC BY-NC 4.0; isi
soalnya milik penyelenggara ujian dan direproduksi di sini semata untuk riset
non-komersial.
