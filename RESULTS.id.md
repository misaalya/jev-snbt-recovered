# Hasil

[English](RESULTS.md) · **Bahasa Indonesia**

Model `jev-1.13.0` (dipanggil sebagai `jev-latest`), dijalankan 18 September
2026. Total 156 soal, satu request per soal, gambar dikirim dalam bentuk teks.
Tidak ada request yang perlu diulang.

## Skor per subtes

| Subtes | Skor | Soal | Acuan |
|---|---|---|---|
| LBE (Literasi Bahasa Inggris) | 100,0% | 20/20 | label Claude |
| LBI (Literasi Bahasa Indonesia) | 89,7% | 26/29 | label Claude |
| PBM (Pemahaman Bacaan dan Menulis) | 75,0% | 15/20 | label Claude |
| PPU (Pengetahuan dan Pemahaman Umum) | 75,0% | 15/20 | label Claude |
| PU (Penalaran Umum) | 60,0% | 18/30 | kunci modul |
| PM (Penalaran Matematika) | 45,0% | 9/20 | kunci modul |
| PK (Pengetahuan Kuantitatif) | 29,4% | 5/17 | kunci modul |

## Skor per jenis acuan

| Kelompok soal | Skor | Soal |
|---|---|---|
| Kunci modul | 47,8% | 32/67 |
| Kunci modul, tanpa dua soal yang kuncinya meragukan | 49,2% | 32/65 |
| Label Claude | 85,4% | 76/89 |
| Gabungan | 69,2% | 108/156 |

Kunci modul hanya ada untuk PU, PK, dan PM. Empat subtes lainnya dinilai dengan
label dari Claude Opus 5, yang bukan kunci resmi. Sebagai pembanding, skor
tebakan acak adalah 20% untuk lima opsi, 25% untuk soal perbandingan kuantitas
PK (empat opsi), dan 12,5% untuk tabel Ya/Tidak berisi tiga pernyataan.

## PU per jenis soal

PU berisi campuran soal verbal dan soal hitungan.

| Soal | Skor |
|---|---|
| q1 sampai q20, penalaran verbal | 75,0% (15/20) |
| q21 sampai q30, hitungan dan membaca diagram | 30,0% (3/10) |

## Kalibrasi

Dihitung dari 154 soal Choice. Dua soal tabel Ya/Tidak tidak dihitung karena
tidak memberi nilai keyakinan Choice.

| Keyakinan | Skor | Soal |
|---|---|---|
| 0,0 - 0,5 | 34,0% | 16/47 |
| 0,5 - 0,7 | 68,4% | 13/19 |
| 0,7 - 0,9 | 75,0% | 21/28 |
| 0,9 - 1,0 | 96,7% | 58/60 |

Semakin tinggi keyakinan Jev, semakin sering jawabannya benar.

Skor Brier: 0,253 untuk semua 154 soal, 0,402 untuk soal berkunci modul, dan
0,143 untuk soal berlabel Claude. Makin kecil makin baik.

Skor jika jawaban yang paling ragu tidak dihitung:

| Soal yang dijawab | Gabungan | Kunci modul | Label Claude |
|---|---|---|---|
| 100% | 69,2% | 49,2% | 85,4% |
| 90% | 77,0% | 53,4% | 88,8% |
| 80% | 81,3% | 59,6% | 91,5% |
| 70% | 85,2% | 63,0% | 91,9% |

## Soal tabel Ya/Tidak

| Cara hitung | Skor |
|---|---|
| Per soal (ketiga pernyataan harus benar) | 0/2 |
| Per pernyataan | 4/6 |

Dua pernyataan yang salah:

- `PM-d1s1-q06` pernyataan 3: acuan "Tidak", Jev menjawab 0,59.
- `PM-d1s1-q14` pernyataan 1: acuan "Ya", Jev menjawab 0,33.

## Perbedaan dengan label Claude

Tingkat kecocokan pada 89 soal, berdasarkan keyakinan label:

| Keyakinan label | Cocok | Soal |
|---|---|---|
| high | 90,4% | 47/52 |
| medium | 87,0% | 20/23 |
| low | 64,3% | 9/14 |

Ada 13 soal yang jawabannya berbeda:

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

Label maupun jawaban Jev di tabel ini bukan kunci resmi.

## Soal dengan kunci modul yang meragukan

Tujuh soal PU sudah ditandai sebelum run ini (lihat
`data/audit/module_key_audit.json`). Jawaban Jev dicantumkan sebagai
pembanding. Kuncinya tidak diubah.

| Soal | Kunci modul | Pemeriksaan | Penjawab buta | Jev | Keyakinan Jev |
|---|---|---|---|---|---|
| PU-d1-q05 | A | E | E | E | 0,90 |
| PU-d1-q24 | E | A | A | A | 0,34 |
| PU-d1-q18 | B | B | E | E | 0,59 |
| PU-d1-q11 | E | D | D | E | 0,54 |
| PU-d1-q10 | B | A | A | B | 0,41 |
| PU-d1-q15 | B | D | D | A | 0,19 |
| PU-d1-q20 | A | B | B | B | 0,39 |

`PU-d1-q05` dan `PU-d1-q24` adalah dua soal yang tidak dihitung pada skor
49,2%.

## Biaya dan latensi

| Run | Request | Token input | Token output | Biaya | p50 | p95 |
|---|---|---|---|---|---|---|
| Soal berkunci modul | 67 | 35.883 | 3.558 | $0,0015 | 884 ms | 1083 ms |
| Soal berlabel Claude | 89 | 70.754 | 4.710 | $0,0030 | 882 ms | 1187 ms |
| Total | 156 | 106.637 | 8.268 | $0,0045 | 883 ms | 1187 ms |

Biaya dihitung dengan tarif $0,042 per satu juta token input, dan token output
tidak ditagih. Ini tarif bawaan `scripts/score.py` (bisa diubah dengan
`--rate-per-mtok`). Dokumentasi TypeSafe belum mencantumkan harga, jadi tarif
ini perlu dicek ulang. Run memakai empat request sekaligus, tanpa respons 429
atau 5xx.

## Batasan

- Soal adalah rekonstruksi komunitas, dan kunci modul bukan kunci resmi. Lihat
  [README](README.id.md).
- Tiga soal isian PK tidak dihitung, jadi yang dinilai 67 dari 70 soal
  berkunci modul.
- Gambar dikirim sebagai teks, bukan gambar asli. Belum ada run tanpa
  transkrip, jadi pengaruh transkrip terhadap skor belum diketahui.
- Hanya satu run dengan satu versi model, jadi belum ada perkiraan galat.

Semua respons tersimpan di `data/results/`, satu baris JSON per soal. Hitung
ulang dengan `python3 scripts/score.py` dan `python3 scripts/score.py
--combined`. Untuk run baru, jalankan `python3 scripts/run_bench.py`.
