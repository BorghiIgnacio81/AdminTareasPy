import datetime
from persona import Persona
from typing import Union


class Usuario(Persona):
    def __init__(self, nombre, apellido, fecha_nacimiento, dni, usuario, password, ultimoAcceso=None):
        super().__init__(nombre, apellido, fecha_nacimiento, dni)
        self.usuario = usuario
        self.password = password
        if ultimoAcceso is None:
            self.ultimoAcceso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.ultimoAcceso = ultimoAcceso
        

    def toDic(self) -> dict:
        return {
            'usuario': self.usuario,
            'password': self.password,
            'ultimoAcceso': self.ultimoAcceso,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'fecha_nacimiento': persona.fecha_nacimiento,
            'dni': persona.dni            
        }
                      

    def __str__(self):
        return f"Usuario: {self.usuario} , Password: {self.password} , ultimoAcceso: {self.ultimoAcceso}"


