from conexion import conectar

try:
    conn = conectar()
    cursor = conn.cursor()

    placa = input("Placa del camión: ")
    modelo = input("Modelo: ")
    capacidad = int(input("Capacidad: "))

    sql = "INSERT INTO camiones (placa, modelo, capacidad) VALUES (%s, %s, %s)"
    cursor.execute(sql, (placa, modelo, capacidad))
    conn.commit()

    print("✅ Camión insertado correctamente.")
    conn.close()
except Exception as e:
    print("❌ Error al insertar:", e)
