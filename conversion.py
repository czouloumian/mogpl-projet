import numpy as np
from collections import deque

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
    liste.append((i, j, (d-1) % 4))

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
        while i+x < n and x<=3:
            if (i+x,j) not in forbidden_list:
                liste.append((i+x,j,d))
            else :
                break
            x += 1

    if d == EST :
        while j+x < m and x<=3:
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
    :param end: point d'arrivé
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






if __name__ == "__main__" :
    mat, xd, yd, xa, ya, direction = read_file("exemple_entree.txt")

    forbidden_list = forbidden_edges(mat)
    print("forbidden list : ", forbidden_list)
    print(len(forbidden_list))

    graphe = create_graph(mat)
    for u in graphe.keys():
        print("sommet : ", u)
        print("voisins : ", graphe[u])
        print("")

    dictionnaire = create_graph(mat)
    print("BFS : ", bfs(dictionnaire, (xd,yd,direction), (xa,ya)))






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