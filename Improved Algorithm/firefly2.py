# -*- coding: utf-8 -*-
"""Firefly2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AX4Wzny2-gUZkl5tXXU9NAQvarvtl-8H
"""

import random
import math

# Clip population values so that they are within the specified range and are non-negative
def clip_pop(pop, intervals):
    return [[max(min(sublist[i], intervals[i][1]), intervals[i][0]) for i in range(len(sublist))] for sublist in pop]

# Generate an initial population of fireflies with random positions within the specified range
def init_ffa(n, intervals):
    return clip_pop([[random.uniform(intervals[i][0], intervals[i][1]) for i in range(len(intervals))] for _ in range(n)], intervals)

# Calculate the brightness of a firefly based on its fitness value
def brightness(fitness_value, beta=1):
    return math.exp(-beta * fitness_value)

# Calculate the distance between two fireflies
def distance(firefly1, firefly2):
    return math.sqrt(sum([(firefly1[i] - firefly2[i]) ** 2 for i in range(len(firefly1))]))

# Update the position of a firefly based on its brightness, the brightness of other fireflies, and the attractiveness coefficient
def move_ff(population, beta, alpha, intervals):
    new_population = population[:]
    for i in range(len(population)):
        for j in range(len(population)):
            if brightness(population[j][-1], beta) > brightness(population[i][-1], beta):
                r = distance(population[i][:-1], population[j][:-1])
                beta_new = beta * math.exp(-alpha * r ** 2)
                tmp_ff = [population[i][k] + beta_new * (population[j][k] - population[i][k]) + random.uniform(-1, 1) for k in range(len(population[i]) - 1)]
                tmp_ff = clip_pop([tmp_ff], intervals)[0]
                if brightness(tmp_ff[-1], beta_new) > brightness(population[i][-1], beta):
                    new_population[i] = tmp_ff + [brightness(tmp_ff[-1], beta_new)]
    return new_population

# Run the firefly algorithm to find the optimal solution for the fitness function, avoiding values out of range and negative values
def FFA(n, fitness_function, intervals, max_iter, alpha=0.5, beta_0=1, gamma=1):
    # Generate an initial population of fireflies with random positions within the specified range
    population = init_ffa(n, intervals)

    # Iterate over the maximum number of iterations
    for t in range(max_iter):
        # Evaluate the fitness of each firefly and update the population with the new brightness values
        for i in range(len(population)):
            population[i][-1] = brightness(fitness_function(population[i][:-1]))

        # Sort the fireflies in descending order based on their brightness values
        population = sorted(population, key=lambda x: x[-1], reverse=True)

        # Move the fireflies to new positions based on their brightness values and the attractiveness coefficient
        population = move_ff(population, beta_0, alpha, intervals)

        # Update the value of the beta coefficient
        beta_0 *= gamma

    # Return the best firefly (i.e., the one with the highest brightness value) and its fitness value
    best_ff = max(population, key=lambda x: x[-1])
    return best_ff[:-1], best_ff[-1]