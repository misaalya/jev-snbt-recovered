# Jev pada SNBT 2025 hasil rekonstruksi — run pertama

[English](RESULTS.md) · **Bahasa Indonesia**

Model `jev-1.13.0` (diminta sebagai `jev-latest`), 18 September 2026. Satu
request per soal, tanpa gambar (setiap gambar hadir sebagai transkrip teks di
dalam state), tanpa perlu retry. Ulangi dengan:

```bash
python3 scripts/build_requests.py && python3 scripts/run_bench.py && python3 scripts/score.py
```

## Angka utama: 67 soal berkunci modul

| Subtes | Akurasi | Soal |
| --- | --- | --- |
| PU (penalaran umum) | **60,0%** | 18/30 |
| PM (penalaran matematika) | **45,0%** | 9/20 |
| PK (pengetahuan kuantitatif) | **29,4%** | 5/17 |
| **Total** | **47,8%** | 32/67 |

Tanpa dua soal yang kuncinya disengketakan audit (`PU-d1-q05`, `PU-d1-q24`):
**49,2%** (32/65). Tebak acak pada lima opsi adalah 20%.

Pembelahan di dalam PU adalah hasil paling tajam pada run ini:

| | Akurasi |
| --- | --- |
| PU q1–q20, penalaran verbal | **75%** (15/20) |
| PU q21–q30, hitungan dan diagram | **30%** (3/10) |

Dibaca bersama PK (29,4%) dan PM (45,0%) yang dua-duanya komputasional, polanya
konsisten: ini model yang membaca dengan baik dan menghitung dengan buruk.
Tidak ada di sini yang merupakan perbandingan dengan model reasoning — Jev
mengembalikan penilaian bertipe tanpa mengerjakan apa pun langkah demi langkah,
sementara soal hitungannya butuh beberapa langkah.

## Kalibrasi

Keyakinan mengikuti kebenaran dengan rapat, dan bagi siapa pun yang membangun
di atasnya ini lebih penting daripada angka utamanya:

| Keyakinan | Akurasi |
| --- | --- |
| 0,0–0,5 | 21,9% (7/32) |
| 0,5–0,7 | 50,0% (4/8) |
| 0,7–0,9 | 72,7% (8/11) |
| 0,9–1,0 | **92,9%** (13/14) |

Skor Brier atas peluang yang diberikan pada opsi benar: 0,402. Mengosongkan
jawaban paling ragu menaikkan akurasi sebagaimana mestinya: 49,2% pada cakupan
penuh, 59,6% pada 80%, 63,0% pada 71%. Modelnya tahu kapan dia tidak tahu.

## Dua soal tabel Ya/Tidak

0 dari 2 soal utuh, 4 dari 6 pernyataan. Kedua kegagalannya hanya satu baris:
`PM-d1s1-q06` pernyataan 3 (0,59 untuk klaim keliru soal 2^64 melawan 2^63) dan
`PM-d1s1-q14` pernyataan 1 (0,33 untuk klaim yang benar). Penilaian utuh memang
tidak memaafkan, dan dengan dua soal saja angka ini tidak berbicara banyak.

## Benchmark kedua: 89 soal dinilai terhadap label Claude

Sengaja dipisahkan dari angka utama. Modul tidak punya kunci untuk PPU, PBM,
LBI, maupun LBE, jadi acuannya di sini adalah label Claude Opus 5 — bacaan satu
model, diaudit beberapa pass, tetapi bukan kebenaran dasar. Bacalah ini sebagai
benchmark kedua dengan acuan yang lebih lemah, bukan sebagai akurasi terhadap
ujiannya.

| Subtes | Skor | Soal |
| --- | --- | --- |
| LBE (literasi bahasa Inggris) | **100,0%** | 20/20 |
| LBI (literasi bahasa Indonesia) | **89,7%** | 26/29 |
| PBM (pemahaman bacaan & menulis) | **75,0%** | 15/20 |
| PPU (pengetahuan & pemahaman umum) | **75,0%** | 15/20 |
| **Total** | **85,4%** | 76/89 |

