import math
import random

# Konstanta
population_size = 50
panjang_kromosom = 10
batasan_x1 = (-10, 10)
batasan_x2 = (-10, 10)
bitx = panjang_kromosom // 2
X1_MIN, X1_MAX = batasan_x1
X2_MIN, X2_MAX = batasan_x2

# Fungsi untuk menghitung fitness
def inisialisasi_populasi():
    return [[random.randint(0, 1) for _ in range(panjang_kromosom)]
             for _ in range(population_size)]


def decode(kromosom):
    krom = ''.join(str(bit) for bit in kromosom)
    # Mengambil 5 bit pertama dan 5 bit kedua dari kromosom
    biner_x1 = kromosom[:bitx] # ambil 5 bit kromosom pertama
    biner_x2 = kromosom[bitx:] # ambil 5 bit kromosom kedua

    desimal_x1 = int(biner_x1, 2)
    desimal_x2 = int(biner_x2, 2)

    x1 = X1_MIN + (X1_MAX - X1_MIN) * desimal_x1 / (2**bitx - 1)
    x2 = X2_MIN + (X2_MAX - X2_MIN) * desimal_x2 / (2**bitx - 1)
    return x1, x2

def hitung_fitness(x1, x2):
    if x1 < X1_MIN or x1 > X1_MAX or x2 < X2_MIN or x2 > X2_MAX:
        return float('inf')  # Fitness tidak valid di luar batasan
    else:
        # Fungsi fitness yang diberikan
        eqt = math.sin(x1) * math.cos(x2) * math.tan(x1+x2) + (3/4) * math.exp(1-(math.sqrt(math.pow(x1, 2))))
    return -eqt

def fitness(krom):
    x1, x2 = decode(krom)
    return hitung_fitness(x1, x2)

def pemilihan_ortu(pop):
    ortu_1 = random.choice(pop)
    ortu_2 = random.choice(pop)
    return a if fitness(a) < fitness(b) else b
