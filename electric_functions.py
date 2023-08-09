import math
import matplotlib.pyplot as plt
import numpy as np

# Classe que representa uma carga elétrica
class Carga:
    # Carga dado em Coulombs (C)
    def __init__(self, x, y, carga):
        self.x = x
        self.y = y
        self.carga = carga


# Retorna o potencial (em volts) de uma carga elétrica em x e y
def calcular_potencial(vetor_cargas, x, y, K):
    potencial = 0
    
    for carga in vetor_cargas:
        potencial += K * carga.carga / calcular_distancia(carga.x, carga.y, x, y)
    
    return potencial


# Distância radial do ponto (x, y) até a partícula
def calcular_distancia(cord_x1, cord_y1, cord_x2, cord_y2):
    return np.sqrt((cord_x1 - cord_x2)**2 + (cord_y1 - cord_y2)**2)


def achar_linha_equipotencial(vetor_cargas, x, y, xy_min, xy_max, qntd_pontos, K):
    potencial = calcular_potencial(vetor_cargas, x, y, K)

    x_grid = np.linspace(xy_min, xy_max, qntd_pontos)
    y_grid = np.linspace(xy_min, xy_max, qntd_pontos)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = calcular_potencial(vetor_cargas, X, Y, K)

    return X, Y, Z