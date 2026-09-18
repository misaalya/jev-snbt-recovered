# Hasil Jev di SNBT 2025

[English](RESULTS.md) · **Bahasa Indonesia**

`jev-1.13.0`, 18 September 2026. 156 soal, satu request per soal, tanpa retry,
$0,0045 untuk seluruh run.

## Ringkasnya

| Subtes | Skor | Acuan jawaban |
|---|---|---|
| **LBE** Literasi Bahasa Inggris | 100,0% (20/20) | label Claude |
| **LBI** Literasi Bahasa Indonesia | 89,7% (26/29) | label Claude |
| **PBM** Pemahaman Bacaan dan Menulis | 75,0% (15/20) | label Claude |
| **PPU** Pengetahuan dan Pemahaman Umum | 75,0% (15/20) | label Claude |
| **PU** Penalaran Umum | 60,0% (18/30) | kunci modul |
| **PM** Penalaran Matematika | 45,0% (9/20) | kunci modul |
| **PK** Pengetahuan Kuantitatif | 29,4% (5/17) | kunci modul |

Bacalah kedua paruhnya terpisah. Empat subtes bahasa dinilai terhadap label
Claude, yang merupakan bacaan satu model dan bukan kunci resmi, jadi baris-baris
itu pengukuran yang lebih lemah daripada tiga baris di bawahnya. Terhadap kunci
modul sendiri Jev memperoleh **47,8%** (32/67); terhadap label Claude,
**85,4%** (76/89); untuk keseluruhan, 69,2% (108/156).

## Jev membaca bahasa Indonesia dengan baik dan tidak bisa berhitung

Hasil paling terang di run ini ada di dalam PU, karena satu subtes itu memuat
kedua jenis soal sekaligus:

| | Skor |
|---|---|
| PU q1–q20, penalaran verbal | **75%** (15/20) |
| PU q21–q30, hitungan dan diagram | **30%** (3/10) |

Angka 30% itu sejajar dengan PK (29,4%) dan PM (45,0%), dua subtes
komputasional, dan 75% sejajar dengan subtes bahasa di atasnya. Garis
pemisahnya di benchmark ini bukan bahasa Indonesia lawan Inggris, bukan pula
mudah lawan sulit — melainkan **membaca lawan menghitung**.

Masuk akal. Jev mengembalikan penilaian bertipe secara langsung; ia tidak
mengerjakan langkah demi langkah. "Peluang terpilihnya sekretaris perempuan
dengan ketua dan bendahara berjenis kelamin berbeda" butuh empat sampai lima
langkah sebelum jawabannya ada, dan sebanyak apa pun soal itu dibaca, angkanya
tidak muncul. Sebaliknya "manakah simpulan yang PALING TEPAT" adalah penilaian
atas teks, dan untuk itulah kelas model ini dibuat.

Jadi khusus untuk bahasa Indonesia: di LBI, Jev cocok dengan label pada 26 dari
29 soal, dan pada soal verbal PU ia benar 15 dari 20 terhadap kunci modul
sendiri. Pemahaman bacaan bahasa Indonesianya sudah di tingkat yang berguna.
Jangan dudukkan dia di depan soal matematika.

## Dia tahu kapan dia tidak tahu

Bagian ini lebih penting daripada angka utamanya kalau kamu hendak membangun di
atasnya. Dari seluruh 154 jawaban Choice:

| Keyakinan Jev | Seberapa sering benar |
|---|---|
| 0,0–0,5 | 34,0% (16/47) |
| 0,5–0,7 | 68,4% (13/19) |
| 0,7–0,9 | 75,0% (21/28) |
| 0,9–1,0 | **96,7%** (58/60) |

Kenaikannya monoton, dan bertahan di kedua paruh benchmark secara terpisah.
Praktisnya, keyakinan itu bisa dipakai sebagai penyaring: membuang sepertiga
jawaban paling ragu menaikkan skor gabungan dari 69,2% ke 85,2%. Di paruh
berkunci modul saja, 49,2% → 63,0%.

Skor Brier 0,253 secara keseluruhan — 0,402 di paruh berkunci, 0,143 di paruh
berlabel.

## Di mana Jev berbeda dengan label kami

