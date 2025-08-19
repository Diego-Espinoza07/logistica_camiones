import sqlite3

def crear_tabla_historial():
    conn = sqlite3.connect("logistica.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_mantenimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kilometraje REAL NOT NULL,
        combustible REAL NOT NULL,
        averias REAL NOT NULL,
        carga REAL NOT NULL,
        rutas REAL NOT NULL,
        resultado TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Tabla 'historial_mantenimiento' creada o ya existía.")

if __name__ == "__main__":
    crear_tabla_historial()
