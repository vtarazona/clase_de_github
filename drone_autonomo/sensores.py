"""
Módulo de sensores y evasión de obstáculos.
Simula sensores de proximidad, GPS, altímetro y brújula.
"""

import random
import math
from drone_autonomo.drone import Posicion


class Obstaculo:
    """Representa un obstáculo en el espacio."""

    def __init__(self, posicion, radio=1.0, nombre="obstáculo"):
        self.posicion = posicion
        self.radio = radio
        self.nombre = nombre

    def contiene(self, punto):
        return self.posicion.distancia_a(punto) <= self.radio

    def __repr__(self):
        return f"Obstaculo('{self.nombre}', pos={self.posicion}, radio={self.radio})"


class SensorProximidad:
    """Simula sensores de proximidad para detectar obstáculos."""

    def __init__(self, alcance=10.0):
        self.alcance = alcance
        self.obstaculos = []

    def registrar_obstaculo(self, obstaculo):
        self.obstaculos.append(obstaculo)

    def detectar(self, posicion_dron):
        """Detecta obstáculos dentro del alcance del sensor."""
        detectados = []
        for obs in self.obstaculos:
            distancia = posicion_dron.distancia_a(obs.posicion)
            if distancia <= self.alcance + obs.radio:
                detectados.append({
                    "obstaculo": obs,
                    "distancia": distancia,
                    "peligro": distancia <= obs.radio * 2,
                })
        return detectados

    def hay_peligro(self, posicion_dron):
        detectados = self.detectar(posicion_dron)
        return any(d["peligro"] for d in detectados)


class GPS:
    """Simula un receptor GPS con ruido configurable."""

    def __init__(self, precision=0.5):
        self.precision = precision

    def leer_posicion(self, posicion_real):
        """Retorna posición con error simulado."""
        return Posicion(
            x=posicion_real.x + random.gauss(0, self.precision),
            y=posicion_real.y + random.gauss(0, self.precision),
            z=posicion_real.z + random.gauss(0, self.precision * 0.5),
        )


class Altimetro:
    """Simula un altímetro barométrico."""

    def __init__(self, precision=0.2):
        self.precision = precision

    def leer_altitud(self, altitud_real):
        return altitud_real + random.gauss(0, self.precision)


class Brujula:
    """Simula una brújula digital."""

    def __init__(self, precision=2.0):
        self.precision = precision  # grados de error

    def leer_rumbo(self, origen, destino):
        """Calcula el rumbo hacia un destino con error simulado."""
        dx = destino.x - origen.x
        dy = destino.y - origen.y
        rumbo_real = math.degrees(math.atan2(dy, dx)) % 360
        return (rumbo_real + random.gauss(0, self.precision)) % 360


class SistemaSensores:
    """Integra todos los sensores del dron."""

    def __init__(self):
        self.gps = GPS()
        self.altimetro = Altimetro()
        self.brujula = Brujula()
        self.proximidad = SensorProximidad()

    def lectura_completa(self, posicion_real, destino=None):
        """Obtiene lectura de todos los sensores."""
        lectura = {
            "gps": self.gps.leer_posicion(posicion_real),
            "altitud": self.altimetro.leer_altitud(posicion_real.z),
            "obstaculos": self.proximidad.detectar(posicion_real),
            "peligro": self.proximidad.hay_peligro(posicion_real),
        }
        if destino:
            lectura["rumbo"] = self.brujula.leer_rumbo(posicion_real, destino)
        return lectura

    def resumen(self, posicion_real):
        lectura = self.lectura_completa(posicion_real)
        pos_gps = lectura["gps"]
        n_obs = len(lectura["obstaculos"])
        peligro = "SI" if lectura["peligro"] else "NO"
        return (
            f"GPS: ({pos_gps.x:.1f}, {pos_gps.y:.1f}, {pos_gps.z:.1f}) | "
            f"Alt: {lectura['altitud']:.1f}m | "
            f"Obstáculos: {n_obs} | Peligro: {peligro}"
        )
