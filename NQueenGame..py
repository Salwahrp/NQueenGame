import random
from pprint import pprint

def input_size_papan():
    ''' Mengambil input dari pengguna untuk ukuran papan '''
    n = input("Masukkan bilangan bulat (jumlah ratu): ")
    return int(n)

def print_papan(papan, n):
    ''' Fungsi pembantu untuk mencetak papan '''
    print('Papan:')
    for i in range(len(papan)):
        if(str(papan[i]) == "1"):
            print("[ " + str(papan[i]) + " ]" + ' ', end='')
        elif(str(papan[i]) == "0"):
            print("[   ]" + ' ', end='')
        if (i + 1) % n == 0:
            print("")
    print('Nilai H: ', determine_h_cost(papan, n))
    print('---------------------')

def generate_random_papan(n):
    ''' Menghasilkan papan acak untuk inisialisasi, ratu ditempatkan per baris '''
    generated_papan = []
    for i in range(n):
        j = random.randint(0, n - 1)
        baris = [0] * n
        baris[j] = 1
        generated_papan.extend(baris)
    return generated_papan

def find_tabrakan(papan, n):
    ''' Fungsi pembantu untuk menghitung tabrakan posisi ratu '''
    tabrakan = 0
    pasangan_tabrakan = []
    max_index = len(papan)
    for i in range(max_index):
        # Untuk setiap ratu di papan, hitung tabrakan dengan ratu lain, dan jenis tabrakan yang terjadi
        if papan[i] == 1:
            for x in range(1, n):
                # memeriksa di atas indeks saat ini
                if (i - n * x >= 0):
                    atas = i - n * x
                    # arah atas
                    if (papan[atas] == 1):
                        tabrakan += 1
                        pasangan_tabrakan.append('atas: ' + str(i) + ' dan ' + str(atas))
                    # arah kiri_atas
                    if (int((atas - x) / n) == int(atas / n)) and (atas - x) >= 0:
                        kiri_atas = atas - x
                        if (papan[kiri_atas] == 1):
                            tabrakan += 1
                            pasangan_tabrakan.append('kiri_atas: ' + str(i) + ' dan ' + str(kiri_atas))
                    # arah kanan_atas
                    if (int((atas + x) / n) == int(atas / n)):
                        kanan_atas = atas + x
                        if (papan[kanan_atas] == 1):
                            tabrakan += 1
                            pasangan_tabrakan.append('kanan_atas: ' + str(i) + ' dan ' + str(kanan_atas))
                # memeriksa di bawah indeks saat ini
                if (i + n * x < max_index):
                    bawah = i + n * x
                    # arah bawah
                    if (papan[bawah] == 1):
                        tabrakan += 1
                        pasangan_tabrakan.append('bawah: ' + str(i) + ' dan ' + str(bawah))
                    # arah kiri_bawah
                    if (int((bawah - x) / n) == int(bawah / n)):
                        kiri_bawah = bawah - x
                        if (papan[kiri_bawah] == 1):
                            tabrakan += 1
                            pasangan_tabrakan.append('kiri_bawah: ' + str(i) + ' dan ' + str(kiri_bawah))
                    # arah kanan_bawah
                    if (int((bawah + x) / n) == int(bawah / n)) and ((bawah + x) < max_index):
                        kanan_bawah = bawah + x
                        if (papan[kanan_bawah] == 1):
                            tabrakan += 1
                            pasangan_tabrakan.append('kanan_bawah: ' + str(i) + ' dan ' + str(kanan_bawah))
                # arah kiri (untuk kelengkapan)
                if (int((i - x) / n) == int(i / n)) and (i - x >= 0):
                    kiri = i - x
                    if (papan[kiri] == 1):
                        tabrakan += 1
                        pasangan_tabrakan.append('kiri: ' + str(i) + ' dan ' + str(kiri))
                # arah kanan (untuk kelengkapan)
                if (int((i + x) / n) == int(i / n)) and (i + x < max_index):
                    kanan = i + x
                    if (papan[kanan] == 1):
                        tabrakan += 1
                        pasangan_tabrakan.append('kanan: ' + str(i) + ' dan ' + str(kanan))
    return [tabrakan, pasangan_tabrakan]

