from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)

"""
Apartir de este punto generamos las conexiones a la bd
"""

class Usuario(BaseModel): 
    names: str

def conectar_bd():
    conn = psycopg2.connect(
        "postgresql://usersapi_rk0r_user:iBaiCtjVPV63IPeudXOoslwnDjnS5AVB@dpg-col7h0tjm4es738c6cl0-a.oregon-postgres.render.com/usersapi_rk0r?sslmode=require"
    )
    return conn

def cerrar_db(conn):
    conn.close()


# C*R*U*D Create* Read* ReadOnly* Update* Delete 


# GET ALL - READ/ALL Obtiene todos
@app.get("/alldata", tags=['names'], summary="GET ALL - READ/ALL Obtiene todos")
def todos(): 
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM onlydata")
    names = cursor.fetchall()
    conexion.commit()
    # este codigo es creado por nosotros y trae tanto las filas como las columnas y hace un mix
    if cursor.description:
        cols = [desc[0] for desc in cursor.description] #columnas
        result = [dict(zip(cols, row)) for row in names] # filas        
    cerrar_db(conexion)
    return result

# GET SHOW - READ/SHOW ID(names) Obtiene solo uno
@app.get("/onlydata/{names}", tags=['names'], summary="GET SHOW - READ/SHOW ID(names) Obtiene solo uno")
def onlynames(names: str):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    sql = f"SELECT * FROM public.onlydata WHERE names LIKE '%{names}%'"
    cursor.execute(sql)
    user = cursor.fetchone()
    conexion.commit()
    response = {
        "ms": "El usuario se ha encontrado con exito",
        "user": user
    }
    cerrar_db(conexion)
    return response

""" 
INSERT INTO 
onlydata (names) 
VALUES ('Julianita') 

"""
# POST - CREATE - shema pydantic / BaseModel -  Crear un name
@app.post("/create", tags=['names'], summary="POST - CREATE - shema pydantic / BaseModel -  Crear un name")
def create(usuario: Usuario): # Body
    try: 
        conexion = conectar_bd()
        cursor = conexion.cursor()
        print(usuario.names)
        cursor.execute("INSERT INTO onlydata (names) VALUES (%s) RETURNING *", (usuario.names,))
        conexion.commit()
        user = cursor.fetchone()[0]
        response = {
            "ms": "El usuario se ha creado con exito",
            "user": user
        }
        cerrar_db(conexion)
        return response
    
    except Exception as e: 
        print(f"Error al crear un usuario {e}")
        return HTMLResponse(content={"mensaje": "Error al crear un usuario"}, status_code= 500)
 
   
""" 
UPDATE onlydata 
SET names = 'Carlosito' 
WHERE names = 'caliche'

"""
# PUT - UPDATE - ID(names) - shema pydantic / BaseModel -  Update un name
@app.put("/update/{names}", tags=['names'], summary="PUT - UPDATE - ID(names) - shema pydantic / BaseModel - Update un name")
def actualizar(usuario: Usuario, names: str): # Body
    try: 
        conexion = conectar_bd()
        cursor = conexion.cursor()
        print(usuario.names)
        cursor.execute("UPDATE onlydata SET names = %s WHERE names = %s RETURNING *;", (usuario.names, names))
        conexion.commit()
        user = cursor.fetchone()[0]
        response = {
            "ms": "El usuario se ha actualizado con exito",
            "user": user
        }
        cerrar_db(conexion)
        return response
    
    except Exception as e: 
        print(f"Error al actualizar un usuario {e}")
        return HTMLResponse(content={"mensaje": "Error al actualizar el usuario"}, status_code= 500)


# DELETE - ID(names)  Borrar un name
@app.delete("/delete/{names}", tags=['names'], summary="DELETE - ID(names)  Borrar un name")
def borrar(names: str): # Body
    try: 
        conexion = conectar_bd()
        cursor = conexion.cursor()
        sql = f"DELETE FROM onlydata WHERE names LIKE '%{names}%'"
        cursor.execute(sql)
        conexion.commit()
        response = {
            "info": "ok",
            "ms": "El usuario se ha borrado con exito",
        }
        cerrar_db(conexion)
        return response
    
    except Exception as e: 
        print(f"Error al borrar un usuario {e}")
        return HTMLResponse(content={"mensaje": "Error al borrar el usuario"}, status_code= 500)
    
     

"""
En este punto cerramos nuestra conexión a la bd
"""


@app.get("/", tags=['config'])
def read_root():
    return {"primerfetch": "true"}

@app.get("/items/{item_id}", tags=['config'])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



