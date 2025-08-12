from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pickle
import numpy as np

app = Flask(__name__)

# ==========================
# CONEXIÓN BASE DE DATOS
# ==========================
def conectar_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='logistica',
        port=3307
    )

# ==========================
# RUTAS LOGÍSTICA (CRUD)
# ==========================
@app.route('/')
def index():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM camiones")
    camiones = cursor.fetchall()
    conexion.close()
    return render_template('index.html', camiones=camiones)

# ==========================
# RUTAS MANTENIMIENTO
# ==========================
@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    # Cargar el modelo
    with open('modelo.pkl', 'rb') as f:
        modelo = pickle.load(f)
    
    # Recibir datos del formulario
    km = float(request.form['kilometraje'])
    combustible = float(request.form['combustible'])
    averias = int(request.form['averias'])
    carga = float(request.form['carga'])
    dificultad = int(request.form['dificultad'])

    # Preparar datos para el modelo
    datos = np.array([[km, combustible, averias, carga, dificultad]])

    # Hacer predicción
    prediccion = modelo.predict(datos)[0]

    resultado = "Mantenimiento pronto" if prediccion == 1 else "En buen estado"
    return render_template('mantenimiento.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)

