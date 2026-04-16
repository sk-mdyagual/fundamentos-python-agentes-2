# Reto de Consolidación - Agencia del Olimpo
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# agente.py — Clases de dominio (NO tiene SQL ni FastAPI)


class PseudoAgente:
    """
    Agente base del Olimpo. Tiene nombre, rol y energía limitada.
    Cada misión completada descuenta energía según lo requerido.
    """
    def __init__(self, nombre: str, rol: str = "invitado", energia: int = 100):
        self.nombre = nombre
        self.rol = rol
        self.energia = energia

    def descontar_energia(self, cantidad: int) -> bool:
        """
        Descuenta energía al completar una misión.
        Retorna True si tenía suficiente energía, False si no alcanzó.
        """
        if self.energia < cantidad:
            return False
        self.energia -= cantidad
        return True

    def recibir_recompensa(self, cantidad: int) -> None:
        """Incrementa la energía al recibir recompensa de una misión."""
        self.energia += cantidad

    def to_dict(self) -> dict:
        """Convierte el agente a diccionario para respuestas JSON."""
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "energia": self.energia,
            "tipo": type(self).__name__
        }


class AgenteAdmin(PseudoAgente):
    """
    Versión especializada para administradores.
    Hereda todo de PseudoAgente. Los admins tienen privilegios especiales.
    """
    def __init__(self, nombre: str, energia: int = 100):
        super().__init__(nombre, rol="admin", energia=energia)

    def descontar_energia(self, cantidad: int) -> bool:
        """
        Override: los admins gastan la mitad de energía en misiones.
        Esa es la ventaja de ser admin.
        """
        costo_real = cantidad // 2
        if self.energia < costo_real:
            return False
        self.energia -= costo_real
        return True


def reconstruir_agente(datos: dict):
    """
    Reconstruye la instancia correcta según el rol almacenado en la DB.
    Si rol == 'admin' → AgenteAdmin, si no → PseudoAgente.
    """
    if datos["rol"] == "admin":
        return AgenteAdmin(datos["nombre"], datos["energia"])
    return PseudoAgente(datos["nombre"], datos["rol"], datos["energia"])
