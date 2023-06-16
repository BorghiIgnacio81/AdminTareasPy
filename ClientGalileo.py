import socket
import pickle
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QLineEdit, QVBoxLayout

# Configuración del cliente
host = '127.0.0.1'
port = 8080

# Creación del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión al servidor
client_socket.connect((host, port))

# Envío de datos al servidor
diccionario = {"temperatura": "", "humedad": "","Diferencia": "","HoraActual": "","HoraMedicion": "","VelocidadViento":"","DireccionViento":""}
direccion = {
    "S": "Sur",
    "SW": "Sur Oeste",
    "SE": "Sur Este",
    "SSE": "Sur Sureste",
    "SSW": "Sur Suroeste",
    "N":"Norte",
    "NE":"Norte Este",
    "NW":"Norte Oeste",
    "NNW":"Norte Noroeste",
    "NNE":"Norte Noreste",
    "E":"Este",
    "ENE":"Este Noreste",
    "ESE":"Este Sureste",
    "W":"Oeste",
    "WSW":"Oeste Suroeste",
    "WNW":"Oeste Noroeste"   
}
message = pickle.dumps(diccionario)
client_socket.send(message)


data = client_socket.recv(1024)
response = pickle.loads(data)
#Carga de GUI
temperatura=response["temperatura"]
humedad=response["humedad"]
VelocidadViento=response["VelocidadViento"]
DireccionViento=response["DireccionViento"]
if DireccionViento in direccion:
    DireccionViento = direccion[DireccionViento]
Actual=str(response["HoraActual"])
horaActual=str(Actual[11:16])
HoraMedicion=response["HoraMedicion"]
difMin=response["Diferencia"]
app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Estacion Galileo")
window.setGeometry(200, 150, 300, 200)
lblTemp = QLabel("Temperatura: "+str(temperatura)+" °C", window)
lblTemp.move(10, 10)
lblTemp.adjustSize()
lblHoraActual = QLabel("Hora Actual", window)
lblHoraActual.move(220, 5)
lblHora = QLabel(str(horaActual), window)
lblHora.move(230, 15)
lblHum = QLabel("Humedad: "+str(humedad), window)
lblHum.move(10, 20)
lblViento = QLabel("Viento: ", window)
lblViento.move(10, 40)
lblVelViento = QLabel("Velocidad: "+str(VelocidadViento), window)
lblVelViento.move(10, 60)
lblVelViento.adjustSize()
lblDirViento = QLabel("Direccion: "+str(DireccionViento), window)
lblDirViento.move(10, 75)
lblDirViento.adjustSize()
lblDiferencia =QLabel("Esta medicion fue tomada a las "+response["HoraMedicion"]+ "\n" +"hace exactamente "+response["Diferencia"], window)
lblDiferencia.move(10,90)
lblDiferencia.adjustSize()
"""comboHora = QComboBox( window)
comboHora.move(10,110)
layout = QVBoxLayout()
layout.addWidget(QLabel("Hora medicion:"))
layout.addWidget(comboHora)
window.setLayout(layout)"""
window.show()
app.exec()
#print("A las " +response["HoraMedicion"]+" la temperatura era de "+response["temperatura"]+" y la humedad del "+response["humedad"]+" hace exactamente "+response["Diferencia"])
#print(response["VelocidadViento"])
#print(response["DireccionViento"])
client_socket.close()
