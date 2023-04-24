# -*- coding: utf-8 -*-
"""PSO_improved.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V28YGQjqWqPvw_8OhCvi4I4o3ied-q9q
"""

import random

# Clip population values so that they are within the specified range and are non-negative
def clip_pop(pop, intervals):
    return [[max(min(sublist[i], intervals[i][1]), intervals[i][0]) for i in range(len(sublist))] for sublist in pop]

# Update the velocity of a particle based on its position, best position and global best position
def update_velocity(particle, best_position, global_best_position, velocity, c1, c2, w=0.5):
    new_velocity = [w * velocity[i] + c1 * random.uniform(0, 1) * (best_position[i] - particle[i]) + c2 * random.uniform(0, 1) * (global_best_position[i] - particle[i]) for i in range(len(particle))]
    return new_velocity

# Update the position of a particle based on its velocity, within the specified range and non-negative
def update_position(particle, velocity, intervals):
    new_particle = [particle[i] + velocity[i] for i in range(len(particle))]
    new_particle = [max(min(new_particle[i], intervals[i][1]), intervals[i][0]) for i in range(len(new_particle))]
    return new_particle

# Run the particle swarm optimization algorithm to find the optimal solution for the SVM fitness function, avoiding values out of range and negative values
def PSO(population, intervals, max_iter, c1, c2, stopping_iter=20):
    # Initialize the velocities with random values
    velocities = [[random.uniform(-1, 1) for i in range(len(intervals))] for _ in range(len(population))]

    # Initialize the positions of the particles with random values within the specified intervals
    population = clip_pop([[random.uniform(intervals[i][0], intervals[i][1]) if i!=0 else int(random.uniform(intervals[i][0], intervals[i][1])) for i in range(len(intervals))] for _ in range(len(population))], intervals)

    # Initialize the best positions with the current positions
    best_positions = population[:]

    # Initialize the global best position with the best position of the first particle
    global_best_position = best_positions[0]

    # Initialize the stopping criterion
    stopping_count = 0
    best_fitness = None

    # Iterate over the maximum number of iterations
    for i in range(max_iter):
        # Calculate the fitness of each particle
        fitnesses = [1 / (1 + particle[0]) for particle in population]

        # Update the best positions and global best position
        for j in range(len(population)):
            if fitnesses[j] > fitnesses[best_positions[j]]:
                best_positions[j] = j
            if fitnesses[j] > fitnesses[global_best_position]:
                global_best_position = j

        # Update the velocity and position of each particle
        for j in range(len(population)):
            velocities[j] = update_velocity(population[j], population[best_positions[j]], population[global_best_position], velocities[j], c1, c2)
            population[j] = update_position(population[j], velocities[j], intervals)

        # Check stopping criterion
        if best_fitness is None or fitnesses[global_best_position] > best_fitness:
            best_fitness = fitnesses[global_best_position]
            stopping_count = 0
        else:
            stopping_count += 1

        if stopping_count >= stopping_iter:
            break

    # Return the global best position and the population and fitness of each particle
    return population[global_best_position], fitnesses