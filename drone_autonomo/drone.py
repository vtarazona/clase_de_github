"""
Módulo principal de control del dron autónomo.
Gestiona el estado del dron, despegue, aterrizaje y vuelo.
"""

import time
import math
from enum import Enum


class EstadoDron(Enum):
    EN_TIERRA = "en_tierra"
    DESPEGANDO = "despegando"
    EN_VUELO = "en_vuelo"
    ATERRIZANDO = "aterrizando"
    EMERGENCIA = "emergencia"


class Posicion:
    """Representa una posición 3D del dron."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def distancia_a(self, otra):
        return math.sqrt(
            (self.x - otra.x) ** 2
            + (self.y - otra.y) ** 2
            + (self.z - otra.z) ** 2
        )

    def __repr__(self):
        return f"Posicion(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"


class Dron:
    """Controlador principal del dron autónomo."""

    VELOCIDAD_MAX = 10.0  # m/s
    ALTITUD_MAX = 120.0   # metros
    ALTITUD_MIN_VUELO = 2.0  # metros
    BATERIA_CRITICA = 15.0  # porcentaje

    def __init__(self, nombre="Dron-01"):
        self.nombre = nombre
        self.estado = EstadoDron.EN_TIERRA
        self.posicion = Posicion(0, 0, 0)
        self.velocidad = 0.0
        self.bateria = 100.0
        self.motores_activos = False
        self.log = []

    def _registrar(self, mensaje):
        entrada = f"[{self.nombre}] {mensaje}"
        self.log.append(entrada)
        print(entrada)

    def encender_motores(self):
        if self.estado != EstadoDron.EN_TIERRA:
            self._registrar("Error: los motores solo se encienden en tierra.")
            return False
        self.motores_activos = True
        self._registrar("Motores encendidos. Sistemas listos.")
        return True

    def apagar_motores(self):
        if self.estado not in (EstadoDron.EN_TIERRA, EstadoDron.EMERGENCIA):
            self._registrar("Error: no se pueden apagar motores en vuelo.")
            return False
        self.motores_activos = False
        self._registrar("Motores apagados.")
        return True

    def despegar(self, altitud_objetivo=5.0):
        if not self.motores_activos:
            self._registrar("Error: encienda los motores antes de despegar.")
            return False
        if self.estado != EstadoDron.EN_TIERRA:
            self._registrar("Error: el dron no está en tierra.")
            return False
        if altitud_objetivo > self.ALTITUD_MAX:
            self._registrar(f"Error: altitud máxima permitida es {self.ALTITUD_MAX}m.")
            return False

        self.estado = EstadoDron.DESPEGANDO
        self._registrar(f"Despegando hacia {altitud_objetivo}m...")

        # Simular ascenso
        while self.posicion.z < altitud_objetivo:
            incremento = min(0.5, altitud_objetivo - self.posicion.z)
            self.posicion.z += incremento
            self.bateria -= 0.1
            self._registrar(f"  Altitud: {self.posicion.z:.1f}m | Batería: {self.bateria:.1f}%")

            if self.bateria <= self.BATERIA_CRITICA:
                self._registrar("ALERTA: batería crítica. Aterrizaje de emergencia.")
                self.aterrizaje_emergencia()
                return False

        self.estado = EstadoDron.EN_VUELO
        self._registrar(f"En vuelo estable a {self.posicion.z:.1f}m.")
        return True

    def mover_a(self, destino):
        """Mueve el dron hacia una posición destino."""
        if self.estado != EstadoDron.EN_VUELO:
            self._registrar("Error: el dron debe estar en vuelo para moverse.")
            return False

        distancia = self.posicion.distancia_a(destino)
        self._registrar(f"Moviendo hacia {destino} (distancia: {distancia:.1f}m)")

        # Simular movimiento paso a paso
        pasos = max(1, int(distancia / 2.0))
        dx = (destino.x - self.posicion.x) / pasos
        dy = (destino.y - self.posicion.y) / pasos
        dz = (destino.z - self.posicion.z) / pasos

        for i in range(pasos):
            self.posicion.x += dx
            self.posicion.y += dy
            self.posicion.z += dz
            self.bateria -= 0.2

            if self.bateria <= self.BATERIA_CRITICA:
                self._registrar("ALERTA: batería crítica durante vuelo.")
                self.aterrizaje_emergencia()
                return False

        self.posicion.x = destino.x
        self.posicion.y = destino.y
        self.posicion.z = destino.z
        self._registrar(f"Llegó a {self.posicion}. Batería: {self.bateria:.1f}%")
        return True

    def aterrizar(self):
        if self.estado not in (EstadoDron.EN_VUELO, EstadoDron.DESPEGANDO):
            self._registrar("Error: el dron no está en vuelo.")
            return False

        self.estado = EstadoDron.ATERRIZANDO
        self._registrar("Iniciando aterrizaje...")

        while self.posicion.z > 0:
            decremento = min(0.5, self.posicion.z)
            self.posicion.z -= decremento
            self.bateria -= 0.05
            self._registrar(f"  Altitud: {self.posicion.z:.1f}m")

        self.posicion.z = 0
        self.estado = EstadoDron.EN_TIERRA
        self.velocidad = 0
        self._registrar(f"Aterrizaje completado. Batería restante: {self.bateria:.1f}%")
        return True

    def aterrizaje_emergencia(self):
        self._registrar("*** ATERRIZAJE DE EMERGENCIA ***")
        self.estado = EstadoDron.EMERGENCIA
        self.posicion.z = 0
        self.velocidad = 0
        self._registrar("Dron en tierra (emergencia).")

    def obtener_telemetria(self):
        return {
            "nombre": self.nombre,
            "estado": self.estado.value,
            "posicion": {"x": self.posicion.x, "y": self.posicion.y, "z": self.posicion.z},
            "velocidad": self.velocidad,
            "bateria": self.bateria,
            "motores": self.motores_activos,
        }
