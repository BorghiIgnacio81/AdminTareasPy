from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
import requests, sys
from tarea import Tarea
from usuario import Usuario
from hashlib import md5


#Variables globales
username = ""
listaTareas = []


class Login(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bienvenido')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        label_name = QLabel('Nombre:', self)
        self.line_name = QLineEdit(self)

        label_password = QLabel('Contraseña:', self)
        self.line_password = QLineEdit(self)
        self.line_password.setEchoMode(QLineEdit.EchoMode.Password)

        button_register = QPushButton('Nuevo Usuario', self)
        button_register.clicked.connect(self.register_user)

        button_login = QPushButton('Ingresar', self)
        button_login.clicked.connect(self.login_user)

        layout.addWidget(label_name)
        layout.addWidget(self.line_name)
        layout.addWidget(label_password)
        layout.addWidget(self.line_password)
        layout.addWidget(button_register)
        layout.addWidget(button_login)

    def register_user(self):
        name = self.line_name.text()
        password = self.line_password.text()

        response = requests.post('http://localhost:8000/register', json={'usuario': name, 'password': md5(password)})

        if response.status_code == 200:
            QMessageBox.information(self, "Alerta", "Usuario registrado con exito.")
        elif response.status_code == 400:
            QMessageBox.information(self, "Alerta", "Usuario ya existe.")
        else:
            QMessageBox.information(self, "Alerta", "Fallo inesperado de registro")

    def login_user(self):
        name = self.line_name.text()
        password = self.line_password.text()

        response = requests.post('http://localhost:8000/login', json={'usuario': name, 'password': md5(password)})

        if response.status_code == 200:
            username = name
            app = QApplication(sys.argv)
            window = AdministradorGUI()
            window.show()
            sys.exit(app.exec())
        else:
            QMessageBox.information(self, "Alerta", "Falló al intentar logear, revise sus credenciales.")


class MiTabla(QAbstractTableModel):
    def __init__(self, datos=None):
        QAbstractTableModel.__init__(self)
        self._datos = datos

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(self._datos[0])

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._datos[index.row()][index.column()])
        return None
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ("Titulo", "Descripción", "Estado", "Creada", "Actualizada", "Accion")[col]
        return QAbstractTableModel.headerData(self, col, orientation, role)


class TareaTableModel(QAbstractTableModel):
        def __init__(self, data = None):
            QAbstractTableModel.__init__(self)
            self.data = data
            self.columns = ["Titulo", "Descripcion", "Estado", "Creada", "Actualizada", "Accion"]
    
        def rowCount(self, parent=None):
            return len(self.data)
    
        def columnCount(self, parent=None):
            return len(self.columns)
    
        def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
            if index.isValid():
                if role == QtCore.Qt.DisplayRole:
                    return str(self.data[index.row()][index.column()])
            return None
    
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.columns[col]
            return QAbstractTableModel.headerData(self, col, orientation, role)


class AdministradorGUI(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        response = dict(requests.get('http://localhost:8000/tareas/listar'))
        
        if response.status_code == 200:
            for tarea in list(response.values()):
                listaTareas.append(Tarea(**tarea))
        else:
            QMessageBox.information(self, "Alerta", "Problemas al cargar las tareas.")
        
        self.setupUi()
        self.llenarTabla()
        

    def setupUi(self):
        self.resize(850, 600)
        self.move(300, 300)
        self.setWindowTitle("Tareas")

        # TODO Un Label que diga "Sesion iniciada: fulanito" usando la variable username

        # Textbox
        self.titulo_textbox = QLineEdit(self)
        self.titulo_textbox.resize(180, 21)
        self.titulo_textbox.move(20, 20)
        self.titulo_textbox.setPlaceholderText("Titulo")

        self.descripcion_textbox = QLineEdit(self)
        self.descripcion_textbox.resize(540, 21)
        self.descripcion_textbox.move(20, 60)
        self.descripcion_textbox.setPlaceholderText("Descripción")

        # Boton
        self.boton_aceptar = QPushButton("Aceptar", self)
        self.boton_aceptar.move(740, 100)
        self.boton_aceptar.clicked.connect(self.click_boton_aceptar)

        self.boton_eliminadas = QPushButton("Ver tareas eliminadas", self)
        self.boton_eliminadas.move(20, 580)
        self.boton_eliminadas.setToolTip("Ver solo las eliminadas")

        self.boton_todas = QPushButton("Ver todas las tareas", self)
        self.boton_todas.setToolTip("Ver todas las tareas incluidas las eliminadas")
        # TableView
        self.model = QStandardItemModel(self)
        self.tableView = QTableView(self)
        self.tableView.move(20, 140)
        self.tableView.resize(760, 440)
        self.tableView.setModel(self.model)

    def llenarTabla(self):
        self.model.clear()  # Limpiar la tabla antes de llenarla nuevamente
        self.model.setHorizontalHeaderLabels(("ID", "Titulo", "Descripción", "Estado", "Creada", "Actualizada", "Acción"))

        for i, tarea in enumerate(listaTareas):
            self.model.setItem(i, 0, QStandardItem(str(tarea.id)))
            self.model.setItem(i, 1, QStandardItem(tarea.titulo))
            self.model.setItem(i, 2, QStandardItem(tarea.descripcion))
            self.model.setItem(i, 3, QStandardItem(tarea.estado))
            self.model.setItem(i, 4, QStandardItem(tarea.creada))
            self.model.setItem(i, 5, QStandardItem(tarea.actualizada))
            self.tableView.setColumnWidth(0, 40)
            self.tableView.setColumnWidth(1, 100)
            self.tableView.setColumnWidth(2, 200)
            self.tableView.setColumnWidth(3, 100)
            self.tableView.setColumnWidth(4, 130)
            self.tableView.setColumnWidth(5, 130)
            index = self.model.index(i, 6)
            botonEliminar = QPushButton("Eliminar")
            botonEliminar.clicked.connect(lambda checked, tarea_id=tarea.id: self.eliminarTarea(tarea_id))
            self.tableView.setIndexWidget(index, botonEliminar)
    
    def eliminarTarea(self, tarea_id):
        # TODO Hacer un delete con el dato al servidor y esperar confirmación
        self.llenarTabla()

    def click_boton_aceptar(self):
        titulo = self.titulo_textbox.text()
        descripcion = self.descripcion_textbox.text()
        tarea = Tarea(None, titulo, descripcion)  # None para el ID, se generará automáticamente en la base de datos
        # TODO Hacer un post con el dato al servidor y esperar confirmación
        self.llenarTabla()

def run_client():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_client()