from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QStackedWidget
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel
import requests, sys
from tarea import Tarea
from usuario import Usuario
from hashlib import md5


#Variables globales
username = ""
listaTareas = []


class Login(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(layout)

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

        response = requests.post('http://localhost:8000/register', json={'usuario': name, 'password': (md5(password.encode('utf-8')).hexdigest())})

        if response.status_code == 200:
            QMessageBox.information(self, "Alerta", "Usuario registrado con exito.")
        elif response.status_code == 400:
            QMessageBox.information(self, "Alerta", "Usuario ya existe.")
        else:
            QMessageBox.information(self, "Alerta", "Fallo inesperado de registro")

    def login_user(self):
        name = self.line_name.text()
        password = self.line_password.text()

        response = requests.post('http://localhost:8000/login', json={'usuario': name, 'password': (md5(password.encode('utf-8')).hexdigest())})

        if response.status_code == 200:
            global username
            username = name
            self.parent().setCurrentIndex(1)
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
        response = requests.get('http://localhost:8000/listar_tareas')
        global listaTareas
        if response.status_code == 200:
            #aux = dict(response.json()).values()
            for tarea in list(dict(response.json()).values()):
                listaTareas.append(Tarea(**tarea))
        else:
            QMessageBox.information(self, "Alerta", "Problemas al cargar las tareas.")
        
        self.setupUi()
        self.llenarTabla()
        

    def setupUi(self):
        

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

        # TableView
        self.model = QStandardItemModel(self)
        self.tableView = QTableView(self)
        self.tableView.move(20, 140)
        self.tableView.resize(840, 440)
        self.tableView.setModel(self.model)

    def llenarTabla(self):
        self.model.clear()  # Limpiar la tabla antes de llenarla nuevamente
        self.model.setHorizontalHeaderLabels(("ID", "Titulo", "Descripción", "Estado", "Creada", "Actualizada", "Acción"))
        global listaTareas
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
        
        response = requests.delete(f'http://localhost:8000/eliminar_tarea?id={tarea_id}')
        if response.status_code == 200:
            print('Tarea eliminada con éxito')
            self.llenarTabla()
        else:
            print('Error al eliminar la tarea:', response.text)

    def click_boton_aceptar(self):
        titulo = self.titulo_textbox.text()
        descripcion = self.descripcion_textbox.text()
        tarea = Tarea(None, titulo, descripcion, None, None, None)  # None para el ID, se generará automáticamente en la base de datos
        # TODO Hacer un post con el dato al servidor y esperar confirmación
        global listaTareas
        print(tarea.toDic())
        response = requests.post('http://localhost:8000/agregar_tarea', json=tarea.toDic())
        print("Llegue aca",response.json())
        listaTareas.append(Tarea(**dict(response.json())))

        self.llenarTabla()

def run_client():
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    
    ventana1 = Login()
    ventana2 = AdministradorGUI()

    stacked_widget.addWidget(ventana1)
    stacked_widget.addWidget(ventana2)
    ventana1.setFixedSize(150, 180)
    stacked_widget.show()
    ventana2.setFixedSize(950, 620)
    ventana2.move(50,50)
    sys.exit(app.exec())


if __name__ == '__main__':
    run_client()
