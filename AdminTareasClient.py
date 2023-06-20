from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
import requests
import sys
from tarea import Tarea
from usuario import Usuario
from hashlib import md5

# Variables globales
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
        global username
        username = self.line_name.text()
        password = self.line_password.text()
        password_hash = md5(password.encode()).hexdigest()
        user = {"usuario": username, "password": password_hash}
        response = requests.post('http://localhost:8000/register', json=user)
        if response.status_code == 200:
            QMessageBox.information(self, 'Registro Exitoso', 'Usuario registrado exitosamente.')
        else:
            QMessageBox.critical(self, 'Error de Registro', 'Ocurrió un error durante el registro.')

    def login_user(self):
        global username
        username = self.line_name.text()
        password = self.line_password.text()
        password_hash = md5(password.encode()).hexdigest()
        user = {"usuario": username, "password": password_hash}
        response = requests.post('http://localhost:8000/login', json=user)
        if response.status_code == 200:
            self.close()
            mainWin = AdministradorGUI()
            mainWin.show()
        else:
            QMessageBox.critical(self, 'Error de Inicio de Sesión', 'Usuario o contraseña incorrectos.')

class MiTabla(QTableView):
    def __init__(self):
        super().__init__()
        self.setModel(TareaTableModel())

class TareaTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.column_names = ['Título', 'Descripción', 'Estado']

    def rowCount(self, parent=QModelIndex()):
        return len(listaTareas)

    def columnCount(self, parent=QModelIndex()):
        return len(self.column_names)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.column_names[section]
            else:
                return section + 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            tarea = listaTareas[index.row()]
            if index.column() == 0:
                return tarea.titulo
            elif index.column() == 1:
                return tarea.descripcion
            elif index.column() == 2:
                return tarea.estado

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

class AdministradorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Administrador de Tareas')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        button_add = QPushButton('Agregar Tarea', self)
        button_add.clicked.connect(self.add_task)

        button_delete = QPushButton('Eliminar Tarea', self)
        button_delete.clicked.connect(self.delete_task)

        layout.addWidget(button_add)
        layout.addWidget(button_delete)

        self.table = MiTabla()
        layout.addWidget(self.table)

        self.update_task_list()

    def add_task(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Agregar Tarea')
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        label_title = QLabel('Título:')
        self.line_title = QLineEdit()

        label_description = QLabel('Descripción:')
        self.line_description = QLineEdit()

        button_add = QPushButton('Agregar')
        button_add.clicked.connect(self.save_task)

        layout.addWidget(label_title)
        layout.addWidget(self.line_title)
        layout.addWidget(label_description)
        layout.addWidget(self.line_description)
        layout.addWidget(button_add)

        dialog.exec()

    def save_task(self):
        title = self.line_title.text()
        description = self.line_description.text()
        tarea = Tarea("", title, description, "pendiente", "", "")
        response = requests.put('http://localhost:8000/actualizar_tarea', json=tarea.dict())
        if response.status_code == 200:
            QMessageBox.information(self, 'Tarea Agregada', 'La tarea se agregó exitosamente.')
            self.update_task_list()
        else:
            QMessageBox.critical(self, 'Error al Agregar Tarea', 'Ocurrió un error al agregar la tarea.')

    def delete_task(self):
        selected_index = self.table.selectedIndexes()
        if len(selected_index) > 0:
            row = selected_index[0].row()
            tarea = listaTareas[row]
            response = requests.delete('http://localhost:8000/eliminar_tarea', json=tarea.dict())
            if response.status_code == 200:
                QMessageBox.information(self, 'Tarea Eliminada', 'La tarea se eliminó exitosamente.')
                self.update_task_list()
            else:
                QMessageBox.critical(self, 'Error al Eliminar Tarea', 'Ocurrió un error al eliminar la tarea.')

    def update_task_list(self):
        response = requests.get('http://localhost:8000/listar_tareas')
        if response.status_code == 200:
            global listaTareas
            listaTareas = [Tarea(**task) for task in response.json()]
            self.table.model().layoutChanged.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWin = Login()
    loginWin.show()
    sys.exit(app.exec())
