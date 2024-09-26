import sys
import yaml
from PyQt5 import QtWidgets, uic

class AgregarEstacion(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AgregarEstacion, self).__init__(parent)
        uic.loadUi('interfaces/AgregarEstacion.ui', self)

        # Conectar el botón de guardar a la función
        self.btn_guardar = self.findChild(QtWidgets.QPushButton, 'btn_guardar')
        self.line_edit_nombre = self.findChild(QtWidgets.QLineEdit, 'line_edit_nombre')
        self.line_edit_linea = self.findChild(QtWidgets.QLineEdit, 'line_edit_linea')
        self.line_edit_direccion = self.findChild(QtWidgets.QLineEdit, 'line_edit_direccion')
        self.line_edit_horario = self.findChild(QtWidgets.QLineEdit, 'line_edit_horario')
        self.line_edit_campo_extra_cadena = self.findChild(QtWidgets.QLineEdit, 'line_edit_campo_extra_cadena')
        self.line_edit_campo_extra_numerico = self.findChild(QtWidgets.QLineEdit, 'line_edit_campo_extra_numerico')

        self.btn_guardar.clicked.connect(self.guardar_estacion)

    def guardar_estacion(self):
        nombre_estacion = self.line_edit_nombre.text()
        linea_estacion = self.line_edit_linea.text()
        direccion = self.line_edit_direccion.text()
        horario_servicio = self.line_edit_horario.text()
        campo_extra_cadena = self.line_edit_campo_extra_cadena.text()
        campo_extra_numerico = self.line_edit_campo_extra_numerico.text()

        if nombre_estacion and linea_estacion and direccion and horario_servicio:
            self.modificar_yaml(nombre_estacion, linea_estacion, direccion, horario_servicio, campo_extra_cadena, campo_extra_numerico)
            self.accept()  # Cierra el diálogo
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, completa todos los campos requeridos.")

    def modificar_yaml(self, nombre, linea, direccion, horario_servicio, campo_extra_cadena, campo_extra_numerico):
        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Asegúrate de que la clave 'estaciones' exista
        if 'estaciones' not in data:
            data['estaciones'] = []

        # Si la línea no existe, agregarla
        if not any(linea_data['nombre'] == linea for linea_data in data['lineas']):
            data['lineas'].append({'nombre': linea, 'estaciones': []})

        # Agregar detalles de la estación
        data['estaciones'].append({
            'nombre': nombre,
            'lineas': [linea],
            'direccion': direccion,
            'horario_servicio': horario_servicio,
            'campo_extra_cadena': campo_extra_cadena,
            'campo_extra_numerico': campo_extra_numerico
        })

        # Guardar los cambios de vuelta en el archivo YAML
        with open("STPMG.yaml", "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)


