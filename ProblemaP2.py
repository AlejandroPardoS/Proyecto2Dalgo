
# Alejandro Pardo
# Alejandro Lancheros

import sys
import copy

def crearArcos(lista_adyacencias, nodoOrigen, nodoFinal, capacidad):
    if nodoOrigen in lista_adyacencias and nodoFinal not in lista_adyacencias[nodoOrigen]:
        if nodoFinal == "f" or nodoOrigen == "i":
            lista_adyacencias[nodoOrigen].append((nodoFinal, capacidad))
        else:
            lista_adyacencias[nodoOrigen].append((int(nodoFinal), capacidad))

def crearNodo(lista_adyacencias, nodo):
    if nodo not in lista_adyacencias:
        lista_adyacencias[nodo] = []


            
def calcular_distancia_euclidiana(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

def calcular_distancia_manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def calcularCapacidad(peptidos1, peptidos2):
    return len(set(peptidos1).intersection(set(peptidos2)))


def bfs(lista_adyacencias, nodo1, nodo2):
    journey = {nodo1: None} 
    queve = [nodo1]  

    while queve:
        nodo = queve.pop(0)
        #print(lista_adyacencias)
        for nodoActual, capacidad in lista_adyacencias[str(nodo)]:
            if nodoActual not in journey and capacidad > 0:
                journey[nodoActual] = nodo 
                
                if nodoActual == nodo2:
                    return journey  
                queve.append(nodoActual)  
                
    return None

def edmonds_karp2(lista_adyacencias, nodo1, nodo2):
    max_flow = 0 
    while True:
        parent = bfs(lista_adyacencias, nodo1, nodo2)
        if parent is None:
            break 

        path_flow = float("inf")
        s = nodo2

        while s != nodo1:
            u = parent[s]
            #print(u)
            for v, capacity in lista_adyacencias[str(u)]:
                if v == s:
                    path_flow = min(path_flow, capacity)
            s = parent[s]

        max_flow += path_flow

        v = nodo2
        while v != nodo1:
            u = parent[v]
            for i, (adj_v, capacity) in enumerate(lista_adyacencias[str(u)]):
                if adj_v == v:
                    lista_adyacencias[str(u)][i] = (adj_v, capacity - path_flow)
            for i, (adj_u, capacity) in enumerate(lista_adyacencias[str(v)]):
                if adj_u == u:
                    lista_adyacencias[str(v)][i] = (adj_u, capacity + path_flow)
            v = parent[v]

    return max_flow

def edmonds_karp(lista_adyacencias, nodo1, nodo2):
    max_flow = 0
    modificaciones = []
    while True:
        parent = bfs(lista_adyacencias, nodo1, nodo2)
        if parent is None:
            break

        path_flow = float("inf")
        s = nodo2

        while s != nodo1:
            u = parent[s]
            for v, capacity in lista_adyacencias[str(u)]:
                if v == s:
                    path_flow = min(path_flow, capacity)
            s = parent[s]

        max_flow += path_flow

        v = nodo2
        while v != nodo1:
            u = parent[v]
            for i, (adj_v, capacity) in enumerate(lista_adyacencias[str(u)]):
                if adj_v == v:
                    modificaciones.append((str(u), i, capacity))
                    lista_adyacencias[str(u)][i] = (adj_v, capacity - path_flow)
            for i, (adj_u, capacity) in enumerate(lista_adyacencias[str(v)]):
                if adj_u == u:
                    modificaciones.append((str(v), i, capacity))
                    lista_adyacencias[str(v)][i] = (adj_u, capacity + path_flow)
            v = parent[v]
        #print(modificaciones)
    # Revertir las modificaciones realizadas si hay
    if modificaciones:
        for nodo, i, capacidad_original in modificaciones:
            lista_adyacencias[nodo][i] = ((lista_adyacencias[nodo][i][0], capacidad_original))

    return max_flow#,  lista_adyacencias

#print(edmonds_karp({"s": [("1",float('inf')), ("2",float('inf'))], "t": [], "1": [(3, 2)], "2": [(5, 3)], "3": [(1, 2), (4, 3)], "4": [], "5": [(2, 3), (4, 1), (7, 1)], "6": [(4, 2), ("t", float('inf'))], "7": [(5, 1), ("t", float('inf'))]}, "s", "t"))
#print(edmonds_karp({"s": [("1",float('inf')), ("2",float('inf'))], "t": [], "1": [(3, 2)], "2": [(5, 3)], "3": [(1, 2), (4, 3)], "4": [(3, 3), (5, 1), (6, 2)], "5": [(2, 3), (4, 1), (7, 1)], "6": [(4, 2), ("t", float('inf'))], "7": [(5, 1), ("t", float('inf'))]}, "s", "t"))

def main():
    calculadoras = []
    lista_adyacencias = {}
    ncasos = int(sys.stdin.readline().strip())
    linea = sys.stdin.readline() 
    for i in range(0, ncasos):
        #try :
        numCelulas, dist = linea.split()
        numCelulas, dist = int(numCelulas), int(dist)
        celulas = []
        crearNodo(lista_adyacencias, "i")
        crearNodo(lista_adyacencias, "f")
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
            if tipo == 1:
                crearArcos(lista_adyacencias, "i", id, float('inf'))
            elif tipo == 2:
                calculadoras.append(id)
            elif tipo == 3:
                crearArcos(lista_adyacencias, id, "f", float('inf'))
            
            for id1, x1, y1, tipo1, peptidos1 in celulas[:-1]:
                capacidad = calcularCapacidad(peptidos, peptidos1)

                if calcular_distancia_manhattan(x1, y1, x, y) <= dist and capacidad>0:
                    if (tipo == 1 and tipo1 == 2):
                        crearArcos(lista_adyacencias, id, id1, capacidad)
                    elif (tipo == 2 and tipo1 == 1):
                        crearArcos(lista_adyacencias, id1, id, capacidad)
                        crearArcos(lista_adyacencias, id, id1, capacidad)
                    elif (tipo == 2 and tipo1 == 3):
                        crearArcos(lista_adyacencias, id, id1, capacidad)
                    elif (tipo == 3 and tipo1 == 2):
                        crearArcos(lista_adyacencias, id1, id, capacidad)
                        crearArcos(lista_adyacencias, id, id1, capacidad)
                    elif (tipo == 2 and tipo1 == 2):
                        crearArcos(lista_adyacencias, id, id1, capacidad)
                        crearArcos(lista_adyacencias, id1, id, capacidad)                
        
        flujo_sin_celula_bloqueo = float('inf')
        #lista_original = copy.deepcopy(lista_adyacencias)
        nuevaLista = copy.deepcopy(lista_adyacencias)
        #nuevaLista = lista_adyacencias
        #print("LISTA_ADYACENCIAS", lista_adyacencias)
        for id_calculadora in calculadoras:
            #nuevaLista = lista_adyacencias.copy()
            #nuevaLista = copy.deepcopy(lista_adyacencias)   #si esta costoso, se puede solo hacer una copia, ¿como?
            original = nuevaLista[id_calculadora]
            nuevaLista[id_calculadora] = []
            #print("ID calculadora", id_calculadora)
            #print("LISTA ANTES", nuevaLista)
            flujo = edmonds_karp(nuevaLista, "i", "f")
            #print("LISTA_ADYACENCIAS", lista_adyacencias)
            #nuevaLista = lista_original.copy()
            nuevaLista[id_calculadora] = original
            nuevaLista = lista_adyacencias
            #print("LISTA DESPU", nuevaLista)
            if flujo < flujo_sin_celula_bloqueo:
                id_celula_bloqueo = id_calculadora
                flujo_sin_celula_bloqueo = flujo
            if flujo_sin_celula_bloqueo == 0:
                break
        
        flujo_total = edmonds_karp(lista_adyacencias, "i", "f")        
        print(id_celula_bloqueo, flujo_total, flujo_sin_celula_bloqueo)
        #print(flujo_total)
        #except:
        #    print("Error")
        lista_adyacencias = {}
        calculadoras = []
        linea = sys.stdin.readline()
        
main()
