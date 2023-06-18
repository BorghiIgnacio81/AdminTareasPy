import uuid
from pydantic import BaseModel

class Usuario(BaseModel):
    def __init__(self, usuario, password):
        self.id = uuid.uuid3
        self.usuario = usuario
        self.password = password

    def toDic(self)->dict:
        return {
            'pid':self.id,
            'usuario':self.usuario,
            'password': self.password
            }