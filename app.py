from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
import pickle
import numpy as np

app = Flask(__name__)

# =========================
# CONFIGURACIÓN BASE DE DATOS
# =========================
def conectar_db():
    return pymysql.connect(
        host='localhost',   # Cambiar si usas Render con BBDD externa
        user='root',
        password='',
        db='logistica',
        port=3307
    )

# =========================
# RUTAS DEL MÓDULO LOGÍSTICA
# =========================
@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM camiones")
    camiones = cursor.fetchall()
    conn.close()
    return render_template('index.html', camiones=camiones)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO camiones (placa, marca, modelo) VALUES (%s, %s, %s)", (placa, marca, modelo))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM camiones WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        placa = request.form['placa']
        marca = request.form['marca']
        modelo = request.form['modelo']
        cursor.execute("UPDATE camiones SET placa=%s, marca=%s, modelo=%s WHERE id=%s",
                       (placa, marca, modelo, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM camiones WHERE id=%s", (id,))
        camion = cursor.fetchone()
        conn.close()
        return render_template('editar.html', camion=camion)

# =========================
# CARGA DEL MODELO DE MANTENIMIENTO
# =========================
with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

# =========================
# RUTAS DEL MÓDULO MANTENIMIENTO
# =========================
@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        datos = [
            float(request.form['kilometraje']),
            float(request.form['combustible']),
            float(request.form['frecuencia']),
            float(request.form['condiciones']),
            float(request.form['rutas'])
        ]
        entrada = np.array(datos).reshape(1, -1)
        prediccion = modelo.predict(entrada)[0]
        resultado = "Mantenimiento Requerido" if prediccion == 1 else "Sin Mantenimiento Urgente"
        return render_template('resultado.html', resultado=resultado)
    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# EJECUCIÓN LOCAL
# =========================
if __name__ == '__main__':
    app.run(debug=True)

