import yaml

class Nodo:
    def __init__(self, estacion):
        self.estacion = estacion
        self.next = None

class GrafoTransporte:
    def __init__(self):
        self.lineas = {}

    def agregar_linea(self, nombre_linea, estaciones):
        nodos = [Nodo(estacion) for estacion in estaciones]
        self.lineas[nombre_linea] = nodos

    def busqueda_secuencial(self, nombre_linea):
        if nombre_linea in self.lineas:
            print(f"Línea {nombre_linea}: ", end="")
            estaciones = self.lineas[nombre_linea]
            estaciones_list = [nodo.estacion for nodo in estaciones]
            print(", ".join(estaciones_list))
        else:
            print(f"La línea {nombre_linea} no existe.")

    def guardar_datos(self, filename):
        data = []
        for nombre_linea, estaciones in self.lineas.items():
            estaciones_list = [nodo.estacion for nodo in estaciones]
            data.append({"nombre": nombre_linea, "estaciones": estaciones_list})
        
        with open(filename, 'w') as file:
            yaml.dump(data, file)

    def cargar_datos(self, filename):
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for linea in data:
                self.agregar_linea(linea['nombre'], linea['estaciones'])

# Crear una instancia del grafo y cargar datos desde el archivo YAML
grafo = GrafoTransporte()
grafo.cargar_datos("STPMG.yaml")

# Mostrar las líneas y estaciones cargadas
for linea in grafo.lineas.keys():
    grafo.busqueda_secuencial(linea)

# Agregar una nueva estación
nueva_estacion = "Nueva Estación"
nombre_linea = "Línea 1"  # Cambia esto a la línea donde deseas agregar la estación

if nombre_linea in grafo.lineas:
    grafo.lineas[nombre_linea].append(Nodo(nueva_estacion))
else:
    print(f"La línea {nombre_linea} no existe.")

# Guardar los datos nuevamente en el archivo YAML
grafo.guardar_datos("STPMG.yaml")

# Mostrar los datos nuevamente desde el archivo
print("\nDatos después de agregar la nueva estación:")
for linea in grafo.lineas.keys():
    grafo.busqueda_secuencial(linea)
