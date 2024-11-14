
# Alejandro Pardo
# Alejandro Lancheros

import sys
"""
@author: josep

Asumo que:
Todos los nodos los dan desde 1 de forma ascendente, sin saltos: No
Que estos siempre van a estar ordenados recorriendo primero los tipo 1, 2 y 3: No
No van a haber nodos volando, o sea, que no tengan conexion con el grafo: Si
No hay sub grafos: Si hay pero con S se soluciona
Todas las distancias o posiciones son Enteros positivos: No
Los indicadores de los nodos son positivos: Si
"""

#============================ Grafo ============================#
def crearNodo(grafo: dict, nodo: str) -> None:
    if nodo not in grafo:
        grafo[nodo] = []

def crearArcos(grafo: dict, nodoOrigen: str, nodoFinal: str, capacidad: int) -> None:
    if nodoOrigen in grafo and nodoFinal not in grafo[nodoOrigen]:
        grafo[nodoOrigen].append((nodoFinal, capacidad))

def crearNodoAux(grafo: dict, nodoAnterior: str, nodoActual: str, capacidad) -> None:
    crearNodo(grafo, nodoAnterior+"-"+nodoActual)
    crearArcos(grafo, nodoAnterior, nodoAnterior+"-"+nodoActual, capacidad)
    crearArcos(grafo, nodoAnterior+"-"+nodoActual, nodoActual, capacidad)

#============================ Calculos ============================#
def calcularDistancia(x1: int, y1: int, x2: int, y2: int) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**(1/2)

def calcularCapacidad(peptidosActuales: list, peptidosAnteriores: list) -> int:
    return len(set(peptidosActuales) & set(peptidosAnteriores))

#============================ Algotimos sobre el grafo ============================#
def bfs(grafo: dict, nodoInit: str, nodoFinit: str) -> dict:
    camino = {nodoInit: None} 
    cola = [nodoInit]  

    while cola:
        nodo = cola.pop(0)
        #print(grafo[str(nodo)])
        for nodoActual, capacidad in grafo[str(nodo)]:
            if nodoActual not in camino and capacidad > 0:
                camino[nodoActual] = nodo 
                #print(camino)
                
                if nodoActual == nodoFinit:
                    return camino  
                cola.append(nodoActual)  
                
    return None

def edmonds_karp(grafo, nodoInit, nodoFinit):
    max_flow = 0 

    while True:
        parent = bfs(grafo, nodoInit, nodoFinit)
        if parent is None:
            break 

        path_flow = float("inf")
        s = nodoFinit

        while s != nodoInit:
            u = parent[s]
            #print(u)
            for v, capacity in grafo[str(u)]:
                if v == s:
                    path_flow = min(path_flow, capacity)
            s = parent[s]

        max_flow += path_flow

        v = nodoFinit
        while v != nodoInit:
            u = parent[v]
            for i, (adj_v, capacity) in enumerate(grafo[str(u)]):
                if adj_v == v:
                    grafo[str(u)][i] = (adj_v, capacity - path_flow)
            for i, (adj_u, capacity) in enumerate(grafo[str(v)]):
                if adj_u == u:
                    grafo[str(v)][i] = (adj_u, capacity + path_flow)
            v = parent[v]

    return max_flow

print(edmonds_karp({"s": [("1",float('inf')), ("2",float('inf'))], "t": [], "1": [(3, 2), (4, 1)], "2": [(4, 1), (5, 3)], "3": [(1, 2), (4, 3), (5, 1), (6, 3)], "4": [(1, 1), (2, 1), (3, 3), (5, 1), (6, 2), (7, 2)], "5": [], "6": [(3, 3), (4, 2), (5, 3), ("t", float('inf'))], "7": [(4, 2), (5, 1), ("t", float('inf'))]}, "s", "t"))
#print(edmonds_karp({"s": [("1",float('inf')), ("2",float('inf'))], "t": [], "1": [(3, 2)], "2": [(5, 3)], "3": [(1, 2), (4, 3)], "4": [], "5": [(2, 3), (4, 1), (7, 1)], "6": [(4, 2), ("t", float('inf'))], "7": [(5, 1), ("t", float('inf'))]}, "s", "t"))


