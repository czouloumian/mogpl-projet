import numpy as np
from collections import deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

NORD = 0
EST = 1
SUD = 2
OUEST = 3

def read_file(file_name : str):
    """
    Lit le fichier texte avec les données de départ
    :param file_name: Nom du fichier texte
    :return:
    """
    with open(file_name, "r") as file :
        n, m = file.readline().split(" ")

        n = int(n)
        m = int(m)

        mat = np.zeros((n,m), dtype=int)

        for i in range (n):
            mat[i] = file.readline().split(" ")

        #xd = x de départ et xa = x d'arrivée

        xd, yd, xa, ya, direction = file.readline().split(" ")

        direction = direction.rstrip("\n")
        direction = direction.upper()


        if direction == "NORD" :
            direction = NORD

        if direction == "SUD" :
            direction = SUD

        if direction == "EST":
            direction = EST

        if direction == "OUEST":
            direction = OUEST

        return mat, int(xd), int(yd), int(xa), int(ya), direction

def forbidden_edges(mat):
    """
    Renvoie la liste des coordonnées des intersections interdites de la grille
    """

    forbidden_list = set()

    for i in range (len(mat)) :
        for j in range (len(mat[0])):
            if mat[i][j] == 1 :
                forbidden_list.add((i,j))
                forbidden_list.add((i+1,j))
                forbidden_list.add((i,j+1))
                forbidden_list.add((i+1,j+1))

    return forbidden_list


def get_neighbors(mat, forbidden_list, i, j, d):
    """
    :param mat: matrice des obstacles
    :param i: position abscisses
    :param j: position ordonnées
    :param d:direction (nord, sud...)
    :return: liste des voisins du noeud
    """
    liste = []
    liste.append((i, j, (d+1)%4))
    liste.append((i, j, (d-1)%4))

    n = len(mat)
    m = len(mat[0])

    x = 1

    if d == NORD :
        while i-x >= 0 and x<=3:
            if (i-x,j) not in forbidden_list:
                liste.append((i-x,j,d))
            else :
                break
            x += 1

    if d == SUD :
        while i+x <= n and x<=3:
            if (i+x,j) not in forbidden_list:
                liste.append((i+x,j,d))
            else :
                break
            x += 1

    if d == EST :
        while j+x <= m and x<=3:
            if (i,j+x) not in forbidden_list:
                liste.append((i,j+x,d))
            else :
                break
            x += 1

    if d == OUEST :
        while j-x >= 0 and x<=3:
            if (i,j-x) not in forbidden_list:
                liste.append((i,j-x,d))
            else :
                break
            x += 1

    return liste

def create_graph(mat):
    """
    Renvoi un dictionnaire correspondant aux relations entre les noeuds
    :param mat: matrice des obstacles
    :return: dictionnaire
    """
    n = len(mat)
    m = len(mat[0])

    dictionary = dict()

    forbidden_list = forbidden_edges(mat)
    # print("forbidden list : ", forbidden_list)

    for i in range (n+1):
        for j in range (m+1):
            if (i,j) not in forbidden_list :
                dictionary[(i,j,NORD)] = get_neighbors(mat,forbidden_list,i,j,NORD)
                dictionary[(i, j, SUD)] = get_neighbors(mat,forbidden_list, i, j, SUD)
                dictionary[(i, j, EST)] = get_neighbors(mat,forbidden_list, i, j, EST)
                dictionary[(i, j, OUEST)] = get_neighbors(mat,forbidden_list, i, j, OUEST)

    return dictionary

def bfs(G, start, end):
    """
    :param G: graphe représenté sous forme de dictionnaire
    :param start: point de départ
    :param end: point d'arrivée
    :return:
    """
    Q = deque([(0, [start])])
    explored = {start}
    min_distances = {start : 0}

    while Q:
        distance, path = Q.popleft()
        node = path[-1]
        min_distances[node] = distance

        i, j, d = node

        if (i,j) == end :
            return path

        for neighbor in G[(i,j,d)]:
            if neighbor not in explored:
                explored.add(neighbor)
                Q.append((distance+1, path+[neighbor]))

    return []


def calculate_heuristic(curr, end):
    """
    Calculate the heuristic
    
    :param curr: current position
    :param end: end position
    """
    #manhattan distance
    i1, j1, _ = curr
    i2, j2 = end
    x = abs(i1-i2)
    if (x %3) == 0:
        x = x // 3
    else:
        x = x//3 +1
    
    y = abs(j1-j2)
    if (y %3) == 0:
        y = y // 3
    else:
        y = y//3 +1

    return x + y

def reconstruct_path(came_from, end):
    """
    Reconstruct_path
    
    :param came_from: Description
    :param end: Description
    """
    #print("debut reconstruct")
    path = [end]
    parent = came_from[end]
    while parent :
        path.append(parent)
        parent = came_from[parent]
    #print("reconstructed: ", path)
    return path[::-1]


