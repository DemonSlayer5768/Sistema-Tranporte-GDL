import yaml  # type: ignore
from PyQt5 import QtWidgets
from Estacion import GrafoTransporte, Estacion, Nodo  

class Agregar:
    def guardar_estacion(Tedit_Nombre, Tedit_Linea, Tedit_Anterior, Tedit_Siguiente):
        # Obtener datos ingresados por el usuario
        nombre = Tedit_Nombre.text().strip()
        linea = Tedit_Linea.text().strip()
        anterior = Tedit_Anterior.text().strip()
        siguiente = Tedit_Siguiente.text().strip()

        # Validar que los campos no estén vacíos
        if not nombre or not linea:
            QtWidgets.QMessageBox.warning(None, "Error", "Los campos Nombre y Línea son obligatorios.")
            return

        # Crear la estructura de la estación
        nueva_estacion = Estacion(
            nombre=nombre,
            lineas=[linea],
            conexiones=[anterior, siguiente]
        )

        # Inicializar el grafo de transporte
        grafo = GrafoTransporte()

        # Verificar si la estación ya existe
        if nombre in grafo.NameStations:
            QtWidgets.QMessageBox.warning(None, "Error", "La estación ya existe.")
            return

        # Crear el nuevo nodo para la estación
        nuevo_nodo = Nodo(nueva_estacion)

        # Agregar la estación al grafo
        if grafo.Head is None:
            grafo.Head = nuevo_nodo
            grafo.cola = nuevo_nodo
        else:
            grafo.cola.next = nuevo_nodo
            nuevo_nodo.anterior = grafo.cola
            grafo.cola = nuevo_nodo

        grafo.NameStations[nombre] = nuevo_nodo

        # Actualizar las líneas en el grafo
        for linea in nueva_estacion.lineas:
            if linea not in grafo.NameLine:
                grafo.NameLine[linea] = []
            grafo.NameLine[linea].append(nombre)

        # Guardar las estaciones en el archivo YAML
        archivo_yaml = "STPMG.yaml"

        # Leer las estaciones existentes del archivo YAML
        try:
            with open(archivo_yaml, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
        except FileNotFoundError:
            data = {"Estaciones": []}  # Si no existe el archivo, inicializar la clave 'Estaciones'

        # Agregar la nueva estación a la lista de estaciones en YAML
        nueva_estacion_yaml = {
            "Estacion": nombre,
            "Lineas": nueva_estacion.lineas,
            "Conexiones": nueva_estacion.conexiones
        }
        data["Estaciones"].append(nueva_estacion_yaml)

        # Guardar los datos actualizados en el archivo YAML
        with open(archivo_yaml, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

        # Confirmar el guardado y limpiar los campos
        QtWidgets.QMessageBox.information(None, "Exito", "Estación guardada correctamente.")
        Agregar.limpiar_campos(Tedit_Nombre, Tedit_Linea, Tedit_Anterior, Tedit_Siguiente)

    def limpiar_campos(Tedit_Nombre, Tedit_Linea, Tedit_Anterior, Tedit_Siguiente):
        # Limpiar los campos de texto
        Tedit_Nombre.clear()
        Tedit_Linea.clear()
        Tedit_Anterior.clear()
        Tedit_Siguiente.clear()
