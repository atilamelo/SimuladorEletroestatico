import tkinter as tk
from tkinter import ttk, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from electric_functions import *
import matplotlib.pyplot as plt

# Valores padrões
default_k = 9e9
default_points = 10
default_xy_min = -10
default_xy_max = 10

# Classe que representa uma carga elétrica


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
        self.electric_charges = []
        self.config_graph()

    
    def ativar_potencial_eletrico(self):
        
        if(self.electric_charges == []):
            print("Necessário alguma carga para cálculo")
            return

        if(self.plot_potential.get() == 0):
            self.config_graph()
            print("Linhas de força desativadas")
            return

        self.config_graph()  # Reconfigura o gráfico para exibir o potencial elétrico

        # Desativar a opção de Linhas de Força
        self.plot_lines.set(0)
        print("Potencial elétrico ativado")

        # Recalcula o potencial elétrico em cada ponto do gráfico
        x = np.linspace(float(self.xy_min_entry.get()), float(self.xy_max_entry.get()), int(self.points_entry.get()))
        y = np.linspace(float(self.xy_min_entry.get()), float(self.xy_max_entry.get()), int(self.points_entry.get()))
        x, y = np.meshgrid(x, y)

        # Cria matrizes para armazenar os valores do potencial elétrico e das linhas equipotenciais
        potencial_matrix = np.zeros_like(x)
        linha_equipotencial_matrix = np.zeros_like(x)

        # Calcula o potencial elétrico e as linhas equipotenciais em cada ponto
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                potencial_matrix[i, j] = calcular_potencial(self.electric_charges, x[i, j], y[i, j], float(self.constant_entry.get()))
                X, Y, Z = achar_linha_equipotencial(self.electric_charges, x[i, j], y[i, j], float(self.xy_min_entry.get()),
                                                    float(self.xy_max_entry.get()), int(self.points_entry.get()),
                                                    float(self.constant_entry.get()))
                # Desenhar a linha potencial correspondente no gráfico
                plt.contour(X, Y, Z, levels=[
                            potencial_matrix[i, j]], colors='green', linestyles='solid', linewidths=1)
        
        plt.draw()


    def config_graph(self):
        print("Gráfico reconfigurado!")

        def on_click(event):
            click_x, click_y = event.xdata, event.ydata

            # Cliques fora do gráfico não são considerados
            if (click_x == None or click_y == None or self.electric_charges == []):
                return

            potencial = calcular_potencial(
                self.electric_charges, click_x, click_y, float(self.constant_entry.get()))
            print(
                f"Potencial elétrico em ({round(click_x, 2)}m, {round(click_y, 2)}m) = {round(potencial, 3)} V (J/C)")
            X, Y, Z = achar_linha_equipotencial(self.electric_charges, click_x, click_y, float(self.xy_min_entry.get()),
                                                float(self.xy_max_entry.get()), int(
                                                    self.points_entry.get()),
                                                float(self.constant_entry.get()))

            # Desenhar a linha potencial correspondente no gráfico
            plt.contour(X, Y, Z, levels=[
                        potencial], colors='green', linestyles='solid', linewidths=1)
            plt.draw()

        # Linhas de contorno negativas sólidas
        plt.clf()
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        # Desabilitando a barra de ferramentas
        plt.rcParams['toolbar'] = 'None'
        plt.gcf().canvas.mpl_connect('button_press_event', on_click)
        plt.xlabel('Eixo X (m)')
        plt.ylabel('Eixo Y (m)')
        plt.xlim(float(self.xy_min_entry.get()),
                 float(self.xy_max_entry.get()))
        plt.ylim(float(self.xy_min_entry.get()),
                 float(self.xy_max_entry.get()))
        plt.title('Simulador de Eletrostática')

        # Separar as partículas positivas e negativas
        particulas_positivas = [(c.x, c.y)
                                for c in self.electric_charges if c.carga > 0]
        particulas_negativas = [(c.x, c.y)
                                for c in self.electric_charges if c.carga < 0]

        # Configuração do gráfico com legenda
        plt.scatter([p[0] for p in particulas_positivas], [
                    p[1] for p in particulas_positivas], c='red', s=50, label='Partículas positivas', edgecolors='k')
        plt.scatter([p[0] for p in particulas_negativas], [p[1] for p in particulas_negativas],
                    c='blue', s=50, label='Partículas negativas', edgecolors='k')


        # Adiciona o valor de carga pra cada uma das partículas
        for carga in self.electric_charges:
            plt.text(carga.x, carga.y, f'{carga.carga} C', ha='right', va='bottom')


        plt.legend()
        plt.draw()

    def add_charge(self):
        x = simpledialog.askfloat(
            "Adicionar Carga", "Digite a coordenada x (m):")
        y = simpledialog.askfloat(
            "Adicionar Carga", "Digite a coordenada y (m):")
        charge = simpledialog.askfloat(
            "Adicionar Carga", "Digite o valor da carga (C):")

        if x is not None and y is not None and charge is not None:
            charge_info = f"Coordenadas: ({x}, {y}) em metros - Carga: {charge} C"
            self.show_charge_info(charge_info)
            self.electric_charges.append(Carga(x, y, charge))
            self.config_graph()

    def show_charge_info(self, charge_info):
        info_window = tk.Toplevel(self.root)
        info_window.title("Informações da Carga")

        info_label = tk.Label(info_window, text=charge_info, padx=10, pady=10)
        info_label.pack()

    
    def redraw_graph(self):
        self.plot_lines.set(0)
        self.plot_potential.set(0)
        self.config_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectrostaticsApp(root)
    root.mainloop()