import random
import math

# Fungsi objektif
def fitness(individu):
    x1, x2 = individu
    try:
        val = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
        val += (3/4) * math.exp(1 - abs(x1))
        return -val  # karena kita ingin minimisasi
    except:
        return float('inf')  # jika tan menghasilkan nilai tak hingga

# Inisialisasi populasi
def init_population(size, bounds):
    return [(
        random.uniform(bounds[0], bounds[1]),
        random.uniform(bounds[0], bounds[1])
    ) for _ in range(size)]

# Seleksi (turnamen)
def selection(populasi):
    return min(random.sample(populasi, 3), key=fitness)

# Crossover (satu titik)
def crossover(parent1, parent2):
    if random.random() < 0.7:
        return (parent1[0], parent2[1]), (parent2[0], parent1[1])
    else:
        return parent1, parent2

# Mutasi (small gaussian perturbation)
def mutate(individu, bounds):
    x1, x2 = individu
    if random.random() < 0.2:
        x1 += random.gauss(0, 0.5)
    if random.random() < 0.2:
        x2 += random.gauss(0, 0.5)
    # clamp to bounds
    x1 = max(min(x1, bounds[1]), bounds[0])
    x2 = max(min(x2, bounds[1]), bounds[0])
    return (x1, x2)

# Genetic Algorithm
def genetic_algorithm(generasi=10, pop_size=30, bounds=(-10, 10)):
    populasi = init_population(pop_size, bounds)

    for gen in range(generasi):
        populasi = sorted(populasi, key=fitness)
        next_gen = populasi[:2]  # elitisme

        while len(next_gen) < pop_size:
            parent1 = selection(populasi)
            parent2 = selection(populasi)
            child1, child2 = crossover(parent1, parent2)
            next_gen.extend([mutate(child1, bounds), mutate(child2, bounds)])

        populasi = next_gen

        best = min(populasi, key=fitness)
        print(f"Generasi {gen+1} - Terbaik: {best} => Fitness: {fitness(best)}")

    return min(populasi, key=fitness)

# Jalankan
hasil_akhir = genetic_algorithm()
print(f"\nHasil akhir terbaik: {hasil_akhir} => Nilai minimum: {fitness(hasil_akhir)}")
