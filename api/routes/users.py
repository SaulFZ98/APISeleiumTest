# APIRouter permite definir rutas modularmente, HTTPException para lanzar errores como 404 o 400 si falla algo
from fastapi import APIRouter, HTTPException
#BaseModel: Base para crear modelos que validan datos automaticamente, EmailStr: valida correos, Field(...):permite definir validaciones(maximos minimos opcional etc)
from pydantic import  BaseModel, EmailStr, Field
#List, Optional:Ayuda a declarar tipos de datos de listas u optionals en los modelos
from typing import List, Optional
#uuid: Usamos para generar IDs inicos para los usuarios
import uuid

#esto crea una instancia del router que luego sera incluida en la app principal (main.py)con app.include_router(...). Esto crea un enrutador independiente. Es como una mini-aplicación de FastAP
router = APIRouter()


# modelo de entrada
class UserIn(BaseModel):
    name: str = Field(...,min_length=2,max_length=50)
    email : EmailStr
    age : Optional[int] = Field(None, gt=0, lt=120)

#modelo de salida,  este modelo extiende UserIn y agrega un campo id, se usa para representar el objeto final que devuelve la API
class User(UserIn):
    id : str


#base de datos de memoria, simula una base de datos en memoria usando una lista de usuarios, Los usuarios se guardan aqui mientras corre la API(pero se borra al reiniciar)
fake_db: List[User] = []


#crear usuario , POST /users: Crea un usuario, Convierte el modelo de entrada (UserIn) en uno con ID (User). uuid.uuid4(): Genera un ID único como string
#En FastAPI, usamos @router cuando queremos organizar nuestras rutas (endpoints) de forma modular y limpia
#Metodo: POTS, Ruta:/users, reponse_modeular = user:Especifica el modelo de respuesta que se devolverá (en este caso, un objeto User con ID). status_code=201:Código HTTP estándar que significa "Creado correctamente".
#Parámetro user: UserIn: FastAPI convierte automáticamente el JSON del cuerpo en una instancia del modelo UserIn y lo valida.
@router.post("/users", response_model=User, status_code=201)
def Create_user(user: UserIn):
    new_user = User(id=str(uuid.uuid4()), **user.dict())
    fake_db.append(new_user)
    return new_user



#obtener todos los usuarios
@router.get("/users",response_model=List[User])
def get_user():
    return fake_db



#obtener un usuario por ID
@router.get("/users/{user_id}",response_model=User)
def get_user(user_id: str):
    for user in fake_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404,detail="Usuario no encontrado")

#Actualizar usuario
#**data.dict(), Es un metodo de los modelos Pydantic que convierte un objeto de modelo en un diccionario Python estándar (dict)
#data.dict(), Convertir datos validados a un formato que se puede usar fácilmente
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, data:UserIn):
    for idx, user in enumerate(fake_db):
        if user.id == user_id:
            update_user = User(id = user_id, **data.dict())
            fake_db[idx] = update_user
            return update_user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#eliminar usuario
#204 significa “No Content”: operación exitosa, pero no hay nada que devolver.
@router.delete("/users/{user_id}",status_code=204)
def delete_user(user_id : str):
    for user in fake_db:
        if user.id == user_id:
            fake_db.remove(user)
            return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
