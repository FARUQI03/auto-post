# Panduan Auto Post Threads Vitaliq (akaun kedua)

Akaun Threads Vitaliq berjalan dalam sistem yang sama dengan akaun Threads utama, tapi fail, gambar dan token dia berasingan. Akaun utama tak terusik.

## Apa yang dah siap

| Fail | Fungsi |
|---|---|
| `content/vitaliq/posts.json` | 21 post, 3 sehari (8:30 pagi, 1:00 tengah hari, 9:30 malam), 28 Nov hingga 4 Dis |
| `content/vitaliq/info.json` | Tempat isi **harga** dan **link order** |
| `content/vitaliq/images/` | Tempat gambar (nama fail ikut senarai bawah) |

## Langkah 1: Dapatkan token akaun Threads Vitaliq (10 minit, kau sahaja boleh buat)

Guna app Meta yang sama, **FARZ Auto Post**.

1. Buka https://developers.facebook.com/apps, pilih **FARZ Auto Post**.
2. **App roles > Roles > Add People > Threads Tester**, taip username Threads Vitaliq.
3. Dalam app Threads (login akaun Vitaliq): **Settings > Account > Website permissions > Invites**, tekan **Accept**.
4. Kembali ke dashboard app: **Use cases > Access the Threads API > Settings**. Di bahagian **User Token Generator**, tekan **Generate token** untuk akaun Vitaliq (login Threads Vitaliq bila diminta). Pastikan permission `threads_basic` dan `threads_content_publish`.
5. Tukar ke token 60 hari. Buka link ni dalam browser (ganti 2 bahagian huruf besar):
   `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=APP_SECRET&access_token=TOKEN_TADI`
   (App secret ada di **App settings > Basic**.) Salin nilai `access_token` yang keluar.

## Langkah 2: Letak token dalam GitHub (2 minit)

1. Buka https://github.com/FARUQI03/auto-post/settings/secrets/actions
2. **New repository secret**
   - Name: `THREADS_VITALIQ_ACCESS_TOKEN`
   - Secret: token 60 hari tadi
3. Siap. User ID tak perlu, sistem guna "me" automatik.

Lepas tu bagitahu Claude, Claude akan run ujian dan pastikan post pertama keluar.

## Langkah 3: Bagi harga, link dan gambar

Hantar je kepada Claude dalam chat, Claude akan masukkan ke repo:
- **Harga**, contoh `RM89 sebotol` atau `RM89, beli 2 RM160`
- **Link order**, contoh link WhatsApp `wa.me/60123456789` atau link landing page
- **Gambar** untuk post bertanda gambar (senarai bawah)
- Kalau ada **caption/creative** sendiri, hantar juga, Claude susun masuk jadual

Post yang ada harga/link akan **tunggu** sampai info diisi. Post tanpa gambar akan keluar sebagai **teks sahaja**, jadi jadual tak tersangkut. Post yang terlepas lebih 6 jam tak akan disiar, supaya tak keluar bertimbun serentak.

## Senarai gambar (1080x1350, JPG)

| Fail | Tarikh | Idea gambar |
|---|---|---|
| `vq-02.jpg` | 28 Nov 1:00 tgh | Orang duduk bersila / silang kaki / depan laptop |
| `vq-04.jpg` | 29 Nov 8:30 pg | Kaki atas sejadah, suasana tenang |
| `vq-06.jpg` | 29 Nov 9:30 mlm | Gambar produk Vitaliq, bersih dan jelas |
| `vq-08.jpg` | 30 Nov 1:00 tgh | Kad teks "Bila kebas perlu jumpa doktor" |
| `vq-10.jpg` | 1 Dis 8:30 pg | Kalendar Disember / suasana pagi |
| `vq-12.jpg` | 1 Dis 9:30 mlm | Produk Vitaliq + harga |
| `vq-14.jpg` | 2 Dis 1:00 tgh | Orang regang tangan di meja office |
| `vq-16.jpg` | 3 Dis 8:30 pg | Anak pegang tangan mak/ayah |
| `vq-18.jpg` | 3 Dis 9:30 mlm | Produk Vitaliq / tangkap layar review sebenar customer (dengan izin) |
| `vq-20.jpg` | 4 Dis 1:00 tgh | Produk Vitaliq dalam suasana rumah |

## Peraturan kandungan kesihatan (penting, elak kena flag Meta / KKM)

- Jangan guna perkataan **sembuh, ubat, rawat, merawat, hilang terus, 100% berkesan, jaminan**.
- Sebut **suplemen**, **bantu jaga**, **pengalaman**, dan nasihat jumpa doktor bila kebas teruk.
- Testimoni mesti **sebenar** (screenshot customer dengan izin). Jangan reka testimoni.
- Kalau produk ada nombor **MAL / KKM** atau **halal**, boleh sebut, ia bantu kepercayaan.

## Token tamat 60 hari

Setiap ~50 hari, panjangkan token (dua-dua akaun sekali):
```
THREADS_ACCESS_TOKEN=xxx THREADS_VITALIQ_ACCESS_TOKEN=yyy python refresh_tokens.py
```
Atau minta Claude ingatkan, kemudian kemas kini secret di GitHub.
