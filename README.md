# KUJANGRUN 2026 - Sistem Registrasi Pelari

## Pembuat
Nama: Maman Mulyana
NIM: 25416255201221
Mata Kuliah: Struktur Data

Program registrasi event lari KujangRun 2026. 
**Lebih dari CRUD** - Implementasi 5 Struktur Data sekaligus.

## Fitur & Struktur Data yang Dipakai
1. **CRUD Lengkap** 
   - Create: `registrasi_pelari()` 
   - Read: `cari_by_nik()` menu 2
   - Update: `status_bayar`, `waktu_finish` bisa diupdate via CSV
   - Delete: `hapus_by_nik()` + `undo_registrasi()` menu 4

2. **Linked List** 
   - `class LinkedList` + `class Node`
   - Fungsi: Nyimpen semua data pelari secara dinamis
   - Kelebihan: Tambah/hapus data di head O(1)

3. **Hash Map / Dictionary**
   - `database_pelari = {}`
   - Fungsi: Search data by NIK super cepat O(1)
   - Dipakai di menu 2 "Cari Pelari by NIK"

4. **Queue - Antrian FIFO** 
   - `deque()` untuk `antrian_start_5K`, `antrian_start_10K`, `antrian_start_21K`
   - `waitlist_10K` untuk kuota 10K yg penuh
   - Fungsi: Simulasi antrian start lomba sesuai aturan FIFO

5. **Stack - Tumpukan LIFO**
   - `stack_undo` : Simpen aksi terakhir buat fitur Undo Registrasi menu 4
   - `stack_bib_5K/10K/21K` : Generate nomor BIB otomatis KJR26-5K-001 dst

6. **Sorting Algorithm**
   - Bubble Sort di `sorting_leaderboard()`
   - Fungsi: Urutin pelari dari umur termuda buat leaderboard menu 5

7. **Validasi & File Handling**
   - Validasi: NIK 16 digit, Umur 10-100 + try except, Kategori .strip().upper(), No HP 08...
   - CSV: Auto save/load `pelari.csv` dan `kategori.csv` biar data persistent

## Cara Run
1. Pastikan 3 file ada di 1 folder:
   - `kujangrun.py`
   - `kategori.csv` - auto kebikin kalo dihapus
   - `pelari.csv` - auto kebikin pas daftar pertama
2. Buka terminal di folder itu
3. Ketik: `python kujangrun.py`

## Aturan Kategori & Umur
- 5K  : Umur 10-100 tahun, kapasitas 8000
- 10K : Umur >= 18 tahun, kapasitas 5000. >60 disarankan 5K 
- 21K : Umur >= 18 tahun, kapasitas 2000. <18 ditolak

## Struktur CSV
**kategori.csv**: nama_kategori,jarak_km,kapasitas,harga,terdaftar  
**pelari.csv**: nik,nama,umur,kategori,ukuran_jersey,no_hp,status_bayar,waktu_finish,bib_number
