import math
import random

# Operator Evolusi
population_size = 50
panjang_kromosom = 8
batasan_x1 = (-10, 10)
batasan_x2 = (-10, 10)
x1Min, x1Max = batasan_x1
x2Min, x2Max = batasan_x2
bitx = panjang_kromosom // 2 # Jumlah bit untuk x1 dan x2
pc = 0.8  # Probabilitas crossover
pm = 0.1  # Probabilitas mutasi

# Fungsi untuk inisialisasi populasi awal menggunakan representasi biner
def inisialisasi_populasi():
    return [[random.randint(0, 1) for _ in range(panjang_kromosom)]
             for _ in range(population_size)]

def decode(kromosom):
    # Mengambil 4 bit pertama dan 4 bit kedua dari kromosom
    biner_x1 = ''.join(str(bit) for bit in kromosom[:bitx])
    biner_x2 = ''.join(str(bit) for bit in kromosom[bitx:]) 

    desimal_x1 = int(biner_x1, 2) # konversi biner ke desimal
    desimal_x2 = int(biner_x2, 2)

    # Menghitung nilai x1 dan x2 berdasarkan rentang yang ditentukan
    x1 = x1Min + (x1Max - x1Min) * desimal_x1 / (2**bitx - 1) 
    x2 = x2Min + (x2Max - x2Min) * desimal_x2 / (2**bitx - 1)
    return x1, x2

def fitness(kromosom):
    x1, x2 = decode(kromosom)
    # Memeriksa apakah x1 dan x2 berada dalam batasan yang ditentukan
    if x1 < x1Min or x1 > x1Max or x2 < x2Min or x2 > x2Max:
        return float('inf')  # Fitness tidak valid di luar batasan
    else:
        # Fungsi objektif yang diberikan
        eqt = -(math.sin(x1) * math.cos(x2) * math.tan(x1+x2) + (3/4) * math.exp(1 - math.sqrt(x1**2)))
    return eqt

def seleksiOrangtua(populasi):
    # Menggunakan metode turnamen untuk seleksi orangtua
    turnamen_size = 5
    turnamen = random.sample(populasi, turnamen_size)
    pemenang = min(turnamen, key=fitness)  # Memilih kromosom dengan fitness minimum
    return pemenang

def crossover(ortu1, ortu2):
    # Melakukan crossover satu titik pada kromosom
    if random.random() < pc:
        point = random.randint(1, panjang_kromosom - 1)
        # print(f"  > Crossover pada titik ke-{point}")
        anak1 = ortu1[:point] + ortu2[point:]
        anak2 = ortu2[:point] + ortu1[point:]
    else:
        anak1, anak2 = ortu1, ortu2  # Tidak terjadi crossover
    return anak1, anak2

def mutasi(kromosom, mutation_rate=pm):
    # Melakukan mutasi pada kromosom
    for i in range(len(kromosom)):
        if random.random() < mutation_rate:
            kromosom[i] = 1 - kromosom[i]  # Mengubah 0 menjadi 1 dan sebaliknya
    return kromosom

def seleksiSurvivor(populasi_lama, populasi_baru):
    elit = min(populasi_lama, key=fitness)  # Ambil individu terbaik dari generasi sebelumnya
    populasi_baru.append(elit)              # Tambahkan ke populasi baru
    populasi_baru = sorted(populasi_baru, key=fitness)[:population_size]  # Seleksi agar jumlah tetap
    return populasi_baru


def evolusi(generasi):
    populasi = inisialisasi_populasi()
    #print("\n=== Proses Evolusi ===")
    for g in range(generasi):
        i = 1
        populasi_baru = []        
        while len(populasi_baru) < population_size:
            ortu1 = seleksiOrangtua(populasi)
            ortu2 = seleksiOrangtua(populasi)
            anak1, anak2 = crossover(ortu1, ortu2)
            anak1 = mutasi(anak1)
            anak2 = mutasi(anak2)
            populasi_baru.extend([anak1, anak2])
            i += 1
        populasi = seleksiSurvivor(populasi, populasi_baru)        
        # Evaluasi kromosom terbaik di generasi ini
        kromosom_terbaik = min(populasi, key=fitness)
        x1, x2 = decode(kromosom_terbaik)
        nilai_fitness = fitness(kromosom_terbaik)
    # Hasil akhir setelah semua generasi dieksekusi
    print(f"\n=== Hasil Akhir ===")
    print(f"Kromosom Terbaik: {''.join(map(str, kromosom_terbaik))}")
    print(f"x1 = {x1:.3f}, x2 = {x2:.3f}, fitness = {nilai_fitness:.4f}")

evolusi(100)