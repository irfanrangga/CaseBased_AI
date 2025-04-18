import random
import math
import numpy as np

# Fungsi objektif yang akan diminimisasi
def objective_function(x1, x2):
    term1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
    term2 = (3/4) * math.exp(1 - math.sqrt(x1*2 + x2*2))
    return -(term1 + term2)  # Karena kita ingin meminimisasi, kita negasikan

# Parameter Algoritma Genetika
POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 20  # 10 bit untuk x1, 10 bit untuk x2
GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.01
X_BOUNDS = (-10, 10)  # Batas untuk x1 dan x2

# Inisialisasi populasi awal
def initialize_population():
    return [[random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)] for _ in range(POPULATION_SIZE)]

# Dekode kromosom menjadi nilai x1 dan x2
def decode_chromosome(chromosome):
    # Pisahkan kromosom menjadi dua bagian untuk x1 dan x2
    x1_bits = chromosome[:CHROMOSOME_LENGTH//2]
    x2_bits = chromosome[CHROMOSOME_LENGTH//2:]
    
    # Konversi biner ke integer
    x1_int = binary_to_int(x1_bits)
    x2_int = binary_to_int(x2_bits)
    
    # Map ke range [-10, 10]
    x1 = X_BOUNDS[0] + (X_BOUNDS[1] - X_BOUNDS[0]) * x1_int / (2**(CHROMOSOME_LENGTH//2) - 1)
    x2 = X_BOUNDS[0] + (X_BOUNDS[1] - X_BOUNDS[0]) * x2_int / (2**(CHROMOSOME_LENGTH//2) - 1)
    
    return x1, x2

# Konversi biner ke integer
def binary_to_int(bits):
    return int(''.join(map(str, bits)), 2)

# Hitung fitness (kita ingin meminimisasi fungsi, jadi fitness adalah kebalikannya)
def calculate_fitness(chromosome):
    x1, x2 = decode_chromosome(chromosome)
    try:
        value = objective_function(x1, x2)
        # Karena kita ingin meminimisasi, fitness adalah kebalikan dari nilai fungsi
        # Ditambah offset kecil untuk menghindari division by zero
        return 1 / (value + 1e-10)
    except:
        # Jika terjadi error (misalnya tan(pi/2)), kembalikan fitness sangat kecil
        return 1e-10

# Seleksi orangtua dengan metode roulette wheel
def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    probabilities = [f/total_fitness for f in fitnesses]
    
    # Pilih dua orangtua
    parent1 = population[np.random.choice(len(population), p=probabilities)]
    parent2 = population[np.random.choice(len(population), p=probabilities)]
    
    return parent1, parent2

# Crossover satu titik
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        crossover_point = random.randint(1, CHROMOSOME_LENGTH-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1.copy(), parent2.copy()

# Mutasi bit-flip
def mutate(child):
    for i in range(len(child)):
        if random.random() < MUTATION_RATE:
            child[i] = 1 - child[i]  # Flip bit
    return child

# Seleksi survivor dengan metode elitism (mempertahankan individu terbaik)
def select_survivors(population, fitnesses, new_population, new_fitnesses):
    combined = list(zip(population + new_population, fitnesses + new_fitnesses))
    combined.sort(key=lambda x: x[1], reverse=True)
    survivors = [x[0] for x in combined[:POPULATION_SIZE]]
    return survivors

# Algoritma Genetika utama
def genetic_algorithm():
    # Inisialisasi populasi
    population = initialize_population()
    best_chromosome = None
    best_fitness = -float('inf')
    
    for generation in range(GENERATIONS):
        # Hitung fitness untuk setiap kromosom
        fitnesses = [calculate_fitness(chrom) for chrom in population]
        
        # Cari kromosom terbaik
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_chromosome = population[fitnesses.index(current_best_fitness)]
        
        # Cetak progress setiap 10 generasi
        if generation % 10 == 0:
            x1, x2 = decode_chromosome(best_chromosome)
            print(f"Generasi {generation}: Best fitness = {1/best_fitness}, x1 = {x1:.4f}, x2 = {x2:.4f}")
        
        # Buat populasi baru
        new_population = []
        new_fitnesses = []
        
        while len(new_population) < POPULATION_SIZE:
            # Seleksi orangtua
            parent1, parent2 = select_parents(population, fitnesses)
            
            # Crossover
            child1, child2 = crossover(parent1, parent2)
            
            # Mutasi
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            # Tambahkan ke populasi baru
            new_population.extend([child1, child2])
            new_fitnesses.extend([calculate_fitness(child1), calculate_fitness(child2)])
        
        # Seleksi survivor
        population = select_survivors(population, fitnesses, new_population, new_fitnesses)
    
    # Hasil akhir
    x1, x2 = decode_chromosome(best_chromosome)
    print("\n=== Hasil Akhir ===")
    print(f"Kromosom terbaik: {best_chromosome}")
    print(f"Nilai x1: {x1:.6f}")
    print(f"Nilai x2: {x2:.6f}")
    print(f"Nilai minimum fungsi: {1/best_fitness:.6f}")
    
    return best_chromosome, x1, x2

# Jalankan algoritma
if __name__ == "_main_":
    best_chromosome, x1, x2 = genetic_algorithm()