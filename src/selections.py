import numpy as np


def roulette_selection(objective_values, population, number_of_offspring):
    population_size = len(population)
    fitness_values = objective_values - objective_values.min()

    if fitness_values.sum() > 0:
        fitness_values = fitness_values / fitness_values.sum()
    else:
        fitness_values = np.ones(population_size) / population_size
    parent_indices = np.random.choice(population_size, number_of_offspring, True, fitness_values).astype(np.int64)

    return population[parent_indices]


def tournament_selection(objective_values, population, number_of_offspring, k=5):
    population_size = len(population)

    candidates_indices = np.random.randint(0, population_size, size=(number_of_offspring, k))
    candidates_scores = objective_values[candidates_indices]
    winners_local_idx = np.argmax(candidates_scores, axis=1)

    rows = np.arange(number_of_offspring)
    parent_indicies = candidates_indices[rows, winners_local_idx]

    return population[parent_indicies]