def astar(graph, start, end):
    """
    Shortest path en utilisant l'algorithme A*
    
    :param graph: graphe représenté sous forme de dictionnaire
    :param start: point de départ
    :param end: point d'arrivée
    :return:
    """

    #open: to be visited
    #g = distance du depart
    #h = heuristique
    #f = g+h
    g = {start: 0}
    h = calculate_heuristic(start, end)
    f = {start : g[start] + h}
    came_from = {start: None}

    #open_list = [(g, h, g+h, [start])]
    open_list = []
    heapq.heappush(open_list, (h,start))

    #closedDict = dict([(k, False) for k in graph.keys()])

    while open_list:
        # print("open_list: ", open_list)
        _, curr = heapq.heappop(open_list)
        # print("curr: ", curr)
        # print("g[curr]",g[curr])
        # print("f[curr]",f[curr])
        i, j, _ = curr
        
        if (i,j) == end:
            #print("came_from: ", came_from)
            path = reconstruct_path(came_from, curr)
            #print("path dans a star ", path)
            return path

        for neighbor in graph[curr]:
            # print("neighbor: ", neighbor)
            new_g = g[curr] + 1 #car toutes les arêtes du graphe ont un poids de 1
            # print("new_g: ", new_g)
            if neighbor not in g or new_g < g[neighbor]:
                came_from[neighbor] = curr
                # print("came_from[neighbor]: ", came_from[neighbor])
                g[neighbor] = new_g
                # print("g[neighbor]: ", g[neighbor])
                f[neighbor] = new_g + calculate_heuristic(neighbor, end)
                # print("f[neighbor]: ", f[neighbor])
                heapq.heappush(open_list, (f[neighbor], neighbor))
    return None


def write_file(filename, result):
    """
    Docstring for write_file
    
    :param filename: Description
    :param result: Description
    """

    res = str(len(result)-1) #taille du resultat, -1 car on ne compte pas la position de depart
    for i in range(len(result)-1):
        # print("result[i]", result[i])
        x_curr, y_curr, d_curr = result[i]
        x_next, y_next, d_next = result[i+1]
        
        if x_curr != x_next:
            res += " a" + str(abs(x_curr - x_next))
        elif y_curr != y_next:
            res += " a" + str(abs(y_curr - y_next))
        else:
            delta = (d_curr - d_next) % 4
            if delta == 1:
                res += " G"
            else:
                res += " D"

    with open(filename, "w") as f:
        f.write(res)


def generate_instance_grid(n, m, o):
    """
    Generate instances based on the size of the grid
    
    :param n: number of lines of the grid
    :param m: number of columns of the grid
    :param o: number of obstacles of the grid

    """
    mat = np.zeros((n,m), dtype=int)
    obstacles = 0
    while obstacles < o:
        x = random.randint(0,n-1)
        y = random.randint(0,m-1)
        if mat[x][y] == 0 and not(x== 0 and y==0):
            mat[x][y] = 1
            obstacles += 1
    return mat, create_graph(mat)

def generate_instance_obs(o):
    """
    Generate instances based on the number of obstacles
    
    :param o: number of obstacles
    """
    mat = np.zeros((20,20), dtype=int)
    obstacles = 0
    while obstacles < o:
        x = random.randint(0,19)
        y = random.randint(0,19)
        if mat[x][y] == 0 and not(x== 0 and y==0):
            mat[x][y] = 1
            obstacles += 1
    return mat, create_graph(mat)

def test_grid():
    """
    Test pour la génération d'instances de graphe selon la taille de la matrice
    """
    list_astar = []
    list_bfs = []
    for i in range(1,6):
        print("i: ", i)
        t_a = 0
        t_bfs = 0
        for j in range(1000):
            _, graphe = generate_instance_grid(i*10, i*10, i*10)
            start = time.time()
            _ = astar(graphe, (0,0,0), (i*10, i*10))
            end = time.time()
            t_a += end - start

            start = time.time()
            _ = bfs(graphe, (0, 0, 0), (i * 10, i * 10))
            end = time.time()
            t_bfs += end - start

        list_astar.append(t_a/1000)
        list_bfs.append(t_bfs/1000)
    return list_astar, list_bfs

def plot_test_grid(list_astar, list_bfs):
    """
    Plot pour le test de la génération d'instances selon la taille
    
    :param list: list of the times taken for each randomly generated graph
    """
    plt.plot([10, 20, 30, 40, 50], list_astar, color="blue", label="A*")
    plt.plot([10, 20, 30, 40, 50], list_bfs, color="red", label="BFS")
    # plt.plot(liste_n, 0.00001*liste_n, color="red", label="O(n)")
    # plt.plot(liste_n, 0.000001*(liste_n**2), color="orange", label="O(n²)")
    # plt.plot(liste_n, 0.00000001*(2**liste_n), color="green", label="O(2ⁿ)")
    plt.xlabel("Taille de la grille")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction de la taille de la grille")
    plt.legend()
    plt.show()
    

