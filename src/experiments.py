import matplotlib.pyplot as plt
import time

from pathfinding_solver import  astar, bfs
from instance_generator import  generate_instance
from graph_model import create_graph
from file_manager import result_out_many

def group_by_ten(results):
    """
    Regroupe les resultats en moyenne par 10 (le nombre d'instances par taille ou par nombre d'obstacles)

    :param results: la liste des résultats
    :return: une liste de moyennes pour le plot
    """
    liste_plot = []
    for i in range(0, len(results),10):
        chunk = results[i:i+10]
        if len(chunk) == 10:
            liste_plot.append(sum(chunk)/10)
    return liste_plot

def run_tests_and_save_grid(instances):
    """
    Fait les tests de temps d'éxecution de BFS et A* pour les instaces dans la liste

    :param instances: Liste des instances à tester
    :return: Renvoie 4 listes avec les chemins et les temps d'éxecution retournés
    """
    paths_bfs = []
    results_bfs = []
    paths_astar = []
    results_astar = []

    for x in instances:
        mat, (xd, yd, direction), (xa, ya) = x
        graphe = create_graph(mat)

        # test astar
        start = time.time()
        path = astar(graphe, (xd, yd, direction), (xa, ya))
        end = time.time()
        results_astar.append(end - start)

        paths_astar.append(path)

        # test bfs
        start = time.time()
        path = bfs(graphe, (xd, yd, direction), (xa, ya))
        end = time.time()
        results_bfs.append(end - start)

        paths_bfs.append(path)

    result_out_many("result_bfs_instances", paths_bfs)
    result_out_many("results_astar_instances", paths_astar)

    means_astar = group_by_ten(results_astar)
    means_bfs = group_by_ten(results_bfs)
    plot_test_grid_astar_bfs(means_astar, means_bfs)

    return paths_bfs, results_bfs, paths_astar, results_astar

def run_tests_and_save_obs(instances):
    """
    Fait les tests de temps d'éxecution de BFS et A* pour les instaces dans la liste

    :param instances: Liste des instances à tester
    :param file_suffix: (str) "obstacles", "grid", ou autre description selon les tests effectués
    :return: Renvoie 4 listes avec les chemins et les temps d'éxecution retournés
    """
    paths_bfs = []
    results_bfs = []
    paths_astar = []
    results_astar = []

    for x in instances:
        mat, (xd, yd, direction), (xa, ya) = x
        graphe = create_graph(mat)

        # test astar
        start = time.time()
        path = astar(graphe, (xd, yd, direction), (xa, ya))
        end = time.time()
        results_astar.append(end - start)

        paths_astar.append(path)

        # test bfs
        start = time.time()
        path = bfs(graphe, (xd, yd, direction), (xa, ya))
        end = time.time()
        results_bfs.append(end - start)

        paths_bfs.append(path)

    result_out_many("result_bfs_obs", paths_bfs)
    result_out_many("results_astar_obs", paths_astar)

    means_astar = group_by_ten(results_astar)
    means_bfs = group_by_ten(results_bfs)
    plot_test_obs_astar_bfs(means_astar, means_bfs)

    return paths_bfs, results_bfs, paths_astar, results_astar

def plot_test_grid_astar_bfs(list_astar, list_bfs):
    """
    Plot pour le test de la génération d'instances selon la taille

    :param list_astar: liste des temps pris avec A* pour chaque graphe généré
    :param list_bfs: liste des temps pris avec BFS pour chaque graphe généré
    """
    plt.plot([10, 20, 30, 40, 50], list_astar, color="blue", label="A*")
    plt.plot([10, 20, 30, 40, 50], list_bfs, color="red", label="BFS")
    plt.xlabel("Taille de la grille")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction de la taille de la grille")
    plt.legend()
    plt.show()

