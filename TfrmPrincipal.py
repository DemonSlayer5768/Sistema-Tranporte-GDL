from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QStringListModel
from Estacion import GrafoTransporte
from TrfmAgregar import guardar_estacion  
from TfrmEliminar import Eliminar
from AlgoritmosOrden import AlgoritmosOrdenamiento

class TransporteApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransporteApp, self).__init__()
        uic.loadUi('interfaces/TfrmPrincipal.ui', self)

        # Crear la instancia de GrafoTransporte y cargar las líneas
        self.grafo_transporte = GrafoTransporte()
        self.cargar_lineas()
        # Crear el modelo para QListView
        self.estaciones_model = QStringListModel(self)
        self.listView.setModel(self.estaciones_model)

        # Conectar los botones TfrmPrincipal
        self.btn_BuscarEstacion.clicked.connect(self.obtener_seleccion)

        # Conectar botones TfrmEliminar
        self.btnEliminar_Estacion.clicked.connect(
            lambda: Eliminar.eliminar_estacion(self.cmb_Linea, self.cmb_Estacion))
        self.btnEliminar_Linea.clicked.connect(
            lambda: Eliminar.eliminar_linea(self.cmb_Linea))

        # Conectar los botones TfrmAgregar 
        self.btn_guardar.clicked.connect(
            lambda: guardar_estacion(self.Tedit_Nombre, self.Tedit_Linea, self.Tedit_Anterior, self.Tedit_Siguiente))
        self.btn_guardar.clicked.connect(
            lambda: guardar_estacion(self.Tedit_Nombre, self.Tedit_Linea, self.Tedit_Anterior, self.Tedit_Siguiente))
        
        
        # Conectar la señal currentChanged llamar funciones cada vez que cambian de pagina
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
       

    def on_tab_changed(self, index):
        current_tab_name = self.tabWidget.tabText(index)
        print(f"Pestaña actual: {current_tab_name}")

        if current_tab_name == "Eliminar":
            Eliminar.cargar_lineas_Eliminar(self.cmb_Linea)

            # Verificar si ya está conectada la señal
            try:
                self.cmb_Linea.currentIndexChanged.disconnect()
            except TypeError:
                pass  # No estaba conectada previamente

            # Conectar la señal
            self.cmb_Linea.currentIndexChanged.connect(
                lambda: Eliminar.cargar_estaciones(self.cmb_Linea, self.cmb_Estacion)
            )

            Eliminar.cargar_estaciones(self.cmb_Linea, self.cmb_Estacion)
        
        elif current_tab_name == "Principal":
            #recargar Lineas 
            TransporteApp.cargar_lineas(self)
            
        
        if current_tab_name == "Ordenar":
            print("si entro")
            AlgoritmosOrdenamiento.cargar_Lineas_Orden(self.cmb_OrdenarLineas)
            

            
    
    
        
    def cargar_lineas(self):
        self.comboBox.clear()  # Limpiar el ComboBox
        self.comboBox.addItem("Todas")  # Agregar la opción 'Todas' 
        self.comboBox.addItems(list(self.grafo_transporte.NameLine.keys()))  # Agregar las líneas

    def obtener_seleccion(self):
        # Obtener la línea seleccionada en el ComboBox
        linea_seleccionada = self.comboBox.currentText()

        if linea_seleccionada == "Todas":
            # Si se selecciona 'Todas', combinar todas las estaciones de todas las líneas
            estaciones = []
            for estaciones_linea in self.grafo_transporte.NameLine.values():
                estaciones.extend(estaciones_linea)
            estaciones = list(set(estaciones))  # Eliminar duplicados
        else:
            # Obtener las estaciones de la línea seleccionada
            estaciones = self.grafo_transporte.NameLine.get(linea_seleccionada, [])

        self.manejar_seleccion(estaciones)

    def manejar_seleccion(self, estaciones):
        # Mostrar las estaciones en el QListView
        self.estaciones_model.setStringList(estaciones)  # Actualizar el modelo de la vista


# Configuración del programa principal
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TransporteApp()
    window.show()
    app.exec_()
