import os
import yaml  # type: ignore

class Nodo:
    def __init__(self, estacion):
        self.estacion = estacion
        self.next = None
        self.anterior = None

class Estacion:
    def __init__(self, nombre, lineas, conexiones):
        self.nombre = nombre
        self.lineas = lineas
        self.conexiones = conexiones

class GrafoTransporte:
    def __init__(self):
        self.NameStations = {}
        self.NameLine = {}
        self.Head = None
        self.cola = None
        self.LoadFromYAML("STPMG.yaml")

    def get_all_estaciones(self):
        estaciones = []
        current_node = self.Head
        while current_node is not None:
            estaciones.append(current_node.estacion)
            current_node = current_node.next
        return estaciones

    def LoadFromYAML(self, file_path):
        self.NameStations.clear()
        self.NameLine.clear()

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump({"Estaciones": []}, file)
            print(f"Archivo {file_path} creado porque no existía.")

        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = yaml.safe_load(file) or {}
            except yaml.YAMLError as exc:
                print(f"Error al leer el archivo YAML: {exc}")
                data = {}

        estaciones_data = data.get("Estaciones", [])

        if isinstance(estaciones_data, list):
            for estacion_data in estaciones_data:
                if isinstance(estacion_data, dict):
                    nombre_estacion = estacion_data.get("Estacion")
                    lineas = estacion_data.get("Lineas", [])
                    conexiones = estacion_data.get("Conexiones", "")

                    if nombre_estacion:
                        nueva_estacion = Estacion(
                            nombre=nombre_estacion,
                            lineas=lineas,
                            conexiones=conexiones
                        )
                        NewNodo = Nodo(nueva_estacion)

                        if self.Head is None:
                            self.Head = NewNodo
                            self.cola = NewNodo
                        else:
                            self.cola.next = NewNodo
                            NewNodo.anterior = self.cola
                            self.cola = NewNodo

                        self.NameStations[nombre_estacion] = NewNodo

                        for linea in lineas:
                            if linea not in self.NameLine:
                                self.NameLine[linea] = []
                            self.NameLine[linea].append(nombre_estacion)
                    else:
                        print("Una estación sin nombre fue ignorada.")
        else:
            print("El archivo YAML no contiene una lista válida de estaciones.")
