import random
import numpy as np

def fitness_function(position):
    x, y = position
    return -(x**2 + y**2 - 4*x - 6*y)  

def particle_swarm_optimization(dimensions, num_particles, max_iterations, threshold):
    w = 0.5
    c1 = 1.2
    c2 = 1.4

    swarm = []
    for _ in range(num_particles):
        position = np.random.uniform(-10, 10, size=dimensions)
        velocity = np.random.uniform(-1, 1, size=dimensions)
        pbest_position = position.copy()
        pbest_fitness = fitness_function(position)
        swarm.append({'position': position, 'velocity': velocity,
                      'pbest_position': pbest_position, 'pbest_fitness': pbest_fitness})

    gbest_position = np.zeros(dimensions)
    gbest_fitness = -float('inf')

    for i in range(max_iterations):
        for p in swarm:
            fitness = fitness_function(p['position'])

            if fitness > p['pbest_fitness']:
                p['pbest_fitness'] = fitness
                p['pbest_position'] = p['position'].copy()

            if fitness > gbest_fitness:
                gbest_fitness = fitness
                gbest_position = p['position'].copy()

        if gbest_fitness >= threshold:
            print(f"Early stopping at iteration {i}")
            break

        for p in swarm:
            rand1 = random.random()
            rand2 = random.random()

            inertia = w * p['velocity']
            cognitive = c1 * rand1 * (p['pbest_position'] - p['position'])
            social = c2 * rand2 * (gbest_position - p['position'])

            p['velocity'] = inertia + cognitive + social
            p['position'] = p['position'] + p['velocity']

    print("SOLUTION FOUND:")
    print(f"  Position: {gbest_position}")
    print(f"  Fitness: {gbest_fitness}")
    return gbest_position, gbest_fitness

particle_swarm_optimization(dimensions=2, num_particles=20, max_iterations=5000, threshold=2)