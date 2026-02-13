#!/usr/bin/env python3
"""
Sistema de Gestion de Herramientas con NFC
Permite registrar operarios, herramientas con etiquetas NFC,
y gestionar prestamos y devoluciones.
"""

from database import init_db
from operarios import alta_operario, baja_operario, buscar_operario, listar_operarios
from herramientas import alta_herramienta, buscar_por_nfc, buscar_por_codigo, listar_herramientas
from prestamos import (
    prestar_herramienta,
    devolver_herramienta,
    historial_herramienta,
    herramientas_de_operario,
)


def mostrar_menu():
    print("\n" + "=" * 50)
    print("  GESTION DE HERRAMIENTAS CON NFC")
    print("=" * 50)
    print("  OPERARIOS")
    print("    1. Dar de alta operario")
    print("    2. Dar de baja operario")
    print("    3. Buscar operario")
    print("    4. Listar operarios")
    print("  HERRAMIENTAS")
    print("    5. Registrar herramienta")
    print("    6. Buscar herramienta por NFC")
    print("    7. Buscar herramienta por codigo")
    print("    8. Listar herramientas")
    print("  PRESTAMOS")
    print("    9. Prestar herramienta (escanear NFC)")
    print("   10. Devolver herramienta (escanear NFC)")
    print("   11. Historial de herramienta")
    print("   12. Herramientas de un operario")
    print("  ------")
    print("    0. Salir")
    print("=" * 50)


def opcion_alta_operario():
    print("\n--- Alta de operario ---")
    numero = input("Numero de empleado: ").strip()
    nombre = input("Nombre: ").strip()
    apellidos = input("Apellidos: ").strip()
    departamento = input("Departamento: ").strip()
    if not numero or not nombre or not apellidos:
        print("Error: numero, nombre y apellidos son obligatorios.")
        return
    ok, msg = alta_operario(numero, nombre, apellidos, departamento)
    print(msg)


def opcion_baja_operario():
    print("\n--- Baja de operario ---")
    numero = input("Numero de empleado: ").strip()
    if not numero:
        print("Error: debe indicar el numero de empleado.")
        return
    ok, msg = baja_operario(numero)
    print(msg)


def opcion_buscar_operario():
    print("\n--- Buscar operario ---")
    numero = input("Numero de empleado: ").strip()
    op = buscar_operario(numero)
    if op:
        print(f"  Empleado: {op['numero_empleado']}")
        print(f"  Nombre:   {op['nombre']} {op['apellidos']}")
        print(f"  Depto:    {op['departamento']}")
        print(f"  Activo:   {'Si' if op['activo'] else 'No'}")
        print(f"  Alta:     {op['fecha_alta']}")
    else:
        print("Operario no encontrado.")


def opcion_listar_operarios():
    print("\n--- Listado de operarios activos ---")
    ops = listar_operarios()
    if not ops:
        print("No hay operarios registrados.")
        return
    print(f"{'No. Emp':<12} {'Nombre':<25} {'Departamento':<20}")
    print("-" * 57)
    for op in ops:
        print(f"{op['numero_empleado']:<12} {op['nombre']} {op['apellidos']:<24} {op['departamento']:<20}")
    print(f"\nTotal: {len(ops)} operarios")


def opcion_alta_herramienta():
    print("\n--- Registrar herramienta ---")
    codigo = input("Codigo de herramienta: ").strip()
    nombre = input("Nombre: ").strip()
    nfc_tag = input("Tag NFC (escanear o introducir): ").strip()
    descripcion = input("Descripcion: ").strip()
    if not codigo or not nombre or not nfc_tag:
        print("Error: codigo, nombre y tag NFC son obligatorios.")
        return
    ok, msg = alta_herramienta(codigo, nombre, nfc_tag, descripcion)
    print(msg)


def opcion_buscar_nfc():
    print("\n--- Buscar herramienta por NFC ---")
    nfc = input("Tag NFC: ").strip()
    h = buscar_por_nfc(nfc)
    if h:
        print(f"  Codigo:      {h['codigo']}")
        print(f"  Nombre:      {h['nombre']}")
        print(f"  Descripcion: {h['descripcion']}")
        print(f"  NFC Tag:     {h['nfc_tag']}")
        print(f"  Estado:      {h['estado']}")
        print(f"  Alta:        {h['fecha_alta']}")
    else:
        print("Herramienta no encontrada con ese tag NFC.")


