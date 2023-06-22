from persona import Persona


class Usuario(Persona):
    def __init__(self, persona: Persona, usuario, password, ultimoAcceso):
        super().__init__(persona.nombre, persona.apellido, persona.fecha_nacimiento, persona.dni)
        self.usuario = usuario
        self.password = password
        self.ultimoAcceso = ultimoAcceso
        

    def toDic(self) -> dict:
        return {'usuario': self.usuario,'password': self.password,'ultimoAcceso': self.ultimoAcceso}|super().toDic()
                      

    def __str__(self):
        return f"Usuario: {self.usuario} , Password: {self.password} , ultimoAcceso: {self.ultimoAcceso}"


