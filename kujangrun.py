import csv
from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def cari_by_nik(self, nik):
        current = self.head
        while current:
            if current.data['nik'] == nik:
                return current.data
            current = current.next
        return None

    def hapus_by_nik(self, nik):
        current = self.head
        prev = None
        while current:
            if current.data['nik'] == nik:
                if prev: prev.next = current.next
                else: self.head = current.next
                return current.data
            prev, current = current, current.next
        return None

    def tampilkan_semua(self):
        data_list = []
        current = self.head
        while current:
            data_list.append(current.data)
            current = current.next
        return data_list


antrian_start_5K = deque()
antrian_start_10K = deque()
antrian_start_21K = deque()
waitlist_10K = deque()

database_pelari = {}

stack_undo = []
stack_bib_5K = deque([f"KJR26-5K-{i:03d}" for i in range(1, 8001)])
stack_bib_10K = deque([f"KJR26-10K-{i:03d}" for i in range(1, 5001)])
stack_bib_21K = deque([f"KJR26-21K-{i:03d}" for i in range(1, 2001)])


def cek_kategori_umur(umur, kategori):
    if kategori == "21K" and umur < 18:
        return False, "Umur <18 tahun tidak boleh ikut Half Marathon 21K"
    if umur > 60 and kategori!= "5K":
        return True, "Saran: Masuk kategori Master 5K lebih aman"
    return True, "Valid"

def generate_bib(kategori):
    if kategori == "5K" and stack_bib_5K: return stack_bib_5K.popleft()
    if kategori == "10K" and stack_bib_10K: return stack_bib_10K.popleft()
    if kategori == "21K" and stack_bib_21K: return stack_bib_21K.popleft()
    return None

def registrasi_pelari(db_list, kategori_data):
   
    while True:
        nik = input("NIK: 16 digit ").strip()
        if len(nik) == 16 and nik.isdigit():
            if nik in database_pelari:
                print("NIK sudah terdaftar!")
                return
            break
        else:
            print("NIK harus 16 digit angka!")

    nama = input("Nama: ").strip()
    if nama == "":
        print("Nama tidak boleh kosong!")
        return

    
    while True:
        try:
            umur = int(input("Umur: ").strip())
            if umur < 10 or umur > 100:
                print("Umur tidak realistis! 10-100 tahun")
                continue
            break
        except ValueError:
            print("Umur harus angka! Contoh: 21")

   
    while True:
        kategori = input("Kategori 5K/10K/21K: ").upper().strip() # <--.strip() di sini
        if kategori in kategori_data:
            break
        else:
            print(f"Kategori salah! Pilihan: {list(kategori_data.keys())}")

    jersey = input("Ukuran Jersey S/M/L/XL: ").upper().strip()

   
    while True:
        no_hp = input("No HP: 08... ").strip()
        if not no_hp.startswith('08'):
            print("No HP harus diawali 08!")
        elif len(no_hp) < 10 or len(no_hp) > 13:
            print("No HP harus 10-13 digit!")
        elif not no_hp.isdigit():
            print("No HP cuma boleh angka, jangan ada spasi/titik/-")
        else:
            break

   
    valid, pesan = cek_kategori_umur(umur, kategori)
    print(pesan)
    if not valid: return


    if kategori_data[kategori]['terdaftar'] >= kategori_data[kategori]['kapasitas']:
        if kategori == "10K":
            waitlist_10K.append({'nik': nik, 'nama': nama})
            print(f"Kuota 10K penuh! Kamu masuk waitlist antrian ke-{len(waitlist_10K)}")
            return
        else:
            print("Kuota penuh!")
            return

    # Generate BIB
    bib = generate_bib(kategori)
    if not bib:
        print("BIB habis!")
        return

    data_pelari = {
        'nik': nik, 'nama': nama, 'umur': umur, 'kategori': kategori,
        'ukuran_jersey': jersey, 'no_hp': no_hp,
        'status_bayar': 'Belum', 'waktu_finish': '-', 'bib_number': bib
    }

    db_list.tambah(data_pelari)
    database_pelari[nik] = data_pelari
    stack_undo.append(('tambah', nik))

    if kategori == "5K": antrian_start_5K.append(nik)
    elif kategori == "10K": antrian_start_10K.append(nik)
    else: antrian_start_21K.append(nik)

    kategori_data[kategori]['terdaftar'] += 1
    simpan_csv(db_list, kategori_data)
    print(f"Registrasi berhasil! BIB kamu: {bib}")

