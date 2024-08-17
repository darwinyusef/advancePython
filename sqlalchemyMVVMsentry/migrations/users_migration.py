from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from migrations.listToSQL_migration import userTable, userDrop
import psycopg2
import sentry_sdk
import os
from dotenv import load_dotenv
load_dotenv()

# Database connection details (replace with your credentials)
pgInfo = os.getenv('POSTGRESQL_KEY')


router = APIRouter(
    prefix="/migrations",
    tags=["migrations"],
    responses={404: {"description": "Not found"}}
)


def conectar_bd():
    # Agregar siempre ?sslmode=require al final
    conexion = psycopg2.connect(pgInfo)
    return conexion


def cerrar_bd(conexion):
    conexion.close()


class Configurate(BaseModel):
    password: str


def userCreateTable():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute(userDrop)
        conexion.commit()
        cursor.execute(userTable)
        conexion.commit()
        cerrar_bd(conexion)
        respuesta = {
            "mensaje": "La tabla ha sido creada con exito",
        }
        return respuesta

    except Exception as e:
        print(f"Error al crear usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la Tabla Usuario")


@router.post("/config")
def config(configurate: Configurate):
    if configurate.password != os.getenv('MIGRATION_KEY'):
        error_message = "Error al crear la BD usuarios el password no es correcto."
        sentry_sdk.capture_message(error_message, level='error')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error inesperado")
    else:
        return userCreateTable()
  