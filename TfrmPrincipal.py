import os
import sys
import yaml  # type: ignore
import time  
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QStringListModel
from TrfmAgregar import AgregarEstacion
from TfrmEliminar import EliminarEstacion_Linea


class TransporteApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransporteApp, self).__init__()
        uic.loadUi('interfaces/TfrmPrincipal.ui', self)

        # Crear la instancia de GrafoTransporte
        self.grafo_transporte = GrafoTransporte()

        self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))

        # Conectar el botón a la función
        self.btn_BuscarEstacion.clicked.connect(self.obtener_seleccion)
        # self.btn_BuscarEstacion.clicked.connect(self.OrdenamientoInsercion)
        self.btn_BuscarEstacion.clicked.connect(self.OrdenamientoMezcla)


        # Conectar el botón de crear estación a la función
        self.btn_creaEstacion.clicked.connect(self.abrir_crear_estacion)
        # Conectar el botón de eliminar la estación
        self.btn_Eliminar_Estacion.clicked.connect(self.Eliminar_Estacion)

        # Crear el modelo para QListView
        self.estaciones_model = QStringListModel(self)
        self.listView.setModel(self.estaciones_model)  # Asignar el modelo al QListView

    def obtener_seleccion(self):
        linea_seleccionada = self.comboBox.currentText()
        print(f"Línea seleccionada: {linea_seleccionada}")
        self.grafo_transporte.LoadFromYAML("STPMG.yaml")  # Refrescar los datos desde el archivo
        self.manejar_seleccion(linea_seleccionada)

    def manejar_seleccion(self, linea):
        estaciones = self.grafo_transporte.NameLine.get(linea, [])
        self.clearListView()
        self.estaciones_model.setStringList(estaciones)

    def clearListView(self):
        self.estaciones_model.setStringList([])
        
    def OrdenamientoMezcla(self):
        estaciones = self.grafo_transporte.get_all_estaciones()

        # Eliminar estaciones repetidas
        estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

        countEstations = len(estaciones_unicas)  # Número de estaciones únicas

        start_time = time.time()

        # Algoritmo de ordenamiento por mezcla
        estaciones_unicas = self.merge_sort(estaciones_unicas)

        # Calcular el tiempo de ordenamiento
        elapsed_time = time.time() - start_time

        # Mostrar estaciones ordenadas en el QListView
        self.estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])

        # Mostrar el diálogo con el tiempo de ordenamiento
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ordenamiento completado")
        msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
        msg.exec_()

        # Mostrar detalles adicionales si es necesario
        print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
        print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
        print(f"Numero de estaciones: {countEstations}")

    # Función auxiliar para el algoritmo de ordenamiento por mezcla
    def merge_sort(self, lista):
        if len(lista) > 1:
            mid = len(lista) // 2  # Punto medio de la lista
            izquierda = lista[:mid]  # Dividir en sublista izquierda
            derecha = lista[mid:]  # Dividir en sublista derecha

            # Ordenar ambas mitades recursivamente
            izquierda = self.merge_sort(izquierda)
            derecha = self.merge_sort(derecha)

            # Mezclar las dos mitades ordenadas
            lista_ordenada = self.merge(izquierda, derecha)
            return lista_ordenada
        else:
            return lista  # Retorna la lista si tiene un solo elemento

    # Función para mezclar dos listas ordenadas
    def merge(self, izquierda, derecha):
        resultado = []
        i = j = 0

        # Mezclar ambas listas mientras haya elementos en ambas
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].nombre < derecha[j].nombre:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Agregar los elementos restantes (si quedan) en las sublistas
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado
    
    # def OrdenamientoSeleccion(self):
    #     estaciones = self.grafo_transporte.get_all_estaciones()

    #     estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

    #     countEstations = len(estaciones_unicas) 

    #     start_time = time.time()

    #     # Algoritmo de ordenamiento por seleccion
    #     n = len(estaciones_unicas)
    #     for i in range(n - 1):
    #         # Encontrar el índice del mínimo elemento desde i hasta el final
    #         min_idx = i
    #         for j in range(i + 1, n):
    #             if estaciones_unicas[j].nombre < estaciones_unicas[min_idx].nombre:
    #                 min_idx = j

    #         estaciones_unicas[i], estaciones_unicas[min_idx] = estaciones_unicas[min_idx], estaciones_unicas[i]

    #     elapsed_time = time.time() - start_time

    #     # Mostrar estaciones ordenadas en el QListView
    #     self.estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])

    #     msg = QtWidgets.QMessageBox()
    #     msg.setWindowTitle("Ordenamiento completado")
    #     msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     msg.exec_()

    #     print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #     print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     print(f"Numero de estaciones: {countEstations}")
        
    # def OrdenamientoBurbuja(self):
    #     estaciones = self.grafo_transporte.get_all_estaciones()

      
    #     estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

    #     countEstations = len(estaciones_unicas) 

    #     start_time = time.time()

    #     # ordenamiento por burbuja
    #     n = len(estaciones_unicas)
    #     for i in range(n - 1):
    #         for j in range(n - i - 1):
    #             if estaciones_unicas[j].nombre > estaciones_unicas[j + 1].nombre:
    #                 estaciones_unicas[j], estaciones_unicas[j + 1] = estaciones_unicas[j + 1], estaciones_unicas[j]

    #     # Tiempo
    #     elapsed_time = time.time() - start_time
    #     print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #     print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     print(f"Numero de estaciones: {countEstations}")

    #     # Mostrar estaciones ordenadas en el QListView
    #     self.estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])
    #     msg = QtWidgets.QMessageBox()
    #     msg.setWindowTitle("Ordenamiento completado")
    #     msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     msg.exec_()



    
    # def OrdenamientoInsercion(self):
    #     linea_seleccionada = self.comboBox.currentText()  # Obtener la línea seleccionada
    #     estaciones = self.grafo_transporte.NameLine.get(linea_seleccionada, [])  # Obtener las estaciones de esa línea

    #     # Medir el tiempo de ejecución
    #     start_time = time.time()
    #     countEstations = 1
    #     # Algoritmo de ordenamiento por inserción
    #     for i in range(1, len(estaciones)):
    #         key = estaciones[i]
    #         j = i - 1
    #         countEstations += 1
    #         while j >= 0 and key < estaciones[j]:  # Comparar los nombres de las estaciones
    #             estaciones[j + 1] = estaciones[j]
    #             j -= 1
    #         estaciones[j + 1] = key

    #     # Mostrar el tiempo transcurrido
    #     elapsed_time = time.time() - start_time
    #     print(f"Estaciones ordenadas por nombre en la línea {linea_seleccionada}: {estaciones}")
    #     print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     print(f"numero estaciones: {countEstations}")

    #     # Mostrar estaciones ordenadas en el QListView
    #     self.estaciones_model.setStringList(estaciones)  # Mostrar los nombres ordenados  
        
    # def OrdenamientoInsercion(self):
    #     estaciones = self.grafo_transporte.get_all_estaciones()
        
    #     # Usar un conjunto para eliminar duplicados y luego convertirlo a lista
    #     estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())
        
    #     countEstations = 1
        
    #     # Medir el tiempo de ejecución
    #     start_time = time.time()

    #     # Algoritmo de ordenamiento por inserción
    #     for i in range(1, len(estaciones_unicas)):
    #         key = estaciones_unicas[i]
    #         countEstations += 1
    #         j = i - 1
    #         while j >= 0 and key.nombre < estaciones_unicas[j].nombre:
    #             estaciones_unicas[j + 1] = estaciones_unicas[j]
    #             j -= 1
    #         estaciones_unicas[j + 1] = key

    #     # Mostrar el tiempo transcurrido
    #     elapsed_time = time.time() - start_time
    #     print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #     print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #     print(f"numero estaciones: {countEstations}")

    #     # Mostrar estaciones ordenadas en el QListView
    #     self.estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])



    def abrir_crear_estacion(self):
        # Crear y mostrar la ventana de crear estación
        self.crear_estacion_window = AgregarEstacion(self)
        if self.crear_estacion_window.exec_():  # Mostrar la ventana como un diálogo modal
            self.grafo_transporte.LoadFromYAML("STPMG.yaml")  # Recargar el YAML después de agregar la estación
            self.comboBox.clear()  # Limpiar el ComboBox
            self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))  # Actualizar las líneas

    def Eliminar_Estacion(self):
        # Crear y mostrar la ventana de eliminar estación
        self.crear_estacion_window = EliminarEstacion_Linea(self)
        if self.crear_estacion_window.exec_():  # Mostrar la ventana como un diálogo modal
            self.grafo_transporte.LoadFromYAML("STPMG.yaml")  # Recargar el YAML después de agregar la estación
            self.comboBox.clear()  # Limpiar el ComboBox
            self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))  # Actualizar las líneas

