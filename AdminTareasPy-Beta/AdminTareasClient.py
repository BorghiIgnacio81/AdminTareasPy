from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QDateEdit
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDate
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

        self.label_name = QLabel('Nombre:', self)
        self.label_name.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.line_name = QLineEdit(self)
        self.line_name.setStyleSheet("""
            QLineEdit {
                width: 125px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 1px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)

        self.label_apellido = QLabel('Apellido:', self)
        self.label_apellido.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.line_apellido = QLineEdit(self)
        self.line_apellido.setStyleSheet("""
            QLineEdit {
                width: 125px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 1px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)

        self.label_fecha = QLabel('Fecha de Nacimiento:', self)
        self.label_fecha.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.date_fecha = QDateEdit(self)
        self.date_fecha.setDisplayFormat("dd/MM/yyyy")
        self.date_fecha.setStyleSheet("""
            QDateEdit {
                width: 125px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 1px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QDateEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)
        self.label_dni = QLabel('DNI:', self)
        self.label_dni.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.line_dni = QLineEdit(self)
        self.line_dni.setStyleSheet("""
            QLineEdit {
                width: 125px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 1px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)
        apellido = self.line_apellido.text()
        nombre = self.line_name.text()
        self.label_usuario = QLabel(f'Usuario: {apellido}, {nombre}', self)
        self.label_usuario.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.label_password = QLabel('Contraseña:', self)
        self.label_password.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        self.line_password = QLineEdit(self)
        self.line_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_password.setStyleSheet("""
            QLineEdit {
                width: 125px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 1px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)

        self.button_register = QPushButton('Nuevo Usuario', self)
        self.button_register.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: #8e9d86;
                border: 2px solid #a3a9a0;
                color: #FAFAFA;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #c0d2b8;
                color: #333;
            }
        """)
        self.button_register.clicked.connect(self.register_user)

        self.button_login = QPushButton('Ingresar', self)
        self.button_login.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: #8e9d86;
                border: 2px solid #a3a9a0;
                color: #FAFAFA;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #c0d2b8;
                color: #333;
            }
        """)
        self.button_login.clicked.connect(self.login_user)

        self.update_usuario_field()  

        layout.addWidget(self.label_name)
        layout.addWidget(self.line_name)
        layout.addWidget(self.label_apellido)
        layout.addWidget(self.line_apellido)
        layout.addWidget(self.label_fecha)
        layout.addWidget(self.date_fecha)
        layout.addWidget(self.label_dni)
        layout.addWidget(self.line_dni)
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.label_password)
        layout.addWidget(self.line_password)
        layout.addWidget(self.button_register)
        layout.addWidget(self.button_login)

        self.line_apellido.textChanged.connect(self.update_usuario_field)
        self.line_name.textChanged.connect(self.update_usuario_field)

    def update_usuario_field(self):
        apellido = self.line_apellido.text()
        nombre = self.line_name.text()
        usuario = apellido + ", " + nombre
        self.label_usuario.setText(f'Usuario: {usuario}')

    def register_user(self):
        name = self.line_name.text()
        apellido = self.line_apellido.text()
        fecha_nacimiento = self.date_fecha.date().toString("dd/MM/yyyy")
        dni = self.line_dni.text()
        password = self.line_password.text()
        usuario = apellido+', '+name
        
        
        register_payload = {
            "user": {
                "nombre": name,
                "apellido": apellido,
                "fecha_nacimiento": fecha_nacimiento,
                "dni": dni,
                "usuario": usuario,
                "password": md5(password.encode('utf-8')).hexdigest(),
                "ultimoAcceso": None
            },
            "person": {
                "nombre": name,
                "apellido": apellido,
                "fecha_nacimiento": fecha_nacimiento,
                "dni": dni
            }
        }

        try:
            response_register = requests.post('http://localhost:8000/register', json=register_payload)
            if response_register.status_code == 200:
                QMessageBox.information(self, "Alerta", "Usuario registrado con éxito.")
            elif response_register.status_code == 400:
                QMessageBox.information(self, "Alerta", "Error al registrar el usuario.")
            else:
                QMessageBox.information(self, "Alerta", "Error desconocido durante el registro del usuario.")
        except requests.exceptions.RequestException as e:
            QMessageBox.information(self, "Alerta", "Error de conexión: " + str(e))




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
        
        self.label = QLabel(self)        
        self.label.move(740,20)
        self.label.resize(180,20)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #222;
            }
        """)

        
        self.setupUi()
        self.llenarTabla()
        

    def setupUi(self):
        # Textbox
        self.titulo_textbox = QLineEdit(self)
        #self.titulo_textbox.resize(180, 21)
        self.titulo_textbox.move(20, 20)
        self.titulo_textbox.setPlaceholderText("Tarea")

        self.titulo_textbox.setStyleSheet("""
            QLineEdit {
                width: 180px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 0px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)

        self.descripcion_textbox = QLineEdit(self)
        self.descripcion_textbox.move(20, 60)
        self.descripcion_textbox.setPlaceholderText("Descripción")

        self.descripcion_textbox.setStyleSheet("""
            QLineEdit {
                width: 500px;
                border-style: solid;
                border-width: 2px;
                border-color: transparent transparent #CCC #CCC;
                padding: 0px 5px;
                background-color: rgba(255,255,255,0.25);
            }

            QLineEdit:focus{
                border-color: transparent transparent #8e9d86 #8e9d86;
            }
        """)

        # Boton
        self.boton_aceptar = QPushButton("Aceptar", self)
        self.boton_aceptar.move(740, 100)
        self.boton_aceptar.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: #8e9d86;
                border: 2px solid #a3a9a0;
                color: #FAFAFA;
                font-weight: bold;
                padding: 2px 7px
            }

            QPushButton:hover {
                background: #c0d2b8;
                color: #333;
            }
        """)
        self.boton_aceptar.clicked.connect(self.click_boton_aceptar)


        self.boton_actualizar = QPushButton("Actualizar", self)
        self.boton_actualizar.move(640, 100)
        self.boton_actualizar.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background: #8e9d86;
                border: 2px solid #a3a9a0;
                color: #FAFAFA;
                font-weight: bold;
                padding: 2px 7px
            }

            QPushButton:hover {
                background: #c0d2b8;
                color: #333;
            }
        """)
        self.boton_actualizar.clicked.connect(self.actualizarTarea)

        # TableView
        self.model = QStandardItemModel(self)
        self.tableView = QTableView(self)
        self.tableView.move(20, 140)
        self.tableView.setStyleSheet("""
            QTableView {
                font-size: 13px;
                background: #c1d3b9;
                border: 2px solid #a3a9a0;
                color: #333;
            }
        """)
        self.tableView.resize(840, 440)
        self.tableView.setModel(self.model)

    def focusInEvent(self, event):
        global username
        self.label.setText(f"Usuario: {username}")

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
            botonEliminar.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    background: #8e9d86;
                    border: 2px solid #a3a9a0;
                    color: #FAFAFA;
                    font-weight: bold;
                    padding: 1px 3px
                }

                QPushButton:hover {
                    background: #c0d2b8;
                    color: #333;
                }
            """)
            botonEliminar.clicked.connect(lambda checked, tarea_id=tarea.id: self.eliminarTarea(tarea_id))
            self.tableView.setIndexWidget(index, botonEliminar)
    
    def eliminarTarea(self, tarea_id):
        # TODO Hacer un delete con el dato al servidor y esperar confirmación
        if (QMessageBox.question(self,"Confirmación","¿Estás seguro de que quieres eliminar esta tarea?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)==QMessageBox.StandardButton.Yes):
            response = requests.delete(f'http://localhost:8000/eliminar_tarea?id={tarea_id}')
            if response.status_code == 200:
                QMessageBox.information(self, "Información", "Tarea eliminada con éxito.")
                global listaTareas
                for i in listaTareas:
                    if i.id == tarea_id:
                        listaTareas.remove(i)
                self.llenarTabla()
            else:
                print('Error al eliminar la tarea:', response.text)

    def click_boton_aceptar(self):
        titulo = self.titulo_textbox.text()
        descripcion = self.descripcion_textbox.text()
        tarea = Tarea(None, titulo, descripcion, None, None, None)  # None para el ID, se generará automáticamente en la base de datos
        # TODO Hacer un post con el dato al servidor y esperar confirmación
        global listaTareas
        response = requests.post('http://localhost:8000/agregar_tarea', json=tarea.toDic())
        listaTareas.append(Tarea(**dict(response.json())))

        self.llenarTabla()

    def actualizarTarea(self):
        fila = self.tableView.currentIndex().row()
        #columna = self.tableView.currentIndex().column()
        id = self.model.data(self.model.index(fila,0, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        titulo = self.model.data(self.model.index(fila,1, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        descrip = self.model.data(self.model.index(fila,2, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        estado = self.model.data(self.model.index(fila,3, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        creada = self.model.data(self.model.index(fila,4, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        actual = self.model.data(self.model.index(fila,5, QModelIndex()), Qt.ItemDataRole.DisplayRole)
        tarea = Tarea(id,titulo,descrip,estado, creada, actual)
        response = requests.put('http://localhost:8000/actualizar_tarea', json=tarea.toDic())
        
        if response.status_code == 200:
            tarea = Tarea(**dict(response.json()))
            QMessageBox.information(self, "Información", "Tarea actualizada con éxito.")
            global listaTareas
            for i, task in enumerate(listaTareas):
                if task.id == tarea.id:
                    listaTareas[i] = tarea
            self.llenarTabla()
        else:
            print('Error al actualizar la tarea:', response.text)


def run_client():
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    
    ventana1 = Login()
    ventana2 = AdministradorGUI()

    stacked_widget.addWidget(ventana1)
    stacked_widget.addWidget(ventana2)
    ventana1.setFixedSize(150, 450)
    stacked_widget.setWindowTitle("Administrador de Tareas")
    stacked_widget.show()
    ventana2.setFixedSize(950, 620)
    sys.exit(app.exec())


if __name__ == '__main__':
    run_client()