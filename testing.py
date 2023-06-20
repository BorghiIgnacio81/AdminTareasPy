import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget


class Ventana1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana 1")

        self.button = QPushButton("Cerrar", self)
        self.button.clicked.connect(self.cerrar_ventana)

    def cerrar_ventana(self):
        self.parent().setCurrentIndex(1)  # Cambiar a la siguiente ventana


class Ventana2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana 2")

        layout = QVBoxLayout()
        self.button = QPushButton("Cerrar", self)
        self.button.clicked.connect(self.cerrar_ventana)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def cerrar_ventana(self):
        self.parent().setCurrentIndex(0)  # Cambiar a la ventana anterior


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    ventana1 = Ventana1()
    ventana2 = Ventana2()

    stacked_widget.addWidget(ventana1)
    stacked_widget.addWidget(ventana2)

    stacked_widget.show()

    sys.exit(app.exec_())