def undo_registrasi(db_list):
    if not stack_undo:
        print("Tidak ada aksi untuk di-undo")
        return
    aksi, nik = stack_undo.pop()
    if aksi == 'tambah':
        data = db_list.hapus_by_nik(nik)
        if data:
            del database_pelari[nik]
            print(f"Registrasi {data['nama']} berhasil di-undo")
            simpan_csv(db_list, load_kategori())

def sorting_leaderboard(db_list):
    data = db_list.tampilkan_semua()
    if not data:
        print("Belum ada data pelari")
        return
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if int(data[j]['umur']) > int(data[j+1]['umur']):
                data[j], data[j+1] = data[j+1], data[j]
    print("\n=== Leaderboard by Umur Termuda ===")
    for d in data[:10]:
        print(f"{d['nama']} - {d['umur']} tahun - {d['kategori']} - BIB {d['bib_number']}")

def simpan_csv(db_list, kategori_data):
    with open('pelari.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nik','nama','umur','kategori','ukuran_jersey','no_hp','status_bayar','waktu_finish','bib_number'])
        writer.writeheader()
        for d in db_list.tampilkan_semua():
            writer.writerow(d)
    with open('kategori.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nama_kategori','jarak_km','kapasitas','harga','terdaftar'])
        writer.writeheader()
        for k, v in kategori_data.items():
            writer.writerow({'nama_kategori': k, **v})

def load_kategori():
    data = {}
    try:
        with open('kategori.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Anti spasi di key CSV juga
                key = row['nama_kategori'].strip()
                row['kapasitas'] = int(row['kapasitas'])
                row['terdaftar'] = int(row['terdaftar'])
                row['harga'] = int(row['harga'])
                row['jarak_km'] = int(row['jarak_km'])
                data[key] = row
    except FileNotFoundError:
        print("File kategori.csv tidak ditemukan. Dibuat otomatis...")
        data = {'5K':{'jarak_km':5,'kapasitas':8000,'harga':150000,'terdaftar':0},
                '10K':{'jarak_km':10,'kapasitas':5000,'harga':250000,'terdaftar':0},
                '21K':{'jarak_km':21,'kapasitas':2000,'harga':400000,'terdaftar':0}}
        simpan_csv(LinkedList(), data)
    return data

# ===== MENU UTAMA =====
def main():
    db = LinkedList()
    kategori = load_kategori()

    while True:
        print("\n=== KUJANGRUN 2026 ===")
        print("1. Registrasi Pelari [CRUD+Validasi+BIB+Queue]")
        print("2. Cari Pelari by NIK [Hash Map - O(1)]")
        print("3. Tampilkan Antrian Start 10K [Queue]")
        print("4. Undo Registrasi Terakhir [Stack]")
        print("5. Leaderboard by Umur [Sorting]")
        print("6. Lihat Waitlist 10K [Queue Tambahan]")
        print("7. Keluar")

        pilih = input("Pilih: ").strip()
        if pilih == '1': registrasi_pelari(db, kategori)
        elif pilih == '2':
            nik = input("Masukkan NIK: ").strip()
            hasil = database_pelari.get(nik)
            print(hasil if hasil else "Data tidak ditemukan")
        elif pilih == '3': print("Antrian 10K:", list(antrian_start_10K)[:10])
        elif pilih == '4': undo_registrasi(db)
        elif pilih == '5': sorting_leaderboard(db)
        elif pilih == '6': print("Waitlist 10K:", list(waitlist_10K))
        elif pilih == '7':
            print("Makasih udah daftar KujangRun 2026!")
            break
        else: print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()