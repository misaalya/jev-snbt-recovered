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

## Asal soalnya

Semua soal berasal dari *Modul MMA SNBT 2025* susunan Tim Mangkuk Mi Ayam:
764 halaman soal hasil ingatan peserta yang ditata ulang oleh relawan
(`dataset/MMASNBT2025.pdf`, tidak ikut disertakan di sini).

Ada dua hal dari sumber itu yang menentukan bentuk seluruh proyek ini.

**Kuncinya bukan kunci resmi.** Kunci jawaban di modul adalah hasil kerja
penyusunnya sendiri, dan hanya ada untuk tiga subtes: PU, PK, dan PM. Di bagian
PU, penyusunnya bahkan memasang catatan *"bukan jawaban yang pasti"*. PPU, PBM,
LBI, dan LBE sama sekali tidak berkunci.

**Sebagian soal sudah cacat sejak dari sumbernya.** `LBI-d1s1-q21` kehilangan
satu opsi, dan di `PPU-d1s1-teks4` tertulis "kristal udara" padahal yang
dimaksud "kristal es". Cacat seperti ini tidak pernah diam-diam dibetulkan:
soalnya tetap ditampilkan apa adanya, lalu diberi `_source_note` yang
menjelaskan masalahnya.

## Bagian mana yang diambil, dan apa yang dikerjakan padanya

Yang diambil adalah **Hari 1 Sesi 1 dari tiap subtes**. Khusus PU yang memang
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

Soal dipindahkan dari PDF ke JSON. Selain mengambil teksnya, ada beberapa hal
lain yang dikerjakan.

- **Tiap soal dibekali bacaannya sendiri.** Di modul, satu bacaan dicetak
  sekali lalu dipakai bersama oleh empat sampai lima soal. Di dataset, bacaan
  itu disalin utuh ke setiap soal yang memakainya, supaya tidak ada soal yang
  menggantung pada teks di luar dirinya.
- **Cetak tebal dan miring ikut dipertahankan.** Ada soal yang menanyakan
  "kata **bercetak tebal**", jadi ekstraksinya membaca struktur XML dari PDF,
  bukan teks polos yang sudah kehilangan format.
- **Batas paragraf disusun ulang**, karena sebagian soal menunjuk paragraf
  tertentu. Kata yang terpenggal di ujung baris disambung kembali (`me-` +
  `nang` → `menang`).
- **Notasi matematika ditulis sebagai teks biasa**: `x²`, `√29`, `2^(n–1)`,
  `6 5/7`. Seluruh soal PK dan PM diketik ulang manual dari gambar halamannya,
  sebab pecahan bertingkat selalu berantakan kalau diambil otomatis.
- **Tidak ada perbaikan yang dilakukan diam-diam.** Setiap kejanggalan bawaan
  dari sumbernya dicatat di `_source_note` pada soal atau bacaan yang
  bersangkutan.

Proses ekstraksinya sendiri tidak ikut diterbitkan karena bergantung pada PDF
sumber yang tidak boleh disebarkan ulang. Yang dibagikan di sini adalah
hasilnya, yaitu `data/questions/`.

## Soal yang bergambar

Jev membaca teks, bukan gambar. Kesepuluh gambar di dataset ini — diagram
garis, diagram lingkaran, bangun geometri, dan satu definisi operator dalam
kurung besar — dipotong dari halamannya, lalu **diterjemahkan menjadi teks oleh
Claude** dan dicocokkan ulang secara manual dengan potongan aslinya. Pengecekan
itu sempat mengubah satu transkrip: di `LBI-d1s1-teks2`, kemiringan garisnya
diukur, dan hasilnya membantah klaim transkrip pertama bahwa dua garis itu
sejajar.

Hasil transkripnya disimpan di `figure_note` dan ikut disisipkan ke setiap soal
yang memakai gambar tersebut, sementara potongan aslinya tetap tersimpan di
`data/figures/` supaya bisa dibandingkan siapa pun. Dengan cara ini model
menerima bentuk masukan yang sama untuk semua soal, dan pembacaan gambarnya
terbuka untuk diperiksa, bukan tersembunyi di dalam model visual.

## Dari mana jawaban acuannya

**PU, PK, dan PM memakai kunci modul**, disalin apa adanya.

