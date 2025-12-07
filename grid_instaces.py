import random
import numpy as np
from graph_model import create_graph
from file_manager import instance_out

def generate_instance_grid(m, n, o):
    """
    Génère les instances selon sur la taille du graphe

    :param m: nombre de lignes de la grille
    :param n: nombre de colonnes de la grille
    :param o: nombre d'obstacles de la grille
    """

    mat = np.zeros((m, n), dtype=int)
    obstacles = 0
    while obstacles < o:
        x = random.randint(0, m - 1)
        y = random.randint(0, n - 1)
        if mat[x][y] == 0 and not (x == 0 and y == 0):
            mat[x][y] = 1
            obstacles += 1
    return mat, create_graph(mat)


def generate_instance_obs(o):
    """
    Génère les instances selon sur la quantité d'obstacles, pour une grille de taille 20x20

    :param o: number of obstacles
    """
    mat = np.zeros((20, 20), dtype=int)
    obstacles = 0
    while obstacles < o:
        x = random.randint(0, 19)
        y = random.randint(0, 19)
        if mat[x][y] == 0 and not (x == 0 and y == 0):
            mat[x][y] = 1
            obstacles += 1
    return mat, create_graph(mat)

def generate_and_save_instances_grid(filename):
    """
    Generate 10 instances per size of the grid
    """
    instances = []
    for i in range(1, 6):
        for _ in range(10):
            mat, _ = generate_instance_grid(i * 10, i * 10, i * 10)
            instance_out(filename, mat, (0, 0, 0), (i * 10, i * 10))
            instances.append((mat, (0, 0, 0), (i * 10, i * 10)))
    return instances
