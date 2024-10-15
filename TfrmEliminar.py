import sys
import yaml  # type: ignore
from PyQt5 import QtWidgets, uic

class EliminarEstacion_Linea(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EliminarEstacion_Linea, self).__init__(parent)
        uic.loadUi('interfaces/TfrmBorrarEstacion_Linea.ui', self)

        # Acceder a ComboBoxes y botones
        self.cmb_Linea = self.findChild(QtWidgets.QComboBox, 'cmb_Linea')
        self.cmb_Estacion = self.findChild(QtWidgets.QComboBox, 'cmb_Estacion')
        self.btnEliminar_Estacion = self.findChild(QtWidgets.QPushButton, 'btnEliminar_Estacion')
        self.btnEliminar_Linea = self.findChild(QtWidgets.QPushButton, 'btnEliminar_Linea')

        # Limpiar el ComboBox para que esté vacío al inicio
        self.cmb_Linea.clear()

        # Conectar señales
        self.cmb_Linea.activated.connect(self.load_stations)
        self.cmb_Linea.mousePressEvent = self.load_lines_on_click  
        self.btnEliminar_Estacion.clicked.connect(self.eliminar_estacion)
        self.btnEliminar_Linea.clicked.connect(self.eliminar_linea)

    def load_lines_on_click(self, event):
        if not self.cmb_Linea.count():  
            self.load_lines()  
        QtWidgets.QComboBox.mousePressEvent(self.cmb_Linea, event)  


    def load_lines(self):
        
        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        unique_lines = set()

        for estacion_data in data:
            lineas = estacion_data.get('Lineas', [])
            unique_lines.update(lineas) 

        # Agregar las líneas únicas ordenadas al ComboBox
        self.cmb_Linea.addItems(sorted(unique_lines))


    def load_stations(self):
        selected_line = self.cmb_Linea.currentText()

        # Limpiar estaciones existentes en cmb_Estacion
        self.cmb_Estacion.clear()

        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        for estacion_data in data:
            if selected_line in estacion_data.get('Lineas', []):
                # Agregar estaciones a cmb_Estacion
                self.cmb_Estacion.addItem(estacion_data.get('Nombre'))

    def eliminar_estacion(self):
        selected_line = self.cmb_Linea.currentText()
        selected_station = self.cmb_Estacion.currentText()

        # Preguntar al usuario si está seguro de eliminar la estación
        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la Estacion <b>'{selected_station}'</b> de la <b>'{selected_line}'</b>?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            with open("STPMG.yaml", "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []

            # Buscar la estacion y eliminarla
            for estacion_data in data:
                if selected_station == estacion_data.get('Nombre') and selected_line in estacion_data.get('Lineas', []):
                    estacion_data['Lineas'].remove(selected_line)

                    # Si la estación ya no tiene líneas, eliminarla completamente
                    if not estacion_data['Lineas']:
                        data.remove(estacion_data)

            # Guardar datos actualizados
            with open("STPMG.yaml", "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file, allow_unicode=True)

            QtWidgets.QMessageBox.information(self, "Eliminar Estacion", f" Estacion <b>'{selected_station}'</b> eliminada de la <b>'{selected_line}'</b>.")

            # Refrescar el ComboBox de estaciones
            self.load_stations()

    def eliminar_linea(self):
        # """Eliminar la línea completa y sus estaciones asociadas si ya no están vinculadas a otras líneas."""
        selected_line = self.cmb_Linea.currentText()

        # Preguntar al usuario si está seguro de eliminar la línea
        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la <b>'{selected_line}'<\b>?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            with open("STPMG.yaml", "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or []

            # Remover la línea seleccionada de todas las estaciones y recopilar estaciones para eliminar
            stations_to_remove = []
            for estacion_data in data:
                if selected_line in estacion_data.get('Lineas', []):
                    estacion_data['Lineas'].remove(selected_line)  # Eliminar la línea de la estación
                    
                    # Si la estación ya no tiene líneas, marcarla para eliminación
                    if not estacion_data['Lineas']:
                        stations_to_remove.append(estacion_data)

            # Eliminar estaciones que ya no están vinculadas a ninguna línea
            for station in stations_to_remove:
                data.remove(station)

            # Eliminar la línea seleccionada de la lista de líneas
            data = [estacion for estacion in data if selected_line not in estacion.get('Lineas', [])]

            # Guardar datos actualizados de nuevo en YAML
            with open("STPMG.yaml", "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file, allow_unicode=True)

            QtWidgets.QMessageBox.information(self, "Eliminar Línea", f"Línea '{selected_line}' eliminada por completo.")

            # Refrescar los ComboBoxes de líneas y estaciones
            self.load_lines()
            self.cmb_Estacion.clear()


# Código para ejecutar la aplicación si es necesario
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EliminarEstacion_Linea()
    window.show()
    sys.exit(app.exec_())
