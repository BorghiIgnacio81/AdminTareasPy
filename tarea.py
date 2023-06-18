import datetime
from typing import Union

class Tarea:
    def __init__(self, id: Union[None,int], titulo: str, descripcion: str, estado: Union[None,str], creada: Union[None,str], actualizada: Union[None,str]):
        if id != None:
            self.id = id
        
        self.titulo = titulo
        self.descripcion = descripcion
        
        if estado == None:
            self.estado = "Pendiente"
        else:
            self.estado = estado

        if creada == None:
            self.creada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.creada = creada

        if actualizada == None:
            self.actualizada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.actualizada = actualizada

    def toDic(self)->dict:
        return {
            'pid':self.id,
            'nombre':self.titulo,
            'estado': self.estado,
            'descripcion': self.descripcion,
            'fecInicio': self.creada.strftime("%d-%m-%Y %H:%M:%S"),
            'ultMod':self.actualizada.strftime("%d-%m-%Y %H:%M:%S")
            }