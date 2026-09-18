# snbt-jev-bench

[English](README.md) · **Bahasa Indonesia**

Pengujian **TypeSafe Jev** pada soal **SNBT 2025**, ujian masuk perguruan
tinggi negeri di Indonesia.

> **Soalnya hasil rekonstruksi, bukan naskah aslinya.** Naskah SNBT tidak
> pernah dirilis setelah ujian selesai, jadi semua soal di sini disusun ulang
> oleh komunitas dari ingatan peserta. Redaksinya bisa meleset dari yang
> benar-benar keluar, beberapa soal cacat, dan kunci jawabannya pun buatan
> penyusun modul, bukan dari penyelenggara ujian. Artinya seluruh angka di
> repositori ini mengukur Jev terhadap rekonstruksi tersebut, bukan terhadap
> SNBT yang sesungguhnya.

Dataset ini berisi 159 soal dari ketujuh subtes. Tiap soal berdiri sendiri:
bacaan dan transkrip gambar yang dirujuknya sudah menyatu di dalam soal itu,
jadi tidak ada yang perlu dicari di tempat lain. Hasil run pertama ada di
**[RESULTS.id.md](RESULTS.id.md)**, lengkap dengan respons mentahnya di
`data/results/`.

## Asal soal

Semua soal berasal dari *Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam:
764 halaman soal hasil ingatan peserta yang ditata ulang oleh relawan
(`dataset/MMASNBT2025.pdf`, tidak ikut disertakan di sini).

**Kuncinya bukan kunci resmi.** Kunci jawaban di modul adalah hasil kerja
penyusunnya sendiri, dan hanya ada untuk tiga subtes: PU, PK, dan PM. Di bagian
PU, penyusunnya bahkan memasang catatan *"bukan jawaban yang pasti"*. PPU, PBM,
LBI, dan LBE sama sekali tidak berkunci.

Yang diambil adalah Hari 1 Sesi 1 dari tiap subtes. Khusus PU yang memang
tidak dibagi per sesi, Hari 1 diambil seluruhnya.

| Subtes | | Soal | Sumber jawaban |
|---|---|---|---|
| PU | Penalaran Umum | 30 | kunci modul |
| PK | Pengetahuan Kuantitatif | 20 | kunci modul |
| PM | Penalaran Matematika | 20 | kunci modul |
| PPU | Pengetahuan dan Pemahaman Umum | 20 | label Claude |
| PBM | Pemahaman Bacaan dan Menulis | 20 | label Claude |
| LBI | Literasi Bahasa Indonesia | 29 | label Claude |
| LBE | Literasi Bahasa Inggris | 20 | label Claude |

Soal dipindahkan dari PDF ke JSON dengan bantuan **claude-code**.

## Soal yang bergambar

Jev membaca teks, bukan gambar. Kesepuluh gambar di dataset ini berupa diagram
garis, diagram lingkaran, bangun geometri, dan satu definisi operator dalam
kurung besar. Semuanya dipotong dari halamannya, lalu **ditranskrip menjadi
teks oleh Claude** dan dicocokkan ulang secara manual dengan potongan
aslinya. Pengecekan
itu sempat mengubah satu transkrip: di `LBI-d1s1-teks2`, kemiringan garisnya
diukur, dan hasilnya membantah klaim transkrip pertama bahwa dua garis itu
sejajar.

## Dari mana jawaban acuannya

**PU, PK, dan PM memakai kunci modul.** Meski begitu kuncinya tetap diuji
ulang, karena sumbernya sendiri menyatakan kunci itu belum tentu benar.

**PPU, PBM, LBI, dan LBE memakai label buatan Claude Opus 5**, karena modulnya
memang tidak menyediakan kunci untuk keempatnya. Label ini hanya berasal dari
satu model (Opus 5), jadi bukan jawaban yang sudah pasti benar.

## Cara soal dikirim ke Jev

Tiap soal dikirim sebagai satu request ke `POST
https://api.typesafe.ai/v1/systemone`. Sebelum ada yang dikirim,
`scripts/build_requests.py` menuliskan dulu seluruh payload-nya ke disk,
sehingga request persis di balik sebuah skor selalu bisa ditengok kembali.

