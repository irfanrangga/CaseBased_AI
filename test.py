import random
import math

POP_SIZE = 6
GEN_LENGTH = 4
TOTAL_GEN = GEN_LENGTH * 2
X_MIN = -10
X_MAX = 10
MAX_GEN = 3
PC = 0.8 
PM = 0.01  
TOURNAMENT_SIZE = 2 

def binary_to_real(binary_str, min_val, max_val):
    decimal = int(binary_str, 2)
    max_dec = 2**GEN_LENGTH - 1
    return min_val + (decimal / max_dec) * (max_val - min_val)

def fitness_function(x1, x2):
    try:
        result = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + 0.75 * math.exp(1 - math.sqrt(x1 ** 2)))
    except:
        result = float('inf')
    return result

def init_population():
    return [''.join(random.choice('01') for _ in range(TOTAL_GEN)) for _ in range(POP_SIZE)]

def decode_chromosome(chromosome):
    x1_bin = chromosome[:GEN_LENGTH]
    x2_bin = chromosome[GEN_LENGTH:]
    x1 = binary_to_real(x1_bin, X_MIN, X_MAX)
    x2 = binary_to_real(x2_bin, X_MIN, X_MAX)
    return x1, x2

def evaluate_population(population):
    return [fitness_function(*decode_chromosome(chrom)) for chrom in population]

def tournament_selection(population, fitnesses):
    best = None
    for _ in range(TOURNAMENT_SIZE):
        idx = random.randint(0, POP_SIZE - 1)
        if best is None or fitnesses[idx] < fitnesses[best]:
            best = idx
    return population[best]

def crossover(parent1, parent2):
    if random.random() < PC:
        point = random.randint(1, TOTAL_GEN - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

def mutate(chromosome):
    mutated = ''
    for bit in chromosome:
        if random.random() < PM:
            mutated += '0' if bit == '1' else '1'
        else:
            mutated += bit
    return mutated

def genetic_algorithm():
    population = init_population()
    best_chrom = None
    best_fit = float('inf')

    for generation in range(MAX_GEN):
        fitnesses = evaluate_population(population)
        
        min_fit_idx = fitnesses.index(min(fitnesses))
        if fitnesses[min_fit_idx] < best_fit:
            best_fit = fitnesses[min_fit_idx]
            best_chrom = population[min_fit_idx]

        new_population = [best_chrom]  

        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])

        population = new_population[:POP_SIZE] 

    x1, x2 = decode_chromosome(best_chrom)
    return best_chrom, x1, x2, best_fit

best_chromosome, x1, x2, f_val = genetic_algorithm()

print("Kromosom Terbaik:", best_chromosome)
print("x1 =", x1)
print("x2 =", x2)
print("Nilai Fungsi Minimum =", f_val)