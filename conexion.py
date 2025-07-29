# conexion.py
import pymysql

def conectar():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # cambia si tienes contraseña
        db='logistica',
        port=3307
    )
