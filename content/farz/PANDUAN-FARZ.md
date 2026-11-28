# Panduan Auto Post Threads FARZ (@farzglobal)

Akaun @farzglobal guna sistem yang sama dengan akaun Threads lain, tapi fail dan token dia berasingan.

## Apa yang dah siap

| Fail | Fungsi |
|---|---|
| `content/farz/posts.json` | 21 post, 3 sehari (9:00 pagi, 2:00 petang, 9:00 malam), 29 Nov hingga 5 Dis |
| `content/farz/images/` | 10 gambar kad FARZ (merah, hitam, putih) untuk post fz-02, 04, 06 ... 20 |
| `content/farz/info.json` | Tempat isi info nanti (tarikh launch, link kedai) |

Konten: bina hype sebelum first drop. Cerita brand, soalan pada follower (warna, saiz, fit), hot take pasal baju, santai hari-hari. Tiada hashtag. Tiada harga, bahan kain atau tarikh launch direka, sebab belum confirm.

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
