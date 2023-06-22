import datetime
from typing import Union

class Tarea:
    def __init__(self, id: Union[None,str], titulo: str, descripcion: str, estado: Union[None,str], creada: Union[None,str], actualizada: Union[None,str]):
        if id == None:
            self.id = ""
        else:
            self.id = id
        
        self.titulo = titulo
        self.descripcion = descripcion
        
        if estado == None:
            self.estado = "Pendiente"
        else:
            self.estado = estado

        if creada == None:
            self.creada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.creada = creada

        if actualizada == None:
            self.actualizada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.actualizada = actualizada

    def toDic(self)->dict:
        return {
            'id':self.id,
            'titulo':self.titulo,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'creada': self.creada,
            'actualizada':self.actualizada
            }
    
    def setId(self, id):
        self.id = id

    def setActualizada(self, time):
        self.actualizada = time