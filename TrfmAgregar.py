import sys
import yaml  # type: ignore
from PyQt5 import QtWidgets, uic

class AgregarEstacion(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AgregarEstacion, self).__init__(parent)
        uic.loadUi('interfaces/AgregarEstacion.ui', self)

        # Conectar los widgets del formulario
        self.btn_guardar = self.findChild(QtWidgets.QPushButton, 'btn_guardar')
        self.Tedit_Nombre = self.findChild(QtWidgets.QLineEdit, 'Tedit_Nombre')
        self.Tedit_Linea = self.findChild(QtWidgets.QLineEdit, 'Tedit_Linea')
        self.Tedit_Direccion = self.findChild(QtWidgets.QLineEdit, 'Tedit_Direccion')
        self.Tedit_EC = self.findChild(QtWidgets.QLineEdit, 'Tedit_EC')
        self.Tedit_EN = self.findChild(QtWidgets.QLineEdit, 'Tedit_EN')

        # Conectar el botón de guardar con la función correspondiente
        self.btn_guardar.clicked.connect(self.guardar_estacion)

    def guardar_estacion(self):
        # Obtener los datos ingresados por el usuario
        nombre_estacion = self.Tedit_Nombre.text().strip()
        linea_estacion = self.Tedit_Linea.text().strip()
        direccion = self.Tedit_Direccion.text().strip()
        ExtraCadena = self.Tedit_EC.text().strip()
        ExtraNumerico = self.Tedit_EN.text().strip()

        # Validación para asegurarse de que los campos requeridos no estén vacíos
        if nombre_estacion and linea_estacion:
            # Validar si ExtraNumerico es realmente un número
            if ExtraNumerico.isdigit():
                ExtraNumerico = int(ExtraNumerico)
                self.modificar_yaml(nombre_estacion, linea_estacion, direccion, ExtraCadena, ExtraNumerico)
                self.accept()  # Cierra el diálogo después de guardar
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "El campo 'Extra Numerico' debe ser un número.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, completa todos los campos requeridos.")

    def modificar_yaml(self, nombre, linea, direccion, ExtraCadena, ExtraNumerico):
        # Cargar el archivo YAML
        try:
            with open("STPMG.yaml", "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []
        except FileNotFoundError:
            # Si el archivo no existe, inicializar una lista vacía
            data = []

        # Verificar si la estación ya existe
        estacion_existente = next((estacion for estacion in data if estacion['Nombre'] == nombre), None)

        if estacion_existente:
            # Si la estación existe, actualizar su información
            estacion_existente['Direccion'] = direccion
            estacion_existente['ExtraCadena'] = ExtraCadena
            estacion_existente['ExtraNumerico'] = ExtraNumerico

            # Si la línea no está en la lista de líneas de la estación, agregarla
            if linea not in estacion_existente['Lineas']:
                estacion_existente['Lineas'].append(linea)
        else:
            # Si la estación no existe, agregarla
            nueva_estacion = {
                'Nombre': nombre,
                'Lineas': [linea],
                'Direccion': direccion,
                'ExtraCadena': ExtraCadena,
                'ExtraNumerico': ExtraNumerico
            }
            data.append(nueva_estacion)

        # Ordenar las estaciones alfabéticamente por nombre
        data.sort(key=lambda x: x['Nombre'])

        # Guardar el archivo YAML actualizado
        with open("STPMG.yaml", "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)

        print(f"Estación '{nombre}' modificada o agregada correctamente.")


# Código para ejecutar la aplicación
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AgregarEstacion()
    window.show()
    sys.exit(app.exec_())