Meski begitu kuncinya tetap diuji. Ke-70 soalnya dikerjakan ulang dari nol,
lalu tiga sesi Claude yang terpisah mengerjakannya sekali lagi tanpa melihat
kunci maupun isi repositori ini. PK dan PM cocok 20/20 pada kedua putaran,
sedangkan PU cocok 24 dari 30 dan 23 dari 30. Kuncinya tetap tidak diubah.
Semua ketidakcocokan dicatat di `data/audit/module_key_audit.json`, dan dua
soal yang kuncinya paling meragukan, `PU-d1-q05` dan `PU-d1-q24`, didaftar di
`data/audit/disputed_items.json` supaya akurasinya bisa dilaporkan dengan dan
tanpa keduanya.

**PPU, PBM, LBI, dan LBE memakai label buatan Claude Opus 5**, karena modulnya
memang tidak menyediakan kunci untuk keempatnya. Label ini tafsir satu model,
bukan jawaban yang sudah pasti benar. Karena itu label disimpan di direktori
yang terpisah dari kunci modul, dan tiap soal membawa kolom `answer_source`
yang menyebutkan asal jawabannya, supaya keduanya tidak pernah tercampur.

Tiap label diberi tingkat keyakinan high, medium, atau low (berturut-turut 52,
23, dan 14 soal) yang ditetapkan saat pelabelan, dan RESULTS.id.md melaporkan
tingkat kecocokan Jev untuk masing-masing tingkat itu. Yang diterbitkan hanya
label akhirnya; tahap-tahap penyusunannya adalah bahan kerja dan tidak ikut
dibagikan. Satu keterbatasan perlu disebut terus terang: yang membuat label dan
yang memeriksanya berasal dari keluarga model yang sama, jadi kecocokan di
antara mereka bukan bukti yang kuat.

## Cara soal dikirim ke Jev

Tiap soal dikirim sebagai satu request ke `POST
https://api.typesafe.ai/v1/systemone`. Sebelum ada yang dikirim,
`scripts/build_requests.py` menuliskan dulu seluruh payload-nya ke disk,
sehingga request persis di balik sebuah skor selalu bisa ditengok kembali.

Soal pilihan ganda biasa menjadi satu **Choice** dengan kriteria berupa opsi
a–e milik soal itu sendiri; tidak ada opsi yang dikarang. Dua jenis soal
menuntut perlakuan lain.

**Dua soal tabel Ya/Tidak** (PM q06 dan q14) bukan satu keputusan, melainkan
tiga pernyataan yang masing-masing harus ditandai. Setiap tabel dikirim sebagai
satu request berisi tiga penilaian **Noul** atas bacaan yang sama. Penilaiannya
dihitung per soal utuh — ketiga pernyataan harus benar — sedangkan angka per
pernyataan dilaporkan terpisah, sebab peluang menebak benarnya 50% dan tidak
sebanding dengan 20% pada soal lima opsi.

**Tiga soal isian** (PK q01, q02, dan q18) tidak punya opsi sama sekali,
sehingga mustahil dijadikan Choice tanpa mengarang pengecohnya — dan kalau
begitu yang terukur justru pengecoh karangan itu, bukan modelnya. Ketiganya
dikeluarkan, jadi yang dinilai 67 soal, bukan 70.

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

Perlu diketahui, `data/results/` sudah berisi run yang diterbitkan, dan runner
selalu melewati soal yang jawabannya sudah ada di sana. Jadi menjalankan ulang
perintah di atas akan melaporkan semuanya sudah selesai, dan penilaiannya
memakai respons yang sudah ikut di-commit — tanpa perlu kunci API sama sekali.
Kalau memang ingin menjalankan run baru, arahkan keluarannya ke berkas lain
lewat `--out data/results/rerun.jsonl`, lalu berikan path yang sama ke
`scripts/score.py --results`.

Run yang terputus bisa dilanjutkan begitu saja: soal yang sudah tercatat akan
dilewati, jadi cukup ulangi perintahnya kalau sempat kena rate limit. Respons
408, 429, dan 5xx diulang dengan jeda yang membesar dan mengikuti
`Retry-After`, sementara kegagalan dicatat sebagai baris hasil, bukan
membatalkan seluruh run.

`scripts/score.py` melaporkan akurasi per subtes, akurasi menurut rentang
keyakinan, skor Brier, akurasi bila jawaban yang paling ragu tidak dihitung,
serta biaya token dan latensinya.

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
