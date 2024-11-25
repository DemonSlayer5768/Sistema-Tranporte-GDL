import time
from PyQt5 import QtWidgets
import Estacion


class AlgoritmosOrdenamiento:
    
    def cargar_Lineas_Orden(cmb_OrdenarLineas):
   
        grafo_transporte = Estacion.GrafoTransporte()
         
        cmb_OrdenarLineas.clear()  # Limpiar el ComboBox
        cmb_OrdenarLineas.addItem("Todas")  # Agregar la opción 'Todas'
        cmb_OrdenarLineas.addItems(list(grafo_transporte.NameLine.keys()))  # Agregar las líneas

    
    # componentes dela clase TransporteApp
    # LineaSeleccionada = TransporteApp.cmb_OrdenarLineas
    # insercion = TransporteApp.rBtn_Insercion
    # burbuja = TransporteApp.rBtn_Burbuja
    # seleccion = TransporteApp.rBtn_Seleccion
    # mezcla  = TransporteApp.rBtn_Mezcla
    # rapido = TransporteApp.rBtn_Rapido
    # btn_ordenar = TransporteApp.btn_Ordenar
    # txtTime = TransporteApp.txtEdit_Time
    # listViewO = TransporteApp.listView_Ordenamiento
    
    
    

    # def OrdenamientoMezcla(Estaciones):
    #         estaciones = Estacion.grafo_transporte.get_all_estaciones()

    #         # Eliminar estaciones repetidas
    #         estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

    #         countEstations = len(estaciones_unicas)  # Número de estaciones únicas

    #         start_time = time.time()

    #         # Algoritmo de ordenamiento por mezcla
    #         estaciones_unicas = merge_sort(estaciones_unicas)

    #         # Calcular el tiempo de ordenamiento
    #         elapsed_time = time.time() - start_time

    #         # Mostrar estaciones ordenadas en el QListView
    #         estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])

    #         # Mostrar el diálogo con el tiempo de ordenamiento
    #         msg = QtWidgets.QMessageBox()
    #         msg.setWindowTitle("Ordenamiento completado")
    #         msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         msg.exec_()

    #         # Mostrar detalles adicionales si es necesario
    #         print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #         print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         print(f"Numero de estaciones: {countEstations}")

    #     # Función auxiliar para el algoritmo de ordenamiento por mezcla
    #     def merge_sort(lista):
    #         if len(lista) > 1:
    #             mid = len(lista) // 2  # Punto medio de la lista
    #             izquierda = lista[:mid]  # Dividir en sublista izquierda
    #             derecha = lista[mid:]  # Dividir en sublista derecha

    #             # Ordenar ambas mitades recursivamente
    #             izquierda = merge_sort(izquierda)
    #             derecha = merge_sort(derecha)

    #             # Mezclar las dos mitades ordenadas
    #             lista_ordenada = merge(izquierda, derecha)
    #             return lista_ordenada
    #         else:
    #             return lista  # Retorna la lista si tiene un solo elemento

    #     # Función para mezclar dos listas ordenadas
    #     def merge(izquierda, derecha):
    #         resultado = []
    #         i = j = 0

    #         # Mezclar ambas listas mientras haya elementos en ambas
    #         while i < len(izquierda) and j < len(derecha):
    #             if izquierda[i].nombre < derecha[j].nombre:
    #                 resultado.append(izquierda[i])
    #                 i += 1
    #             else:
    #                 resultado.append(derecha[j])
    #                 j += 1

    #         # Agregar los elementos restantes (si quedan) en las sublistas
    #         resultado.extend(izquierda[i:])
    #         resultado.extend(derecha[j:])
    #         return resultado
        
    #     def OrdenamientoSeleccion():
    #         estaciones = self.grafo_transporte.get_all_estaciones()

    #         estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

    #         countEstations = len(estaciones_unicas) 

    #         start_time = time.time()

    #         # Algoritmo de ordenamiento por seleccion
    #         n = len(estaciones_unicas)
    #         for i in range(n - 1):
    #             # Encontrar el índice del mínimo elemento desde i hasta el final
    #             min_idx = i
    #             for j in range(i + 1, n):
    #                 if estaciones_unicas[j].nombre < estaciones_unicas[min_idx].nombre:
    #                     min_idx = j

    #             estaciones_unicas[i], estaciones_unicas[min_idx] = estaciones_unicas[min_idx], estaciones_unicas[i]

    #         elapsed_time = time.time() - start_time

    #         # Mostrar estaciones ordenadas en el QListView
    #         estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])

    #         msg = QtWidgets.QMessageBox()
    #         msg.setWindowTitle("Ordenamiento completado")
    #         msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         msg.exec_()

    #         print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #         print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         print(f"Numero de estaciones: {countEstations}")
            
    #     def OrdenamientoBurbuja():
    #         estaciones = self.grafo_transporte.get_all_estaciones()

        
    #         estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())

    #         countEstations = len(estaciones_unicas) 

    #         start_time = time.time()

    #         # ordenamiento por burbuja
    #         n = len(estaciones_unicas)
    #         for i in range(n - 1):
    #             for j in range(n - i - 1):
    #                 if estaciones_unicas[j].nombre > estaciones_unicas[j + 1].nombre:
    #                     estaciones_unicas[j], estaciones_unicas[j + 1] = estaciones_unicas[j + 1], estaciones_unicas[j]

    #         # Tiempo
    #         elapsed_time = time.time() - start_time
    #         print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #         print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         print(f"Numero de estaciones: {countEstations}")

    #         # Mostrar estaciones ordenadas en el QListView
    #         estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])
    #         msg = QtWidgets.QMessageBox()
    #         msg.setWindowTitle("Ordenamiento completado")
    #         msg.setText(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         msg.exec_()



        
    #     def OrdenamientoInsercion():
    #         linea_seleccionada = comboBox.currentText()  # Obtener la línea seleccionada
    #         estaciones = Estacion.grafo_transporte.NameLine.get(linea_seleccionada, [])  # Obtener las estaciones de esa línea

    #         # Medir el tiempo de ejecución
    #         start_time = time.time()
    #         countEstations = 1
    #         # Algoritmo de ordenamiento por inserción
    #         for i in range(1, len(estaciones)):
    #             key = estaciones[i]
    #             j = i - 1
    #             countEstations += 1
    #             while j >= 0 and key < estaciones[j]:  # Comparar los nombres de las estaciones
    #                 estaciones[j + 1] = estaciones[j]
    #                 j -= 1
    #             estaciones[j + 1] = key

    #         # Mostrar el tiempo transcurrido
    #         elapsed_time = time.time() - start_time
    #         print(f"Estaciones ordenadas por nombre en la línea {linea_seleccionada}: {estaciones}")
    #         print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         print(f"numero estaciones: {countEstations}")

    #         # Mostrar estaciones ordenadas en el QListView
    #         self.estaciones_model.setStringList(estaciones)  # Mostrar los nombres ordenados  
            
    #     def OrdenamientoInsercion():
    #         estaciones = grafo_transporte.get_all_estaciones()
            
    #         # Usar un conjunto para eliminar duplicados y luego convertirlo a lista
    #         estaciones_unicas = list({estacion.nombre: estacion for estacion in estaciones}.values())
            
    #         countEstations = 1
            
    #         # Medir el tiempo de ejecución
    #         start_time = time.time()

    #         # Algoritmo de ordenamiento por inserción
    #         for i in range(1, len(estaciones_unicas)):
    #             key = estaciones_unicas[i]
    #             countEstations += 1
    #             j = i - 1
    #             while j >= 0 and key.nombre < estaciones_unicas[j].nombre:
    #                 estaciones_unicas[j + 1] = estaciones_unicas[j]
    #                 j -= 1
    #             estaciones_unicas[j + 1] = key

    #         # Mostrar el tiempo transcurrido
    #         elapsed_time = time.time() - start_time
    #         print(f"Estaciones ordenadas por nombre: {[estacion.nombre for estacion in estaciones_unicas]}")
    #         print(f"Tiempo de ordenamiento: {elapsed_time:.6f} segundos")
    #         print(f"numero estaciones: {countEstations}")

    #         # Mostrar estaciones ordenadas en el QListView
    #         estaciones_model.setStringList([estacion.nombre for estacion in estaciones_unicas])

