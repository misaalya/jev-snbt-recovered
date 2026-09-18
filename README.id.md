# snbt-jev-bench

[English](README.md) · **Bahasa Indonesia**

Pengujian **TypeSafe Jev** memakai soal **SNBT 2025**, ujian masuk perguruan
tinggi negeri di Indonesia.

> **Soal di sini bukan naskah asli.** Naskah SNBT tidak pernah dirilis, jadi
> soal-soal ini disusun ulang oleh komunitas berdasarkan ingatan peserta.
> Redaksinya bisa berbeda dari aslinya, beberapa soal ada yang cacat, dan
> kuncinya dibuat oleh penyusun modul, bukan oleh panitia. Jadi semua angka di
> sini mengukur Jev terhadap soal rekonstruksi, bukan terhadap SNBT yang
> sebenarnya.

Dataset berisi 159 soal dari tujuh subtes. Setiap soal sudah lengkap dengan
bacaan dan transkrip gambarnya. Hasilnya ada di
**[RESULTS.id.md](RESULTS.id.md)**, dan respons mentahnya di `data/results/`.

## Sumber soal

Soal diambil dari *Modul MMA SNBT 2025* karya Tim Mangkuk Mi Ayam, berisi 764
halaman soal hasil ingatan peserta (`dataset/MMASNBT2025.pdf`, tidak disertakan
di repositori ini).

**Kuncinya tidak resmi.** Kunci dibuat oleh penyusun modul dan hanya tersedia
untuk PU, PK, dan PM. Untuk PU, penyusunnya sendiri menulis *"bukan jawaban yang
pasti"*. PPU, PBM, LBI, dan LBE tidak punya kunci.

Soal yang dipakai adalah Hari 1 Sesi 1 dari setiap subtes. PU tidak dibagi per
sesi, jadi seluruh soal PU Hari 1 dipakai.

| Subtes | | Soal | Sumber jawaban |
|---|---|---|---|
| PU | Penalaran Umum | 30 | kunci modul |
| PK | Pengetahuan Kuantitatif | 20 | kunci modul |
| PM | Penalaran Matematika | 20 | kunci modul |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | label Claude |
| PBM | Pemahaman Bacaan dan Menulis | 20 | label Claude |
| LBI | Literasi Bahasa Indonesia | 29 | label Claude |
| LBE | Literasi Bahasa Inggris | 20 | label Claude |

Soal dipindahkan dari PDF ke JSON dengan bantuan **Claude Code**.

## Soal bergambar

Jev hanya membaca teks. Ada sepuluh gambar di dataset ini: diagram garis,
diagram lingkaran, bangun geometri, dan satu definisi operator. Semua gambar
**diubah menjadi teks oleh Claude**, lalu dicek manual dengan gambar aslinya.
Satu transkrip diperbaiki dari pengecekan ini: di `LBI-d1s1-teks2`, dua garis
yang awalnya disebut sejajar ternyata tidak sejajar setelah kemiringannya
diukur.

## Sumber jawaban acuan

**PU, PK, dan PM memakai kunci modul.** Kunci ini tetap diperiksa ulang karena
penyusunnya sendiri tidak menjamin kebenarannya.

**PPU, PBM, LBI, dan LBE memakai label dari Claude Opus 5**, karena modul tidak
menyediakan kunci. Label ini hanya dari satu model, jadi belum tentu benar.

## Cara soal dikirim ke Jev

Setiap soal dikirim sebagai satu request ke `POST
https://api.typesafe.ai/v1/systemone`. Semua payload ditulis dulu ke disk oleh
`scripts/build_requests.py`, jadi request di balik setiap skor bisa dicek.

Soal pilihan ganda dikirim sebagai satu **Choice** dengan opsi a sampai e dari
soal itu sendiri. Ada dua pengecualian:

- **Dua soal tabel Ya/Tidak** (PM q06 dan q14) dikirim sebagai tiga penilaian
  **Noul**, satu per pernyataan. Nilai dihitung per soal utuh. Skor per
  pernyataan dilaporkan terpisah karena peluang tebakannya 50%, bukan 20%.
- **Tiga soal isian** (PK q01, q02, q18) tidak punya opsi. Kalau dibuatkan
  opsi, yang diukur adalah opsi buatan itu, bukan modelnya. Jadi ketiganya
  tidak dipakai, dan yang dinilai 67 soal, bukan 70.

## Menjalankan benchmark

```bash
python3 scripts/build_requests.py        # tulis payload request
python3 scripts/run_bench.py --dry-run   # cek tanpa mengirim

cp .env.example .env                     # lalu isi kunci API
python3 scripts/run_bench.py --limit 5   # uji cepat
python3 scripts/run_bench.py             # 67 soal berkunci modul
python3 scripts/score.py

# 89 soal lainnya, dinilai dengan label Claude
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined      # semua 156 soal
```

`data/results/` sudah berisi hasil run yang dipublikasikan. Runner akan
melewati soal yang jawabannya sudah ada, jadi perintah di atas bisa dijalankan
tanpa kunci API. Untuk run baru, simpan hasilnya ke file lain dengan
`--out data/results/rerun.jsonl`, lalu pakai path yang sama di
`scripts/score.py --results`.

Kalau run terputus, cukup jalankan ulang perintahnya. Respons 408, 429, dan 5xx
otomatis dicoba ulang, dan request yang gagal tetap dicatat tanpa menghentikan
run.

`scripts/score.py` menampilkan akurasi per subtes dan per tingkat keyakinan,
skor Brier, akurasi jika jawaban paling ragu tidak dihitung, serta biaya dan
latensi.

## Ringkasan hasil

| Kelompok soal | Skor |
|---|---|
| 67 soal, kunci modul | 47,8% |
| 89 soal, label Claude | 85,4% |
| 156 soal, gabungan | 69,2% |

Rincian lengkap ada di **[RESULTS.id.md](RESULTS.id.md)**.

## Isi repositori

```
data/questions/with_key/        PU, PK, PM (jawaban dari kunci modul)
data/questions/claude_labeled/  PPU, PBM, LBI, LBE (jawaban dari label Claude)
data/audit/                     hasil pemeriksaan kunci modul dan soal yang meragukan
data/figures/                   potongan gambar asli
data/results/                   hasil run di RESULTS.id.md, satu baris per soal
scripts/build_requests.py       mengubah soal menjadi payload request
scripts/run_bench.py            mengirim payload, mencatat jawaban dan token
scripts/score.py                menilai hasil run
```

`data/requests/` dibuat ulang secara lokal dan tidak dilacak git. Isi
`data/results/` disimpan apa adanya, jadi angka di RESULTS.id.md bisa dihitung
ulang dan dibandingkan dengan run baru.

## Atribusi

Soal: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Tata letaknya berlisensi CC BY-NC 4.0.
Isi soal milik penyelenggara ujian dan dipakai di sini hanya untuk riset
non-komersial.
