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