Dipecah menurut keyakinan labelnya: high 90,4% (47/52), medium 87,0% (20/23),
low 64,3% (9/14). Ketidaksepakatannya menumpuk persis di tempat label sudah
menyatakan diri ragu — pola yang memang diharapkan dari kedua sisi.

Kalibrasi pada set ini jelas lebih baik daripada pada set berkunci:

| Keyakinan Jev | Skor |
| --- | --- |
| 0,0–0,5 | 60,0% (9/15) |
| 0,5–0,7 | 81,8% (9/11) |
| 0,7–0,9 | 76,5% (13/17) |
| 0,9–1,0 | **97,8%** (45/46) |

Skor Brier 0,143, berhadapan dengan 0,402 pada set berkunci. Cakupan: 85,4%
pada cakupan penuh, 91,5% pada 80%, 91,9% pada 70%. Biaya 70.754 token input
($0,0030), latensi p50 882 ms, p95 1187 ms.

Ada dua bacaan atas angka 85,4% ini dan run ini tidak bisa memisahkannya: bisa
jadi subtes bahasa memang lebih mudah bagi Jev daripada subtes komputasional,
atau dua model yang membaca teks yang sama berkorelasi sedemikian rupa sehingga
angkanya terangkat di atas yang akan diberikan kunci resmi. Jenis soalnya pun
berbeda — ini soal membaca dan bahasa, sementara PK dan PM aritmetika.

### 13 ketidaksepakatan

Tidak ada kolom yang berwenang di sini, jadi ini soal terbuka, bukan kesalahan:

| Soal | Label (keyakinan) | Jev (keyakinan) |
| --- | --- | --- |
| PPU-d1s1-q11 | E (low) | A (0,98) |
| PBM-d1s1-q15 | D (medium) | B (0,87) |
| LBI-d1s1-q26 | E (medium) | A (0,80) |
| PPU-d1s1-q04 | A (medium) | E (0,80) |
| LBI-d1s1-q13 | C (low) | D (0,70) |
| PBM-d1s1-q03 | A (high) | B (0,56) |
| PBM-d1s1-q04 | C (low) | E (0,54) |
| LBI-d1s1-q09 | E (low) | C (0,46) |
| PBM-d1s1-q16 | E (high) | C (0,44) |
| PPU-d1s1-q20 | A (high) | B (0,40) |
| PPU-d1s1-q17 | D (high) | A (0,27) |
| PPU-d1s1-q16 | A (low) | D (0,12) |
| PBM-d1s1-q10 | B (high) | C (0,10) |

Empat layak ditinjau ulang karena kedua sisi yakin ke arah berlawanan:
`PPU-d1s1-q11` (label low, Jev 0,98), `PBM-d1s1-q15` (Jev 0,87 melawan label
yang pada pembacaan ulang sebelumnya sudah diubah dari E ke D), `LBI-d1s1-q26`
dan `PPU-d1s1-q04` (keduanya 0,80). Sisanya berkeyakinan rendah di setidaknya
satu sisi, tempat perbedaan memang wajar.

## Gabungan: seluruh 156 soal yang bisa ditanyakan

Setiap soal yang bisa ditanyakan harness, dinilai terhadap acuan yang
dimilikinya: 67 terhadap kunci modul, 89 terhadap label Claude. Lebih luas
daripada kedua bagiannya — ketujuh subtes terwakili — tetapi acuannya campuran,
jadi angka ini lebih lemah daripada angka utama dan tidak menggantikan
keduanya.

| Subtes | Skor | Acuan |
| --- | --- | --- |
| LBE | 100,0% (20/20) | label Claude |
| LBI | 89,7% (26/29) | label Claude |
| PBM | 75,0% (15/20) | label Claude |
| PPU | 75,0% (15/20) | label Claude |
| PU | 60,0% (18/30) | kunci modul |
| PM | 45,0% (9/20) | kunci modul |
| PK | 29,4% (5/17) | kunci modul |
| **Total** | **69,2%** (108/156) | campuran |

