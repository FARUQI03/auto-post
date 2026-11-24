# Panduan Setup Auto Post Instagram & Threads

Sistem ni siarkan post secara automatik ke Instagram dan Threads ikut jadual yang kau tulis dalam `content/posts.json`. Ia berjalan percuma di GitHub Actions (setiap 30 minit), guna API rasmi Meta. Tak perlu bayar Buffer/Later.

## Isi folder

| Fail | Fungsi |
|---|---|
| `content/posts.json` | Senarai post: caption, hashtag, gambar, masa siar |
| `content/images/` | Letak gambar post di sini (JPG, nisbah 4:5 atau 1:1) |
| `autopost.py` | Skrip yang siarkan post |
| `refresh_tokens.py` | Panjangkan token (buat sebulan sekali) |
| `.github/workflows/autopost.yml` | Jadual automatik setiap jam |
| `state/posted.json` | Rekod post yang dah keluar (jangan edit) |

---

## Langkah 1: Sediakan akaun (5 minit)

1. Tukar Instagram kau kepada **Professional account** (Business atau Creator): Instagram > Settings > Account type and tools > Switch to professional account.
2. Pastikan akaun Threads kau guna Instagram yang sama.

## Langkah 2: Buat Meta App (15 minit)

1. Pergi ke https://developers.facebook.com/apps dan klik **Create App**.
2. Pilih use case **"Manage messaging & content on Instagram"** dan juga **"Access the Threads API"** (boleh tambah kedua-dua dalam satu app, atau buat 2 app berasingan).
3. **Instagram:** dalam bahagian *Instagram > API setup with Instagram login*:
   - Klik **Add account** dan login Instagram kau.
   - Klik **Generate token**. Salin token ini = `IG_ACCESS_TOKEN` (sah 60 hari).
   - Salin juga **Instagram user ID** yang dipaparkan = `IG_USER_ID`.
   - Pastikan permission `instagram_business_basic` dan `instagram_business_content_publish` ada.
4. **Threads:** dalam bahagian *Threads API*:
   - Tambah akaun kau sebagai **Threads Tester** (App roles > Roles), kemudian terima jemputan di Threads app: Settings > Account > Website permissions > Invites.
   - Guna **Graph API Explorer** untuk Threads (atau butang *Generate token* dalam dashboard) dengan permission `threads_basic` dan `threads_content_publish`.
   - Tukar ke long-lived token (60 hari):
     `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=APP_SECRET&access_token=SHORT_TOKEN`
   - Dapatkan user ID: `https://graph.threads.net/v1.0/me?fields=id,username&access_token=TOKEN`
   - Simpan sebagai `THREADS_ACCESS_TOKEN` dan `THREADS_USER_ID`.

> App boleh kekal dalam **Development mode** sebab kau hanya post ke akaun sendiri. Tak perlu App Review.

## Langkah 3: Letak dalam GitHub (10 minit)

1. Buat repo baru di GitHub (contoh `auto-post`). **Mesti public**, sebab Meta perlu muat turun gambar dari URL awam. (Kalau nak private, simpan gambar di tempat lain seperti Cloudinary dan letak URL penuh dalam `images`.)
2. Upload semua fail dalam folder ini ke repo tersebut (termasuk folder `.github`).
3. Pergi **Settings > Secrets and variables > Actions > New repository secret**, tambah 4 secret:
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`
   - `THREADS_USER_ID`
   - `THREADS_ACCESS_TOKEN`
4. Pergi tab **Actions**, enable workflows jika diminta.

> Kalau kau guna Facebook Login (Instagram yang link dengan Facebook Page) dan bukan Instagram Login, tambah variable `IG_API_HOST` = `graph.facebook.com` di tab *Variables*.

## Langkah 4: Uji

1. Tab **Actions > Auto Post IG & Threads > Run workflow**.
2. Tick **Dry run** dan isi `contoh-002` di kotak post id. Semak log, ia patut paparkan caption.
3. Bila yakin, run semula tanpa dry run. `contoh-002` ialah post Threads teks sahaja, jadi paling senang untuk uji pertama.

---

## Cara tambah post baru

Tambah satu blok dalam `content/posts.json`:

```json
{
  "id": "post-010",
  "publish_at": "2026-12-10T09:00:00+08:00",
  "platforms": ["instagram", "threads"],
  "images": ["post-010.jpg"],
  "caption": "Caption utama di sini",
  "hashtags_instagram": ["hashtag1", "hashtag2"],
  "hashtags_threads": ["satutag"]
}
```

Peraturan penting:
- `publish_at` mesti ada `+08:00` (waktu Malaysia).
- **Instagram wajib ada gambar.** Threads boleh teks sahaja.
- 2 hingga 10 gambar = carousel.
- Threads: maksimum 500 aksara, dan hanya 1 hashtag dikira.
- Instagram: maksimum 2,200 aksara, sehingga 30 hashtag (cadangan 5 hingga 10).
- Boleh guna `caption_instagram` dan `caption_threads` untuk caption berbeza ikut platform.
- Post akan keluar dalam masa 30 minit selepas `publish_at` (GitHub Actions kadang lewat 5 hingga 15 minit).

## Penyelenggaraan

- **Setiap 50 hari**, panjangkan token:
  ```
  THREADS_ACCESS_TOKEN=xxx python refresh_tokens.py
  ```
  Untuk token Instagram Login, buka: `https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=TOKEN_LAMA`
  Kemudian kemas kini secret di GitHub.
- Had Meta: 100 post Instagram dan 250 post Threads setiap 24 jam. Lebih dari cukup.
- Kalau post gagal, ia akan dicuba semula setiap 30 minit. Sebab gagal dicatat dalam `state/posted.json`.
