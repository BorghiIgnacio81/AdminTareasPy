from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton
import requests
import sys


class MainWindow(QMainWindow):
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

        button_list_users = QPushButton('Listar usuarios', self)
        button_list_users.clicked.connect(self.list_users)

        layout.addWidget(label_name)
        layout.addWidget(self.line_name)
        layout.addWidget(label_password)
        layout.addWidget(self.line_password)
        layout.addWidget(button_register)
        layout.addWidget(button_login)
        layout.addWidget(button_list_users)

    def register_user(self):
        name = self.line_name.text()
        password = self.line_password.text()

        response = requests.post('http://localhost:8000/register', json={'name': name, 'password': password})

        if response.status_code == 200:
            print('Usuario Registrado con exito')
        else:
            print('Fallo registrando el nuevo usuario')

    def login_user(self):
        name = self.line_name.text()
        password = self.line_password.text()

        response = requests.post('http://localhost:8000/login', json={'name': name, 'password': password})

        if response.status_code == 200:
            print('Usuario conectado')
        else:
            print('Fallo')

    def list_users(self):
        response = requests.get('http://localhost:8000/list_users')

        if response.status_code == 200:
            print('Lista de usuarios:', response.json())
        else:
            print('Fallo al intentar recuperar la lista de usuarios')


def run_client():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_client()
