import math

population_size = 50
panjang_kromosom = 32
batasan_x = (-10, 10)

def inisialisasi_populasi():
    return [[random.randint(0, 1) for _ in range(panjang_kromosom)]
             for _ in range(population_size)]


