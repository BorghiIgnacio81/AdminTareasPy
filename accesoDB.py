from tarea import Tarea
from usuario import Usuario
import sqlite3
import datetime

class AdminTarea:

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                descripcion TEXT,
                creada DATE,
                actualizada DATE,
                estado TEXT,
                status INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario TEXT PRIMARY KEY,
                password TEXT
            )
        ''')

        self.connection.commit()
    
    
    #Metodos de usuarios
    async def agregar_usuario(self, usuario: Usuario):
        self.cursor.execute("INSERT INTO usuarios (usuario, password) VALUES ( ?, ?)",(usuario.usuario, usuario.password))
        self.connection.commit()

        #self.cursor.close()
        self.cursor.execute("SELECT * FROM usuarios")
        rows = self.cursor.fetchall()
        print("Aca llega")

        # Imprimir los datos
        for row in rows:
            print(row)

        return True

    async def login(self, usuario: Usuario)->bool:
        return self.cursor.execute(int(f"SELECT COUNT(*) FROM usuarios WHERE usuario='{usuario.usuario}' AND password='{usuario.password}")) == 1
    

    #Metodos de tareas
    def agregar_tarea(self, tarea: Tarea):
        tarea_query = '''
            INSERT INTO tareas (id, titulo, descripcion, creada, actualizada, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        tarea_data = (tarea.id, tarea.titulo, tarea.descripcion, tarea.creada, tarea.actualizada, tarea.estado)
        self.cursor.execute(tarea_query, tarea_data)
        self.connection.commit()
        return tarea.id
        #Response post {"status":"OK", "idTarea": "tarea_id"}

    
    
    
    def actualizar_estado_tarea(self, tarea: Tarea):
        try:
            self.cursor.execute('''
                UPDATE tareas SET estado=?, actualizada=? WHERE id=?
                ''', (tarea.estado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tarea.id))
            self.connection.commit()
        except:
            raise Exception("Problemas al intentar modificar la base de datos.")
    
    
    def eliminar_tarea(self, tarea: Tarea):
        #delete 
        #tarea = self.traer_tarea(tarea.id)
        self.cursor.execute('''
            INSERT INTO tareas_eliminadas (
                id_tarea,
                titulo,
                creada,
                actualizada,
                estado,
                fechaEliminacion) VALUES (?, ?, ?, ?, ?, ?)
        ''', (tarea.id, tarea.titulo, tarea.creada, tarea.actualizada, tarea.estado, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.connection.commit()
        self.cursor.execute('''
            DELETE FROM tareas WHERE id=?
            ''', (tarea.id,))
        self.connection.commit()


    def traer_todas_tareas(self):
        #post con un diccionario grande
        tareas = []
        for tarea_dict in self.tareas.all():
            tarea = Tarea(tarea_dict["titulo"], tarea_dict["descripcion"])
            tarea.estado = tarea_dict["estado"]
            tarea.creada = tarea_dict["creada"]
            tarea.actualizada = tarea_dict["actualizada"]
            tareas.append(tarea)
        return tareas.toDic()
        #return tareas