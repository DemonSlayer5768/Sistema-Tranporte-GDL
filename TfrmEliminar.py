import yaml  # type: ignore
from PyQt5 import QtWidgets
from Estacion import GrafoTransporte, Estacion, Nodo 

class Eliminar:
    
   
    
    @staticmethod
    def cargar_lineas_Eliminar(cmb_Linea):
        grafo_transporte = GrafoTransporte()
         
        cmb_Linea.clear()  # Limpiar el ComboBox
        cmb_Linea.addItem("Todas")  # Agregar la opción 'Todas'
        cmb_Linea.addItems(list(grafo_transporte.NameLine.keys()))  # Agregar las líneas


    
    @staticmethod
    def cargar_estaciones(linea_seleccionada, cmb_Estacion):
        # Instancia del grafo de transporte
        grafo_transporte = GrafoTransporte()
        
        # Si la entrada es un QComboBox, obtenemos el texto seleccionado
        if isinstance(linea_seleccionada, QtWidgets.QComboBox):
            linea_seleccionada = linea_seleccionada.currentText()

        print("Línea seleccionada:", linea_seleccionada)

        # Filtrado de estaciones según la línea seleccionada
        if linea_seleccionada == "Todas":
            estaciones_filtradas = [
                nodo.estacion.nombre for nodo in grafo_transporte.NameStations.values()
            ]  # Todas las estaciones
        else:
            estaciones_filtradas = [
                nodo.estacion.nombre
                for nodo in grafo_transporte.NameStations.values()
                if Eliminar.cumple_criterio(linea_seleccionada, nodo.estacion.lineas)
            ]

        print("Estaciones filtradas:", estaciones_filtradas)

        # Cargar estaciones en el QComboBox
        cmb_Estacion.clear()
        cmb_Estacion.addItems(estaciones_filtradas)



    @staticmethod
    def cumple_criterio(linea, lineas_estacion):
        return linea in lineas_estacion


    @staticmethod
    def eliminar_estacion(cmb_Linea, cmb_Estacion):
        # Obtener línea y estación seleccionadas
        nombre_estacion = cmb_Estacion.currentText().strip()
        nombre_linea = cmb_Linea.currentText().strip()

        # Validar que los campos no estén vacíos
        if not nombre_estacion or not nombre_linea:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione una línea y una estación para eliminar.")
            return

        # Confirmar eliminación
        respuesta = QtWidgets.QMessageBox.question(
            None,
            "Confirmar eliminación",
            f"¿Eliminar la estación '{nombre_estacion}' de la línea '{nombre_linea}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        ) 

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
                # Inicializar el grafo de transporte
                grafo = GrafoTransporte()

                # Verificar si la estación existe en el grafo
                if nombre_estacion not in grafo.NameStations:
                    QtWidgets.QMessageBox.warning(None, "Error", "La estación no existe en el grafo.")
                    return

                # Obtener el nodo de la estación
                nodo_estacion = grafo.NameStations[nombre_estacion]

                # Actualizar conexiones
                if nodo_estacion.anterior:
                    nodo_estacion.anterior.next = nodo_estacion.next
                if nodo_estacion.next:
                    nodo_estacion.next.anterior = nodo_estacion.anterior

                # Actualizar la cabeza y cola del grafo si corresponde
                if grafo.Head == nodo_estacion:
                    grafo.Head = nodo_estacion.next
                if grafo.cola == nodo_estacion:
                    grafo.cola = nodo_estacion.anterior

                # Eliminar la estación del grafo
                del grafo.NameStations[nombre_estacion]

                # Actualizar las líneas asociadas
                if nombre_linea in grafo.NameLine:
                    grafo.NameLine[nombre_linea].remove(nombre_estacion)
                    if not grafo.NameLine[nombre_linea]:  # Eliminar línea si no tiene estaciones
                        del grafo.NameLine[nombre_linea]

                # Actualizar el archivo YAML
                archivo_yaml = "STPMG.yaml"
                with open(archivo_yaml, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file) or {}

                # Eliminar la estación del archivo YAML
                data["Estaciones"] = [
                    estacion for estacion in data.get("Estaciones", [])
                    if estacion["Estacion"] != nombre_estacion
                ]

                with open(archivo_yaml, "w", encoding="utf-8") as file:
                    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

                # Confirmar eliminación
                QtWidgets.QMessageBox.information(None, "Éxito", f"La estación '{nombre_estacion}' ha sido eliminada.")
                cmb_Estacion.clear()  # Refrescar ComboBox de estaciones

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Ocurrió un error al eliminar la estación: {str(e)}")
                
    @staticmethod
    def eliminar_linea(cmb_Linea):
        # Obtener la línea seleccionada
        nombre_linea = cmb_Linea.currentText().strip()

        # Validar que el campo no esté vacío
        if not nombre_linea:
            QtWidgets.QMessageBox.warning(None, "Error", "Seleccione una línea para eliminar.")
            return

        # Confirmar eliminación
        respuesta = QtWidgets.QMessageBox.question(
            None,
            "Confirmar eliminación",
            f"¿Eliminar la línea '{nombre_linea}' y todas sus estaciones asociadas?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
                # Inicializar el grafo de transporte
                grafo = GrafoTransporte()

                # Verificar si la línea existe en el grafo
                if nombre_linea not in grafo.NameLine:
                    QtWidgets.QMessageBox.warning(None, "Error", "La línea no existe en el grafo.")
                    return

                # Obtener las estaciones asociadas a la línea
                estaciones_asociadas = grafo.NameLine[nombre_linea]

                # Eliminar las estaciones del grafo
                for estacion in estaciones_asociadas:
                    if estacion in grafo.NameStations:
                        nodo_estacion = grafo.NameStations[estacion]

                        # Actualizar conexiones
                        if nodo_estacion.anterior:
                            nodo_estacion.anterior.next = nodo_estacion.next
                        if nodo_estacion.next:
                            nodo_estacion.next.anterior = nodo_estacion.anterior

                        # Actualizar la cabeza y cola del grafo si corresponde
                        if grafo.Head == nodo_estacion:
                            grafo.Head = nodo_estacion.next
                        if grafo.cola == nodo_estacion:
                            grafo.cola = nodo_estacion.anterior

                        # Eliminar la estación del grafo
                        del grafo.NameStations[estacion]

                # Eliminar la línea del grafo
                del grafo.NameLine[nombre_linea]

                # Actualizar el archivo YAML
                archivo_yaml = "STPMG.yaml"
                with open(archivo_yaml, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file) or {}

                # Eliminar las estaciones y la línea del archivo YAML
                data["Estaciones"] = [
                    estacion for estacion in data.get("Estaciones", [])
                    if nombre_linea not in estacion["Lineas"]
                ]

                with open(archivo_yaml, "w", encoding="utf-8") as file:
                    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

                # Confirmar eliminación
                QtWidgets.QMessageBox.information(None, "Éxito", f"La línea '{nombre_linea}' y sus estaciones han sido eliminadas.")
                cmb_Linea.clear()  # Refrescar ComboBox de líneas

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Ocurrió un error al eliminar la línea: {str(e)}")
