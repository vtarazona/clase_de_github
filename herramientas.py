from database import get_connection


def alta_herramienta(codigo, nombre, nfc_tag, descripcion=""):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO herramientas (codigo, nombre, nfc_tag, descripcion) VALUES (?, ?, ?, ?)",
            (codigo, nombre, nfc_tag, descripcion),
        )
        conn.commit()
        return True, "Herramienta registrada correctamente."
    except Exception as e:
        return False, f"Error al registrar herramienta: {e}"
    finally:
        conn.close()


def buscar_por_nfc(nfc_tag):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM herramientas WHERE nfc_tag = ?", (nfc_tag,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def buscar_por_codigo(codigo):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM herramientas WHERE codigo = ?", (codigo,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def listar_herramientas(estado=None):
    conn = get_connection()
    if estado:
        rows = conn.execute(
            "SELECT * FROM herramientas WHERE estado = ? ORDER BY nombre", (estado,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM herramientas ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def actualizar_estado(herramienta_id, nuevo_estado):
    conn = get_connection()
    conn.execute(
        "UPDATE herramientas SET estado = ? WHERE id = ?",
        (nuevo_estado, herramienta_id),
    )
    conn.commit()
    conn.close()
