import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, dirigido=False):
        self.lista_adyacencia = {}
        self.dirigido = dirigido

    def agregar_vertice(self, vertice):
        if vertice not in self.lista_adyacencia:
            self.lista_adyacencia[vertice] = []

    def agregar_arista(self, vertice1, vertice2):
        self.agregar_vertice(vertice1)
        self.agregar_vertice(vertice2)
        self.lista_adyacencia[vertice1].append(vertice2)
        if not self.dirigido:
            self.lista_adyacencia[vertice2].append(vertice1)

    def mostrar_grafo(self):
        print("Lista de Adyacencia:")
        for vertice in self.lista_adyacencia:
            print(f"{vertice} -> {self.lista_adyacencia[vertice]}")

    def graficar_grafo(self):
        if self.dirigido:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        for vertice in self.lista_adyacencia:
            for adyacente in self.lista_adyacencia[vertice]:
                G.add_edge(vertice, adyacente)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=15, font_weight='bold')
        plt.title("Representación Gráfica del Grafo")
        plt.show()


# Ejemplo de uso:
grafo = Grafo(dirigido=False)
grafo.agregar_arista("A", "B")
grafo.agregar_arista("A", "C")
grafo.agregar_arista("B", "D")
grafo.agregar_arista("C", "D")

grafo.mostrar_grafo()
grafo.graficar_grafo()
