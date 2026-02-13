from database import get_connection


def alta_operario(numero_empleado, nombre, apellidos, departamento=""):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO operarios (numero_empleado, nombre, apellidos, departamento) VALUES (?, ?, ?, ?)",
            (numero_empleado, nombre, apellidos, departamento),
        )
        conn.commit()
        return True, "Operario dado de alta correctamente."
    except Exception as e:
        return False, f"Error al dar de alta operario: {e}"
    finally:
        conn.close()


def baja_operario(numero_empleado):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE operarios SET activo = 0 WHERE numero_empleado = ? AND activo = 1",
        (numero_empleado,),
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected:
        return True, "Operario dado de baja."
    return False, "Operario no encontrado o ya estaba de baja."


def buscar_operario(numero_empleado):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM operarios WHERE numero_empleado = ?", (numero_empleado,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def listar_operarios(solo_activos=True):
    conn = get_connection()
    if solo_activos:
        rows = conn.execute("SELECT * FROM operarios WHERE activo = 1 ORDER BY nombre").fetchall()
    else:
        rows = conn.execute("SELECT * FROM operarios ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]
