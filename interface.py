import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import projet


def plot_grid(m, n, p):
    grid, _ = projet.generate_instance_grid(m,n,p)

    plt.imshow(grid, cmap="gray_r")
    plt.title(f"Grille {m}x{n} avec {p} obstacles")
    plt.show()


def generer(): #fonction generee par le bouton 
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

tk.Button(root, text="Générer la grille", command=generer).pack(pady=10)

root.mainloop()