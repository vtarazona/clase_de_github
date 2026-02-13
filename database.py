import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "herramientas_nfc.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_empleado TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            departamento TEXT,
            activo INTEGER DEFAULT 1,
            fecha_alta TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS herramientas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            nfc_tag TEXT UNIQUE NOT NULL,
            estado TEXT DEFAULT 'disponible',
            fecha_alta TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            herramienta_id INTEGER NOT NULL,
            operario_id INTEGER NOT NULL,
            fecha_prestamo TEXT DEFAULT (datetime('now','localtime')),
            fecha_devolucion TEXT,
            FOREIGN KEY (herramienta_id) REFERENCES herramientas(id),
            FOREIGN KEY (operario_id) REFERENCES operarios(id)
        )
    """)

    conn.commit()
    conn.close()
