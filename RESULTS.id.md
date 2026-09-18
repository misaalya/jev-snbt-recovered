# Hasil

[English](RESULTS.md) · **Bahasa Indonesia**

Model `jev-1.13.0`, dipanggil dengan nama `jev-latest`. Dijalankan 18 September
2026 atas 156 soal, satu request untuk tiap soal, dengan gambar yang sudah
diubah menjadi teks. Tidak ada satu pun request yang perlu diulang.

## Skor tiap subtes

| Subtes | Skor | Soal | Acuan |
|---|---|---|---|
| LBE — Literasi Bahasa Inggris | 100,0% | 20/20 | label Claude |
| LBI — Literasi Bahasa Indonesia | 89,7% | 26/29 | label Claude |
| PBM — Pemahaman Bacaan dan Menulis | 75,0% | 15/20 | label Claude |
| PPU — Pengetahuan dan Pemahaman Umum | 75,0% | 15/20 | label Claude |
| PU — Penalaran Umum | 60,0% | 18/30 | kunci modul |
| PM — Penalaran Matematika | 45,0% | 9/20 | kunci modul |
| PK — Pengetahuan Kuantitatif | 29,4% | 5/17 | kunci modul |

## Skor menurut acuan jawabannya

| Kelompok soal | Skor | Soal |
|---|---|---|
| Kunci modul | 47,8% | 32/67 |
| Kunci modul, tanpa dua soal yang kuncinya meragukan | 49,2% | 32/65 |
| Label Claude | 85,4% | 76/89 |
| Gabungan keduanya | 69,2% | 108/156 |

Kunci modul hanya menutup PU, PK, dan PM. Empat subtes sisanya tidak berkunci,
jadi dinilai memakai label Claude Opus 5 — tafsir satu model, bukan kunci
resmi. Sebagai pembanding, menebak acak di antara lima opsi menghasilkan 20%,
soal perbandingan kuantitas di PK yang hanya empat opsi menghasilkan 25%, dan
tabel Ya/Tidak berisi tiga pernyataan yang dinilai utuh menghasilkan 12,5%.

## PU dipilah menurut jenis soalnya

PU satu-satunya subtes di sini yang mencampur soal verbal dengan soal hitungan.

| Soal | Skor |
|---|---|
| q1–q20, penalaran verbal | 75,0% (15/20) |
| q21–q30, hitungan dan pembacaan diagram | 30,0% (3/10) |

## Kalibrasi

Dihitung atas 154 soal yang dijawab sebagai Choice. Dua soal tabel Ya/Tidak
tidak ikut, karena yang dikembalikannya peluang tiap pernyataan, bukan
keyakinan Choice.

| Keyakinan | Skor | Soal |
|---|---|---|
| 0,0–0,5 | 34,0% | 16/47 |
| 0,5–0,7 | 68,4% | 13/19 |
| 0,7–0,9 | 75,0% | 21/28 |
| 0,9–1,0 | 96,7% | 58/60 |

Skor Brier atas peluang yang diberikan pada jawaban acuan: 0,253 untuk seluruh
154 soal, 0,402 di soal berkunci modul, dan 0,143 di soal berlabel Claude.

Skor kalau jawaban yang paling ragu dibiarkan kosong:

| Cakupan | Gabungan | Kunci modul | Label Claude |
|---|---|---|---|
| 100% | 69,2% | 49,2% | 85,4% |
| 90% | 77,0% | 53,4% | 88,8% |
| 80% | 81,3% | 59,6% | 91,5% |
| 70% | 85,2% | 63,0% | 91,9% |

## Dua soal tabel Ya/Tidak

| Cara menghitung | Skor |
|---|---|
| Per soal utuh, ketiga pernyataan harus benar | 0/2 |
| Per pernyataan | 4/6 |

Dua pernyataan yang meleset: `PM-d1s1-q06` pernyataan 3, acuannya "Tidak"
sedangkan Jev menjawab 0,59; dan `PM-d1s1-q14` pernyataan 1, acuannya "Ya"
sedangkan Jev menjawab 0,33.

## Beda jawaban dengan label Claude

Tingkat kecocokan pada 89 soal berlabel, dipilah menurut keyakinan labelnya:

| Keyakinan label | Cocok | Soal |
|---|---|---|
| high | 90,4% | 47/52 |
| medium | 87,0% | 20/23 |
| low | 64,3% | 9/14 |

