import numpy as np


def one_point_crossover(p1, p2):
    point = np.random.randint(1, len(p1) - 1)
    c1 = np.concatenate((p1[:point], p2[point:]))
    c2 = np.concatenate((p2[:point], p1[point:]))

    return c1, c2
