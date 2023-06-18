from tarea import Tarea
from usuario import Usuario
from AdminTareaControler import AdminTarea
from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel

app = FastAPI()

admin = AdminTarea("DBAdminTareas.db")

# <<< Lo que se pasa por la url >>>
#def show_person(name: Optional[str] = Query(
# None, 
# min_length=1, 
# max_lenght=50,
# title="Nombre de la persona",
# description="Esto representa el nombre de la persona."
# )
# ):

#def show_person(
# person_id: int = Path(..., gt=0) 
# ):

class Task(BaseModel):
    id: str
    titulo : str
    descripcion : str
    estado : str
    creada : str
    actualizada : str

class User(BaseModel):
    usuario : str
    password : str

@app.post('/register')
async def register_user(user: User = Body (...)):
    usuario = Usuario(**(user.dict()))
    print(usuario)
    try:
        await admin.agregar_usuario(usuario)
        return {'status': 'OK'}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail='El usuario o el password es incorrecto')

@app.post('/login')
async def login_user(user: User = Body (...)):
    usuario = Usuario(**(user.dict()))
    if (await admin.login(usuario)):
        return {'status': 'OK'}
    else: 
        raise HTTPException(status_code=403, detail='El usuario o el password es incorrecto')

@app.get('/listar_tareas')
async def listarTareas():
    return (await admin.traer_todas_tareas)

# @app.put('/actualizar_tarea')
# def tareaUpdate(tarea: Tarea = Body (...)):
#     try:
#         admin.actualizar_estado_tarea(tarea)
#         return {'status': 'OK'}
#     except Exception as e:
#         raise HTTPException(status_code=403, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
