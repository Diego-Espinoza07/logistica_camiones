from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect("logistica.db")
    conn.row_factory = sqlite3.Row
    return conn

# Página principal: listado de camiones
@app.route('/')
def index():
    conn = conectar_db()
    camiones = conn.execute("SELECT * FROM camiones").fetchall()
    conn.close()
    return render_template("index_logistica.html", camiones=camiones)

# Agregar camiones (GET muestra formulario, POST procesa datos)
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        año = request.form['año']
        capacidad = request.form['capacidad']

        conn = conectar_db()
        conn.execute("INSERT INTO camiones (placa, modelo, año, capacidad) VALUES (?, ?, ?, ?)",
                     (placa, modelo, año, capacidad))
        conn.commit()
        conn.close()

        return redirect('/')
    else:
        return render_template('agregar.html')

# Eliminar camión
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar_db()
    conn.execute("DELETE FROM camiones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Editar camión
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar_db()
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        año = request.form['año']
        capacidad = request.form['capacidad']
        conn.execute("UPDATE camiones SET placa = ?, modelo = ?, año = ?, capacidad = ? WHERE id = ?",
                     (placa, modelo, año, capacidad, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        camion = conn.execute("SELECT * FROM camiones WHERE id = ?", (id,)).fetchone()
        conn.close()
        return render_template("editar.html", camion=camion)

# Página mantenimiento: mostrar formulario para predicción
@app.route('/mantenimiento', methods=['GET'])
def mantenimiento():
    return render_template("index_mantenimiento.html")

# Procesar predicción (simulada) y generar gráfica dinámica
@app.route('/predecir', methods=['POST'])
def predecir():
    # Recoger datos del formulario
    kilometraje = float(request.form['kilometraje'])
    combustible = float(request.form['combustible'])
    averias = float(request.form['averias'])
    carga = float(request.form['carga'])
    rutas = float(request.form['rutas'])

    # Cálculo de ejemplo para riesgo
    score = kilometraje * 0.1 + combustible * 0.2 + averias * 0.3 + carga * 0.2 + rutas * 0.2
    resultado = "Alto riesgo" if score > 50 else "Bajo riesgo"

    # Guardar resultado en historial en base de datos
    conn = conectar_db()
    conn.execute(
        "INSERT INTO historial_mantenimiento (kilometraje, combustible, averias, carga, rutas, resultado) VALUES (?, ?, ?, ?, ?, ?)",
        (kilometraje, combustible, averias, carga, rutas, resultado)
    )
    conn.commit()
    conn.close()

    # Generar gráfica sencilla con matplotlib
    valores = [kilometraje, combustible, averias, carga, rutas]
    etiquetas = ['Kilometraje', 'Combustible', 'Averías', 'Carga', 'Rutas']

    plt.figure(figsize=(8,5))
    plt.bar(etiquetas, valores, color='skyblue')
    plt.title('Datos de Entrada para Predicción')
    plt.ylabel('Valor')
    plt.tight_layout()

    # Guardar imagen en carpeta 'static'
    if not os.path.exists('static'):
        os.makedirs('static')
    ruta_grafica = os.path.join('static', 'grafica.png')
    plt.savefig(ruta_grafica)
    plt.close()

    # Renderizar plantilla con resultado y gráfica
    return render_template("index_mantenimiento.html", resultado=resultado, grafica='grafica.png')

# Mostrar historial de mantenimiento (con encabezados y enumeración)
@app.route('/historial')
def historial_mantenimiento():
    conn = conectar_db()
    registros = conn.execute("SELECT * FROM historial_mantenimiento ORDER BY id DESC").fetchall()
    conn.close()

    encabezados = registros[0].keys() if registros else []
    registros_enumerados = list(enumerate(registros))

    return render_template("historial_mantenimiento.html", registros=registros_enumerados, encabezados=encabezados)

# Eliminar registro de historial por índice
@app.route('/eliminar_historial/<int:indice>')
def eliminar_historial(indice):
    conn = conectar_db()
    registro = conn.execute("SELECT id FROM historial_mantenimiento ORDER BY id DESC LIMIT 1 OFFSET ?", (indice,)).fetchone()
    if registro:
        conn.execute("DELETE FROM historial_mantenimiento WHERE id = ?", (registro['id'],))
        conn.commit()
    conn.close()
    return redirect(url_for('historial_mantenimiento'))

if __name__ == '__main__':
    app.run(debug=True)
