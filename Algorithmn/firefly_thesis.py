import random
import math

# Define the firefly algorithm function
def firefly_algorithm(population, fitness_function, intervals, max_iter, alpha, beta, gamma):
    # Clip population values so that they are within the specified range and are non-negative
    def clip_pop(pop):
        return [[max(min(sublist[i], intervals[i][1]), intervals[i][0], 0) for i in range(len(sublist))] for sublist in pop]

    # Initialize the brightness with the fitness of each particle
    brightness = [fitness_function(particle) for particle in clip_pop(population)]

    # Iterate over the maximum number of iterations
    for t in range(max_iter):
        # Update the position of each firefly based on the attractiveness of other fireflies
        for i in range(len(population)):
            for j in range(len(population)):
                if brightness[j] > brightness[i]:
                    r = math.sqrt(sum([(x - y) ** 2 for x, y in zip(population[i], population[j])]))
                    beta_ = beta * math.exp(-gamma * r ** 2)
                    for k in range(len(population[i])):
                        population[i][k] = population[i][k] + beta_ * (population[j][k] - population[i][k]) + alpha * (random.uniform(0, 1) - 0.5)
                        population[i][k] = max(min(population[i][k], intervals[k][1]), intervals[k][0], 0)
                    brightness[i] = fitness_function(clip_pop([population[i]])[0])

    # Find the best solution among the final population
    best_solution = clip_pop([population[0]])[0]
    best_fitness = brightness[0]
    for i in range(len(population)):
        if brightness[i] > best_fitness:
            best_fitness = brightness[i]
            best_solution = clip_pop([population[i]])[0]

    # Return the best solution and its fitness
    return best_solution, best_fitness