Dipecah menurut acuan: 47,8% terhadap kunci modul, 85,4% terhadap label Claude.
Dua angka itulah yang menyusun 69,2%, dan jaraknya cukup lebar sehingga angka
gabungan ini selalu harus dikutip bersama keduanya, tidak pernah sendirian.
Angkanya juga mengikuti pembagian materi — subtes berkunci modul adalah yang
komputasional dan subtes berlabel adalah yang bahasa — sehingga angka gabungan
mencerminkan komposisi itu sebanyak ia mencerminkan Jev.

Kalibrasi atas seluruh 156 soal (154 di antaranya punya confidence Choice; dua
soal Ya/Tidak justru mengembalikan peluang per pernyataan):

| Keyakinan | Skor |
| --- | --- |
| 0,0–0,5 | 34,0% (16/47) |
| 0,5–0,7 | 68,4% (13/19) |
| 0,7–0,9 | 75,0% (21/28) |
| 0,9–1,0 | **96,7%** (58/60) |

Brier 0,253. Cakupan: 70,1% pada cakupan penuh, 81,3% pada 80%, 85,2% pada 70%.
Kenaikan monotonnya bertahan meski acuannya campuran, dan itu hal paling
berguna di bagian ini: berapa pun skornya, keyakinan Jev sendiri mengurutkan
jawabannya dengan benar.

Seluruh run: 156 request, 106.637 token input, **$0,0045**, p50 883 ms, p95
1187 ms.

Ulangi dengan `python3 scripts/score.py --combined`.

## Soal yang kuncinya disengketakan

Jev berasal dari keluarga model yang berbeda dari para auditor, jadi jawabannya
adalah bacaan independen ketiga atas tujuh soal PU yang diperdebatkan:

| Soal | Modul | Audit | Pemecah buta | Jev (keyakinan) |
| --- | --- | --- | --- | --- |
| q05 | A | E | E | **E (0,90)** |
| q24 | E | A | A | **A (0,34)** |
| q18 | B | B | E | **E (0,59)** |
| q11 | E | D | D | E (0,54) |
| q10 | B | A | A | B (0,41) |
| q15 | B | D | D | A (0,19) |
| q20 | A | B | B | B (0,39) |

`PU-d1-q05` kini punya tiga pembaca independen yang memilih E, satu di antaranya
pada keyakinan 0,90 — jawaban paling yakin Jev di antara soal-soal yang
diperdebatkan. Itu memperkuat dugaan bahwa A milik modul adalah kekeliruan
kunci yang sesungguhnya. `PU-d1-q24` mendapat suara ketiga untuk A, meski pada
keyakinan rendah. Sisanya tetap belum selesai dan kuncinya dibiarkan seperti di
modul.

## Biaya dan latensi

| Run | Request | Token input | Biaya | p50 | p95 |
| --- | --- | --- | --- | --- | --- |
| Berkunci (67) | 67 | 35.883 | $0,0015 | 884 ms | 1083 ms |
| Kesepakatan (89) | 89 | 70.754 | $0,0030 | 882 ms | 1187 ms |

Pada $0,042 per 1 juta token input, output gratis. Periksa tarifnya terhadap
harga terkini sebelum mengutipnya: dokumentasinya tidak memuat halaman harga,
jadi `score.py` menerimanya lewat `--rate-per-mtok`. Tidak ada request yang
perlu diulang; tidak ada 429 maupun 5xx pada konkurensi 4.

## Caveat

- Soalnya adalah rekonstruksi komunitas dari ingatan peserta, dan kuncinya
  karya penyusun modul, bukan kunci resmi. Lihat README.
- 3 soal isian PK dikecualikan: tidak punya opsi, jadi tidak bisa ditanyakan
  sebagai Choice tanpa distraktor karangan.
- Gambar sampai ke model hanya sebagai transkrip teks yang ditulis tangan. Arm
  tanpa-gambar belum dijalankan, jadi sumbangan transkrip itu terhadap skornya
  belum dipisahkan.
- Satu run, satu versi model, tanpa pengulangan: tidak ada di sini yang punya
  batas galat.
