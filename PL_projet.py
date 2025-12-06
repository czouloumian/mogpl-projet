import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Paramètres
M = 20  # nombre de lignes
N = 20  # nombre de colonnes
P = 8  # nombre total d'obstacles

# Poids aléatoires
np.random.seed(42)
w = np.random.randint(0, 1001, size=(M, N))

# Création du modèle
model = gp.Model("PL_projet")

# Variables binaires
x = model.addVars(M, N, vtype=GRB.BINARY, name="x")

# Fonction objectif
model.setObjective(gp.quicksum(w[i,j]*x[i,j] for i in range(M) for j in range(N)), GRB.MINIMIZE)

# Contrainte: nombre total d'obstacles = P
model.addConstr(gp.quicksum(x[i,j] for i in range(M) for j in range(N)) == P)

# Contrainte: max 2P/M par ligne
for i in range(M):
    model.addConstr(gp.quicksum(x[i,j] for j in range(N)) <= 2*P/M)

# Contrainte: max 2P/N par colonne
for j in range(N):
    model.addConstr(gp.quicksum(x[i,j] for i in range(M)) <= 2*P/N)

# Contrainte: pas de séquence 101 horizontale
for i in range(M):
    for j in range(1, N-1):
        model.addConstr(x[i,j-1] + x[i,j+1] <= 1 + x[i,j])

# Contrainte: pas de séquence 101 verticale
for j in range(N):
    for i in range(1, M-1):
        model.addConstr(x[i-1,j] + x[i+1,j] <= 1 + x[i,j])

# Résolution
model.optimize()

# Affichage de la grille
grid = np.zeros((M,N), dtype=int)
for i in range(M):
    for j in range(N):
        grid[i,j] = int(x[i,j].X)
print("Grille optimale :")
print(grid)
