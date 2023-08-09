import matplotlib.pyplot as plt
import math

def calcular_distancia(cord_x1, cord_y1, cord_x2, cord_y2):
    return math.sqrt((cord_x2 - cord_x1)**2 + (cord_y2 - cord_y1)**2)

def on_click(event):
    x, y = event.xdata, event.ydata
    print(f"Clicked on ({x}, {y})")
    threshold = 0.005  # Define a threshold to consider the click within the vicinity of a "carga"

    # Check if the click is close to any "carga" in the vetor_cargas list
    for carga in vetor_cargas:
        carga_x, carga_y = carga["coordenadas"]
        if abs(x - carga_x) < threshold and abs(y - carga_y) < threshold:
            print(f"Clicked on carga with value: {carga['valor']}")
            # Add code here to modify the plot based on the selected "carga"
            break  # Exit the loop since we have found the clicked "carga"

# Constantes
k = 9000000000.00  # ou 9e9 N m²/C²

vetor_cargas = []; # Vetor que armazena as cargas elétricas

quantidade_cargas = int(input("Digite a quantidade de cargas (1 a 4): "))
while (quantidade_cargas > 4 or quantidade_cargas < 1):
    quantidade_cargas = int(input("Informação inválida!, digite novamente -> "))

for i in range(0, quantidade_cargas):
    print(f"\nDigite a carga {i+1}:\n")
    valor_carga = float(input(f"Valor da carga (Coulomb): "))
    coord_x = (float(input(f"Coordenada x: ")))
    coord_y = (float(input(f"Coordenada y: ")))
    coord = (coord_x, coord_y)
    vetor_cargas.append({"valor": valor_carga, "coordenadas": coord})

for carga in vetor_cargas:
    plt.plot(carga["coordenadas"][0], carga["coordenadas"][1], marker='o', color='b', linestyle='--')
    plt.text(carga["coordenadas"][0], carga["coordenadas"][1], f'{carga["valor"]}', ha='right', va='bottom')

plt.gcf().canvas.mpl_connect('button_press_event', on_click)
plt.xlabel('Eixo X (metros)')
plt.ylabel('Eixo Y (metros)')
plt.title('Distribuição de Cargas Elétricas')
plt.show()