def opcion_buscar_codigo():
    print("\n--- Buscar herramienta por codigo ---")
    codigo = input("Codigo: ").strip()
    h = buscar_por_codigo(codigo)
    if h:
        print(f"  Codigo:      {h['codigo']}")
        print(f"  Nombre:      {h['nombre']}")
        print(f"  Descripcion: {h['descripcion']}")
        print(f"  NFC Tag:     {h['nfc_tag']}")
        print(f"  Estado:      {h['estado']}")
        print(f"  Alta:        {h['fecha_alta']}")
    else:
        print("Herramienta no encontrada.")


def opcion_listar_herramientas():
    print("\n--- Listado de herramientas ---")
    filtro = input("Filtrar por estado (disponible/prestada/todas) [todas]: ").strip().lower()
    estado = filtro if filtro in ("disponible", "prestada") else None
    lista = listar_herramientas(estado)
    if not lista:
        print("No hay herramientas registradas.")
        return
    print(f"{'Codigo':<12} {'Nombre':<25} {'NFC Tag':<20} {'Estado':<12}")
    print("-" * 69)
    for h in lista:
        print(f"{h['codigo']:<12} {h['nombre']:<25} {h['nfc_tag']:<20} {h['estado']:<12}")
    print(f"\nTotal: {len(lista)} herramientas")


def opcion_prestar():
    print("\n--- Prestar herramienta ---")
    nfc = input("Escanee el tag NFC de la herramienta: ").strip()
    numero = input("Numero de empleado del operario: ").strip()
    if not nfc or not numero:
        print("Error: tag NFC y numero de empleado son obligatorios.")
        return
    ok, msg = prestar_herramienta(nfc, numero)
    print(msg)


def opcion_devolver():
    print("\n--- Devolver herramienta ---")
    nfc = input("Escanee el tag NFC de la herramienta: ").strip()
    if not nfc:
        print("Error: debe escanear el tag NFC.")
        return
    ok, msg = devolver_herramienta(nfc)
    print(msg)


def opcion_historial():
    print("\n--- Historial de herramienta ---")
    nfc = input("Tag NFC: ").strip()
    registros = historial_herramienta(nfc)
    if not registros:
        print("No hay registros para esta herramienta.")
        return
    print(f"{'Fecha prestamo':<22} {'Fecha devolucion':<22} {'Empleado':<12} {'Operario'}")
    print("-" * 80)
    for r in registros:
        devolucion = r["fecha_devolucion"] or "EN USO"
        print(f"{r['fecha_prestamo']:<22} {devolucion:<22} {r['numero_empleado']:<12} {r['nombre']} {r['apellidos']}")


def opcion_herramientas_operario():
    print("\n--- Herramientas en posesion de operario ---")
    numero = input("Numero de empleado: ").strip()
    lista = herramientas_de_operario(numero)
    if not lista:
        print("El operario no tiene herramientas en posesion.")
        return
    print(f"{'Codigo':<12} {'Nombre':<25} {'NFC Tag':<20} {'Desde'}")
    print("-" * 75)
    for h in lista:
        print(f"{h['codigo']:<12} {h['nombre']:<25} {h['nfc_tag']:<20} {h['fecha_prestamo']}")
    print(f"\nTotal: {len(lista)} herramientas")


def main():
    init_db()
    print("Base de datos inicializada.")

    opciones = {
        "1": opcion_alta_operario,
        "2": opcion_baja_operario,
        "3": opcion_buscar_operario,
        "4": opcion_listar_operarios,
        "5": opcion_alta_herramienta,
        "6": opcion_buscar_nfc,
        "7": opcion_buscar_codigo,
        "8": opcion_listar_herramientas,
        "9": opcion_prestar,
        "10": opcion_devolver,
        "11": opcion_historial,
        "12": opcion_herramientas_operario,
    }

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opcion: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        funcion = opciones.get(opcion)
        if funcion:
            funcion()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
