from tarea import Tarea
from usuario import Usuario
import sqlite3
import datetime

class AdminTarea:
    
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, descripcion TEXT, estado TEXT, creada DATE, actualizada DATE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT PRIMARY KEY, password TEXT)''')
        self.connection.commit()
    
    
    #<<< Metodos de usuarios >>>
    async def agregar_usuario(self, usuario: Usuario):
        self.cursor.execute("INSERT INTO usuarios (usuario, password) VALUES ( ?, ?)",
                            (usuario.usuario, usuario.password))
        self.connection.commit()

    async def login(self, usuario: Usuario)->bool:
        result = self.cursor.execute(f"SELECT COUNT(*) FROM usuarios WHERE usuario='{usuario.usuario}' AND password='{usuario.password}'").fetchone()
        return int(result[0]) == 1


    # <<< Metodos de tareas >>>
    async def agregar_tarea(self, tarea: Tarea):
        self.cursor.execute('''INSERT INTO tareas (titulo, descripcion, estado, creada, actualizada) VALUES (?, ?, ?, ?, ?)''',
                             (tarea.titulo, tarea.descripcion, tarea.estado, tarea.creada, tarea.actualizada))
        self.connection.commit()
        tarea.setId(str(self.cursor.lastrowid))
        return tarea.toDic()

    async def actualizar_estado_tarea(self, tarea: Tarea):
        self.cursor.execute('''UPDATE tareas SET estado=?, actualizada=? WHERE id=?''',
                                 (tarea.estado, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tarea.id))
        self.connection.commit()
    
    async def eliminar_tarea(self, tarea: Tarea):
        self.cursor.execute('''DELETE FROM tareas WHERE id=?''', (tarea.id))
        self.connection.commit()

    async def traer_todas_tareas(self)->dict:
        result = self.cursor.execute("SELECT * FROM tareas ORDER BY id ASC")
        aux = result.fetchall()
        tareas = []
        for tarea in aux:
            #[{obj1},{obj2}]
            tareas.append((Tarea(str(tarea[0]),tarea[1], tarea[2], tarea[3], tarea[4], tarea[5])).toDic())
        return dict(enumerate(tareas)) #{{1:"obj1"}{2:"obj2"}} -> se obtienen los objetos con list(diccionario.values())