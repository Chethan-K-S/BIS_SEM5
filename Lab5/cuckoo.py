import numpy as np
import math

# --- Levy flight ---
def levy_flight(Lambda, dim):
    sigma = (math.gamma(1 + Lambda) * np.sin(np.pi * Lambda / 2) / 
             (math.gamma((1 + Lambda) / 2) * Lambda * 2**((Lambda - 1) / 2)))**(1 / Lambda)
    u = np.random.normal(0, sigma, size=dim)
    v = np.random.normal(0, 1, size=dim)
    step = u / abs(v)**(1 / Lambda)
    return step

# --- Sigmoid for binary conversion ---
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# --- Fitness function for knapsack ---
def fitness_function(x_bin, weights, values, capacity):
    total_weight = np.sum(x_bin * weights)
    total_value = np.sum(x_bin * values)
    if total_weight > capacity:
        return -1  # Penalize overweight solutions heavily
    else:
        return total_value

# --- Cuckoo Search for Binary Knapsack ---
def cuckoo_search_knapsack(weights, values, capacity, n=25, Pa=0.25, Maxt=500):
    dim = len(weights)
    # Initialize nests (continuous vectors)
    nests = np.random.uniform(low=-1, high=1, size=(n, dim))
    # Convert to binary solutions
    nests_bin = np.array([sigmoid(nest) > np.random.rand(dim) for nest in nests])
    fitness = np.array([fitness_function(x, weights, values, capacity) for x in nests_bin])
    
    best_idx = np.argmax(fitness)
    best_nest = nests[best_idx].copy()
    best_bin = nests_bin[best_idx].copy()
    best_fitness = fitness[best_idx]

    t = 0
    while t < Maxt:
        for i in range(n):
            # Generate new solution by Levy flight
            step = levy_flight(1.5, dim)
            new_nest = nests[i] + 0.01 * step
            # Convert new_nest to binary
            new_bin = sigmoid(new_nest) > np.random.rand(dim)
            new_fitness = fitness_function(new_bin, weights, values, capacity)

            # If new solution is better, replace
            if new_fitness > fitness[i]:
                nests[i] = new_nest
                nests_bin[i] = new_bin
                fitness[i] = new_fitness

                if new_fitness > best_fitness:
                    best_fitness = new_fitness
                    best_nest = new_nest.copy()
                    best_bin = new_bin.copy()

        # Abandon fraction Pa of worst nests
        num_abandon = int(Pa * n)
        worst_indices = np.argsort(fitness)[:num_abandon]
        for idx in worst_indices:
            nests[idx] = np.random.uniform(-1, 1, dim)
            nests_bin[idx] = sigmoid(nests[idx]) > np.random.rand(dim)
            fitness[idx] = fitness_function(nests_bin[idx], weights, values, capacity)

            if fitness[idx] > best_fitness:
                best_fitness = fitness[idx]
                best_nest = nests[idx].copy()
                best_bin = nests_bin[idx].copy()

        t += 1

    return best_bin, best_fitness

if __name__ == "__main__":
    print("Enter the number of items:")
    n_items = int(input())

    weights = []
    values = []

    print("Enter the weights of the items (space-separated):")
    weights = np.array(list(map(float, input().split())))
    if len(weights) != n_items:
        raise ValueError("Number of weights does not match number of items.")

    print("Enter the values of the items (space-separated):")
    values = np.array(list(map(float, input().split())))
    if len(values) != n_items:
        raise ValueError("Number of values does not match number of items.")

    print("Enter the knapsack capacity:")
    capacity = float(input())

    print("Enter population size (default 25):")
    n = input()
    n = int(n) if n.strip() else 25

    print("Enter abandonment probability Pa (default 0.25):")
    Pa = input()
    Pa = float(Pa) if Pa.strip() else 0.25

    print("Enter maximum iterations Maxt (default 500):")
    Maxt = input()
    Maxt = int(Maxt) if Maxt.strip() else 500

    best_solution, best_value = cuckoo_search_knapsack(weights, values, capacity, n=n, Pa=Pa, Maxt=Maxt)

    print("\nBest solution (items selected):", best_solution.astype(int))
    print("Total value:", best_value)
    print("Total weight:", np.sum(best_solution * weights))
