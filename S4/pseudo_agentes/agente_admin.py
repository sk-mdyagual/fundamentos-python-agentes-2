
from .pseudo_agente_base import PseudoAgente
from .pseudo_agente_base import Historial

class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str = "Athena"):
        ## super() llama al constructor del padre (PseudoAgente)
        ## Así no repetimos la lógica de inicialización
        super().__init__(nombre)

    ## Override: gestionar_historial SIN consumo de tokens para admin
    def gestionar_historial(self, op: str, rol: str) -> str | list[Historial]:
        # No se descuentan tokens para el administrador
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado (sin costo - Admin)"
            self.registrar_log("hist all", rol, mensaje)
            return self.historial_chat
        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado (sin costo - Admin)"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return mensaje
