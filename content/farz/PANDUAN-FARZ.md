# Panduan Auto Post Threads FARZ (@farzglobal)

Akaun @farzglobal guna sistem yang sama dengan akaun Threads lain, tapi fail dan token dia berasingan.

## Apa yang dah siap

| Fail | Fungsi |
|---|---|
| `content/farz/posts.json` | 35 post, 5 sehari (7:30 pg, 11:30 pg, 3:00 ptg, 8:00 mlm, 10:30 mlm), 29 Nov hingga 5 Dis, loghat Terengganu |
| `content/farz/images/` | 16 gambar kad FARZ (merah, hitam, putih), selang-seli dengan post teks |
| `content/farz/info.json` | Tempat isi info nanti (tarikh launch, link kedai) |

Konten: loghat Terengganu. Promote brand FARZ (cerita brand, tanya warna/saiz/fit, teaser first drop) campur post random untuk tarik perhatian (sarapang, keropok lekor, musim tengkujuh, cuti Jumaat orang Ganu, tempat lepak). Tiada hashtag. Tiada harga, bahan kain atau tarikh launch direka, sebab belum confirm.

## Langkah 1: Token Threads @farzglobal (10 minit)

Guna app Meta yang sama, **FARZ Auto Post**.

1. Buka https://developers.facebook.com/apps, pilih **FARZ Auto Post**.
2. **App roles > Roles > Add People > Threads Tester**, taip `farzglobal`.
3. Dalam app Threads (login @farzglobal): **Settings > Account > Website permissions > Invites**, tekan **Accept**.
4. Dashboard app: **Use cases > Access the Threads API > Settings > User Token Generator**, tekan **Generate token** untuk farzglobal. Pastikan `threads_basic` dan `threads_content_publish`.
5. Tukar ke token 60 hari, buka dalam browser (ganti 2 bahagian huruf besar):
   `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=APP_SECRET&access_token=TOKEN_TADI`
   (App secret di **App settings > Basic**.) Salin nilai `access_token`.

## Langkah 2: Letak dalam GitHub (2 minit)

1. https://github.com/FARUQI03/auto-post/settings/secrets/actions
2. **New repository secret**: Name `THREADS_FARZ_ACCESS_TOKEN`, Secret = token 60 hari tadi.

Siap. Bagitahu Claude, Claude akan test dan pastikan post keluar.

## Nota

- Post terlepas lebih 6 jam tak disiar (tak keluar bertimbun).
- Token tamat 60 hari. `refresh_tokens.py` boleh panjangkan semua token Threads sekali.
- Nak tukar caption, tambah gambar produk sebenar atau umum tarikh launch: hantar je pada Claude.
