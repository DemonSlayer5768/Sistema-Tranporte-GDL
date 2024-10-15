import sys
import yaml  # type: ignore
from PyQt5 import QtWidgets, uic

class EliminarEstacion_Linea(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EliminarEstacion_Linea, self).__init__(parent)
        uic.loadUi('interfaces/TfrmBorrarEstacion_Linea.ui', self)

        # Access ComboBoxes and buttons
        self.cmb_Linea = self.findChild(QtWidgets.QComboBox, 'cmb_Linea')
        self.cmb_Estacion = self.findChild(QtWidgets.QComboBox, 'cmb_Estacion')
        self.btnEliminar_Estacion = self.findChild(QtWidgets.QPushButton, 'btnEliminar_Estacion')
        self.btnEliminar_Linea = self.findChild(QtWidgets.QPushButton, 'btnEliminar_Linea')

        # Load lines into cmb_Linea on form load
        self.load_lines()

        # Connect signals
        self.cmb_Linea.currentIndexChanged.connect(self.load_stations)
        self.btnEliminar_Estacion.clicked.connect(self.eliminar_estacion)
        self.btnEliminar_Linea.clicked.connect(self.eliminar_linea)

    def load_lines(self):
        """Load all available lines from the YAML file into cmb_Linea, ensuring no duplicate lines."""
        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        # Create a set to store unique lines
        unique_lines = set()

        # Assuming 'Lineas' is a key in the YAML structure
        for estacion_data in data:
            lineas = estacion_data.get('Lineas', [])
            unique_lines.update(lineas)  # Add lines to the set (automatically handles duplicates)

        # Clear existing items in the ComboBox
        self.cmb_Linea.clear()

        # Add the sorted unique lines to the ComboBox
        self.cmb_Linea.addItems(sorted(unique_lines))


    def load_stations(self):
        """Load the stations of the selected line into cmb_Estacion."""
        selected_line = self.cmb_Linea.currentText()

        # Clear existing stations in cmb_Estacion
        self.cmb_Estacion.clear()

        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        for estacion_data in data:
            if selected_line in estacion_data.get('Lineas', []):
                # Add stations to cmb_Estacion
                self.cmb_Estacion.addItem(estacion_data.get('Nombre'))

    def eliminar_estacion(self):
        """Delete the selected station from the line."""
        selected_line = self.cmb_Linea.currentText()
        selected_station = self.cmb_Estacion.currentText()

        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        # Find the station and remove it
        for estacion_data in data:
            if selected_station == estacion_data.get('Nombre') and selected_line in estacion_data.get('Lineas', []):
                estacion_data['Lineas'].remove(selected_line)

                # If the station no longer has any lines, remove the station completely
                if not estacion_data['Lineas']:
                    data.remove(estacion_data)

        # Save updated data
        with open("STPMG.yaml", "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)

        QtWidgets.QMessageBox.information(self, "Eliminar Estación", f"Estación '{selected_station}' eliminada de la línea '{selected_line}'.")

        # Refresh the station ComboBox
        self.load_stations()


    def eliminar_linea(self):
        """Delete the entire line and its associated stations if no longer linked to any other lines."""
        selected_line = self.cmb_Linea.currentText()

        with open("STPMG.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or []

        # Remove the selected line from all stations and collect stations to remove
        stations_to_remove = []
        for estacion_data in data:
            if selected_line in estacion_data.get('Lineas', []):
                estacion_data['Lineas'].remove(selected_line)  # Remove the line from the station
                
                # If the station no longer has any lines, mark it for removal
                if not estacion_data['Lineas']:
                    stations_to_remove.append(estacion_data)

        # Remove stations that are no longer linked to any line
        for station in stations_to_remove:
            data.remove(station)

        # Remove the selected line from the lines list
        data = [estacion for estacion in data if selected_line not in estacion.get('Lineas', [])]

        # Save updated data back to YAML
        with open("STPMG.yaml", "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)

        QtWidgets.QMessageBox.information(self, "Eliminar Línea", f"Línea '{selected_line}' eliminada por completo.")

        # Refresh the line and station ComboBoxes
        self.load_lines()
        self.cmb_Estacion.clear()



# Código para ejecutar la aplicación si es necesario
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EliminarEstacion_Linea()
    window.show()
    sys.exit(app.exec_())
