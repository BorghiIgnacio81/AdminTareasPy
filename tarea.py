import datetime
import uuid
from pydantic import BaseModel

class Tarea(BaseModel):
    def __init__(self, titulo, descripcion):
        self.id = uuid.uuid3
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = "pendiente"
        self.creada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.actualizada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def toDic(self)->dict:
        return {
            'pid':self.id,
            'nombre':self.titulo,
            'estado': self.estado,
            'descripcion': self.descripcion,
            'fecInicio': self.creada.strftime("%d-%m-%Y %H:%M:%S"),
            'ultMod':self.actualizada.strftime("%d-%m-%Y %H:%M:%S")
            }