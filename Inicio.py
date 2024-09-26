import sys
import yaml
from PyQt5 import QtWidgets, uic 
from PyQt5.QtCore import QStringListModel
from AgregarEstacion import AgregarEstacion


class Nodo:
    def __init__(self, estacion):
        self.estacion = estacion
        self.Next = None
        self.anterior = None

class Estacion:
    def __init__(self, nombre, lineas, direccion, horario_servicio, campo_extra_cadena, campo_extra_numerico):
        self.nombre = nombre
        self.lineas = lineas
        self.direccion = direccion
        self.horario_servicio = horario_servicio
        self.campo_extra_cadena = campo_extra_cadena
        self.campo_extra_numerico = campo_extra_numerico

    def ShowInfo(self):
        print(f"Línea(s): {', '.join(self.lineas)}")
        print(f"Estación: {self.nombre}")
        print(f"Siguiente estación: {self.direccion}")
        print(f"Horario de Servicio: {self.horario_servicio}")
        print()

class GrafoTransporte:
    def __init__(self):
        self.NameStations = {}
        self.NameLine = {}
        self.Head = None
        self.cola = None
        self.LoadFromYAML("STPMG.yaml")

    def LoadFromYAML(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        for linea_data in data['lineas']:
            nombre_linea = linea_data['nombre']
            estaciones = linea_data['estaciones']
            self.CreateEstations(estaciones, nombre_linea)

    def CreateEstations(self, nombres, linea):
        # Crear una lista para almacenar las estaciones de esta línea
        estaciones_linea = []
        
        for i, Name in enumerate(nombres):
            direccion = nombres[i + 1] if i < len(nombres) - 1 else f"Fin de la línea ({linea})"
            nueva_estacion = Estacion(
                nombre=Name,
                lineas=[linea],
                direccion=direccion,
                horario_servicio="De 5:00 AM a 11:00 PM",
                campo_extra_cadena="N/A",
                campo_extra_numerico=0
            )
            NewNodo = Nodo(nueva_estacion)

            if self.Head is None:
                self.Head = NewNodo
                self.cola = NewNodo
            else:
                self.cola.Next = NewNodo
                NewNodo.anterior = self.cola
                self.cola = NewNodo

            # Añadir la estación a la lista de estaciones de esta línea
            estaciones_linea.append(Name)
            self.NameStations[Name] = NewNodo

        # Almacenar solo las estaciones de esta línea
        self.NameLine[linea] = estaciones_linea


class TransporteApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransporteApp, self).__init__()
        uic.loadUi('interfaces/UI_TranporteGDL.ui', self)

        # Crear la instancia de GrafoTransporte
        self.grafo_transporte = GrafoTransporte()

        # Agregar líneas al ComboBox
        self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))

        # Conectar el botón a la función
        self.btn_BuscarEstacion.clicked.connect(self.obtener_seleccion)
        
          # Conectar el botón de crear estación a la función
        self.btn_creaEstacion.clicked.connect(self.abrir_crear_estacion)

        # Crear el modelo para QListView
        self.estaciones_model = QStringListModel(self)
        self.listView.setModel(self.estaciones_model)  # Asignar el modelo al QListView

    def obtener_seleccion(self):
        linea_seleccionada = self.comboBox.currentText()
        print(f"Línea seleccionada: {linea_seleccionada}")
        self.manejar_seleccion(linea_seleccionada)


    def manejar_seleccion(self, linea):
        # Obtener las estaciones de la línea seleccionada
        estaciones = self.grafo_transporte.NameLine.get(linea, [])
        print(f"Estaciones para {linea}: {', '.join(estaciones)}")

        # Limpiar el modelo de la lista
        self.clearListView()  # Limpiar la lista antes de agregar las nuevas estaciones
        print("Limpiando lista...")

        # Ahora actualizar el modelo con las estaciones de la línea seleccionada
        self.estaciones_model.setStringList(estaciones)

        # Verificar que las estaciones nuevas se hayan añadido correctamente
        print(f"Contenido nuevo de la lista: {self.estaciones_model.stringList()}")

    def clearListView(self):
        # Método para limpiar la lista
        self.estaciones_model.setStringList([])  # Esto limpia la lista vaciándola

        # Asegurarse de que el modelo esté vinculado al QListView
        self.listView.setModel(self.estaciones_model)



    def abrir_crear_estacion(self):
        # Crear y mostrar la ventana de crear estación
        self.crear_estacion_window = AgregarEstacion(self)
        if self.crear_estacion_window.exec_():  # Mostrar la ventana como un diálogo modal
            self.grafo_transporte.LoadFromYAML("STPMG.yaml")  # Recargar el YAML después de agregar la estación
            self.comboBox.clear()  # Limpiar el ComboBox
            self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))  # Actualizar las líneas


# Configuración del programa principal
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TransporteApp()
    window.show()
    app.exec_()
