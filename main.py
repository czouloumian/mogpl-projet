from file_manager import read_file
from file_manager import result_out
from graph_model import create_graph
from pathfinding_solver import astar

def main():
    #TODO: à changer
    mat, xd, yd, xa, ya, direction = read_file("exemple_entree.txt")
    #instances = generate_and_save_instances_grid("test_instances.txt")
    #paths_bfs, results_bfs, paths_astar, results_astar = run_tests_grid_and_save(instances, "file_out")
    #forbidden_list = forbidden_edges(mat)
    #print("forbidden list : ", forbidden_list)
    # # print(len(forbidden_list))
    graphe = create_graph(mat)
    #instance_out("test_sortie", mat, (xd,yd,direction), (xa,ya))
    #dictionnaire = create_graph(mat)
    #bfs_sol = bfs(dictionnaire, (xd,yd,direction), (xa,ya))
    #print("BFS : ", bfs_sol)
    a = astar(graphe, (xd,yd, direction), (xa,ya))
    print("A*: ", len(a),a)
    # result_out("test_bfs.txt", bfs_sol) 
    result_out("test_astar.txt", a)
  
if __name__ == "__main__" :
    main()
