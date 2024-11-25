import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel
import Estacion




class AlgoritmosOrdenamiento:
    
    @staticmethod
    def cargar_Lineas_Orden(cmb_OrdenarLineas):
   
        grafo_transporte = Estacion.GrafoTransporte()
         
        cmb_OrdenarLineas.clear()  # Limpiar el ComboBox
        cmb_OrdenarLineas.addItem("Todas")  # Agregar la opción 'Todas'
        cmb_OrdenarLineas.addItems(list(grafo_transporte.NameLine.keys()))  # Agregar las líneas

    @staticmethod
    def recibirDatos(cmb_OrdenarLineas, listView_Ordenamiento,txt_Time, Metodo):
        grafo_transporte = Estacion.GrafoTransporte()

        # Obtener la línea seleccionada
        if isinstance(cmb_OrdenarLineas, QtWidgets.QComboBox):
            cmb_OrdenarLineas = cmb_OrdenarLineas.currentText()

        # Filtrar las estaciones según la línea seleccionada
        if cmb_OrdenarLineas == "Todas":
            estaciones_filtradas = [
                nodo.estacion.nombre for nodo in grafo_transporte.NameStations.values()
            ]
        else:
            estaciones_filtradas = [
                nodo.estacion.nombre
                for nodo in grafo_transporte.NameStations.values()
                if AlgoritmosOrdenamiento.cumple_criterio(cmb_OrdenarLineas, nodo.estacion.lineas)
            ]

        # print("Estaciones filtradas:", estaciones_filtradas)
        print("Método seleccionado:", Metodo)

        # Ordenar las estaciones según el método seleccionado
        estaciones_ordenadas = []
        if Metodo == "Insercion":
            estaciones_ordenadas = AlgoritmosOrdenamiento.Insercion(estaciones_filtradas,txt_Time)
        elif Metodo == "Burbuja":
            estaciones_ordenadas = AlgoritmosOrdenamiento.Burbuja(estaciones_filtradas,txt_Time)
        elif Metodo == "Seleccion":
            estaciones_ordenadas = AlgoritmosOrdenamiento.Seleccion(estaciones_filtradas,txt_Time)
        elif Metodo == "Mezcla":
            estaciones_ordenadas = AlgoritmosOrdenamiento.Mezcla(estaciones_filtradas,txt_Time)
        elif Metodo == "Rapido":
            estaciones_ordenadas = AlgoritmosOrdenamiento.Rapido(estaciones_filtradas,txt_Time)

        # Mostrar las estaciones ordenadas en el ListView
        modelo = QStringListModel()
        modelo.setStringList(estaciones_ordenadas)
        listView_Ordenamiento.setModel(modelo)




    @staticmethod
    def cumple_criterio(linea, lineas_estacion):
        return linea in lineas_estacion
    
    @staticmethod
    def Insercion(estaciones,txt_Time):
        print("Ejecutando Inserción")
        inicio = time.time()
        for i in range(1, len(estaciones)):
            clave = estaciones[i]
            j = i - 1
            while j >= 0 and estaciones[j] > clave:
                estaciones[j + 1] = estaciones[j]
                j -= 1
            estaciones[j + 1] = clave
        fin = time.time()
        print(f"Tiempo de ejecución (Inserción): {fin - inicio:.6f} segundos")
        txt_Time.append(f"{fin - inicio:.6f} segundos")
        return estaciones

    @staticmethod
    def Burbuja(estaciones,txt_Time):
        print("Ejecutando Burbuja")
        inicio = time.time()
        n = len(estaciones)
        for i in range(n):
            for j in range(0, n - i - 1):
                if estaciones[j] > estaciones[j + 1]:
                    estaciones[j], estaciones[j + 1] = estaciones[j + 1], estaciones[j]
        fin = time.time()
        print(f"Tiempo de ejecución (Burbuja): {fin - inicio:.6f} segundos")
        txt_Time.append(f"{fin - inicio:.6f} segundos")
        return estaciones

    @staticmethod
    def Seleccion(estaciones,txt_Time):
        print("Ejecutando Selección")
        inicio = time.time()
        n = len(estaciones)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if estaciones[j] < estaciones[min_idx]:
                    min_idx = j
            estaciones[i], estaciones[min_idx] = estaciones[min_idx], estaciones[i]
        fin = time.time()
        print(f"Tiempo de ejecución {fin - inicio:.6f} segundos")
        txt_Time.append(f"{fin - inicio:.6f} segundos")
        return estaciones

    @staticmethod
    def Mezcla(estaciones,txt_Time):
        print("Ejecutando Mezcla")
        inicio = time.time()

        def merge_sort(lista):
            if len(lista) > 1:
                mid = len(lista) // 2
                izquierda = lista[:mid]
                derecha = lista[mid:]

                merge_sort(izquierda)
                merge_sort(derecha)

                i = j = k = 0
                while i < len(izquierda) and j < len(derecha):
                    if izquierda[i] < derecha[j]:
                        lista[k] = izquierda[i]
                        i += 1
                    else:
                        lista[k] = derecha[j]
                        j += 1
                    k += 1

                while i < len(izquierda):
                    lista[k] = izquierda[i]
                    i += 1
                    k += 1

                while j < len(derecha):
                    lista[k] = derecha[j]
                    j += 1
                    k += 1

        merge_sort(estaciones)
        fin = time.time()
        print(f"Tiempo de ejecución (Mezcla): {fin - inicio:.6f} segundos")
        txt_Time.append(f"{fin - inicio:.6f} segundos")
        
        return estaciones

    @staticmethod
    def Rapido(estaciones,txt_Time):
        print("Ejecutando Rápido")
        inicio = time.time()

        def quick_sort(lista):
            if len(lista) <= 1:
                return lista
            else:
                pivote = lista[0]
                menores = [x for x in lista[1:] if x <= pivote]
                mayores = [x for x in lista[1:] if x > pivote]
                return quick_sort(menores) + [pivote] + quick_sort(mayores)

        resultado = quick_sort(estaciones)
        fin = time.time()
        # print(f"Tiempo de ejecución (Rápido): {fin - inicio:.6f} segundos")
        txt_Time.append(f"{fin - inicio:.6f} segundos")
        return resultado
