"""
Script principal - Simulación de vuelo autónomo de dron.
Ejecuta una misión de ejemplo con waypoints y sensores.
"""

from drone_autonomo.drone import Dron, Posicion
from drone_autonomo.navegacion import PlanDeVuelo, Navegador
from drone_autonomo.sensores import SistemaSensores, Obstaculo


def crear_mision_ejemplo():
    """Crea un plan de vuelo de ejemplo: patrulla rectangular."""
    plan = PlanDeVuelo("Patrulla de Reconocimiento")

    plan.agregar_waypoint(0, 0, 10, "Punto de inicio")
    plan.agregar_waypoint(50, 0, 10, "Esquina Norte")
    plan.agregar_waypoint(50, 50, 15, "Esquina Noreste")
    plan.agregar_waypoint(0, 50, 15, "Esquina Este")
    plan.agregar_waypoint(0, 0, 5, "Regreso a base")

    return plan


def main():
    print("=" * 60)
    print("  SISTEMA DE CONTROL DE DRON AUTÓNOMO")
    print("  Simulador de vuelo v1.0")
    print("=" * 60)

    # Crear dron
    dron = Dron("Halcón-X1")

    # Configurar sensores
    sensores = SistemaSensores()
    sensores.proximidad.registrar_obstaculo(
        Obstaculo(Posicion(25, 0, 10), radio=3.0, nombre="Torre")
    )
    sensores.proximidad.registrar_obstaculo(
        Obstaculo(Posicion(50, 25, 12), radio=2.0, nombre="Árbol alto")
    )

    # Crear misión
    plan = crear_mision_ejemplo()

    # Mostrar info pre-vuelo
    print(f"\nDron: {dron.nombre}")
    print(f"Batería: {dron.bateria}%")
    print(f"Plan: {plan.nombre}")
    print(f"Waypoints: {len(plan.waypoints)}")
    print(f"Distancia total estimada: {plan.distancia_total():.1f}m")
    print()

    # Verificar sensores antes del vuelo
    print("--- Lectura de sensores pre-vuelo ---")
    print(sensores.resumen(dron.posicion))
    print()

    # Ejecutar misión
    navegador = Navegador(dron)
    navegador.cargar_plan(plan)
    exito = navegador.ejecutar_mision()

    # Reporte final
    print(f"\n{'=' * 60}")
    print("  REPORTE FINAL DE MISIÓN")
    print(f"{'=' * 60}")
    telemetria = dron.obtener_telemetria()
    print(f"  Estado: {telemetria['estado']}")
    print(f"  Posición final: ({telemetria['posicion']['x']:.1f}, "
          f"{telemetria['posicion']['y']:.1f}, "
          f"{telemetria['posicion']['z']:.1f})")
    print(f"  Batería: {telemetria['bateria']:.1f}%")
    print(f"  Resultado: {'ÉXITO' if exito else 'FALLO'}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
