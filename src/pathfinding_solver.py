import heapq
import math
from collections import deque

def bfs(G, start, end):
    """
    Algorithme BFS

    :param G: graphe représenté sous forme de dictionnaire
    :param start: point de départ
    :param end: point d'arrivée
    :return: Le meilleur chemin, si un chemin existe, une liste vide sinon
    """
    Q = deque([(0, [start])])
    explored = {start}
    min_distances = {start: 0}

    while Q:
        distance, path = Q.popleft()
        node = path[-1]
        min_distances[node] = distance

        i, j, d = node

        if (i, j) == end:
            return path

        for neighbor in G[(i, j, d)]:
            if neighbor not in explored:
                explored.add(neighbor)
                Q.append((distance + 1, path + [neighbor]))

    return []


def calculate_heuristic(curr, end):
    """
    Calcule l'heuristique pour l'algorithme A*

    :param curr: current position
    :param end: end position
    :return: l'heuristique
    """
    i1, j1, _ = curr
    i2, j2 = end

    return math.ceil(abs(i1 - i2)/3) + math.ceil(abs(j1 - j2)/3)


def reconstruct_path(came_from, end):
    """
    Reconstruit le chemin depuis le dictionnaire came_from

    :param came_from: Un dictionnaire contenant, pour chaque sommet, son prédécesseur dans le chemin
    :param end: Le point d'arrivée
    :return: le chemin reconstruit
    """
    path = [end]
    parent = came_from[end]
    while parent:
        path.append(parent)
        parent = came_from[parent]
    return path[::-1]


def astar(graph, start, end):
    """
    Algorithme A*

    :param graph: graphe représenté sous forme de dictionnaire
    :param start: point de départ
    :param end: point d'arrivée
    :return: le meilleur chemin si un chemin existe, une liste vide sinon
    """

    g = {start: 0}
    h = calculate_heuristic(start, end)
    f = {start: g[start] + h}
    came_from = {start: None}

    open_list = []
    heapq.heappush(open_list, (h, start))

    while open_list:
        _, curr = heapq.heappop(open_list)
        i, j, _ = curr

        if (i, j) == end:
            path = reconstruct_path(came_from, curr)
            return path

        for neighbor in graph[curr]:
            new_g = g[curr] + 1  # car toutes les arêtes du graphe ont un poids de 1
            if neighbor not in g or new_g < g[neighbor]:
                came_from[neighbor] = curr
                g[neighbor] = new_g
                f[neighbor] = new_g + calculate_heuristic(neighbor, end)
                heapq.heappush(open_list, (f[neighbor], neighbor))
    return []
