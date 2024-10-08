import sys
import yaml # type: ignore
from PyQt5 import QtWidgets, uic

class AgregarEstacion(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AgregarEstacion, self).__init__(parent)
        uic.loadUi('interfaces/AgregarEstacion.ui', self)

        self.btn_guardar = self.findChild(QtWidgets.QPushButton, 'btn_guardar')
        self.line_edit_nombre = self.findChild(QtWidgets.QLineEdit, 'line_edit_nombre')
        self.line_edit_linea = self.findChild(QtWidgets.QLineEdit, 'line_edit_linea')
        self.line_edit_direccion = self.findChild(QtWidgets.QLineEdit, 'line_edit_direccion')

        self.btn_guardar.clicked.connect(self.guardar_estacion)

    def guardar_estacion(self):
        nombre_estacion = self.line_edit_nombre.text().strip()
        linea_estacion = self.line_edit_linea.text().strip()
        direccion = self.line_edit_direccion.text().strip()

        if nombre_estacion and linea_estacion:
            self.modificar_yaml(nombre_estacion, linea_estacion, direccion)
            self.accept()  # Cierra el diálogo
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, completa todos los campos requeridos.")

    def modificar_yaml(self, nombre, linea, direccion):
        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        # Asegúrate de que la clave 'lineas' exista
        if 'lineas' not in data:
            data['lineas'] = []

        # Buscar la línea correspondiente
        linea_encontrada = next((linea_data for linea_data in data['lineas'] if linea_data['nombre'] == linea), None)

        # Si la línea no existe, agregarla
        if not linea_encontrada:
            linea_encontrada = {'nombre': linea, 'estaciones': []}
            data['lineas'].append(linea_encontrada)

        # Si la estación no existe, agregarla a la línea
        if nombre not in linea_encontrada['estaciones']:
            linea_encontrada['estaciones'].append(nombre)

        # Ordenar las estaciones para mantener un orden correcto
        linea_encontrada['estaciones'].sort()


        # Guardar los cambios de vuelta en el archivo YAML
        with open("STPMG.yaml", "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)

# Código para ejecutar la aplicación si es necesario
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AgregarEstacion()
    window.show()
    sys.exit(app.exec_())
