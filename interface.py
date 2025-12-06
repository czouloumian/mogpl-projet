import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import projet
import PL_projet

grid = None  # variable globale

def show_grid_window(m, n, p):
    global grid
    grid = PL_projet.solution_linear_program(m, n, p)

    # Nouvelle fenêtre
    grid_window = tk.Toplevel(root)
    grid_window.title("Grille et saisie du chemin")

    # Frames pour mettre la grille à gauche et les entrées à droite
    frame_grid = tk.Frame(grid_window)
    frame_grid.pack(side=tk.LEFT, padx=10, pady=10)

    frame_inputs = tk.Frame(grid_window)
    frame_inputs.pack(side=tk.RIGHT, padx=10, pady=10)

    # Figure Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap="gray_r")

    # Ajouter les railles
    ax.set_xticks([x - 0.5 for x in range(1, grid.shape[1])])
    ax.set_yticks([y - 0.5 for y in range(1, grid.shape[0])])
    ax.grid(color='black', linewidth=1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.set_title(f"Grille {m}x{n} avec {p} obstacles")
    canvas = FigureCanvasTkAgg(fig, master=frame_grid)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Saisie départ/direction/arrivée
    tk.Label(frame_inputs, text="Ligne de départ").pack()
    entry_i = tk.Entry(frame_inputs)
    entry_i.pack()

    tk.Label(frame_inputs, text="Colonne de départ").pack()
    entry_j = tk.Entry(frame_inputs)
    entry_j.pack()

    tk.Label(frame_inputs, text="Direction initiale d (NORD = 0, EST = 1, SUD = 2, OUEST = 3)").pack()
    entry_d = tk.Entry(frame_inputs)
    entry_d.pack()

    tk.Label(frame_inputs, text="Ligne d'arrivée").pack()
    entry_dest_i = tk.Entry(frame_inputs)
    entry_dest_i.pack()

    tk.Label(frame_inputs, text="Colonne d'arrivée").pack()
    entry_dest_j = tk.Entry(frame_inputs)
    entry_dest_j.pack()

    def generate_path_in_window():
        try:
            i = int(entry_i.get())
            j = int(entry_j.get())
            d = int(entry_d.get())
            dest_i = int(entry_dest_i.get())
            dest_j = int(entry_dest_j.get())

            if not (0 <= d <= 3):
                raise ValueError("Direction doit être entre 0 et 3")
            if not (0 <= i <= len(grid)) or not (0 <= j <= len(grid[0])):
                raise ValueError("Point de départ hors de la grille")
            if not (0 <= dest_i <= len(grid)) or not (0 <= dest_j <= len(grid[0])):
                raise ValueError("Point d'arrivée hors de la grille")

            path = projet.astar(projet.create_graph(grid), (i, j, d), (dest_i, dest_j))

            # Tracer la grille
            ax.clear()
            ax.imshow(grid, cmap="gray_r")
            ax.set_xticks([x - 0.5 for x in range(1, grid.shape[1])])
            ax.set_yticks([y - 0.5 for y in range(1, grid.shape[0])])
            ax.grid(color='black', linewidth=1)
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            # Tracer le chemin sur les railles (déplacement du milieu d'une case à l'autre)
            if path:
                for idx in range(len(path) - 1):
                    i0, j0, _ = path[idx]
                    i1, j1, _ = path[idx + 1]

                    # Conversion : soustraire 1 pour passer de 1-index à 0-index
                    i0 -= 1
                    j0 -= 1
                    i1 -= 1
                    j1 -= 1

                    # Ignorer rotations sur place
                    if i0 == i1 and j0 == j1:
                        continue

                    # Horizontal ?
                    if i0 == i1:
                        y = i0 + 0.5  # milieu du bord horizontal
                        step = 1 if j1 > j0 else -1
                        for jj in range(j0, j1, step):
                            ax.plot([jj + 0.5, jj + 0.5 + step], [y, y], color='red', linewidth=2, marker='o')

                    # Vertical ?
                    elif j0 == j1:
                        x = j0 + 0.5  # milieu du bord vertical
                        step = 1 if i1 > i0 else -1
                        for ii in range(i0, i1, step):
                            ax.plot([x, x], [ii + 0.5, ii + 0.5 + step], color='red', linewidth=2, marker='o')


                ax.set_title("Chemin trouvé")
            else :
                ax.set_title("Aucun chemin trouvé")

            canvas.draw()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(frame_inputs, text="Générer le chemin", command=generate_path_in_window).pack(pady=10)

def generate_grid_main():
    try:
        m = int(entry_m.get())
        n = int(entry_n.get())
        p = int(entry_p.get())

        if m <= 0 or n <= 0:
            raise ValueError("M et N doivent être positifs")
        if not (0 <= p <= m * n):
            raise ValueError("P doit être entre 0 et M*N")

        show_grid_window(m, n, p)
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

# --- fenêtre principale ---
root = tk.Tk()
root.title("Projet MOGPL")

tk.Label(root, text="Nombre de lignes (M)").pack()
entry_m = tk.Entry(root)
entry_m.pack()

tk.Label(root, text="Nombre de colonnes (N)").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Label(root, text="Nombre d'obstacles (P)").pack()
entry_p = tk.Entry(root)
entry_p.pack()

tk.Button(root, text="Générer la grille", command=generate_grid_main).pack(pady=10)

root.mainloop()
