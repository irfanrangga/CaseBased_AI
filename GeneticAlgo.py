import math
import random

# Konstanta
population_size = 10
panjang_kromosom = 8
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

def crossover(ortu1, ortu2):
    # Melakukan crossover satu titik pada kromosom
    if random.random() < pc:
        point = random.randint(1, panjang_kromosom - 1)
        print(f"  > Crossover pada titik ke-{point}")
        anak1 = ortu1[:point] + ortu2[point:]
        anak2 = ortu2[:point] + ortu1[point:]
    else:
        anak1, anak2 = ortu1, ortu2  # Tidak ada crossover, anak sama dengan ortu
    return anak1, anak2

def mutasi(kromosom, probabilitas_mutasi=pm):
    # Melakukan mutasi pada kromosom
    for i in range(len(kromosom)):
        if random.random() < probabilitas_mutasi:
            kromosom[i] = 1 - kromosom[i]  # Mengubah 0 menjadi 1 dan sebaliknya
    return kromosom

def seleksi(populasi):
    # Menggunakan metode turnamen untuk seleksi
    turnamen_size = 2
    turnamen = random.sample(populasi, turnamen_size)
    pemenang = min(turnamen, key=fitness)  # Memilih kromosom dengan fitness terbaik
    return pemenang

def evolusi(generasi):
    pop = inisialisasi_populasi()
    
    print("\n=== Populasi Awal ===")
    for i, krom in enumerate(pop):
        x1, x2 = decode(krom)
        fit = fitness(krom)
        print(f"Individu-{i+1}: {''.join(map(str,krom))} -> x1 = {x1:.4f}, x2 = {x2:.4f}, fitness = {fit:.6f}")
    
    print("\n=== Proses Evolusi ===")
    
    for g in range(generasi):
        i = 1
        pop_baru = []
        
        print(f"\n-- Generasi {g+1} --")
        
        while len(pop_baru) < population_size:
            ortu1 = seleksi(pop)
            ortu2 = seleksi(pop)
            print(f"Seleksi ke-{i}")
            print(f"Ortu 1: {''.join(map(str,ortu1))}, Ortu 2: {''.join(map(str,ortu2))}")

            anak1, anak2 = crossover(ortu1, ortu2)
            print(f"  > Crossover hasil: ")
            print(f"    Anak1: {''.join(map(str, anak1))}, Anak2: {''.join(map(str, anak2))}")

            anak1 = mutasi(anak1)
            anak2 = mutasi(anak2)
            print(f"  > Setelah mutasi: ")
            print(f"    Anak1: {''.join(map(str, anak1))}, Anak2: {''.join(map(str, anak2))}")
            print()

            pop_baru.extend([anak1, anak2])
            i += 1

        elit = min(pop, key=fitness)
        pop_baru.append(elit)
        print(f"  > Kromosom terbaik saat ini: {''.join(map(str, elit))}")
        # Ganti populasi lama dengan populasi baru (batas 10)
        pop = pop_baru[:population_size]
        
        # Evaluasi kromosom terbaik di generasi ini
        kromosom_terbaik = min(pop, key=fitness)
        x1, x2 = decode(kromosom_terbaik)
        nilai_fitness = fitness(kromosom_terbaik)

        kromosom_str = ''.join(map(str, kromosom_terbaik))
        #print(f"{g+1:>8} || {nilai_fitness:>12.6f} || {kromosom_str:>12} || {x1:>10.4f} || {x2:>10.4f}")


evolusi(10)