class Nodo:
    def __init__(self, estacion):
        self.estacion = estacion
        self.Next = None
        self.anterior = None

class Estacion:
    def __init__(self, nombre, lineas, direccion, campo_extra_cadena, campo_extra_numerico):
        self.nombre = nombre
        self.lineas = lineas
        self.direccion = direccion
        self.campo_extra_cadena = campo_extra_cadena
        self.campo_extra_numerico = campo_extra_numerico

    # def ShowInfo(self):
    #     print(f"Línea(s): {', '.join(self.lineas)}")
    #     print(f"Estación: {self.nombre}")
    #     print(f"Direccion: {self.direccion}")
    #     print(f"Campo Cadena: {self.campo_extra_cadena}")
    #     print(f"campo Numerico: {self.campo_extra_numerico}")
        

class GrafoTransporte:
    def get_all_estaciones(self):
        estaciones = []
        current_node = self.Head
        while current_node is not None:
            estaciones.append(current_node.estacion)
            current_node = current_node.Next
        return estaciones

    def __init__(self):
        self.NameStations = {}
        self.NameLine = {}
        self.Head = None
        self.cola = None
        self.LoadFromYAML("STPMG.yaml")

    def LoadFromYAML(self, file_path):
        self.NameStations.clear()
        self.NameLine.clear()
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            # Crear un archivo YAML vacío si no existe
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump([], file)
            print(f"Archivo {file_path} creado porque no existía.")

        # Leer el archivo YAML (aunque esté vacío)
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = yaml.safe_load(file) or []  # Cargar YAML y manejar si está vacío
            except yaml.YAMLError as exc:
                print(f"Error al leer el archivo YAML: {exc}")
                data = []

        if isinstance(data, list):
            for estacion_data in data:
                if isinstance(estacion_data, dict):  
                    nombre_estacion = estacion_data.get("Nombre")
                    lineas = estacion_data.get("Lineas", [])
                    direccion = estacion_data.get("Direccion", "")
                    campo_extra_cadena = estacion_data.get("ExtraCadena", "")
                    campo_extra_numerico = estacion_data.get("ExtraNumerico", 0)

                    if nombre_estacion:  # Solo procesar si el nombre de la estación existe
                        nueva_estacion = Estacion(
                            nombre=nombre_estacion,
                            lineas=lineas,
                            direccion=direccion,
                            campo_extra_cadena=campo_extra_cadena,
                            campo_extra_numerico=campo_extra_numerico
                        )

                        NewNodo = Nodo(nueva_estacion)

                        if self.Head is None:
                            self.Head = NewNodo
                            self.cola = NewNodo
                        else:
                            self.cola.Next = NewNodo
                            NewNodo.anterior = self.cola
                            self.cola = NewNodo

                        self.NameStations[nombre_estacion] = NewNodo

                        for linea in lineas:
                            if linea not in self.NameLine:
                                self.NameLine[linea] = []
                            self.NameLine[linea].append(nombre_estacion)
                else:
                    print("Dato inválido encontrado en el archivo YAML.")
        else:
            print("El archivo YAML no contiene una lista válida de estaciones.")




# Configuración del programa principal
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TransporteApp()
    window.show()
    app.exec_()