def plot_test_obs_astar_bfs(list_sol_a, list_sol_bfs):
    """
    Test du temps d'exécution des algos et BFS A* selon le nombre d'obstacles

    :param list_astar: liste des temps pris avec A* pour chaque graphe généré
    :param list_bfs: liste des temps pris avec BFS pour chaque graphe généré
    """
    plt.plot([10, 20, 30, 40, 50], list_sol_a, color="blue", label="A*")
    plt.plot([10, 20, 30, 40, 50], list_sol_bfs, color="red", label="BFS")
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction du nombre d'obstacles dans une grille 20x20")


def test_grid():
    """
    Test du temps d'exécution de l'algo A* selon le nombre d'obstacles
    Génère deux listes : une lorsqu'une solution a été trouvée et une autre lorsqu'il n'y a pas de solution

    :return: les deux listes (avec solution et sans solution)
    """
    list_sol = []  # grilles pour lesquelles une solution a été trouvée
    list_no_sol = []  # grilles pour lesquelles il n'y avait pas de solution
    for i in range(1, 6):
        print("i ", i)
        t_sol = 0
        t_no_sol = 0
        n_sol_found = 1000
        n_sol_not_found = 0
        for j in range(1000):
            a = None
            redo = 0
            max_redo = 100
            while not a and redo < max_redo:
                _, graphe = generate_instance(i * 10, i * 10, i * 10)
                start = time.time()
                a = astar(graphe, (0, 0, 0), (i*10, i*10))
                end = time.time()
                redo += 1
                if a:
                    t_sol += end - start
                else:
                    t_no_sol += end - start
                    n_sol_not_found += 1

            if redo == max_redo:
                n_sol_found -= 1
        list_sol.append(t_sol / n_sol_found)
        list_no_sol.append(t_no_sol / n_sol_not_found)
    return list_sol, list_no_sol


def plot_test_grid(list_sol, list_no_sol):
    """
    Plot pour le test du temps d'exécution selon la quantité d'obstacles.
    Lorsqu'il y a et lorsqu'il n'y a pas de solution.
    """
    plt.plot([10, 20, 30, 40, 50], list_sol, color="blue", label="Solution trouvée")
    plt.plot([10, 20, 30, 40, 50], list_no_sol, color="red", label="Pas de solution trouvée")
    plt.xlabel("Taille de la grille")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction de la taille de la grille")
    plt.legend()
    plt.show()

def test_obs():
    """
    Test du temps d'exécution de l'algo A* selon le nombre d'obstacles
    Génère deux listes : une lorsqu'une solution a été trouvée et une autre lorsqu'il n'y a pas de solution

    :return: les deux listes (avec solution et sans solution)
    """
    list_sol = []  # grilles pour lesquelles une solution a été trouvée
    list_no_sol = []  # grilles pour lesquelles il n'y avait pas de solution
    for i in range(1, 6):
        print("i ", i)
        t_sol = 0
        t_no_sol = 0
        n_sol_found = 1000
        n_sol_not_found = 0
        for j in range(1000):
            a = None
            redo = 0
            max_redo = 100
            while not a and redo < max_redo:
                mat, graphe = generate_instance(20,20,i * 10)
                start = time.time()
                a = astar(graphe, (0, 0, 0), (20, 20))
                end = time.time()
                redo += 1
                if a:
                    t_sol += end - start
                else :
                    t_no_sol += end - start
                    n_sol_not_found += 1

            if redo == max_redo:
                n_sol_found -= 1
        list_sol.append(t_sol / n_sol_found)
        list_no_sol.append(t_no_sol/n_sol_not_found)
    return list_sol, list_no_sol


def plot_test_obs(list_sol, list_no_sol):
    """
    Plot pour le test du temps d'exécution selon la quantité d'obstacles.
    Lorsqu'il y a et lorsqu'il n'y a pas de solution.
    """
    plt.plot([10, 20, 30, 40, 50], list_sol, color="blue", label="Solution trouvée")
    plt.plot([10, 20, 30, 40, 50], list_no_sol, color="red", label="Pas de solution trouvée")
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction du nombre d'obstacles dans une grille 20x20")
    plt.legend()
    plt.show()