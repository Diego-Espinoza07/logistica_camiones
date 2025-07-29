import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='logistica',
        port=3307
    )
    cursor = conn.cursor()

    id_camion = int(input("ID del camión a actualizar: "))
    nueva_placa = input("Nueva placa: ")
    nuevo_modelo = input("Nuevo modelo: ")
    nueva_capacidad = int(input("Nueva capacidad: "))

    query = "UPDATE camiones SET placa=%s, modelo=%s, capacidad=%s WHERE id=%s"
    cursor.execute(query, (nueva_placa, nuevo_modelo, nueva_capacidad, id_camion))
    conn.commit()

    if cursor.rowcount > 0:
        print("✅ Camión actualizado correctamente.")
    else:
        print("⚠️ No se encontró un camión con ese ID.")

    conn.close()
except Exception as e:
    print("❌ Error al actualizar:", e)
