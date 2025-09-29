import numpy as np
import random

def distance_matrix(cities):
    n = len(cities)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i][j] = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
    return dist

def tour_length(tour, dist):
    return sum(dist[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))

def initialize_population(num_wolves, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(num_wolves)]

def gwo_tsp(cities, num_wolves=20, max_iter=100):
    dist = distance_matrix(cities)
    population = initialize_population(num_wolves, len(cities))
    fitness = [tour_length(tour, dist) for tour in population]

    alpha, beta, delta = sorted(zip(population, fitness), key=lambda x: x[1])[:3]

    for iter in range(max_iter):
        a = 2 - iter * (2 / max_iter)
        new_population = []

        for wolf in population:
            new_tour = []
            for i in range(len(cities)):
                r1, r2 = random.random(), random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[0][i] - wolf[i])
                X1 = alpha[0][i] - A1 * D_alpha

                # Repeat for beta and delta
                # Combine X1, X2, X3 and discretize
                new_tour.append(int(X1) % len(cities))

            # Ensure it's a valid permutation
            new_tour = list(dict.fromkeys(new_tour))
            while len(new_tour) < len(cities):
                new_tour.append(random.choice([i for i in range(len(cities)) if i not in new_tour]))

            new_population.append(new_tour)

        population = new_population
        fitness = [tour_length(tour, dist) for tour in population]
        alpha, beta, delta = sorted(zip(population, fitness), key=lambda x: x[1])[:3]

    return alpha[0], alpha[1]

# Example usage
cities = [(0,0), (1,5), (5,2), (6,6), (8,3)]
best_tour, best_distance = gwo_tsp(cities)
print("Best tour:", best_tour)
print("Distance:", best_distance)