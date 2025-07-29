from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def conectar_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='logistica',
        port=3307
    )

@app.route('/')
def index():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM camiones")
        camiones = cursor.fetchall()
        conexion.close()
        return render_template('index.html', camiones=camiones)
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/agregar')
def formulario_agregar():
    return render_template('form_camion.html')

@app.route('/insertar', methods=['POST'])
def insertar_camion():
    placa = request.form.get('placa')
    modelo = request.form.get('modelo')
    capacidad = request.form.get('capacidad')
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO camiones (placa, modelo, capacidad) VALUES (%s, %s, %s)", (placa, modelo, capacidad))
        conexion.commit()
        conexion.close()
        return redirect('/')
    except Exception as e:
        return f"❌ Error al insertar: {e}"

@app.route('/editar/<int:id>')
def editar_camion(id):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM camiones WHERE id = %s", (id,))
        camion = cursor.fetchone()
        conexion.close()
        return render_template('form_editar.html', camion=camion)
    except Exception as e:
        return f"❌ Error al cargar camión para editar: {e}"

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_camion(id):
    placa = request.form.get('placa')
    modelo = request.form.get('modelo')
    capacidad = request.form.get('capacidad')
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("UPDATE camiones SET placa=%s, modelo=%s, capacidad=%s WHERE id=%s", (placa, modelo, capacidad, id))
        conexion.commit()
        conexion.close()
        return redirect('/')
    except Exception as e:
        return f"❌ Error al actualizar: {e}"

@app.route('/eliminar/<int:id>')
def eliminar_camion(id):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM camiones WHERE id = %s", (id,))
        conexion.commit()
        conexion.close()
        return redirect('/')
    except Exception as e:
        return f"❌ Error al eliminar: {e}"

if __name__ == '__main__':
    app.run(debug=True)
