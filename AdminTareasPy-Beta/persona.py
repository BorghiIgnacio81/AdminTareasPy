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

        
