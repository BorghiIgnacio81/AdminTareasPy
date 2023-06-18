class Usuario:
    def __init__(self, usuario, password):
        self.usuario = usuario
        self.password = password

    def __str__(self):
        return f"Usuario: {self.usuario} , Password: {self.password}"

    def toDic(self)->dict:
        return {
            'usuario':self.usuario,
            'password': self.password
            }