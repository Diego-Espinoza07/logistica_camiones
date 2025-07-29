from flask import Flask, render_template
from conexion import conectar
import pymysql

@app.route('/')
def index():
    try:
        conexion = conectar()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, placa, modelo, capacidad FROM camiones")
        camiones = cursor.fetchall()
        conexion.close()
        return render_template("index.html", camiones=camiones)
    except Exception as e:
        print("❌ Error al mostrar camiones:", e)
        return render_template("index.html", camiones=[])
