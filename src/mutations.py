import numpy as np


def random_mutation(genome):
    idx = np.random.randint(0, len(genome))
    genome[idx] = np.random.randint(0, 256)
    return genome
