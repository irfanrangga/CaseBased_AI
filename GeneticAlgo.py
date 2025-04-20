import math
import random

# Konstanta
population_size = 50
panjang_kromosom = 10
batasan_x1 = (-10, 10)
batasan_x2 = (-10, 10)
bitx = panjang_kromosom // 2
pc = 0.9  # Probabilitas crossover
pm = 0.5  # Probabilitas mutasi
x1Min, x1Max = batasan_x1
x2Min, x2Max = batasan_x2

# Fungsi untuk inisialisasi populasi awal menggunakan representasi biner
def inisialisasi_populasi():
    return [[random.randint(0, 1) for _ in range(panjang_kromosom)]
             for _ in range(population_size)]

def decode(kromosom):
    krom = ''.join(str(bit) for bit in kromosom)
    # Mengambil 5 bit pertama dan 5 bit kedua dari kromosom
    biner_x1 = ''.join(str(bit) for bit in kromosom[:bitx])
    biner_x2 = ''.join(str(bit) for bit in kromosom[bitx:]) 

    desimal_x1 = int(biner_x1, 2) # konversi biner ke desimal
    desimal_x2 = int(biner_x2, 2)

    x1 = x1Min + (x1Max - x1Min) * desimal_x1 / (2**bitx - 1) 
    x2 = x2Min + (x2Max - x2Min) * desimal_x2 / (2**bitx - 1)
    return x1, x2

def fitness(kromosom):
    x1, x2 = decode(kromosom)
    # Memeriksa apakah x1 dan x2 berada dalam batasan yang ditentukan
    if x1 < x1Min or x1 > x1Max or x2 < x2Min or x2 > x2Max:
        return float('inf')  # Fitness tidak valid di luar batasan
    else:
        # Fungsi fitness yang diberikan
        eqt = math.sin(x1) * math.cos(x2) * math.tan(x1+x2) + (3/4) * math.exp(1-(math.sqrt(x1**2)))
    return -eqt

def crossover(kromosom1, kromosom2):
    # Melakukan crossover satu titik
    if random.random() > pc:
        return kromosom1, kromosom2  # Tidak melakukan crossover
    else:
        # Memilih titik crossover secara acak
        titik_crossover = random.randint(1, panjang_kromosom - 1)
        anak1 = kromosom1[:titik_crossover] + kromosom2[titik_crossover:]
        anak2 = kromosom2[:titik_crossover] + kromosom1[titik_crossover:]
    return anak1, anak2

def mutasi(kromosom, probabilitas_mutasi=pm):
    # Melakukan mutasi pada kromosom
    for i in range(len(kromosom)):
        if random.random() < probabilitas_mutasi:
            kromosom[i] = 1 - kromosom[i]  # Mengubah 0 menjadi 1 dan sebaliknya
    return kromosom

# def seleksi(populasi):
#     # Menggunakan metode turnamen untuk seleksi
#     turnamen_size = 2
#     turnamen = random.sample(populasi, turnamen_size)
#     pemenang = min(turnamen, key=fitness)  # Memilih kromosom dengan fitness terbaik
#     return pemenang

# Fungsi untuk memilih orang tua (ortu) untuk crossover dengan roulette wheel selection
def pemilihan_ortu(populasi):
    ortu_1 = random.choice(populasi)
    ortu_2 = random.choice(populasi)
    if fitness(ortu_1) < fitness(ortu_2):
        return ortu_1
    else:
        return ortu_2
    
def evolusi(generasi=100):
    pop = inisialisasi_populasi()
    for g in range(generasi):
        pop_baru = []
        while len(pop_baru) < population_size:
            ortu1 = pemilihan_ortu(pop)
            ortu2 = pemilihan_ortu(pop)
            anak1, anak2 = crossover(ortu1, ortu2)
            anak1 = mutasi(anak1)
            anak2 = mutasi(anak2)
            pop_baru.extend([anak1, anak2])
        pop = pop_baru[:population_size]
        
        terbaik = min(pop, key=fitness)
        x1, x2 = decode(terbaik)
        print(f"Generasi {g+1}: Fitness terbaik = {fitness(terbaik):.6f}, x1 = {x1:.4f}, x2 = {x2:.4f}")
    
    return min(pop, key=fitness)

def main(jumlah_generasi):
    populasi = inisialisasi_populasi()

    # Header tabel
    print(f"{'Generasi':>8} || {'Fitness':>9} || {'Kromosom':10} || {'x1':7} || {'x2':7}")    
    for generasi in range(jumlah_generasi):
        populasi_baru = []

        while len(populasi_baru) < population_size:
            # Seleksi orang tua
            ortu1 = pemilihan_ortu(populasi)
            ortu2 = pemilihan_ortu(populasi)

            # Crossover
            anak1, anak2 = crossover(ortu1[:], ortu2[:])  # copy agar tidak berubah

            # Mutasi
            anak1 = mutasi(anak1)
            anak2 = mutasi(anak2)

            populasi_baru.extend([anak1, anak2])

        # Update populasi
        populasi = populasi_baru[:population_size]

        # Cari kromosom terbaik di generasi ini
        kromosom_terbaik = min(populasi, key=fitness)
        kromosom_string = ''.join(str(bit) for bit in kromosom_terbaik)
        terbaik = min(populasi, key=fitness)
        x1, x2 = decode(terbaik)
        nilai_fitness = fitness(terbaik)

        # Tampilkan hasil generasi
        print(f"{generasi+1:>8} || {nilai_fitness:.6f} || {kromosom_string} || {x1:7.4f} || {x2:7.4f}")


main(10)