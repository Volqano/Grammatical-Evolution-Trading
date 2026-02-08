import numpy as np


def one_point_crossover(p1, p2):
    point = np.random.randint(1, len(p1) - 1)
    c1 = np.concatenate((p1[:point], p2[point:]))
    c2 = np.concatenate((p2[:point], p1[point:]))

    return c1, c2


def two_point_crossover(p1, p2):
    pt1, pt2 = np.sort(np.random.choice(range(1, len(p1) - 1), 2, replace=False))
    c1 = np.concatenate((p1[:pt1], p2[pt1:pt2], p1[pt2:]))
    c2 = np.concatenate((p2[:pt1], p1[pt1:pt2], p2[pt2:]))

    return c1, c2