def main():
    listaResultados = []
    lista_adyacencias = {}
    ncasos = int(sys.stdin.readline().strip())
    linea = sys.stdin.readline() 
    for i in range(0, ncasos):
        numCelulas, dist = linea.split()
        numCelulas, dist = int(numCelulas), int(dist)
        celulas = []
        crearNodo(lista_adyacencias, "s")
        crearNodo(lista_adyacencias, "t")
        for i in range(numCelulas):
            linea = sys.stdin.readline()
            linea = linea.split()
            id = (linea[0])
            x = int(linea[1])
            y = int(linea[2])
            tipo = int(linea[3])
            peptidos = linea[4:]
            celulas.append((id, x, y, tipo, peptidos))
            crearNodo(lista_adyacencias, id)
            #lista_adyacencias[id] = []
            if tipo == 1:
                crearArcos(lista_adyacencias, "s", id, float('inf'))
            elif tipo == 3:
                crearArcos(lista_adyacencias, id, "t", float('inf'))
            #armar el grafo
            for nodoAnterior, posicionXanterior, posicionYanterior, tipoAnterior, peptidosAnterior in celulas[:-1]:
                capacidad = calcularCapacidad(peptidos, peptidosAnterior)

                if calcularDistancia(posicionXanterior, posicionYanterior, x, y) <= dist and capacidad>0:
                    if (tipo == 1 and tipoAnterior == 2):
                        crearArcos(lista_adyacencias, id, nodoAnterior, capacidad)
                    elif (tipo == 2 and tipoAnterior == 1):
                        crearArcos(lista_adyacencias, nodoAnterior, id, capacidad)
                    elif (tipo == 2 and tipoAnterior == 3):
                        crearArcos(lista_adyacencias, id, nodoAnterior, capacidad)
                    elif (tipo == 3 and tipoAnterior == 2):
                        crearArcos(lista_adyacencias, nodoAnterior, id, capacidad)
                    elif (tipo == 2 and tipoAnterior == 2):
                        crearArcos(lista_adyacencias, id, nodoAnterior, capacidad)
                        crearNodoAux(lista_adyacencias, nodoAnterior, id, capacidad)
            #print(encontrarCelula(lista_adyacencias))
        print(lista_adyacencias)
        listaResultados.append(edmonds_karp(lista_adyacencias, "s", "t"))
        print(listaResultados)
        linea = sys.stdin.readline()
        
#main()

"""def main():
    lista_adyacencias = {}
    ncasos = int(sys.stdin.readline().strip())
    linea = sys.stdin.readline() 
    for i in range(0, ncasos):
        numCelulas, dist = linea.split()
        numCelulas, dist = int(numCelulas), int(dist)
        celulas = []
        for i in range(numCelulas):
            linea = sys.stdin.readline()
            linea = linea.split()
            id = int(linea[0])
            x = int(linea[1])
            y = int(linea[2])
            tipo = int(linea[3])
            peptidos = linea[4:]
            celulas.append((id, x, y, tipo, peptidos))
            lista_adyacencias[(id,tipo)] = []
        #armar el grafo
        for i in range(numCelulas):
            id1, x1, y1, tipo1, peptidos1 = celulas[i]
            
            for j in range(i + 1, numCelulas):
                id2, x2, y2, tipo2, peptidos2 = celulas[j]
                if tipo1 == 1 and tipo2 == 3:
                    continue
                if tipo1 == 3 and tipo2 == 1:
                    continue
                if tipo1 == 3 and tipo2 == 3:
                    continue
                if tipo1 == 1 and tipo2 == 1:
                    continue
                
                distancia = calcular_distancia_euclidiana(x1, y1, x2, y2)
                
                if distancia <= dist:
                    # Contar péptidos comunes
                    peptidos_comunes = set(peptidos1).intersection(set(peptidos2))
                    peso = len(peptidos_comunes)
                    
                    # Agregar la conexión a la lista de adyacencia si hay péptidos comunes
                    if peso > 0:
                        lista_adyacencias[(id1,tipo1)].append((id2, peso))
                        lista_adyacencias[(id1,tipo1)].append((id1, peso))
        print(encontrarCelula(lista_adyacencias))
        linea = sys.stdin.readline()
        """
#main()

