from database import get_connection
from herramientas import actualizar_estado


def prestar_herramienta(nfc_tag, numero_empleado):
    conn = get_connection()

    herramienta = conn.execute(
        "SELECT * FROM herramientas WHERE nfc_tag = ?", (nfc_tag,)
    ).fetchone()
    if not herramienta:
        conn.close()
        return False, "Herramienta no encontrada con ese tag NFC."

    if herramienta["estado"] != "disponible":
        conn.close()
        return False, "La herramienta no esta disponible (estado actual: {}).".format(
            herramienta["estado"]
        )

    operario = conn.execute(
        "SELECT * FROM operarios WHERE numero_empleado = ? AND activo = 1",
        (numero_empleado,),
    ).fetchone()
    if not operario:
        conn.close()
        return False, "Operario no encontrado o no esta activo."

    conn.execute(
        "INSERT INTO prestamos (herramienta_id, operario_id) VALUES (?, ?)",
        (herramienta["id"], operario["id"]),
    )
    conn.execute(
        "UPDATE herramientas SET estado = 'prestada' WHERE id = ?",
        (herramienta["id"],),
    )
    conn.commit()
    conn.close()
    return True, "Herramienta '{}' prestada a {} {}.".format(
        herramienta["nombre"], operario["nombre"], operario["apellidos"]
    )


def devolver_herramienta(nfc_tag):
    conn = get_connection()

    herramienta = conn.execute(
        "SELECT * FROM herramientas WHERE nfc_tag = ?", (nfc_tag,)
    ).fetchone()
    if not herramienta:
        conn.close()
        return False, "Herramienta no encontrada con ese tag NFC."

    if herramienta["estado"] != "prestada":
        conn.close()
        return False, "La herramienta no esta en prestamo."

    prestamo = conn.execute(
        "SELECT p.*, o.nombre, o.apellidos FROM prestamos p "
        "JOIN operarios o ON p.operario_id = o.id "
        "WHERE p.herramienta_id = ? AND p.fecha_devolucion IS NULL "
        "ORDER BY p.fecha_prestamo DESC LIMIT 1",
        (herramienta["id"],),
    ).fetchone()

    if prestamo:
        conn.execute(
            "UPDATE prestamos SET fecha_devolucion = datetime('now','localtime') WHERE id = ?",
            (prestamo["id"],),
        )

    conn.execute(
        "UPDATE herramientas SET estado = 'disponible' WHERE id = ?",
        (herramienta["id"],),
    )
    conn.commit()
    conn.close()

    if prestamo:
        return True, "Herramienta '{}' devuelta por {} {}.".format(
            herramienta["nombre"], prestamo["nombre"], prestamo["apellidos"]
        )
    return True, "Herramienta '{}' marcada como disponible.".format(herramienta["nombre"])


def historial_herramienta(nfc_tag):
    conn = get_connection()
    rows = conn.execute(
        "SELECT p.fecha_prestamo, p.fecha_devolucion, o.numero_empleado, o.nombre, o.apellidos, h.nombre as herramienta "
        "FROM prestamos p "
        "JOIN operarios o ON p.operario_id = o.id "
        "JOIN herramientas h ON p.herramienta_id = h.id "
        "WHERE h.nfc_tag = ? "
        "ORDER BY p.fecha_prestamo DESC",
        (nfc_tag,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def herramientas_de_operario(numero_empleado):
    conn = get_connection()
    rows = conn.execute(
        "SELECT h.codigo, h.nombre, h.nfc_tag, p.fecha_prestamo "
        "FROM prestamos p "
        "JOIN herramientas h ON p.herramienta_id = h.id "
        "JOIN operarios o ON p.operario_id = o.id "
        "WHERE o.numero_empleado = ? AND p.fecha_devolucion IS NULL "
        "ORDER BY p.fecha_prestamo DESC",
        (numero_empleado,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
