from taskEx import Task
import random, datetime
from tinydb import TinyDB, Query

class NewAdmin:
    def __init__(self):
        self.listaDeTareas = []
        self.__cargarLista()

    def __cargarLista(self):
        db = TinyDB('db.json')
        result = db.all()
        if(len(result)):
            for x in result:
                self.listaDeTareas.append(Task(**x))
        else:
            print("Lista vacía")
        
    #Añadir tarea
    def addTask(self, nombre, descripcion):
        nuevoPid = random.randint(1,1000)
        flag = True
        while(flag):
            flag = False
            if(len(self.listaDeTareas)!= 0):
                for x in self.listaDeTareas:
                    if( nuevoPid == x.getPid()):
                        nuevoPid = random.randint(1,1000)
                        flag = True
                        break
        nuevaTarea = Task(nuevoPid, nombre, None, descripcion, None, None)
        self.listaDeTareas.append(nuevaTarea)
        print("<<<  Tarea agregada con éxito   >>>")



    #Obtener una tarea
    def getTask(self, pid)->Task:
        for x in self.listaDeTareas:
            if(pid == Task(x).getPid()):
                return x




    #Actualizar tareas
    def statusUpdate(self, pid, estado, nombre, descripcion):
        aux = None
        for x in self.listaDeTareas:
            if( pid == x.getPid()):
                aux = x
                break
        if(aux == None):
            raise Exception(f"El id {pid} no se encuentra en la lista de tareas.")
        else:
            if(estado != None and estado != ""):
                aux.cambiarEstado(int(estado))
            if(nombre != None and nombre != ""):
                aux.setNombre(nombre)
            if(descripcion != None and descripcion != ""):
                aux.setDescripcion(descripcion)
        print("<<<  Tarea actualizada con éxito   >>>")
 



    #Eliminar tarea

    def eliminarTarea(self, pid):
        aux = True
        for x in self.listaDeTareas:
            if(pid == x.getPid()):
                aux = False
                self.listaDeTareas.remove(x)
                print("Eliminacion realizada con exito.")
        
        if(aux):
            raise Exception(f"El id {pid} no se encuentra en la lista de tareas.")



    #Listar tareas

    def taskList(self)->list:
        return self.listaDeTareas
    


    #Rearmar la base de datos con los nuevos elementos.

    def redo(self):
        db = TinyDB('db.json')
        db.drop_tables()
        for x in self.listaDeTareas:
            db.insert(x.toDic())
        print("<<<   Cambios salvados   >>>")
