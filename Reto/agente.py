import datetime
from typing import Dict, List

Historial = Dict[str, str]


class PseudoAgente:
    """
    Agente básico con nombre, energía y capacidad de registro.
    """
    def __init__(self, nombre: str, energia: int = 100, rol: str = "agente"):
        self.nombre = nombre
        self.energia = energia
        self.rol = rol
        self.historial_chat: List[Historial] = []

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str):
        """Registra un evento en el historial del agente."""
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)

    def consumir_energia(self, cantidad: int) -> bool:
        """
        Descuenta energía del agente. Retorna True si fue exitoso,
        False si no tiene suficiente energía.
        """
        if self.energia >= cantidad:
            self.energia -= cantidad
            return True
        return False

    def info(self) -> Dict[str, any]:
        """Retorna la información básica del agente como diccionario."""
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "energia": self.energia
        }


class AgenteAdmin(PseudoAgente):
    """
    Agente administrativo con privilegios especiales.
    Las operaciones de admin NO consumen energía.
    """
    def __init__(self, nombre: str, energia: int = 100):
        super().__init__(nombre, energia, rol="admin")

    def consumir_energia(self, cantidad: int) -> bool:
        """
        Override: Los administradores NO consumen energía.
        Siempre retorna True para mantener compatibilidad con el flujo.
        """
        # No se descuenta energía para el administrador
        self.registrar_log(
            "energia",
            "admin",
            f"[{self.nombre}] Operación administrativa sin costo de energía"
        )
        return True


# Función auxiliar para reconstruir agentes desde datos de la DB
def reconstruir_agente(datos: Dict) -> PseudoAgente:
    """
    Reconstruye una instancia de agente desde un diccionario de datos.
    Retorna AgenteAdmin si el rol es 'admin', PseudoAgente en caso contrario.
    
    Esta función es clave para cumplir con R2: al despertar un agente
    desde la base de datos, debe recuperar su clase correcta.
    """
    nombre = datos["nombre"]
    energia = datos["energia"]
    rol = datos["rol"]
    
    if rol == "admin":
        return AgenteAdmin(nombre=nombre, energia=energia)
    else:
        return PseudoAgente(nombre=nombre, energia=energia, rol=rol)
