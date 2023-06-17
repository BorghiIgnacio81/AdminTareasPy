import datetime

class Task:
   
    def __init__ (self, pid, nombre, estado, descripcion, fecInicio, ultMod):
        self.__pid = pid
        self.__nombre = nombre
        self.__descripcion = descripcion

        if(estado != None):
            self.__estado = estado
        else:
            self.__estado = 0
        
        if(fecInicio == None):
            self.__fecInicio = datetime.datetime.now()
        else:
            self.__fecInicio = datetime.datetime.strptime(fecInicio, "%d-%m-%Y %H:%M:%S")
        
        if(ultMod == None):
            self.__ultMod = datetime.datetime.now()
        else:
            self.__ultMod = datetime.datetime.strptime(ultMod, "%d-%m-%Y %H:%M:%S")

    def __str__(self)-> str:
        return f"{self.__pid} - {self.__nombre} - Status: {self.__calcularEstado()} - Ultima modificación: {self.__calcularModificacion()} \nDescripción: {self.__descripcion}"

    def toDic(self)->dict:
        return {
            'pid':self.__pid,
            'nombre':self.__nombre,
            'estado': self.__estado,
            'descripcion': self.__descripcion,
            'fecInicio': self.__fecInicio.strftime("%d-%m-%Y %H:%M:%S"),
            'ultMod':self.__ultMod.strftime("%d-%m-%Y %H:%M:%S")
            }

    def __calcularEstado(self)-> str:
        if(self.__estado == -1):
            return "Dormido"
        elif(self.__estado == 0):
            return "Listo"
        else:
            return "En ejecución"
    
    def __calcularModificacion(self)->str:
        timestamp = str(self.__ultMod - self.__fecInicio) #0:00:00.002423
        artimestamp = timestamp.split(":")
        minutos = int(artimestamp[0])*60 + int(artimestamp[1])
        if(minutos < 60):
            return f"{minutos} mins"
        else:
            return f"{int(minutos/60)} hrs"
        
        
    

    #setters
    def cambiarEstado (self, estado):
        self.__estado = estado
        self.__ultMod = datetime.datetime.now()
    
    def setNombre(self, nombre):
        self.__nombre = nombre
        self.__ultMod = datetime.datetime.now()

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion
        self.__ultMod = datetime.datetime.now()
    


    #getters
    def getPid(self)->int:
        return self.__pid
    
    def getNombre(self)->str:
        return self.__nombre
    
    def getEstado(self)->int:
        return self.__estado
    
    