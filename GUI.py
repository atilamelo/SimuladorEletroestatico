import tkinter as tk
from tkinter import ttk, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Valores padrões
default_k = 9e9
default_points = 10
default_xy_min = -10
default_xy_max = 10

class Carga:
    # Carga dado em Coulombs (C)
    def __init__(self, x, y, carga):
        self.x = x
        self.y = y
        self.carga = carga


class ElectrostaticsApp:
    def __init__(self, root):
        # Lista de cargas elétricas
        self.electric_charges = []

        self.root = root
        self.root.title("Simulador de Eletrostática")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.settings_frame = ttk.Frame(self.root)
        self.settings_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.plot_lines = tk.BooleanVar()
        self.plot_potential = tk.BooleanVar()

        ttk.Label(self.settings_frame, text="Características do Simulador", font=("Arial", 12, "bold"), anchor="center").grid(
            row=0, column=0, pady=(0, 20))

        self.check_potential = ttk.Checkbutton(
            self.settings_frame, text="Potencial Elétrico", variable=self.plot_potential, command=self.ativar_potencial_eletrico)
        self.check_potential.grid(
            row=2, column=0, sticky=tk.W, pady=(0, 20))

        ttk.Label(self.settings_frame, text="Constante Eletroestática (N.m²/C) ").grid(
            row=3, column=0, sticky=tk.W)
        self.constant_entry = ttk.Entry(self.settings_frame)
        self.constant_entry.grid(row=4, column=0, pady=(0, 10))
        self.constant_entry.insert(0, default_k)

        ttk.Label(self.settings_frame, text="Quantidade de Pontos").grid(row=5, column=0, sticky=tk.W)
        self.points_entry = ttk.Entry(self.settings_frame)
        self.points_entry.grid(row=6, column=0, pady=(0, 10))
        self.points_entry.insert(0, default_points)

        ttk.Label(self.settings_frame, text="XY Min (m) ").grid(
            row=7, column=0, sticky=tk.W)
        self.xy_min_entry = ttk.Entry(self.settings_frame)
        self.xy_min_entry.grid(row=8, column=0)
        self.xy_min_entry.insert(0, default_xy_min)

        ttk.Label(self.settings_frame, text="XY Min (m) ").grid(
            row=9, column=0, sticky=tk.W)
        self.xy_max_entry = ttk.Entry(self.settings_frame)
        self.xy_max_entry.grid(row=10, column=0, pady=(0, 20))
        self.xy_max_entry.insert(0, default_xy_max)

        ttk.Button(self.settings_frame, text="Adicionar Carga", command=self.add_charge).grid(
            row=11, column=0, pady=10)
        ttk.Button(self.settings_frame, text="Redesenhar Gráfico",
                   command=self.redraw_graph).grid(row=12, column=0, pady=(0, 10))
        ttk.Button(self.settings_frame, text="Remover todas as cargas",
                   command=self.remove_charges).grid(row=13, column=0, pady=(0, 10))

        # Gráficos
        self.config_graph()


    def remove_charges(self):
        ...

    
    def ativar_potencial_eletrico(self):
        ...


    def config_graph(self):
        ...

    def add_charge(self):
        ...

    def show_charge_info(self, charge_info):
        ...

    
    def redraw_graph(self):
        ...


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectrostaticsApp(root)
    root.mainloop()