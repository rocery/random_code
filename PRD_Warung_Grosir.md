# Product Requirements Document (PRD)
## Aplikasi Web Pemesanan Warung Grosir

**Versi:** 1.0  
**Tanggal:** 2025-08-19  
**Status:** Draft

---

## 1. Overview

Aplikasi web yang memungkinkan pembeli memilih produk dari warung grosir, memasukkannya ke keranjang, lalu melakukan checkout melalui WhatsApp ke admin warung. Pemilik warung dapat mengelola semua produk dan warung melalui satu akun admin.

---

## 2. Tujuan Produk

- Mempermudah pembeli dalam memilih dan memesan produk grosir secara online
- Mengotomatisasi proses pengiriman pesanan ke WhatsApp admin
- Memudahkan pemilik dalam mengelola 3 warung dari satu dashboard

---

## 3. Target Pengguna

| Role | Deskripsi |
|------|-----------|
| **Pembeli** | Pelanggan yang mengakses website untuk memilih dan memesan produk |
| **Admin / Pemilik** | Pemilik 3 warung yang mengelola produk, stok, dan pengaturan warung |

---

## 4. Fitur Utama

### 4.1 Halaman Publik (Pembeli)

#### 4.1.1 Pemilihan Warung
- Pembeli memilih warung yang ingin dipesan dari daftar warung yang aktif
- Hanya warung yang diaktifkan oleh admin yang tampil
- Jika hanya 1 warung yang aktif, langsung diarahkan ke halaman produk warung tersebut

#### 4.1.2 Halaman Produk
- Menampilkan daftar produk yang tersedia dari warung yang dipilih
- Setiap produk menampilkan:
  - Nama produk
  - Foto produk (jika ada)
  - Harga satuan
  - Satuan (kg, pcs, dus, dll)
  - Tag
  - Status: Tersedia / Habis
- Pembeli dapat filter produk berdasarkan tag
- Pembeli dapat mencari produk berdasarkan nama
- Produk yang berstatus "Habis" atau "Nonaktif" tidak bisa ditambahkan ke keranjang
- Pembeli dapat mengatur jumlah (qty) produk yang ingin dibeli, maksimal sesuai stok yang diset admin
- Tombol "Tambah ke Keranjang"

#### 4.1.3 Keranjang Belanja
- Menampilkan daftar produk yang dipilih beserta qty dan subtotal
- Pembeli dapat mengubah qty atau menghapus item
- Menampilkan total harga keseluruhan
- Form input nomor telepon pembeli (wajib diisi sebelum checkout)
- Tombol "Checkout via WhatsApp"

#### 4.1.4 Checkout via WhatsApp
- Saat checkout, sistem membuat pesan WhatsApp otomatis berisi:
  ```
  Halo Admin [Nama Warung], saya ingin memesan:

  1. [Nama Produk A] x [Qty] = Rp [Subtotal]
  2. [Nama Produk B] x [Qty] = Rp [Subtotal]
  ...

  Total: Rp [Total]
  No. Telepon Saya: [Nomor Pembeli]
  ```
- Pembeli diarahkan ke WhatsApp Web / App dengan nomor admin warung yang dipilih dan pesan sudah terisi otomatis

---

### 4.2 Dashboard Admin (Pemilik)

#### 4.2.1 Autentikasi
- Login dengan email dan password
- Satu akun untuk mengelola semua 3 warung
- Logout

#### 4.2.2 Manajemen Warung
- Melihat daftar warung miliknya
- Mengaktifkan / menonaktifkan warung (toggle)
- Bisa mengaktifkan lebih dari 1 warung sekaligus, atau hanya 1 saja
- Edit informasi warung: nama, nomor WhatsApp admin, deskripsi singkat

#### 4.2.3 Manajemen Produk (per Warung)
- Melihat daftar semua produk di warung tertentu
- **Tambah produk** dengan field:
  - Nama produk
  - Foto (upload gambar, opsional)
  - Harga satuan (wajib)
  - Satuan (wajib: kg, pcs, dus, lusin, dll)
  - Stok maksimal (wajib; pembeli tidak bisa memesan melebihi angka ini)
  - Tag (pilih dari tag yang sudah ada atau buat baru)
  - Urutan tampil (angka; diatur manual)
  - Status awal (Aktif / Nonaktif)
- **Edit produk**: mengubah semua field produk
- **Hapus produk**: menghapus permanen
- **Nonaktifkan produk**: produk tidak tampil di halaman publik
- **Tandai Habis**: produk tetap tampil tapi dengan label "Habis" dan tidak bisa dipesan
- Filter/cari produk berdasarkan nama, status, atau tag
- Drag-and-drop atau input angka untuk mengatur urutan tampil produk

#### 4.2.4 Manajemen Tag (per Warung)
- Melihat daftar tag yang ada
- Tambah tag baru
- Edit nama tag
- Hapus tag (produk yang menggunakan tag tersebut tidak terhapus, hanya tag-nya yang dilepas)

---

## 5. User Flow

### Pembeli
```
Buka Website
    → Pilih Warung (jika >1 aktif)
    → Lihat Daftar Produk
    → Pilih Produk + Qty → Tambah ke Keranjang
    → Buka Keranjang
    → Isi Nomor Telepon
    → Klik Checkout
    → Diarahkan ke WhatsApp Admin dengan pesan otomatis
```

### Admin
```
Login
    → Dashboard
    → Pilih Warung → Kelola Produk (CRUD, status)
    → Pengaturan Warung (aktifkan/nonaktifkan, edit info WA)
    → Logout
```

---

## 6. Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Framework** | Next.js (App Router) |
| **UI Component** | Shadcn/ui + Tailwind CSS |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Supabase Auth |
| **Storage** | Supabase Storage (foto produk) |
| **Hosting** | Vercel |

---

## 7. Persyaratan Non-Fungsional

| Aspek | Persyaratan |
|-------|-------------|
| **Platform** | Website, responsive (mobile-first) |
| **Browser** | Chrome, Safari, Firefox (mobile & desktop) |
| **Performa** | Halaman produk load < 3 detik |
| **WhatsApp** | Menggunakan wa.me link dengan pesan pre-filled |
| **Keamanan** | Halaman admin hanya bisa diakses setelah login |

---

## 8. Data Model (Ringkasan)

### Warung
- id, nama, deskripsi, nomor_whatsapp, status_aktif, foto_logo

### Produk
- id, warung_id, nama, foto (opsional), harga (wajib), satuan (wajib), stok_maksimal, status (aktif / nonaktif / habis), urutan_tampil, tags (array)

### Tag
- id, warung_id, nama_tag

### Admin
- id, email, password_hash, nama

---

## 9. Out of Scope (Tidak Termasuk v1)

- Sistem pembayaran online
- Riwayat pesanan / order history
- Notifikasi push / email
- Fitur pencarian warung berdasarkan lokasi
- Multi-admin per warung
- Rating / ulasan produk
- Laporan penjualan

---

## 10. Keputusan Desain

- **Stok maksimal dikelola manual oleh admin.** Karena checkout hanya via WhatsApp dan sistem tidak dapat memverifikasi apakah pesanan benar-benar terjadi, admin bertanggung jawab mengupdate stok secara manual dari dashboard.
