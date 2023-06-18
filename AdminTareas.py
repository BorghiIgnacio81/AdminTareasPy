from datetime import datetime
from tarea import Tarea
from usuario import Usuario
from accesoDB import AdminTarea
from fastapi import FastAPI, HTTPException, Body
from passlib.hash import md5_crypt

app = FastAPI()
admin = AdminTarea("DBAdminTareas.db")

@app.post('/register')
def register_user(user: Usuario = Body (...)):
    print(user)
    usuario = Usuario(**user)
    try:
        admin.agregar_usuario(usuario)
        return {'status': 'OK'}
    except Exception:
        raise HTTPException(status_code=400, detail='El usuario o el password es incorrecto')

@app.post('/login')
def login_user(user: Usuario = Body (...)):
    print(user)
    usuario = Usuario(**user)
    if admin.login(usuario):
        return {'status': 'OK'}
    else: 
        raise HTTPException(status_code=403, detail='El usuario o el password es incorrecto')

@app.get('/listar_tareas')
def listarTareas():
    return admin.traer_todas_tareas

@app.put('/actualizar_tarea')
def tareaUpdate(tarea: Tarea = Body (...)):

    try:
        admin.actualizar_estado_tarea(tarea)
        return {'status': 'OK'}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
