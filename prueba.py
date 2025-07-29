import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        port=3307,  # 👈 Muy importante: XAMPP usa el puerto 3307
        user='root',
        password='',  # 👈 Tu contraseña real
        db='logistica'
    )
    print("✅ Conexión exitosa a la base de datos 'logistica'")

    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tablas = cursor.fetchall()
        print("📦 Tablas en la base de datos:")
        for tabla in tablas:
            print(" -", tabla[0])

    conn.close()

except Exception as e:
    print("❌ Error al conectar o consultar:", e)
