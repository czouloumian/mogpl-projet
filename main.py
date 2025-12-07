from file_manager import read_file, result_out, demander_fichier
from graph_model import create_graph
from pathfinding_solver import astar, bfs
import instance_generator 
import experiments

def main():

    experiments.run_tests_and_save_grid(instance_generator.generate_and_save_instances_grid())
    experiments.run_tests_and_save_obs(instance_generator.generate_and_save_instances_obstacle())

    # file_name = demander_fichier()
    # mat, xd, yd, xa, ya, direction = read_file(file_name)
    # graphe = create_graph(mat)
    # bfs_sol = bfs(graphe, (xd,yd,direction), (xa,ya))
    # print("Solution donnée par l'algorithme du BFS : ", bfs_sol)
    # a = astar(graphe, (xd,yd, direction), (xa,ya))
    # print("Solution donnée par l'algorithme A* : ",a)

    # sauvegarder = input("Voulez-vous sauvegarder le fichier ? (o/n) : ").strip().lower()

    # if sauvegarder == "o" or sauvegarder == "oui":
    #     fichier_sortie = input("Entrez le nom du fichier de sauvegarde : ").strip()

    #     result_out(fichier_sortie, a)

    #     print(f"Le fichier a été sauvegardé sous : {fichier_sortie}")


    

if __name__ == "__main__" :
    main()
