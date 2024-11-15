
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
        #print(modificaciones)
        for nodo, i, capacidad_original in modificaciones:
            lista_adyacencias[nodo][i] = ((lista_adyacencias[nodo][i][0], capacidad_original))

    return max_flow

def main():
    calculadoras = []
    calculadoras_potenciales = []
    lista_adyacencias = {}
    tipo_celulas = {}
    ncasos = int(sys.stdin.readline().strip())
    linea = sys.stdin.readline() 
    for i in range(0, ncasos):
        try :
            numCelulas, dist = linea.split()
            numCelulas, dist = int(numCelulas), int(dist)
            #if numCelulas > 4000:
            #    print("No creemos que nuestro algoritmo resuelva en el tiempo esperado este caso")
            #    continue
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
                tipo_celulas[str(id)] = tipo
                crearNodo(lista_adyacencias, id)
                if tipo == 1:
                    crearArcos(lista_adyacencias, "i", id, float('inf'))
                #elif tipo == 2:
                #    calculadoras.append(id)
                elif tipo == 3:
                    crearArcos(lista_adyacencias, id, "f", float('inf'))
                
                for id1, x1, y1, tipo1, peptidos1 in celulas[:-1]:
                    if (tipo == 1 and tipo1 == 1):
                        continue
                    if (tipo == 1 and tipo1 == 3):
                        continue
                    if (tipo == 3 and tipo1 == 3):
                        continue
                    if (tipo == 3 and tipo1 == 1):
                        continue

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
                
                if tipo == 2 and id not in calculadoras:
                    calculadoras.append(id)
                
            for id in calculadoras:    
                tuplas = lista_adyacencias[id]
                #print("TUPLAS" , tuplas)
                #print("TIPOS", tipo_celulas)
                if tuplas != []:
                    for id2, capacidad2 in tuplas:
                        if capacidad2 > 0 and tipo_celulas[str(id2)] == 3 and id not in calculadoras_potenciales:
                            calculadoras_potenciales.append(id)
                #calculadoras.append(id)
                            
                                
            
            flujo_sin_celula_bloqueo = float('inf')
            nuevaLista = copy.deepcopy(lista_adyacencias)
            #print(calculadoras_potenciales)
            for id_calculadora in calculadoras_potenciales:
                #if lista_adyacencias[id_calculadora] == []:
                #    continue
                original = nuevaLista[id_calculadora]
                nuevaLista[id_calculadora] = []
                flujo = edmonds_karp(nuevaLista, "i", "f")
                nuevaLista[id_calculadora] = original
                nuevaLista = lista_adyacencias
                if flujo < flujo_sin_celula_bloqueo:
                    id_celula_bloqueo = id_calculadora
                    flujo_sin_celula_bloqueo = flujo
                if flujo_sin_celula_bloqueo == 0:
                    break
            
            flujo_total = edmonds_karp(lista_adyacencias, "i", "f")        
            print(id_celula_bloqueo, flujo_total, flujo_sin_celula_bloqueo)
            #print(flujo_total)
        except:
            print("Error")
        lista_adyacencias = {}
        tipo_celulas = {}
        calculadoras = []
        calculadoras_potenciales = []
        linea = sys.stdin.readline()
        
main()
