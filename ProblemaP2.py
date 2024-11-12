
# Alejandro Pardo
# Alejandro Lancheros

import sys

def encontrarCelula(lista_adyacencias):
    return lista_adyacencias

def calcular_distancia(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)
    
def main():
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
            lista_adyacencias[id] = []
        #armar el grafo
        for i in range(numCelulas):
            id1, x1, y1, tipo1, peptidos1 = celulas[i]
            
            for j in range(i + 1, numCelulas):
                id2, x2, y2, tipo2, peptidos2 = celulas[j]
                
                distancia = calcular_distancia(x1, y1, x2, y2)
                
                if distancia <= dist:
                    # Contar péptidos comunes
                    peptidos_comunes = set(peptidos1).intersection(set(peptidos2))
                    peso = len(peptidos_comunes)
                    
                    # Agregar la conexión a la lista de adyacencia si hay péptidos comunes
                    if peso > 0:
                        if tipo1 == 3 and tipo2 == 3:
                            continue
                        lista_adyacencias[id1].append((id2, peso))
                        lista_adyacencias[id2].append((id1, peso))
        print(encontrarCelula(lista_adyacencias))
        linea = sys.stdin.readline()
        
main()

