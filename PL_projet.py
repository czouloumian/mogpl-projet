import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solution_linear_program(M,N,P):
    """
    Retourne la solution optimale pour le programme lineaire.
    :param M: nombre de lignes de la grille
    :param N: nombre de colonnes de la grille
    :param P: nombre d'obstacles à poser
    :return: la grille avec les obstacles placés
    """

    np.random.seed(42)
    w = np.random.randint(0, 1001, size=(M, N))

    model = gp.Model("PL_projet")

    x = model.addVars(M, N, vtype=GRB.BINARY, name="x")

    model.setObjective(gp.quicksum(w[i,j]*x[i,j] for i in range(M) for j in range(N)), GRB.MINIMIZE)

    model.addConstr(gp.quicksum(x[i,j] for i in range(M) for j in range(N)) == P) #nb obstacles = P

    for i in range(M): #qte obstacles par ligne <= 2P/M
        model.addConstr(gp.quicksum(x[i,j] for j in range(N)) <= 2*P/M)

    for j in range(N): #qte obstacles par colonne <= 2P/N
        model.addConstr(gp.quicksum(x[i,j] for i in range(M)) <= 2*P/N)

    for i in range(M):
        for j in range(1, N-1):
            model.addConstr(x[i,j-1] + x[i,j+1] <= 1 + x[i,j])

    for j in range(N):
        for i in range(1, M-1):
            model.addConstr(x[i-1,j] + x[i+1,j] <= 1 + x[i,j])

    model.optimize()

    grid = np.zeros((M,N), dtype=int)
    for i in range(M):
        for j in range(N):
            grid[i,j] = int(x[i,j].X)

    return grid