Pada 89 soal tanpa kunci resmi, Jev dan label Claude berbeda di 13 soal. Tidak
ada pihak yang berwenang di sini, jadi ini soal terbuka, bukan kesalahan Jev —
dan perbedaannya duduk persis di tempat label sudah mengaku ragu: kesepakatan
90,4% pada label berkeyakinan tinggi, 87,0% pada sedang, 64,3% pada rendah.

Empat layak dilihat manusia, karena kedua sisi yakin dan arahnya berlawanan:

| Soal | Label kami | Jev |
|---|---|---|
| PPU-d1s1-q11 | E (keyakinan rendah) | **A (0,98)** |
| PBM-d1s1-q15 | D (sedang) | **B (0,87)** |
| LBI-d1s1-q26 | E (sedang) | **A (0,80)** |
| PPU-d1s1-q04 | A (sedang) | **E (0,80)** |

Sembilan sisanya berkeyakinan rendah di setidaknya satu sisi, tempat perbedaan
memang wajar. Daftar lengkapnya ada di repo.

## Jev menemukan kemungkinan kekeliruan di kunci jawaban

Sebelum run ini, sebuah audit sudah menandai dua jawaban PU di modul sebagai
kemungkinan keliru. Jev berasal dari keluarga model yang berbeda dari para
auditor, jadi jawabannya adalah bacaan independen ketiga:

| Soal | Kata modul | Audit kami | Pemecah buta | Jev |
|---|---|---|---|---|
| PU-d1-q05 | A | E | E | **E (0,90)** |
| PU-d1-q24 | E | A | A | **A (0,34)** |
| PU-d1-q18 | B | B | E | **E (0,59)** |

`PU-d1-q05` kini punya tiga pembaca independen yang memilih E, dan itu jawaban
paling yakin Jev di antara semua soal yang disengketakan. Soalnya menyebut
angka malaria "tidak menurun" — bukan naik — sementara opsi (a) yang jadi kunci
mengklaim angkanya meningkat, sesuatu yang tidak pernah dinyatakan teksnya.
Opsi (e) justru rantai sebab yang dinyatakan terang-terangan di teks.

Kuncinya tidak kami ubah. Itu kunci milik modul, dan repo ini mencatat
sengketanya alih-alih menimpanya. Tapi kalau kamu menilai PU, laporkan
dua-duanya: 47,8% atas 67 soal, 49,2% atas 65 soal tanpa kedua soal itu.

## Soal tabel Ya/Tidak

Jev mendapat 0 dari 2 soal tabel, dan 4 dari 6 pernyataannya. Kedua kegagalannya
hanya satu baris: satu klaim keliru tentang 2^64 diterima pada 0,59, dan satu
klaim benar ditolak pada 0,33. Menilai tabel secara utuh memang sengaja keras,
dan dengan hanya dua soal semacam ini di naskahnya, angka tersebut tidak
berbicara banyak.

## Biaya dan kecepatan

| Run | Request | Token input | Biaya | p50 | p95 |
|---|---|---|---|---|---|
| 67 soal berkunci | 67 | 35.883 | $0,0015 | 884 ms | 1083 ms |
| 89 soal berlabel | 89 | 70.754 | $0,0030 | 882 ms | 1187 ms |

Pada $0,042 per satu juta token input, output gratis — periksa tarif itu
terhadap harga terkini sebelum mengutipnya. Tidak ada yang perlu diulang, dan
tidak ada rate limit yang kena pada empat request bersamaan.

## Yang tidak bisa disimpulkan dari sini

- Soalnya rekonstruksi komunitas dari ingatan, dan kuncinya karya penyusun
  modul, bukan kunci resmi. Lihat [README](README.id.md).
- Tiga soal isian PK dikecualikan — tidak ada opsi untuk dipilih.
- Jev tidak pernah melihat gambar. Setiap gambar sampai kepadanya sebagai
  transkrip teks yang kami tulis dengan tangan, jadi sebagian dari yang diukur
  di sini adalah mutu transkrip itu. Run tanpa transkrip akan memisahkan
  keduanya; itu belum dikerjakan.
- Satu run, satu versi model, tanpa pengulangan. Tidak satu pun angka di sini
  punya batas galat.

Mengulanginya: `python3 scripts/run_bench.py && python3 scripts/score.py`.
