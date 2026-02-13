"""
Módulo de navegación autónoma.
Gestiona rutas con waypoints y planificación de vuelo.
"""

import math
from drone_autonomo.drone import Posicion


class Waypoint:
    """Un punto de paso en la ruta de vuelo."""

    def __init__(self, x, y, z, nombre="", accion=None):
        self.posicion = Posicion(x, y, z)
        self.nombre = nombre
        self.accion = accion  # Función opcional a ejecutar al llegar
        self.visitado = False

    def __repr__(self):
        estado = "visitado" if self.visitado else "pendiente"
        return f"Waypoint('{self.nombre}' {self.posicion} [{estado}])"


class PlanDeVuelo:
    """Plan de vuelo con una lista ordenada de waypoints."""

    def __init__(self, nombre="Misión"):
        self.nombre = nombre
        self.waypoints = []
        self.indice_actual = 0

    def agregar_waypoint(self, x, y, z, nombre="", accion=None):
        wp = Waypoint(x, y, z, nombre or f"WP-{len(self.waypoints) + 1}", accion)
        self.waypoints.append(wp)
        return wp

    def siguiente_waypoint(self):
        if self.indice_actual < len(self.waypoints):
            return self.waypoints[self.indice_actual]
        return None

    def marcar_completado(self):
        if self.indice_actual < len(self.waypoints):
            self.waypoints[self.indice_actual].visitado = True
            self.indice_actual += 1

    def esta_completo(self):
        return self.indice_actual >= len(self.waypoints)

    def progreso(self):
        if not self.waypoints:
            return 0.0
        return (self.indice_actual / len(self.waypoints)) * 100

    def distancia_total(self):
        if len(self.waypoints) < 2:
            return 0.0
        total = 0.0
        for i in range(len(self.waypoints) - 1):
            total += self.waypoints[i].posicion.distancia_a(self.waypoints[i + 1].posicion)
        return total

    def __repr__(self):
        return (
            f"PlanDeVuelo('{self.nombre}', "
            f"waypoints={len(self.waypoints)}, "
            f"progreso={self.progreso():.0f}%)"
        )


class Navegador:
    """Controla la navegación autónoma del dron siguiendo un plan de vuelo."""

    def __init__(self, dron):
        self.dron = dron
        self.plan = None

    def cargar_plan(self, plan):
        self.plan = plan
        print(f"[Navegador] Plan cargado: {plan}")
        print(f"[Navegador] Distancia total: {plan.distancia_total():.1f}m")

    def ejecutar_mision(self):
        """Ejecuta el plan de vuelo completo de forma autónoma."""
        if not self.plan:
            print("[Navegador] Error: no hay plan de vuelo cargado.")
            return False

        print(f"\n{'='*50}")
        print(f"  INICIANDO MISIÓN: {self.plan.nombre}")
        print(f"  Waypoints: {len(self.plan.waypoints)}")
        print(f"{'='*50}\n")

        # Encender y despegar
        if not self.dron.encender_motores():
            return False
        if not self.dron.despegar(altitud_objetivo=self.plan.waypoints[0].posicion.z):
            return False

        # Recorrer waypoints
        while not self.plan.esta_completo():
            wp = self.plan.siguiente_waypoint()
            print(f"\n--- Navegando a: {wp.nombre} ---")

            if not self.dron.mover_a(wp.posicion):
                print("[Navegador] Fallo en navegación. Misión abortada.")
                return False

            # Ejecutar acción del waypoint si existe
            if wp.accion:
                print(f"[Navegador] Ejecutando acción en {wp.nombre}...")
                wp.accion()

            self.plan.marcar_completado()
            print(f"[Navegador] Progreso: {self.plan.progreso():.0f}%")

        # Aterrizar
        print("\n--- Misión completada. Aterrizando... ---")
        self.dron.aterrizar()
        self.dron.apagar_motores()

        print(f"\n{'='*50}")
        print(f"  MISIÓN COMPLETADA: {self.plan.nombre}")
        print(f"  Batería restante: {self.dron.bateria:.1f}%")
        print(f"{'='*50}")
        return True
