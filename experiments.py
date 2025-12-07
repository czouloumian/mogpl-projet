import matplotlib.pyplot as plt
import time

from pathfinding_solver import  astar, bfs
from instance_generator import  generate_instance
from graph_model import create_graph
from file_manager import result_out_many

def test_grid():
    """
    Test pour la génération d'instances de graphe selon la taille de la matrice
    """
    list_astar = []
    list_bfs = []
    for i in range(1, 6):
        print("i: ", i)
        t_a = 0
        t_bfs = 0
        for j in range(1000):
            _, graphe = generate_instance(i * 10, i * 10, i * 10)
            start = time.time()
            _ = astar(graphe, (0, 0, 0), (i * 10, i * 10))
            end = time.time()
            t_a += end - start

            start = time.time()
            _ = bfs(graphe, (0, 0, 0), (i * 10, i * 10))
            end = time.time()
            t_bfs += end - start

        list_astar.append(t_a / 1000)
        list_bfs.append(t_bfs / 1000)
    return list_astar, list_bfs


def run_tests_and_save_grid(instances):
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

    result_out_many("result_bfs", paths_bfs)
    result_out_many("results_astar", paths_astar)

    means_astar = group_by_ten(results_astar)
    means_bfs = group_by_ten(results_bfs)
    plot_test_grid(means_astar, means_bfs)

    return paths_bfs, results_bfs, paths_astar, results_astar


def group_by_ten(results):
    """
    Regroupes les resultats en moyenne par 10 pour le plot
    """
    liste_plot = []
    for i in range(0, len(results),10):
        chunk = results[i:i+10]
        if len(chunk) == 10:
            liste_plot.append(sum(chunk)/10)
    return liste_plot


def plot_test_grid(list_astar, list_bfs):
    """
    Plot pour le test de la génération d'instances selon la taille

    :param list: list of the times taken for each randomly generated graph
    """
    plt.plot([10, 20, 30, 40, 50], list_astar, color="blue", label="A*")
    plt.plot([10, 20, 30, 40, 50], list_bfs, color="red", label="BFS")
    plt.xlabel("Taille de la grille")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction de la taille de la grille")
    plt.legend()
    plt.show()

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

    result_out_many("result_bfs", paths_bfs)
    result_out_many("results_astar", paths_astar)

    means_astar = group_by_ten(results_astar)
    means_bfs = group_by_ten(results_bfs)
    plot_test_obs_solution(means_astar, means_bfs)

    return paths_bfs, results_bfs, paths_astar, results_astar

def test_obs():
    """
    Test pour la génération d'instances de graphe selon le nombre d'obstacles
    """
    list_sol_astar = []  # grilles pour lesquelles une solution a été trouvée
    list_sol_bfs = []
    list_no_sol = []  # grilles pour lesquelles il n'y avait pas de solution
    for i in range(1, 6):
        t_sol_a = 0
        t_sol_bfs = 0
        t_no_sol = 0
        print("i: ", i)
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
                    t_sol_a += end - start
                    start = time.time()
                    bfs_sol = bfs(graphe, (0, 0, 0), (20, 20))
                    end = time.time()
                    t_sol_bfs += end - start
                # else :
                #   t_no_sol += end - start
                #  n_sol_not_found += 1

            if redo == max_redo:
                print("no sol trouvée pour i = ", i, " et j = ", j)
                n_sol_found -= 1
        print("nb sol ", n_sol_found)
        print("nb pas sol ", n_sol_not_found)
        list_sol_astar.append(t_sol_a / n_sol_found)
        list_sol_bfs.append(t_sol_bfs / n_sol_found)
        # list_no_sol.append(t_no_sol/n_sol_not_found)
    return list_sol_astar, list_sol_bfs


def plot_test_obs_solution(list_sol_a, list_sol_bfs):
    """
    Plot pour le test de la génération d'instances d'obstacles

    :param list_sol: list of the times taken for each randomly generated graph
    """
    plt.plot([10, 20, 30, 40, 50], list_sol_a, color="blue", label="A*")
    plt.plot([10, 20, 30, 40, 50], list_sol_bfs, color="red", label="BFS")
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction du nombre d'obstacles dans une grille 20x20")
    plt.legend()
    plt.show()


def plot_test_obs_no_solution(list_no_sol):
    """
    Plot pour le test de la génération d'instances d'obstacles

    :param list_no_sol: list of the times taken for each randomly generated graph
    """
    plt.plot([10, 20, 30, 40, 50], list_no_sol, color="blue")
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction du nombre d'obstacles dans une grille 20x20, aucun chemin possible")
    plt.show()