Ke-13 soal yang jawabannya berbeda:

| Soal | Label | Keyakinan label | Jev | Keyakinan Jev |
|---|---|---|---|---|
| PPU-d1s1-q11 | E | low | A | 0,98 |
| PBM-d1s1-q15 | D | medium | B | 0,87 |
| LBI-d1s1-q26 | E | medium | A | 0,80 |
| PPU-d1s1-q04 | A | medium | E | 0,80 |
| LBI-d1s1-q13 | C | low | D | 0,70 |
| PBM-d1s1-q03 | A | high | B | 0,56 |
| PBM-d1s1-q04 | C | low | E | 0,54 |
| LBI-d1s1-q09 | E | low | C | 0,46 |
| PBM-d1s1-q16 | E | high | C | 0,44 |
| PPU-d1s1-q20 | A | high | B | 0,40 |
| PPU-d1s1-q17 | D | high | A | 0,27 |
| PPU-d1s1-q16 | A | low | D | 0,12 |
| PBM-d1s1-q10 | B | high | C | 0,10 |

Tidak ada satu pun kolom di tabel ini yang berisi kunci resmi.

## Soal yang kunci modulnya meragukan

Tujuh soal PU sudah ditandai sebelum run ini lewat pemeriksaan yang tercatat di
`data/audit/module_key_audit.json`. Jawaban Jev ditaruh berdampingan sekadar
sebagai pembanding, dan kuncinya sendiri tidak diubah.

| Soal | Kunci modul | Pemeriksaan | Penjawab buta | Jev | Keyakinan Jev |
|---|---|---|---|---|---|
| PU-d1-q05 | A | E | E | E | 0,90 |
| PU-d1-q24 | E | A | A | A | 0,34 |
| PU-d1-q18 | B | B | E | E | 0,59 |
| PU-d1-q11 | E | D | D | E | 0,54 |
| PU-d1-q10 | B | A | A | B | 0,41 |
| PU-d1-q15 | B | D | D | A | 0,19 |
| PU-d1-q20 | A | B | B | B | 0,39 |

`PU-d1-q05` dan `PU-d1-q24` adalah dua soal yang dikeluarkan pada angka 49,2%
di atas.

## Biaya dan latensi

| Run | Request | Token input | Token output | Biaya | p50 | p95 |
|---|---|---|---|---|---|---|
| Soal berkunci modul | 67 | 35.883 | 3.558 | $0,0015 | 884 ms | 1083 ms |
| Soal berlabel Claude | 89 | 70.754 | 4.710 | $0,0030 | 882 ms | 1187 ms |
| Total | 156 | 106.637 | 8.268 | $0,0045 | 883 ms | 1187 ms |

Biayanya dihitung dengan tarif $0,042 per satu juta token input dan output
tidak ditagih, yaitu tarif bawaan `scripts/score.py` (bisa diubah lewat
`--rate-per-mtok`). Dokumentasi TypeSafe tidak memuat halaman harga, jadi tarif
ini sebaiknya dicocokkan dulu dengan harga yang berlaku. Empat request berjalan
bersamaan, dan tidak ada respons 429 maupun 5xx.

## Sejauh mana angka ini berlaku

- Soalnya rekonstruksi komunitas dari ingatan peserta, dan kunci modulnya
  buatan penyusun modul, bukan kunci resmi. Selengkapnya di
  [README](README.id.md).
- Tiga soal isian PK tidak masuk hitungan mana pun di atas, jadi yang terpakai
  67 dari 70 soal berkunci modul. Ketiganya memang tidak punya opsi jawaban di
  sumbernya.
- Gambar dikirim dalam bentuk transkrip teks yang ditulis manual; tidak ada
  gambar yang dikirim ke model. Run tanpa transkrip belum pernah dicoba,
  sehingga seberapa besar pengaruh transkrip itu terhadap skor belum terpisah.
- Semuanya berasal dari satu run pada satu versi model, tanpa pengulangan, jadi
  tidak ada angka di atas yang disertai perkiraan galat.

Respons di balik setiap angka di atas tersimpan di `data/results/`, satu baris
JSON per soal berisi jawaban, peluangnya, dan pemakaian tokennya. Hitung ulang
dengan `python3 scripts/score.py` dan `python3 scripts/score.py --combined`;
untuk run yang benar-benar baru, jalankan `python3 scripts/run_bench.py`.
