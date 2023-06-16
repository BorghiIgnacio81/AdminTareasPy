import socket
import pickle
import requests
from datetime import datetime

r = requests.get('https://www.frcon.utn.edu.ar/galileo/downld02.txt')
HOST = '127.0.0.1'  
PORT = 8080        
server = socket.socket(family = socket.AF_INET, type=socket.SOCK_STREAM)
server.bind(('127.0.0.1',8080))
server.listen()
while True:
    connection, address = server.accept()
    while True:
            data = connection.recv(1024)
            diccionario= pickle.loads(data)
            aux = r.text.split("\r\n")
            medicion = aux[len(aux)-2].replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("  ", " ").split(" ")
            horaA = datetime.now()
            
            horaM = str(medicion[1])
            horaM_formatted = f"{horaA:%Y-%m-%d} {horaM}:00"
            horaMe = datetime.strptime(horaM_formatted, "%Y-%m-%d %H:%M:%S")
            dif = horaA - horaMe
            difMin = dif.total_seconds() / 60
            difMin = int(difMin)
            diccionario["temperatura"] = medicion[3]
            diccionario["humedad"] = medicion[6]+" %"
            diccionario["Diferencia"] = str(difMin)+" minutos"
            diccionario["HoraActual"] = horaA
            diccionario["HoraMedicion"] = horaM
            diccionario["VelocidadViento"] = medicion[7]+"Km/h"
            diccionario["DireccionViento"] = medicion[8]
            message = pickle.dumps(diccionario)
            connection.send(message)
            if data:
                print('Enviando de regreso los dato al cliente ')
                connection.sendall(data)
            else:
                print('no hay mas datos de', address)
                break