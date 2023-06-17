from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from passlib.hash import md5_crypt
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(BaseModel):
    name: str
    password: str


class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)

    def verify_password(self, password):
        return md5_crypt.verify(password, self.password)


Base.metadata.create_all(bind=engine)


@app.post('/register')
def register_user(user: User):
    session = Session()
    if session.query(UserDB).filter_by(name=user.name).first():
        raise HTTPException(status_code=400, detail='Username already exists')

    user_db = UserDB(name=user.name, password=md5_crypt.hash(user.password))
    session.add(user_db)
    session.commit()
    session.close()
    return {'message': 'User registered successfully'}


@app.post('/login')
def login_user(user: User):
    session = Session()
    user_db = session.query(UserDB).filter_by(name=user.name).first()
    if user_db and user_db.verify_password(user.password):
        session.close()
        return {'message': 'User logged in successfully'}
    else: 
        session.close()
        raise HTTPException(status_code=403, detail='Username or Password is wrong')


@app.get('/list_users')
def list_users():
    session = Session()
    user_list = session.query(UserDB).all()
    session.close()
    result = [user.name for user in user_list]
    return {'User list': result}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
