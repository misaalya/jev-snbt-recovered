# Hasil

[English](RESULTS.md) · **Bahasa Indonesia**

Model `jev-1.13.0`, diminta sebagai `jev-latest`. Dijalankan 18 September 2026.
156 soal, satu request per soal, penilaian sekuensial, gambar disediakan
sebagai transkrip teks. Tidak ada request yang memerlukan pengulangan.

## Skor per subtes

| Subtes | Skor | Soal | Acuan |
|---|---|---|---|
| LBE — Literasi Bahasa Inggris | 100,0% | 20/20 | label Claude |
| LBI — Literasi Bahasa Indonesia | 89,7% | 26/29 | label Claude |
| PBM — Pemahaman Bacaan dan Menulis | 75,0% | 15/20 | label Claude |
| PPU — Pengetahuan dan Pemahaman Umum | 75,0% | 15/20 | label Claude |
| PU — Penalaran Umum | 60,0% | 18/30 | kunci modul |
| PM — Penalaran Matematika | 45,0% | 9/20 | kunci modul |
| PK — Pengetahuan Kuantitatif | 29,4% | 5/17 | kunci modul |

## Skor per acuan

| Set | Skor | Soal |
|---|---|---|
| Kunci modul | 47,8% | 32/67 |
| Kunci modul, tanpa dua soal yang disengketakan | 49,2% | 32/65 |
| Label Claude | 85,4% | 76/89 |
| Gabungan | 69,2% | 108/156 |

Kunci modul mencakup PU, PK, dan PM. Empat subtes sisanya tidak punya kunci di
modul dan dinilai terhadap label Claude Opus 5, yang merupakan bacaan satu
model, bukan kunci jawaban resmi. Pemilihan acak di antara lima opsi
menghasilkan 20%; empat soal perbandingan kuantitas di PK menghasilkan 25%;
tabel Ya/Tidak tiga pernyataan yang dinilai utuh menghasilkan 12,5%.

## PU menurut jenis soal

PU satu-satunya subtes dalam set ini yang memuat soal verbal dan komputasional
sekaligus.

| Soal | Skor |
|---|---|
| q1–q20, penalaran verbal | 75,0% (15/20) |
| q21–q30, hitungan dan pembacaan diagram | 30,0% (3/10) |

## Kalibrasi

Atas 154 soal yang dijawab sebagai Choice. Dua soal tabel Ya/Tidak
mengembalikan peluang per pernyataan dan tidak membawa confidence Choice.

| Keyakinan | Skor | Soal |
|---|---|---|
| 0,0–0,5 | 34,0% | 16/47 |
| 0,5–0,7 | 68,4% | 13/19 |
| 0,7–0,9 | 75,0% | 21/28 |
| 0,9–1,0 | 96,7% | 58/60 |

Skor Brier atas peluang yang diberikan pada jawaban acuan: 0,253 untuk seluruh
154 soal, 0,402 pada set berkunci modul, 0,143 pada set berlabel Claude.

Skor bila jawaban paling ragu ditahan:

| Cakupan | Gabungan | Kunci modul | Label Claude |
|---|---|---|---|
| 100% | 69,2% | 49,2% | 85,4% |
| 90% | 77,0% | 53,4% | 88,8% |
| 80% | 81,3% | 59,6% | 91,5% |
| 70% | 85,2% | 63,0% | 91,9% |

## Soal tabel Ya/Tidak

| Ukuran | Skor |
|---|---|
| Soal utuh, ketiga pernyataan benar | 0/2 |
| Pernyataan satuan | 4/6 |

Dua pernyataan yang salah adalah `PM-d1s1-q06` pernyataan 3, yang acuannya
"Tidak" sedangkan Jev mengembalikan 0,59, dan `PM-d1s1-q14` pernyataan 1, yang
acuannya "Ya" sedangkan Jev mengembalikan 0,33.

## Perbedaan dengan label Claude

Kesepakatan pada 89 soal berlabel, menurut keyakinan yang tercatat pada
labelnya:

| Keyakinan label | Kesepakatan | Soal |
|---|---|---|
| high | 90,4% | 47/52 |
| medium | 87,0% | 20/23 |
| low | 64,3% | 9/14 |

13 soal yang jawabannya berbeda:

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

Tidak ada kolom di tabel ini yang merupakan kunci resmi.

## Soal yang kunci modulnya disengketakan

Tujuh soal PU sudah ditandai sebelum run ini, dalam audit yang tercatat di
`data/audit/module_key_audit.json`. Jawaban Jev dicantumkan di sampingnya
sebagai pembanding. Kuncinya tidak diubah.

| Soal | Kunci modul | Audit | Pemecah buta | Jev | Keyakinan Jev |
|---|---|---|---|---|---|
| PU-d1-q05 | A | E | E | E | 0,90 |
| PU-d1-q24 | E | A | A | A | 0,34 |
| PU-d1-q18 | B | B | E | E | 0,59 |
| PU-d1-q11 | E | D | D | E | 0,54 |
| PU-d1-q10 | B | A | A | B | 0,41 |
| PU-d1-q15 | B | D | D | A | 0,19 |
| PU-d1-q20 | A | B | B | B | 0,39 |

`PU-d1-q05` dan `PU-d1-q24` adalah dua soal yang dikecualikan pada angka 49,2%
di atas.

## Biaya dan latensi

| Run | Request | Token input | Token output | Biaya | p50 | p95 |
|---|---|---|---|---|---|---|
| Set berkunci modul | 67 | 35.883 | 3.558 | $0,0015 | 884 ms | 1083 ms |
| Set berlabel Claude | 89 | 70.754 | 4.710 | $0,0030 | 882 ms | 1187 ms |
| Total | 156 | 106.637 | 8.268 | $0,0045 | 883 ms | 1187 ms |

Biaya dihitung pada $0,042 per satu juta token input dengan output tidak
ditagih, yaitu tarif default yang dipakai `scripts/score.py`
(`--rate-per-mtok`); dokumentasinya tidak memuat halaman harga, jadi tarif itu
perlu diperiksa terhadap harga terkini. Empat request berjalan bersamaan. Tidak
ada respons 429 maupun 5xx.

## Ruang lingkup pengukuran

- Soalnya adalah rekonstruksi komunitas atas naskah 2025 dari ingatan peserta,
  dan kunci modul adalah karya penyusunnya, bukan kunci resmi. Lihat
  [README](README.id.md).
- Tiga soal isian PK dikecualikan dari seluruh angka di atas, sehingga tersisa
  67 dari 70 soal berkunci modul. Ketiganya tidak punya opsi jawaban di
  sumbernya.
- Gambar disediakan sebagai transkrip teks yang ditulis tangan; tidak ada
  gambar yang dikirim ke model. Run tanpa transkrip belum dilakukan, sehingga
  sumbangan transkrip terhadap skor belum terpisahkan.
- Satu run, satu versi model, tanpa pengulangan. Tidak ada angka di atas yang
  membawa perkiraan galat.

Respons di balik setiap angka di atas tersimpan di `data/results/`, satu baris
JSON per soal berisi jawaban, peluangnya, dan pemakaian token. Hitung ulang
dengan `python3 scripts/score.py` dan `python3 scripts/score.py --combined`;
run baru dapat dibuat dengan `python3 scripts/run_bench.py`.
