# agente.py — Clases de dominio POO para los Cyber-Mercenarios

# HP máximo canónico por clase. Lo usa rng.py para calcular el ratio de salud
# (un Tanque con 80 HP está mejor que un Hacker con 80 HP).
HP_MAX_POR_CLASE: dict[str, int] = {
    "hacker": 100,
    "tanque": 200,
    "sniper": 110,
    "fixer": 90,
    "novato": 100,
}


class MercenarioBase:
    """
    Clase base para todos los mercenarios.
    Atributos:
    - hp: Puntos de salud (si llega a 0, muere).
    - creditos: Dinero acumulado por contratos.
    """
    def __init__(self, alias: str, clase_nombre: str = "novato", hp: int = 100, creditos: int = 0, estado_vital: str = "vivo"):
        self.alias = alias
        self.clase_nombre = clase_nombre
        self.hp = hp
        self.creditos = creditos
        self.estado_vital = estado_vital

    def recibir_dano(self, cantidad: int, tipo_contrato: str = "estandar") -> bool:
        """
        Reduce los HP al ejecutar contratos peligrosos.
        Retorna True si sobrevive, False si muere.
        """
        self.hp -= cantidad
        if self.hp <= 0:
            self.hp = 0
            self.estado_vital = "muerto"
            return False
        return True

    def cobrar_pago(self, monto: int) -> None:
        """Aumenta los créditos tras completar un contrato."""
        self.creditos += monto

    def to_dict(self) -> dict:
        return {
            "alias": self.alias,
            "clase_nombre": self.clase_nombre,
            "hp": self.hp,
            "creditos": self.creditos,
            "estado_vital": self.estado_vital,
            "tipo_instancia": type(self).__name__
        }


class Hacker(MercenarioBase):
    """
    Especialista en redes corporativas.
    Recibe la mitad del daño en contratos de tipo 'infiltracion' o 'hackeo'.
    """
    def __init__(self, alias: str, hp: int = 80, creditos: int = 0, estado_vital: str = "vivo"):
        super().__init__(alias, clase_nombre="hacker", hp=hp, creditos=creditos, estado_vital=estado_vital)

    def recibir_dano(self, cantidad: int, tipo_contrato: str = "estandar") -> bool:
        if tipo_contrato in ["infiltracion", "hackeo"]:
            cantidad = cantidad // 2
        return super().recibir_dano(cantidad)


class Tanque(MercenarioBase):
    """
    Especialista en combate pesado.
    Tiene una armadura subdérmica que absorbe 10 puntos de daño fijo en contratos de 'combate'.
    """
    def __init__(self, alias: str, hp: int = 150, creditos: int = 0, estado_vital: str = "vivo"):
        super().__init__(alias, clase_nombre="tanque", hp=hp, creditos=creditos, estado_vital=estado_vital)

    def recibir_dano(self, cantidad: int, tipo_contrato: str = "estandar") -> bool:
        if tipo_contrato in ["combate", "asalto"]:
            cantidad = max(1, cantidad - 10)  # La armadura absorbe daño, pero mínimo recibe 1
        return super().recibir_dano(cantidad)


def instanciar_mercenario(datos: dict) -> MercenarioBase:
    """Factory Pattern: Reconstruye la instancia desde la base de datos."""
    clase = datos["clase_nombre"].lower()
    if clase == "hacker":
        return Hacker(datos["alias"], datos["hp"], datos["creditos"], datos.get("estado_vital", "vivo"))
    elif clase == "tanque":
        return Tanque(datos["alias"], datos["hp"], datos["creditos"], datos.get("estado_vital", "vivo"))
    return MercenarioBase(datos["alias"], datos["clase_nombre"], datos["hp"], datos["creditos"], datos.get("estado_vital", "vivo"))
