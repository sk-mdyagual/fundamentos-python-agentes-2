"""
agente.py — Módulo de dominio para La Agencia de Agentes

Contiene:
  - Clase PseudoAgente  (agente base con energía y métodos de dominio)
  - Clase AgenteAdmin   (agente especializado con privilegios de rango superior)

Restricción: No hay imports de sqlite3, fastapi ni requests aquí.
             Este módulo solo conoce lógica de negocio pura.

Uso desde main.py:
    from agente import PseudoAgente, AgenteAdmin
"""

import datetime
import random


# ---------------------------------------------------------------------------
# Clase PseudoAgente — agente base
# ---------------------------------------------------------------------------
class PseudoAgente:
    """
    Agente base de La Agencia. Gestiona su propia energía y puede
    ejecutar misiones descontando el costo de energía correspondiente.
    """

    def __init__(self, nombre: str, energia: int = 100, rol: str = "agente"):
        # Atributos de instancia: viven mientras el objeto exista en memoria.
        # La energía refleja la capacidad operativa del agente.
        self.nombre = nombre
        self.energia = energia
        self.rol = rol

    # ------------------------------------------------------------------
    # descontar_energia: reduce energía con piso en 0
    # ------------------------------------------------------------------
    def descontar_energia(self, cantidad: int) -> None:
        """Descuenta energía al agente. Nunca baja de cero."""
        self.energia = max(0, self.energia - cantidad)

    # ------------------------------------------------------------------
    # ejecutar_mision: lógica de dominio para completar una misión
    # ------------------------------------------------------------------
    def ejecutar_mision(self, energia_requerida: int) -> dict:
        """
        Intenta ejecutar una misión descontando el costo de energía.
        Retorna un dict con: exito (bool), mensaje (str), energia_restante (int).

        Si la energía disponible es insuficiente, la misión no se ejecuta
        y el agente conserva toda su energía actual.
        """
        if self.energia < energia_requerida:
            return {
                "exito": False,
                "mensaje": (
                    f"Energía insuficiente. Requerida: {energia_requerida}, "
                    f"disponible: {self.energia}"
                ),
                "energia_restante": self.energia,
            }
        self.descontar_energia(energia_requerida)
        return {
            "exito": True,
            "mensaje": f"Misión completada. Energía consumida: {energia_requerida}.",
            "energia_restante": self.energia,
        }

    def estado(self) -> dict:
        """Retorna un snapshot del estado actual del agente."""
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "energia": self.energia,
        }


# ---------------------------------------------------------------------------
# Clase AgenteAdmin — hereda de PseudoAgente
# ---------------------------------------------------------------------------
# Heredar de PseudoAgente es mejor que copiar y pegar porque cualquier mejora
# hecha en la clase base se propaga automáticamente a AgenteAdmin, evitando
# duplicación e inconsistencias.
class AgenteAdmin(PseudoAgente):
    """
    Agente de rango administrador. Hereda todos los comportamientos de
    PseudoAgente pero con el privilegio de que las misiones le cuestan
    la mitad de energía — reflejo de su entrenamiento avanzado.
    """

    def __init__(self, nombre: str, energia: int = 100, rol: str = "admin"):
        # super().__init__ delega la inicialización al padre evitando repetición.
        super().__init__(nombre, energia, rol)

    # Override: las misiones le cuestan la mitad de energía al administrador
    def ejecutar_mision(self, energia_requerida: int) -> dict:
        """
        Los administradores consumen la mitad de energía por misión,
        con un mínimo de 1 para que siempre exista algún costo operativo.
        La decisión de cuánto se descuenta la toma la clase, no el endpoint.
        """
        costo_real = max(1, energia_requerida // 2)
        if self.energia < costo_real:
            return {
                "exito": False,
                "mensaje": (
                    f"Energía insuficiente (Admin). "
                    f"Costo reducido: {costo_real}, disponible: {self.energia}"
                ),
                "energia_restante": self.energia,
            }
        self.descontar_energia(costo_real)
        return {
            "exito": True,
            "mensaje": (
                f"Misión completada (Admin - costo reducido). "
                f"Energía consumida: {costo_real}."
            ),
            "energia_restante": self.energia,
        }
