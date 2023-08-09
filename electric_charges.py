import matplotlib.pyplot as plt
import numpy as np
import math

# Constantes
K = 9000000000.00  # ou 9e9 N m²/C²
XY_MIN, XY_MAX = [-5, 5]
QNTD_PONTOS = 1000

# Classe que representa uma carga elétrica
class Carga:
    # Carga dado em Coulombs (C)
    def __init__(self, x, y, carga):
        self.x = x
        self.y = y
        self.carga = carga


# Retorna o potencial (em volts) de uma carga elétrica em x e y
def calcular_potencial(vetor_cargas, x, y):
    potencial = 0
    
    for carga in vetor_cargas:
        potencial += K * carga.carga / calcular_distancia(carga.x, carga.y, x, y)
    
    return potencial


def calcular_distancia(cord_x1, cord_y1, cord_x2, cord_y2):
    return np.sqrt((cord_x1 - cord_x2)**2 + (cord_y1 - cord_y2)**2)

def achar_linha_equipotencial(vetor_cargas, x, y):
    potencial = calcular_potencial(vetor_cargas, x, y)

    x_grid = np.linspace(XY_MIN, XY_MAX, QNTD_PONTOS)
    y_grid = np.linspace(XY_MIN, XY_MAX, QNTD_PONTOS)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = calcular_potencial(vetor_cargas, X, Y)

    return X, Y, Z


def on_click(event):
    click_x, click_y = event.xdata, event.ydata
    
    # Cliques fora do gráfico não são considerados
    if(click_x == None or click_y == None):
        return
    
    potencial = calcular_potencial(vetor_cargas, click_x, click_y)
    print(f"Potencial elétrico em ({round(click_x, 2)}m, {round(click_y, 2)}m) = {round(potencial, 3)} V (J/C)")
    X, Y, Z = achar_linha_equipotencial(vetor_cargas, click_x, click_y)
    
    # Desenhar a linha potencial correspondente no gráfico
    plt.contour(X, Y, Z, levels=[potencial], colors='green', linestyles='solid', linewidths=1)
    plt.draw() 

vetor_cargas = []; # Vetor que armazena as cargas elétricas

quantidade_cargas = int(input("Digite a quantidade de cargas (1 a 4): "))
while (quantidade_cargas > 4 or quantidade_cargas < 1):
    quantidade_cargas = int(input("Informação inválida!, digite novamente -> "))

for i in range(0, quantidade_cargas):
    print(f"\nDigite a carga {i+1}:\n")
    valor_carga = float(input(f"Valor da carga (Coulomb): "))
    coord_x = (float(input(f"Coordenada x: ")))
    coord_y = (float(input(f"Coordenada y: ")))
    vetor_cargas.append(Carga(coord_x, coord_y, valor_carga))


for carga in vetor_cargas:
    plt.plot(carga.x, carga.y, marker='o', color='b', linestyle='--')
    plt.text(carga.x, carga.y, f'{carga.carga}', ha='right', va='bottom')

plt.gcf().canvas.mpl_connect('button_press_event', on_click)
plt.xlabel('Eixo X (metros)')
plt.ylabel('Eixo Y (metros)')
plt.title('Distribuição de Cargas Elétricas')
plt.show()