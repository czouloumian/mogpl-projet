import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import projet
import PL_projet


def plot_grid(m, n, p):
    grid= PL_projet.solution_linear_program(m,n,p)

    plt.imshow(grid, cmap="gray_r")
    plt.title(f"Grille {m}x{n} avec {p} obstacles")
    plt.show()


def generate(): #fonction generee par le bouton 
    try:
        m = int(entry_m.get())
        n = int(entry_n.get())
        p = int(entry_p.get())

        if n <= 0:
            raise ValueError("La taille N doit être positive.")
        if not (0 <= p <= m * n):
            raise ValueError("P doit être entre 0 et M*N.")

        plot_grid(m, n, p)

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

def generate_path():
    global grid

    if grid is None:
        messagebox.showerror("Erreur", "Génère d'abord une grille !")
        return

    try:
        i = int(entry_i.get())
        j = int(entry_j.get())
        d = int(entry_d.get())

        if not (0 <= d <= 3):
            raise ValueError("La direction doit être entre 0 et 3.")

        path = projet.astar(projet.create_graph(grid), i, j, d)  

        plt.imshow(grid, cmap="gray_r")
        xs = [pos[1] for pos in path] 
        ys = [pos[0] for pos in path]
        plt.plot(xs, ys, marker="o")
        plt.title("Chemin trouvé")
        plt.show()

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))



root = tk.Tk()
root.title("Génération de grille")

tk.Label(root, text="Nombre de lignes (M)").pack()
entry_m = tk.Entry(root)
entry_m.pack()

tk.Label(root, text="Nombre de colonnes (N)").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Label(root, text="Nombre d'obstacles (P)").pack()
entry_p = tk.Entry(root)
entry_p.pack()

tk.Button(root, text="Générer la grille", command=generate).pack(pady=10)

tk.Label(root, text="Point de départ i (ligne)").pack()
entry_i = tk.Entry(root)
entry_i.pack()

tk.Label(root, text="Point de départ j (colonne)").pack()
entry_j = tk.Entry(root)
entry_j.pack()

tk.Label(root, text="Direction d (0=N, 1=E, 2=S, 3=O)").pack()
entry_d = tk.Entry(root)
entry_d.pack()

tk.Button(root, text="Générer le chemin", command=generate_path).pack(pady=10)

root.mainloop()
