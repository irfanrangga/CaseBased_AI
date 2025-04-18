import math
import random


population_size = 50
panjang_kromosom = 10
batasan_x1 = (-10, 10)
batasan_x2 = (-10, 10)
bitx = panjang_kromosom // 2


def inisialisasi_populasi():
    return [[random.randint(0, 1) for _ in range(panjang_kromosom)]
             for _ in range(population_size)]


def decode(krom):
    biner_x1 = krom[bitx]
    biner_x2 = krom[bitx]

    desimal_x1 = int(biner_x1, 2)
    desimal_x2 = int(biner_x2, 2)

    x1 = X1_MIN + (X1_MAX - X1_MIN) * desimal_x1 / (2**bitx - 1)
    x2 = X2_MIN + (X2_MAX - X2_MIN) * desimal_x2 / (2**bitx - 1)
    return x1, x2

