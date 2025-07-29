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

    id_camion = int(input("ID del camión a eliminar: "))
    query = "DELETE FROM camiones WHERE id = %s"
    cursor.execute(query, (id_camion,))
    conn.commit()

    if cursor.rowcount > 0:
        print("🗑️ Camión eliminado exitosamente.")
    else:
        print("⚠️ No se encontró un camión con ese ID.")

    conn.close()
except Exception as e:
    print("❌ Error al eliminar:", e)
