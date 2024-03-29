class Persona:
    def __init__(self, nombre, apellido, fecha_nacimiento, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.dni = dni
    
    def toDic(self) -> dict:
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento,
            'dni': self.dni
        }
    
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


nuevoUsuario = Usuario(Persona("Juan", "Perez", "30-12-1999", "3234523"), "juanchiz34", "pipipipip", "Hoy")

print(nuevoUsuario.toDic())