Soal pilihan ganda biasa menjadi satu **Choice** berisi opsi a–e milik soal itu
sendiri; tidak ada opsi yang dikarang. Dua jenis soal dikecualikan dari pola
itu.

- **Dua tabel Ya/Tidak** (PM q06 dan q14) dikirim sebagai satu request berisi
  tiga penilaian **Noul**, satu untuk tiap pernyataan. Nilainya dihitung per
  soal utuh, sedangkan angka per pernyataan dilaporkan terpisah karena peluang
  menebak benarnya 50%, bukan 20%.
- **Tiga soal isian** (PK q01, q02, q18) tidak punya opsi sama sekali.
  Menjadikannya Choice berarti mengarang pengecoh, dan yang terukur nanti
  pengecohnya, bukan modelnya. Ketiganya dikeluarkan: yang dinilai 67 soal,
  bukan 70.

## Menjalankan benchmark

```bash
python3 scripts/build_requests.py        # tulis payload request-nya
python3 scripts/run_bench.py --dry-run   # validasi tanpa mengirim

cp .env.example .env                     # lalu isikan kunci API
python3 scripts/run_bench.py --limit 5   # uji cepat
python3 scripts/run_bench.py             # 67 soal yang punya kunci modul
python3 scripts/score.py

# 89 soal sisanya, dinilai memakai label Claude
python3 scripts/build_requests.py --split claude_labeled
python3 scripts/run_bench.py --requests data/requests/claude_labeled.jsonl \
                             --out data/results/claude_labeled.jsonl
python3 scripts/score.py --agreement --results data/results/claude_labeled.jsonl

python3 scripts/score.py --combined      # seluruh 156 soal sekaligus
```

`data/results/` sudah berisi run yang diterbitkan, dan runner melewati soal
yang jawabannya sudah tercatat di sana. Jadi perintah di atas bisa dijalankan
ulang untuk menilai respons yang sudah di-commit, tanpa kunci API. Untuk run
baru, arahkan keluarannya ke berkas lain lewat `--out data/results/rerun.jsonl`
dan berikan path yang sama ke `scripts/score.py --results`.

Sifat melewati itu sekaligus membuat run yang terputus cukup diulang
perintahnya. Respons 408, 429, dan 5xx diulang otomatis dengan jeda yang
membesar, dan kegagalan dicatat sebagai baris hasil, bukan membatalkan run.

`scripts/score.py` melaporkan akurasi per subtes dan per rentang keyakinan,
skor Brier, akurasi bila jawaban yang paling ragu tidak dihitung, serta biaya
token dan latensinya.

## Ringkasan hasil

| Kelompok soal | Skor |
|---|---|
| 67 soal, kunci modul | 47,8% |
| 89 soal, label Claude | 85,4% |
| 156 soal, acuan campuran | 69,2% |

Rincian per subtes, kalibrasi, daftar perbedaan dengan label, dan biayanya ada
di **[RESULTS.id.md](RESULTS.id.md)**.

## Isi repositori

```
data/questions/with_key/        PU, PK, PM — jawaban dari kunci modul
data/questions/claude_labeled/  PPU, PBM, LBI, LBE — jawaban dari label Claude
data/audit/                     hasil pemeriksaan kunci modul dan soal yang meragukan
data/figures/                   potongan gambar aslinya
data/results/                   run yang dilaporkan di RESULTS.id.md, satu baris per soal
scripts/build_requests.py       soal -> payload request System One
scripts/run_bench.py            mengirim payload, mencatat jawaban dan pemakaian token
scripts/score.py                menilai satu run memakai kunci modul atau label Claude
```

`scripts/build_requests.py` menulis ke `data/requests/`, yang dibuat ulang
secara lokal dan tidak ikut dilacak git. Sementara `data/results/` berisi run
yang diterbitkan persis seperti dicatat runner, jadi angka di RESULTS.id.md
bisa dihitung ulang sendiri dan run baru bisa dibandingkan baris per baris
dengannya.

## Atribusi

Soal: **Modul MMA SNBT 2025**, Tim Mangkuk Mi Ayam
(<https://linktr.ee/MangkukMieAyam>). Penataannya berlisensi CC BY-NC 4.0,
sedangkan isi soalnya milik penyelenggara ujian dan ditampilkan di sini semata
untuk keperluan riset non-komersial.
