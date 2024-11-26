from Estacion import GrafoTransporte
from collections import deque
import heapq


class AlgoritmosBusqueda:

    @staticmethod
    def cargar_Estaciones(cmb_EstacionP, cmb_EstacionD,ListView):
        grafo_transporte = GrafoTransporte()
        
        cmb_EstacionP.clear()  # Limpiar el ComboBox
        cmb_EstacionP.addItem("")  # Añadir un item vacío para indicar "Seleccione una estación"
        cmb_EstacionP.addItems(list(grafo_transporte.NameStations.keys()))  # Añadir estaciones
        
        cmb_EstacionD.clear()  # Limpiar el ComboBox
        cmb_EstacionD.addItem("")  # Añadir un item vacío para indicar "Seleccione una estación"
        cmb_EstacionD.addItems(list(grafo_transporte.NameStations.keys()))  # Añadir estaciones
        
        # Conectar la señal de cambio de texto de EstacionP
        cmb_EstacionP.currentTextChanged.connect(lambda: AlgoritmosBusqueda.on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD, ListView))
        cmb_EstacionD.currentTextChanged.connect(lambda: AlgoritmosBusqueda.on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD, ListView))


    @staticmethod
    def Cargar_ListView(ListView, recorrido):
        from PyQt5.QtCore import QStringListModel
        # Crear el modelo para QListView
        # print('recorrido es', recorrido)
        estaciones_model = QStringListModel()
        estaciones_model.setStringList(recorrido)
        # Establecer el modelo en el QListView
        ListView.setModel(estaciones_model)

        
    @staticmethod
    def on_Estacion_Changed(cmb_EstacionP, cmb_EstacionD ,ListView):
        # Obtener las estaciones seleccionadas
        EstacionP = cmb_EstacionP.currentText()
        EstacionD = cmb_EstacionD.currentText()
        
        # Verificar si ambas estaciones están seleccionadas
        if EstacionP and EstacionD:
            # Llamar a tipo_Algoritmo para ejecutar el algoritmo
            AlgoritmosBusqueda.tipo_Algoritmo(EstacionP, EstacionD, 'Metodo' ,ListView)

    @staticmethod
    def tipo_Algoritmo(EstacionP, EstacionD, Metodo, ListView):
        if Metodo == 'Anchura':
            resultado = AlgoritmosBusqueda.Anchura(EstacionP, EstacionD)
        elif Metodo == 'Prim':
            resultado = AlgoritmosBusqueda.Prim(EstacionP, EstacionD)
        elif Metodo == 'Kruskal':
            resultado = AlgoritmosBusqueda.kruskal(EstacionP, EstacionD)
        elif Metodo == 'Dijkstra':
            resultado = AlgoritmosBusqueda.Dijkstra(EstacionP, EstacionD)
        else:
            resultado = ["Método no reconocido."]
        
        AlgoritmosBusqueda.Cargar_ListView(ListView, resultado)


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
                # return [f"Recorrido por Anchura: \n {' -> '.join(camino)}"]
                camino_formateado = '\n'.join([' -> '.join(camino[i:i+3]) for i in range(0, len(camino), 3)])
                return [f"Recorrido por Anchura: \n{camino_formateado}"]

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

        return["No se encontró un camino entre las estaciones."]
    
    @staticmethod
    def Prim(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        # Aseguramos que las estaciones existen en el grafo
        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            return ["Una o ambas estaciones no existen."]

        # Obtener las estaciones de inicio y fin directamente desde el grafo
        EstacionP = grafo_transporte.NameStations[EstacionP]
        EstacionD = grafo_transporte.NameStations[EstacionD]

        visitados = set()
        mst = []
        min_heap = []

        # Comenzamos con la estación de inicio
        visitados.add(EstacionP)
        for conexion in EstacionP.conexiones:
            heapq.heappush(min_heap, (1, EstacionP, conexion))  # Asumimos peso 1

        camino = [EstacionP.estacion.nombre]  # Lista para almacenar el camino

        while min_heap:
            peso, nodo_origen, nodo_destino = heapq.heappop(min_heap)

            # Verificamos si el nodo destino no ha sido visitado
            if nodo_destino not in visitados:
                visitados.add(nodo_destino)
                mst.append((nodo_origen.estacion.nombre, nodo_destino.estacion.nombre, peso))

                # Añadimos el nodo al camino
                camino.append(nodo_destino.estacion.nombre)

                # Si llegamos al destino, podemos detener el proceso
                if nodo_destino == EstacionD:
                    break

                # Añadimos las conexiones del nodo destino al heap
                for conexion in nodo_destino.conexiones:
                    if conexion not in visitados:
                        heapq.heappush(min_heap, (1, nodo_destino, conexion))  # Asumimos peso 1

        # Verificamos si hemos llegado al nodo destino
        if EstacionD not in visitados:
            return ["No se encontró un camino entre las estaciones."]

        # Formatear el camino en grupos de 3 estaciones
        camino_formateado = '\n'.join([' -> '.join(camino[i:i+3]) for i in range(0, len(camino), 3)])

        return [f"Recorrido por Prim:"] + [camino_formateado]



    
    @staticmethod
    def kruskal(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
           return[ "Una o ambas estaciones no existen."]

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

        # print("Árbol de Expansión Mínima (MST):")
        # for estacion1, estacion2, peso in arbol_mst:
        #     print(f"{estacion1} - {estacion2} con peso {peso}")
        
        # Imprimir el recorrido entre las estaciones
        recorrido = []
        for estacion1, estacion2, _ in arbol_mst:
            recorrido.append(estacion1)
        recorrido.append(estacion2)  # Añadir la última estación
        camino_formateado = '\n'.join([' -> '.join(recorrido[i:i+3]) for i in range(0, len(recorrido), 3)])
        
        return[f"Recorrido por Kruskal: {camino_formateado}"]
        

    @staticmethod
    def Dijkstra(EstacionP, EstacionD):
        grafo_transporte = GrafoTransporte()

        # Verificar si las estaciones existen en el grafo
        if EstacionP not in grafo_transporte.NameStations or EstacionD not in grafo_transporte.NameStations:
            print("Una o ambas estaciones no existen.")
            return ["Una o ambas estaciones no existen."]

        # Inicializar estructuras para Dijkstra
        distancias = {estacion: float('inf') for estacion in grafo_transporte.NameStations}  # Distancia infinita por defecto
        distancias[EstacionP] = 0  # La estación de partida tiene distancia 0
        padres = {EstacionP: None}  # Diccionario para almacenar el camino más corto
        cola_prioridad = [(0, grafo_transporte.NameStations[EstacionP])]  # Cola de prioridad con el costo inicial

        while cola_prioridad:
            # Extraer el nodo con la distancia más corta
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            # Si llegamos a la estación de destino, reconstruimos el camino
            if nodo_actual.estacion.nombre == EstacionD:
                camino = []
                while nodo_actual:
                    camino.append(nodo_actual.estacion.nombre)
                    nodo_actual = padres.get(nodo_actual.estacion.nombre)  # Regresamos al nodo padre
                camino.reverse()
                # Formatear el camino en un formato amigable
                camino_formateado = '\n'.join([' -> '.join(camino[i:i+3]) for i in range(0, len(camino), 3)])
                return [f"Recorrido por Dijkstra: \n{camino_formateado}"]

            # Explorar las conexiones del nodo actual
            for vecino in nodo_actual.conexiones:
                # Calcular la distancia del vecino
                nueva_distancia = distancia_actual + 1  # Asumimos que todas las conexiones tienen costo 1, puedes ajustarlo según tu modelo

                # Si encontramos un camino más corto hacia el vecino, lo actualizamos
                if nueva_distancia < distancias[vecino.estacion.nombre]:
                    distancias[vecino.estacion.nombre] = nueva_distancia
                    padres[vecino.estacion.nombre] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        return ["No se encontró un camino entre las estaciones."]