def determine_h_cost(papan, n, verbose=False):
    ''' Fungsi untuk menentukan heuristik - total tabrakan pada papan '''
    tabrakan, pasangan_tabrakan = find_tabrakan(papan, n)
    if verbose:
        pprint(pasangan_tabrakan)
        
    # mengembalikan setengah dari jumlah tabrakan, karena setiap posisi tabrakan dihitung dua kali oleh helper function
    return int(tabrakan / 2)

def find_child(papan, n, sideways_move=False):
    ''' Fungsi untuk menemukan penerus dari semua kemungkinan perubahan posisi ratu dengan membandingkan nilai heuristiknya dengan pergerakan ratu per baris '''
    child = []
    current_h_cost = determine_h_cost(papan, n)
    same_cost_children = []

    for baris in range(n):
        for kolom in range(n):
            # Membangun papan sementara yang mengubah posisi ratu pada papan saat ini
            temp_papan = []
            temp_papan.extend(papan[:baris * n])
            baris_baru = [0] * n
            baris_baru[kolom] = 1
            temp_papan.extend(baris_baru)
            temp_papan.extend(papan[(baris + 1) * n:])
            temp_h_cost = determine_h_cost(temp_papan, n)
            if (sideways_move):
                # jika pergerakan menyamping diizinkan, dan biaya heuristik penerus yang dihasilkan lebih rendah atau sama dengan biaya heuristik saat ini, simpan penerus yang dihasilkan dan perbarui biaya heuristik saat ini
                if (temp_papan != papan):
                    if (temp_h_cost < current_h_cost):
                        child = temp_papan.copy()
                        current_h_cost = temp_h_cost
                    elif (temp_h_cost == current_h_cost):
                        same_cost_children.append(temp_papan)
                        x = random.randint(0, len(same_cost_children) - 1)
                        child = same_cost_children[x]
            else:
                # jika pergerakan menyamping tidak diizinkan, dan biaya heuristik penerus yang dihasilkan lebih rendah dari biaya heuristik saat ini, simpan penerus yang dihasilkan dan perbarui biaya heuristik saat ini
                if (temp_papan != papan) and (temp_h_cost < current_h_cost):
                    child = temp_papan.copy()
                    current_h_cost = temp_h_cost
    return child

def steepest_hill_climbing(papan, n, max_iterations=1000, verbose=False):
    ''' Algoritma Steepest Hill Climbing, mengembalikan langkah-langkah saat ini dan apakah hasilnya berhasil atau tidak '''
    steps = 0
    success = False
    current_papan = papan.copy()

    if (verbose):
        print_papan(current_papan, n)

    # Sampai iterasi maksimum tercapai, cari solusi
    for i in range(max_iterations):
        # Dapatkan penerus heuristik terbaik dari fungsi pembantu find_child
        next_node = find_child(current_papan, n).copy()

        if (verbose and len(next_node) != 0):
            print_papan(next_node, n)

        # Perbarui jumlah langkah yang diambil untuk eksekusi ini
        steps += 1
        # Jika ada penerus dan biaya heuristiknya nol, maka solusi sudah ditemukan
        if (len(next_node) != 0) and (determine_h_cost(next_node, n) == 0):
            success = True
            break
        # Jika tidak ada penerus yang dihasilkan, solusi tidak dapat ditemukan
        if (len(next_node) == 0):
            break
        # Jadikan penerus saat ini sebagai node berikutnya
        current_papan = next_node.copy()
    return steps, success

n = input_size_papan()
iterations = 1000

# Skrip untuk menjalankan fungsi-fungsi
print('Steepest Hill Climbing:')
success_rate_steepest_hill_climbing = False
for i in range(iterations):
    print('\nJumlah iterasi ' + str(i + 1) + ':')
    step_count, success = steepest_hill_climbing(generate_random_papan(n), n, verbose=True)
    if (success):
        print('Berhasil.')
        print('Jumlah langkah adalah: ' + str(step_count))
        break;
    else:
        print('Gagal.')
        print('Jumlah langkah adalah: ' + str(step_count))