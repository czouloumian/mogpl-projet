NORD = 0
EST = 1
SUD = 2
OUEST = 3

def forbidden_edges(mat):
    """
    Renvoie la liste des coordonnées des intersections interdites de la grille

    :param mat: la matrice de la grille
    :return: la liste des coordonnées interdites
    """

    forbidden_list = set()

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 1:
                forbidden_list.add((i, j))
                forbidden_list.add((i + 1, j))
                forbidden_list.add((i, j + 1))
                forbidden_list.add((i + 1, j + 1))

    return forbidden_list


def get_neighbors(mat, forbidden_list, i, j, d):
    """
    Renvoie les voisins du noeud

    :param mat: matrice des obstacles
    :param i: position abscisses
    :param j: position ordonnées
    :param d:direction (nord, sud...)
    :return: liste des voisins du noeud
    """
    liste = []
    liste.append((i, j, (d + 1) % 4))
    liste.append((i, j, (d - 1) % 4))

    m = len(mat)
    n = len(mat[0])

    x = 1

    if d == NORD:
        while i - x >= 0 and x <= 3:
            if (i - x, j) not in forbidden_list:
                liste.append((i - x, j, d))
            else:
                break
            x += 1

    if d == SUD:
        while i + x <= m and x <= 3:
            if (i + x, j) not in forbidden_list:
                liste.append((i + x, j, d))
            else:
                break
            x += 1

    if d == EST:
        while j + x <= n and x <= 3:
            if (i, j + x) not in forbidden_list:
                liste.append((i, j + x, d))
            else:
                break
            x += 1

    if d == OUEST:
        while j - x >= 0 and x <= 3:
            if (i, j - x) not in forbidden_list:
                liste.append((i, j - x, d))
            else:
                break
            x += 1

    return liste


def create_graph(mat):
    """
    Renvoie un dictionnaire correspondant aux relations entre les noeuds

    :param mat: matrice des obstacles
    :return: dictionnaire
    """
    m = len(mat)
    n = len(mat[0])

    dictionary = dict()

    forbidden_list = forbidden_edges(mat)

    for i in range(m + 1):
        for j in range(n + 1):
            if (i, j) not in forbidden_list:
                dictionary[(i, j, NORD)] = get_neighbors(mat, forbidden_list, i, j, NORD)
                dictionary[(i, j, SUD)] = get_neighbors(mat, forbidden_list, i, j, SUD)
                dictionary[(i, j, EST)] = get_neighbors(mat, forbidden_list, i, j, EST)
                dictionary[(i, j, OUEST)] = get_neighbors(mat, forbidden_list, i, j, OUEST)

    return dictionary



