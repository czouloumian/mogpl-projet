import numpy as np

NORD = 0
EST = 1
SUD = 2
OUEST = 3

def read_file(file_name: str):
    """
    Lit le fichier texte avec les données de départ
    :param file_name: Nom du fichier texte
    :return: La matrice de la grille, le point de départ, la direction de départ et le point d'arrivée
    """
    with open(file_name, "r") as file:
        m, n = file.readline().split(" ")

        m = int(m)
        n = int(n)

        mat = np.zeros((m, n), dtype=int)

        for i in range(m):
            mat[i] = file.readline().split(" ")

        # xd = x de départ et xa = x d'arrivée
        xd, yd, xa, ya, direction = file.readline().split(" ")

        direction = direction.rstrip("\n")
        direction = direction.upper()

        if direction == "NORD":
            direction = NORD

        if direction == "SUD":
            direction = SUD

        if direction == "EST":
            direction = EST

        if direction == "OUEST":
            direction = OUEST

        return mat, int(xd), int(yd), int(xa), int(ya), direction

def translate_direction(direction):
    if direction == NORD:
        return "nord"
    elif direction == EST:
        return "est"
    elif direction == SUD:
        return "sud"
    elif direction == OUEST:
        return "ouest"

def instance_out(filename, mat, start, end):
    """
    Sauvegarde une instance de graphe dans un fichier
    :param filename: Nom du fichier
    :param mat: Matrice de la grille
    :param start: Point de départ
    :param end: Point d'arrivée
    """
    m = str(len(mat))
    n = str(len(mat[0]))
    xd, yd, direction = start
    xa, ya = end
    direction = translate_direction(direction)
    with open(filename, "a") as f:
        line = m + " " + n + "\n"
        f.write(line)
        for i in mat:
            line = ""
            for n in i:
                line += str(n) + " "
            line += "\n"
            f.write(line)
        line = str(xd) + " " + str(yd) + " " + str(xa) + " " + str(ya) + " " + str(direction) + "\n"
        f.write(line)
        line = "0 0"
        f.write(line)
        f.write("\n")
    return


def result_out(filename, result):
    """
    Traduit le chemin et le stocke dans un fichier

    :param filename: Nom du fichier
    :param result: Chemin du résultat
    """

    res = str(len(result) - 1)  # taille du resultat, -1 car on ne compte pas la position de depart
    # si aucun chemin existe, alors result = [] donc on ajoute -1 au fichier
    for i in range(len(result) - 1):
        x_curr, y_curr, d_curr = result[i]
        x_next, y_next, d_next = result[i + 1]

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


def result_out_many(filename, paths):
    """
    Traduit les résultats de plusieurs instances et les stocke dans un fichier

    :param filename: Nom du fichier
    :param paths: Liste avec les chemins de chacune des instances
    """
    with open(filename, "w") as f:
        for result in paths:
            res = str(len(result) - 1)  # taille du resultat, -1 car on ne compte pas la position de depart.
            #si aucun chemin existe, alors result = [] donc on ajoute -1 au fichier
            for i in range(len(result) - 1):
                x_curr, y_curr, d_curr = result[i]
                x_next, y_next, d_next = result[i + 1]

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
        f.write(res + "\n")


