from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit
#CLASES PROPIAS
from Estacion import GrafoTransporte
from TrfmAgregar import Agregar  
from TfrmEliminar import Eliminar
from AlgoritmosOrden import AlgoritmosOrdenamiento
from AlgoritmosBusqueda import Recorrido

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

        # Conectar la señal currentChanged llamar funciones cada vez que cambian de pagina
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        
        # Conectar los botones TfrmPrincipal
        self.btn_BuscarEstacion.clicked.connect(self.obtener_seleccion)
        self.rBtn_Matriz.toggled.connect(self.imprimirMatriz)

        # Conectar botones TfrmEliminar
        self.btnEliminar_Estacion.clicked.connect(
            lambda: Eliminar.eliminar_estacion(self.cmb_Linea, self.cmb_Estacion))
        self.btnEliminar_Linea.clicked.connect(
            lambda: Eliminar.eliminar_linea(self.cmb_Linea))

        # Conectar los botones TfrmAgregar 
        self.btn_guardar.clicked.connect(
            lambda: Agregar.guardar_estacion(self.Tedit_Nombre, self.Tedit_Linea, self.Tedit_Anterior, self.Tedit_Siguiente))
        self.btn_guardar.clicked.connect(
            lambda: Agregar.guardar_estacion(self.Tedit_Nombre, self.Tedit_Linea, self.Tedit_Anterior, self.Tedit_Siguiente))
        
        #conexiones de los radios Buttons en algoritmosOrdenamiento 
        radio_buttons = [
            self.rBtn_Insercion,
            self.rBtn_Burbuja,
            self.rBtn_Seleccion,
            self.rBtn_Mezcla,
            self.rBtn_Rapido
        ]
        
        # Asigna nombres a los botones para identificarlos 
        self.rBtn_Insercion.setObjectName("Insercion")
        self.rBtn_Burbuja.setObjectName("Burbuja")
        self.rBtn_Seleccion.setObjectName("Seleccion")
        self.rBtn_Mezcla.setObjectName("Mezcla")
        self.rBtn_Rapido.setObjectName("Rapido")
        
                
        # Conectar todos los botones al mismo método con un bucle
        for rbtn in radio_buttons:
            rbtn.toggled.connect(self.handleRadioButtonToggled)

    def handleRadioButtonToggled(self):
        # Llama a la función AlgoritmosOrdenamiento.recibirDatos solo si el botón está marcado
        if self.sender().isChecked():
            boton_nombre = self.sender().objectName()  # Identifica el botón por su nombre
            AlgoritmosOrdenamiento.recibirDatos(
                self.cmb_OrdenarLineas, 
                self.listView_Ordenamiento, 
                self.txtEdit_Time,
                boton_nombre
            )
            # print("seleccione el btn ", boton_nombre)
            
        
       

    def on_tab_changed(self, index):
        current_tab_name = self.tabWidget.tabText(index)
        # print(f"Pestaña actual: {current_tab_name}")

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
            TransporteApp.cargar_lineas(self)
            #recargar el archivo yaml cuando de cambie de pantalla
            
        
        if current_tab_name == "Ordenar":
            AlgoritmosOrdenamiento.cargar_Lineas_Orden(self.cmb_OrdenarLineas)
            
        elif current_tab_name == "Busqueda":
            print("entre")
            

            
    
    
        
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

    def imprimirMatriz(self):
        # Obtener la línea seleccionada
        linea_seleccionada = self.comboBox.currentText()

        if linea_seleccionada == "Todas":
            # Construir una lista de todas las estaciones y sus conexiones combinadas
            estaciones = []
            conexiones_globales = {}
            
            for linea, estaciones_linea in self.grafo_transporte.NameLine.items():
                estaciones.extend(estaciones_linea)
                for estacion in estaciones_linea:
                    nodo = self.grafo_transporte.NameStations.get(estacion)
                    if nodo:
                        if isinstance(nodo.estacion.conexiones, list):
                            conexiones_globales[estacion] = nodo.estacion.conexiones
                        elif isinstance(nodo.estacion.conexiones, str):
                            conexiones_globales[estacion] = nodo.estacion.conexiones.split(",")
                        else:
                            conexiones_globales[estacion] = []  # Caso por defecto si no es lista ni cadena

            estaciones = list(set(estaciones))  # Eliminar duplicados

            # Asegurarse de que la lista de estaciones tenga exactamente 50 elementos
            while len(estaciones) < 50:
                estaciones.append(f"Ficticia-{len(estaciones) + 1}")
            estaciones = estaciones[:50]  # Limitar a 50 si hay más

        else:
            # Obtener las estaciones y conexiones de la línea seleccionada
            estaciones = self.grafo_transporte.NameLine.get(linea_seleccionada, [])
            conexiones_globales = {}
            for estacion in estaciones:
                nodo = self.grafo_transporte.NameStations.get(estacion)
                if nodo:
                    if isinstance(nodo.estacion.conexiones, list):
                        conexiones_globales[estacion] = nodo.estacion.conexiones
                    elif isinstance(nodo.estacion.conexiones, str):
                        conexiones_globales[estacion] = nodo.estacion.conexiones.split(",")
                    else:
                        conexiones_globales[estacion] = []

        if not estaciones:
            QMessageBox.warning(self, "Advertencia", f"No hay estaciones para la línea: {linea_seleccionada}")
            return

        # Crear la matriz de adyacencia
        matriz = []
        for estacion_origen in estaciones:
            fila = []
            for estacion_destino in estaciones:
                if estacion_destino in conexiones_globales.get(estacion_origen, []):
                    fila.append(1)  # Hay conexión
                else:
                    fila.append(0)  # No hay conexión
            matriz.append(fila)

        # Imprimir en consola
        print(f"Matriz de adyacencia para la línea '{linea_seleccionada}':")
        for fila in matriz:
            print(" ".join(map(str, fila)))

        # Formatear matriz para QMessageBox
        matriz_texto = "\n".join(" ".join(map(str, fila)) for fila in matriz)

        # # Mostrar en QMessageBox
        # msg_box = QMessageBox(self)
        # msg_box.setWindowTitle(f"Matriz de Adyacencia - {linea_seleccionada}")
        # msg_box.setText(f"Matriz de adyacencia para la línea '{linea_seleccionada}':\n\n{matriz_texto}")
        # msg_box.exec_()
        # Crear un QDialog para mostrar la matriz
        
        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Matriz de Adyacencia - {linea_seleccionada}")
        dialogo.resize(800, 600)  # Ajusta el tamaño inicial
        dialogo.setWindowState(dialogo.windowState() | Qt.WindowMaximized)  # Maximizar al abrir

        # Crear un QTextEdit para mostrar la matriz
        texto_matriz = QTextEdit(dialogo)
        texto_matriz.setPlainText(matriz_texto)
        texto_matriz.setReadOnly(True)  # Evitar ediciones

        # Diseño del diálogo
        layout = QVBoxLayout(dialogo)
        layout.addWidget(texto_matriz)
        dialogo.setLayout(layout)

        # Mostrar el diálogo
        dialogo.exec_()

        

# Configuración del programa principal
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = TransporteApp()
    window.show()
    app.exec_()
