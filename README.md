# Projet MOGPL

Caroline ZOULOUMIAN et Mariana DUARTE FERREIRA

Ce projet vise à optimiser le déplacement d’un robot sur une grille (N x M) contenant des obstacles, sur lesquels le robot ne peut pas passer.  
Le robot peut avancer de 1 à 3 cases ou tourner à gauche/droite, chaque action durant une seconde.  
L’objectif est de calculer le temps minimal nécessaire pour atteindre un point d’arrivée depuis un point de départ donné.

## I - Exécution du code

Le programme peut être exécuté de deux manières :  

### a) Avec interface graphique

1. Assurez-vous que Python (version >= 3.8) est installé sur votre machine.
2. Accédez au répertoire du projet via le terminal :
    ```bash
    cd <CHEMIN_DU_PROJET>/src
    ```
3. Lancez le fichier suivant :
    ```bash
    python3 interface.py
    ```
4. Saisissez :  
    - La taille de la grille (M lignes et N colonnes)  
    - Le nombre d'obstacles P
5. L’interface affichera la grille générée.  
6. Définissez les points de départ et d'arrivée du robot.  
7. Si un chemin existe, le chemin optimal sera affiché.

### b) En mode fichier

Si vous disposez d'un fichier (au format décrit en section II) contenant la grille et les points de départ/arrivée :  

1. Assurez-vous que Python (version >= 3.8) est installé sur votre machine.  
2. Accédez au répertoire du projet via le terminal :
    ```bash
    cd <CHEMIN_DU_PROJET>/src
    ```
3. Lancez le fichier suivant :
    ```bash
    python3 main.py
    ```
4. Le programme demandera le nom du fichier d’entrée (ou son chemin absolu/relatif).  

5. Deux algorithmes calculeront le chemin optimal : **BFS** et **A\***.  

6. La solution sera affichée à l’écran et peut être sauvegardée dans un fichier.

## II - Format du fichier d'entrée

1. **Première ligne** :  
Deux entiers M et N séparés par un espace, représentant le nombre de lignes et de colonnes de la grille.  

Exemple :
9 10


2. **M lignes suivantes** :  
Chacune contient N nombres séparés par des espaces :  
- `0` pour une case libre  
- `1` pour un obstacle  

Exemple :

0 0 0 0 0 0 1 0 0 0 

0 0 0 0 0 0 0 0 1 0 

0 0 0 1 0 0 0 0 0 0 

0 0 1 0 0 0 0 0 0 0


3. **Points de départ et d'arrivée** :  
Quatre entiers suivis de l’orientation du robot :  

D1 D2 F1 F2 direction


- `D1, D2` : coordonnées du point de départ  
- `F1, F2` : coordonnées du point d’arrivée  
- `direction` : orientation initiale (`nord`, `sud`, `est`, `ouest`)  

Exemple :
7 2 2 7 sud

4. **Fin du fichier** :  
Une ligne contenant `0 0` indique la fin des instances.