def test_obs():
    """
    Test pour la génération d'instances de graphe selon le nombre d'obstacles
    """
    list_sol_astar = [] #grilles pour lesquelles une solution a été trouvée
    list_sol_bfs = []
    list_no_sol = [] #grilles pour lesquelles il n'y avait pas de solution
    for i in range(1,6):
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
                mat, graphe = generate_instance_obs(i*10)
                start = time.time()
                a = astar(graphe, (0,0,0), (20, 20))
                end = time.time()
                redo += 1
                if a :
                    t_sol_a += end - start
                    start = time.time()
                    bfs_sol = bfs(graphe, (0, 0, 0), (20, 20))
                    end = time.time()
                    t_sol_bfs += end - start
                #else :
                #   t_no_sol += end - start
                #  n_sol_not_found += 1


            if redo == max_redo:
                print("no sol trouvée pour i = ", i, " et j = ", j)
                n_sol_found -= 1
        print("nb sol ", n_sol_found)
        print("nb pas sol ", n_sol_not_found)
        list_sol_astar.append(t_sol_a/n_sol_found)
        list_sol_bfs.append(t_sol_bfs / n_sol_found)
        #list_no_sol.append(t_no_sol/n_sol_not_found)
    return list_sol_astar, list_sol_bfs

def plot_test_obs_solution(list_sol_a, list_sol_bfs):
    """
    Plot pour le test de la génération d'instances d'obstacles
    
    :param list_sol: list of the times taken for each randomly generated graph
    """
    plt.plot([10,20,30,40,50], list_sol_a, color="blue", label = "A*")
    plt.plot([10, 20, 30, 40, 50], list_sol_bfs, color="red", label = "BFS")
    # plt.plot(liste_n, 0.00001*liste_n, color="red", label="O(n)")
    # plt.plot(liste_n, 0.000001*(liste_n**2), color="orange", label="O(n²)")
    # plt.plot(liste_n, 0.00000001*(2**liste_n), color="green", label="O(2ⁿ)")
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
    # plt.plot(liste_n, 0.00001*liste_n, color="red", label="O(n)")
    # plt.plot(liste_n, 0.000001*(liste_n**2), color="orange", label="O(n²)")
    # plt.plot(liste_n, 0.00000001*(2**liste_n), color="green", label="O(2ⁿ)")
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'exécution en fonction du nombre d'obstacles dans une grille 20x20, aucun chemin possible")
    plt.show()



if __name__ == "__main__" :
    mat, xd, yd, xa, ya, direction = read_file("exemple_entree.txt")

    forbidden_list = forbidden_edges(mat)
    #print("forbidden list : ", forbidden_list)
    # # print(len(forbidden_list))

    graphe = create_graph(mat)
    # # for u in graphe.keys():
    # #     print("sommet : ", u)
    # #     print("voisins : ", graphe[u])
    # #     print("")

    dictionnaire = create_graph(mat)
    bfs_sol = bfs(dictionnaire, (xd,yd,direction), (xa,ya))
    print("BFS : ", bfs_sol)

    # a = astar(graphe, (xd,yd, direction), (xa,ya))
    # print("A*: ", len(a),a)

    # write_file("test_bfs.txt", bfs_sol) 
    # write_file("test_astar.txt", a)

    #la, lbfs = test_grid()
    #plot_test_grid(la, lbfs)
    #list_sol_a, list_sol_bfs = test_obs()
    #plot_test_obs_no_solution(list_no_sol)
    #plot_test_obs_solution(list_sol_a, list_sol_bfs)
    # #1. Créer un graphe NetworkX
    # G = nx.DiGraph()

    # #2. Ajouter les arêtes depuis le dictionnaire
    # for u, neighbors in graphe.items():
    #   for v in neighbors:
    #      G.add_edge(u, v)

    # #3. Desiner
    # pos = nx.spring_layout(G)  # calcule une position des noeuds
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    # plt.show()
    
    # #mat = [[0,0], [0,0]]
    # #graphe = create_graph(mat)

    # 1. Créer un graphe NetworkX
    #G = nx.DiGraph()

    # 2. Ajouter les arêtes depuis le dictionnaire
    #for u, neighbors in graphe.items():
     #   for v in neighbors:
      #      G.add_edge(u, v)

    # 3. Dessiner
    #pos = nx.spring_layout(G)  # calcule une position des noeuds
    #nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    #plt.show()

    #mat = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    #graphe = create_graph(mat)
    #print(graphe)
    #a = astar(graphe, (0, 0, 2), (3, 3))
    #print("A*: ", len(a), a)

    #print(graphe)
    #a = astar(graphe, (0,0,2), (2,2))
    #print("A*: ", len(a),a)

