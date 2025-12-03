import numpy as np
from collections import deque
import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt

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
    print("forbidden list : ", forbidden_list)

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
            return distance, path

        for neighbor in G[(i,j,d)]:
            if neighbor not in explored:
                explored.add(neighbor)
                Q.append((distance+1, path+[neighbor]))

    return float("inf"), []


def calculate_heuristic(curr, end):
    """
    Calculate the heuristic
    
    :param curr: current position
    :param end: end position
    """
    #manhattan distance
    i1, j1, _ = curr
    i2, j2 = end
    print("heuristique i1, j1,i2, j2", i1, j1, i2, j2)
    print("h ", abs(i1-i2) + abs(j1-j2))
    return abs(i1-i2) + abs(j1-j2)

def reconstruct_path(came_from, end):
    """
    Reconstruct_path
    
    :param came_from: Description
    :param end: Description
    """
    #print("debut reconstruct")
    path = [end]
    parent = came_from[end]
    while parent != None:
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
        print("open_list: ", open_list)
        _, curr = heapq.heappop(open_list)
        print("curr: ", curr)
        print("g[curr]",g[curr])
        print("f[curr]",f[curr])
        i, j, _ = curr
        
        if (i,j) == end:
            #print("came_from: ", came_from)
            path = reconstruct_path(came_from, curr)
            #print("path dans a star ", path)
            return path

        for neighbor in graph[curr]:
            print("neighbor: ", neighbor)
            new_g = g[curr] + 1 #car toutes les arêtes du graphe ont un poids de 1
            print("new_g: ", new_g)
            if neighbor not in g or new_g < g[neighbor]:
                came_from[neighbor] = curr
                print("came_from[neighbor]: ", came_from[neighbor])
                g[neighbor] = new_g
                print("g[neighbor]: ", g[neighbor])
                f[neighbor] = new_g + calculate_heuristic(neighbor, end)
                print("f[neighbor]: ", f[neighbor])
                heapq.heappush(open_list, (f[neighbor], neighbor))
    return None


if __name__ == "__main__" :
    mat, xd, yd, xa, ya, direction = read_file("exemple_entree.txt")

    # forbidden_list = forbidden_edges(mat)
    # print("forbidden list : ", forbidden_list)
    # print(len(forbidden_list))

    graphe = create_graph(mat)
    # for u in graphe.keys():
    #     print("sommet : ", u)
    #     print("voisins : ", graphe[u])
    #     print("")

    dictionnaire = create_graph(mat)
    print("BFS : ", bfs(dictionnaire, (xd,yd,direction), (xa,ya)))

    a = astar(graphe, (xd,yd, direction), (xa,ya))
    print("A*: ", len(a),a)

    #1. Créer un graphe NetworkX
    G = nx.DiGraph()

    #2. Ajouter les arêtes depuis le dictionnaire
    for u, neighbors in graphe.items():
      for v in neighbors:
         G.add_edge(u, v)

    #3. Desiner
    pos = nx.spring_layout(G)  # calcule une position des noeuds
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()
    
    #mat = [[0,0], [0,0]]
    #graphe = create_graph(mat)

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


# conversion du fichier d'entrée en graphe

#infos à prendre du fichier txt
#       - dimensions
#       - coordonnees des obstacles (obstacle = 4 sommets de la grille + 4 aretes où in ne peut pas aller)
#       - directions nord-sud-est-ouest du départ
#       - coordonnees du depart

#graphe créé:
#       - sommets: 4 par sommet car 4 directions possible. ex: (0,0) nord
#       - peut tourner à droite ou à gauche, de 1. donc nord <-> est, nord <-> ouest, sud <-> est, sud <-> ouest
#       - peut avancer de 1, 2 ou 3 cases
#       - aretes pour tourner: poids de 1
#       - aretes avancer de 1, 2 ou 3: poids de 1

#algo: DFS modifié
#       - racine: point de départ avec direction
#       - subtilité: pour éviter les boucles, il faut ne pas pouvoir retourner un noeud déjà visité dans une même branche