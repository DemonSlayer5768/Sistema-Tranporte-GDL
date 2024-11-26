from Estacion import GrafoTransporte
from collections import deque
import heapq


class AlgoritmosBusqueda:

    @staticmethod
    def cargar_Estaciones(cmb_EstacionP, cmb_EstacionD):
        grafo_transporte = GrafoTransporte()
        
        cmb_EstacionP.clear()  # Limpiar el ComboBox
        cmb_EstacionP.addItem("")  # Añadir un item vacío para indicar "Seleccione una estación"
        cmb_EstacionP.addItems(list(grafo_transporte.NameStations.keys()))  # Añadir estaciones
        
        cmb_EstacionD.clear()  # Limpiar el ComboBox
        cmb_EstacionD.addItem("")  # Añadir un item vacío para indicar "Seleccione una estación"
        cmb_EstacionD.addItems(list(grafo_transporte.NameStations.keys()))  # Añadir estaciones
        
        # Conectar la señal de cambio de texto de EstacionP
        cmb_EstacionP.currentTextChanged.connect(lambda: AlgoritmosBusqueda.on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD))
        cmb_EstacionD.currentTextChanged.connect(lambda: AlgoritmosBusqueda.on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD))

    @staticmethod
    def on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD):
        # Obtener las estaciones seleccionadas
        EstacionP = cmb_EstacionP.currentText()
        EstacionD = cmb_EstacionD.currentText()
        
        # Verificar si ambas estaciones están seleccionadas
        if EstacionP and EstacionD:
            # Llamar a tipo_Algoritmo para ejecutar el algoritmo
            AlgoritmosBusqueda.tipo_Algoritmo(EstacionP, EstacionD, 'Metodo')  # Aquí 'Metodo' es un ejemplo

    @staticmethod
    def tipo_Algoritmo(EstacionP, EstacionD, Metodo):
        if Metodo == 'Anchura':
            AlgoritmosBusqueda.Anchura(EstacionP, EstacionD)
        elif Metodo == 'Prim':
            AlgoritmosBusqueda.Prim(EstacionP,EstacionD)
        elif Metodo == 'Kruskal':
            AlgoritmosBusqueda.kruskal(EstacionP, EstacionD)
        elif Metodo == 'Dijkstra':
            AlgoritmosBusqueda.Dijkstra(EstacionP, EstacionD)

    @staticmethod
    def Anchura(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        # Verificar si las estaciones existen en el grafo
        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            print("Una o ambas estaciones no existen.")
            return

        # Inicializar la cola para BFS
        cola = deque([grafo_transporte.NameStations[EstacionP]])  # Empezar desde la estación de partida
        visitados = set()  # Conjunto de estaciones visitadas
        padres = {}  # Diccionario para almacenar el camino (padre de cada estación)

        while cola:
            nodo_actual = cola.popleft()

            # Si llegamos a la estación de destino, reconstruimos el camino
            if nodo_actual.estacion.nombre == EstacionD:
                camino = []
                while nodo_actual:
                    camino.append(nodo_actual.estacion.nombre)
                    nodo_actual = padres.get(nodo_actual)  # Regresamos al nodo padre
                camino.reverse()
                print(f"Recorrido: {' -> '.join(camino)}")
                return

            # Marcar como visitado y explorar las conexiones dentro de la misma línea
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)

                # Explorar las conexiones de la estación actual
                for vecino in nodo_actual.conexiones:
                    if vecino not in visitados:
                        # Asegurarse de que el vecino está en la misma línea que la estación actual
                        if set(vecino.estacion.lineas).intersection(set(nodo_actual.estacion.lineas)):
                            cola.append(vecino)
                            padres[vecino] = nodo_actual

        print("No se encontró un camino entre las estaciones.")
    
    @staticmethod
    def Prim(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            print("Una o ambas estaciones no existen.")
            return

        # Paso 1: Inicialización
        visitados = set()
        camino = []
        min_heap = [(0, EstacionP)]  # (costo, estación)
        padres = {EstacionP: None}  # Diccionario de padres para reconstruir el camino

        while min_heap:
            costo, estacion_actual = heapq.heappop(min_heap)

            if estacion_actual not in visitados:
                visitados.add(estacion_actual)
                if estacion_actual == EstacionD:
                    # Si llegamos a la estación de destino, reconstruir el camino
                    while estacion_actual:
                        camino.append(estacion_actual)
                        estacion_actual = padres.get(estacion_actual)
                    camino.reverse()
                    print(f"Recorrido: {' -> '.join(camino)}")
                    return

                # Explorar vecinos
                for vecino in grafo_transporte.NameStations.get(estacion_actual, {}).get("conexiones", []):
                    if vecino not in visitados:
                        padres[vecino] = estacion_actual
                        heapq.heappush(min_heap, (costo + 1, vecino))  # Asumir costo 1

        print("No se encontró un camino entre las estaciones.")
    
    @staticmethod
    def kruskal(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            print("Una o ambas estaciones no existen.")
            return

        aristas = []
        for linea, estaciones in grafo_transporte.NameLine.items():
            for i in range(len(estaciones) - 1):
                estacion1 = estaciones[i]
                estacion2 = estaciones[i + 1]
                aristas.append((1, estacion1, estacion2))  # Peso, estación1, estación2

        aristas.sort(key=lambda x: x[0])

        parent = {}
        rank = {}

        def find(station):
            if parent[station] != station:
                parent[station] = find(parent[station])
            return parent[station]

        def union(station1, station2):
            root1 = find(station1)
            root2 = find(station2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root1] += 1

        for _, estacion1, estacion2 in aristas:
            parent[estacion1] = estacion1
            parent[estacion2] = estacion2
            rank[estacion1] = 0
            rank[estacion2] = 0

        arbol_mst = []
        for peso, estacion1, estacion2 in aristas:
            if find(estacion1) != find(estacion2):
                union(estacion1, estacion2)
                arbol_mst.append((estacion1, estacion2, peso))

        print("Árbol de Expansión Mínima (MST):")
        for estacion1, estacion2, peso in arbol_mst:
            print(f"{estacion1} - {estacion2} con peso {peso}")
        
        # Imprimir el recorrido entre las estaciones
        recorrido = []
        for estacion1, estacion2, _ in arbol_mst:
            recorrido.append(estacion1)
        recorrido.append(estacion2)  # Añadir la última estación
        print(f"Recorrido: {' -> '.join(recorrido)}")

    @staticmethod
    def Dijkstra(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            print("Una o ambas estaciones no existen.")
            return

        # Implementación de Dijkstra
        print(f"Implementar Dijkstra entre {EstacionP} y {EstacionD}")
