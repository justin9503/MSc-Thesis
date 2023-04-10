# Clip population values so that they are within the specified range and are non-negative
def clip_pop(pop, intervals):
    return [[max(min(sublist[i], intervals[i][1]), intervals[i][0], 0) for i in range(len(sublist))] for sublist in pop]

# Update the position of a particle based on its velocity, within the specified range and non-negative
def update_position(particle, velocity, intervals):
    new_particle = [particle[i] + velocity[i] for i in range(len(particle))]
    new_particle = [max(min(new_particle[i], intervals[i][1]), intervals[i][0], 0) for i in range(len(new_particle))]
    return new_particle

# Run the particle swarm optimization algorithm to find the optimal solution for the SVM fitness function, avoiding values out of range and negative values
def PSO(population, fitness_function, intervals, max_iter, c1, c2):
    # Initialize the velocities with random values
    velocities = [[random.uniform(-1, 1) for i in range(len(intervals))] for _ in range(len(population))]

    # Initialize the positions of the particles with random values within the specified intervals
    population = clip_pop([[random.uniform(intervals[i][0], intervals[i][1]) for i in range(len(intervals))] for _ in range(len(population))], intervals)

    # Initialize the best positions with the current positions
    best_positions = population[:]

    # Initialize the global best position with the best position of the first particle
    global_best_position = best_positions[0]

    # Iterate over the maximum number of iterations
    for _ in range(max_iter):
        # Calculate the fitness of each particle using the SVM fitness function
        fitnesses = [fitness(particle, fitness_function) for particle in population]

        # Update the best positions and global best position
        for i in range(len(population)):
            if fitnesses[i] > fitness(best_positions[i], fitness_function):
                best_positions[i] = population[i][:]
            if fitnesses[i] > fitness(global_best_position, fitness_function):
                global_best_position = population[i][:]

        # Update the velocity and position of each particle
        for i in range(len(population)):
            velocities[i] = update_velocity(population[i], best_positions[i], global_best_position, velocities[i], c1, c2)
            population[i] = update_position(population[i], velocities[i], intervals)

    # Return the global best position and the population and fitness of each particle
    return global_best_position, fitnesses