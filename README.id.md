# snbt-jev-bench

[English](README.md) · **Bahasa Indonesia**

Benchmark **TypeSafe Jev** pada **SNBT 2025**, ujian masuk perguruan tinggi di
Indonesia.

> **Soal di sini adalah soal hasil recovery, bukan naskah resmi.** Naskah SNBT
> tidak dirilis setelah ujian. Setiap soal di repositori ini direkonstruksi
> komunitas dari ingatan peserta, sehingga redaksinya bisa berbeda dari yang
> benar-benar diujikan, sebagian soal jelas cacat, dan kunci jawabannya adalah
> kunci versi rekonstruksi, bukan kunci penyelenggara. Seluruh angka dalam
> repositori ini adalah pengukuran terhadap rekonstruksi tersebut, bukan
> terhadap ujian yang sesungguhnya.

Dataset ini memuat 159 soal yang mencakup ketujuh subtes. Setiap soal berdiri
sendiri: bacaan dan transkrip gambar yang dirujuknya disematkan di dalam soal
itu sendiri. Hasil run pertama tercatat di **[RESULTS.id.md](RESULTS.id.md)**, dengan
respons mentahnya di `data/results/`.

## Sumber soal

Soal diambil dari *Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam: 764
halaman soal hasil ingatan peserta yang ditata ulang oleh relawan
(`dataset/MMASNBT2025.pdf`, tidak disertakan dalam repositori ini).

Dua konsekuensi dari asal-usul itu menentukan bagaimana keseluruhan proyek ini
disusun.

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

Soal diekstraksi dari PDF menjadi JSON. Di luar pengambilan teks biasa, hal-hal
berikut diterapkan.

- **Setiap soal membawa bacaannya sendiri.** Satu bacaan dicetak sekali di
  modul dan dipakai bersama oleh empat sampai lima soal; di dalam dataset,
  bacaan itu disematkan utuh ke setiap soal yang merujuknya, sehingga tidak ada
  soal yang memerlukan rujukan dari luar.
- **Cetak tebal dan miring dipertahankan.** Beberapa soal menanyakan "kata
  **bercetak tebal**", sehingga ekstraksinya membaca representasi XML dari PDF,
  bukan teks polos.
- **Batas paragraf direkonstruksi**, karena sebagian soal merujuk paragraf
  tertentu. Pemenggalan kata di ujung baris disambung kembali (`me-` + `nang` →
  `menang`).
- **Matematika ditulis sebagai teks biasa**: `x²`, `√29`, `2^(n–1)`, `6 5/7`.
  Seluruh soal PK dan PM diketik ulang dengan tangan dari gambar halaman,
  karena pecahan bertingkat tidak bertahan melalui ekstraksi teks.
- **Tidak ada koreksi yang diterapkan secara senyap.** Setiap kejanggalan yang
  diwarisi dari sumbernya dicatat dalam `_source_note` pada soal atau bacaan
  yang bersangkutan.

Proses ekstraksinya sendiri tidak disertakan dalam repositori ini karena
bergantung pada PDF sumber, yang tidak dapat disebarkan ulang di sini. Yang
diterbitkan adalah hasilnya, `data/questions/`.

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
sehingga transkripnya dapat diaudit terhadap potongan itu. Dengan begitu model
menerima masukan berupa teks yang sama untuk setiap soal, dan transkripnya
tersedia untuk diperiksa alih-alih dikerjakan di dalam model visual.

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

**PPU, PBM, LBI, dan LBE memakai label yang ditulis Claude Opus 5**, karena
modulnya tidak menyediakan kunci untuk keempatnya. Label ini adalah bacaan satu
model dan bukan kebenaran dasar. Label disimpan pada direktori terpisah dari
jawaban modul sehingga keduanya tidak pernah tergabung, dan setiap soal memuat
kolom `answer_source` yang menyebut asal jawabannya.

Setiap label mencatat tingkat keyakinan high, medium, atau low (berturut-turut
52, 23, dan 14 soal) yang ditetapkan saat pelabelan dan dilaporkan di
RESULTS.id.md berdampingan dengan tingkat kesepakatan Jev terhadapnya. Yang
diterbitkan hanya label akhir; tahap-tahap penyusunannya adalah bahan kerja dan
tidak termasuk dalam repositori ini. Satu keterbatasan perlu dinyatakan terus
terang: label dan verifikasinya berasal dari keluarga model yang sama, sehingga
kesepakatan di antara keduanya merupakan bukti yang lemah.

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

`data/results/` sudah memuat run yang diterbitkan, dan runner melewati
identifier yang ditemukannya di sana, sehingga mengulang perintah di atas akan
melaporkan semua soal sebagai selesai dan menilai respons yang sudah
di-commit tanpa perlu kunci API. Untuk membuat run baru, arahkan keluarannya ke
tempat lain dengan `--out data/results/rerun.jsonl` dan berikan path yang sama
ke `scripts/score.py --results`.

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
data/audit/                     audit kunci modul dan daftar soal yang disengketakan
data/figures/                   potongan gambar aslinya
data/results/                   run yang dilaporkan di RESULTS.id.md, satu baris per soal
scripts/build_requests.py       soal -> payload request System One
scripts/run_bench.py            mengirim payload, mencatat jawaban dan pemakaian token
scripts/score.py                menilai satu run terhadap kunci modul atau label
```

`scripts/build_requests.py` menulis ke `data/requests/` yang dihasilkan secara
lokal dan tidak dilacak. `data/results/` memuat run yang diterbitkan persis
seperti dicatat runner, sehingga angka di RESULTS.id.md dapat dihitung ulang dan
run baru dapat dibandingkan baris per baris terhadapnya.

## Atribusi

Soal: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Penataannya berlisensi CC BY-NC 4.0; isi
soalnya milik penyelenggara ujian dan direproduksi di sini semata untuk riset
non-komersial.
