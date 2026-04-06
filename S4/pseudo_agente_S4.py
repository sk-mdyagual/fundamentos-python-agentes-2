import datetime
import random

Historial = dict[str, str]

class PseudoAgente:
    def __init__(self, nombre: str = "Athena"):
        self.nombre = nombre
        self.historial_chat: list[Historial] = []
        self.tokens: int = 100

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str) -> None:
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje,
        }
        self.historial_chat.append(d_log)

    def gestionar_historial(self, op: str, rol: str) -> str | list[Historial]:
        self.tokens -= 10
        if op == "all":
            self.registrar_log("historial all", rol, "Se mostro todo el historial.")
            return self.historial_chat
        if op == "clear":
            self.historial_chat.clear()
            self.registrar_log("historial clear", rol, "Se limpio todo el historial.")
            return "[PseudoAgente] Historial eliminado correctamente."
        return "[PseudoAgente] Opcion de historial no reconocida."

    def lanzar_dado(self) -> str:
        self.tokens -= 1
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"


# La herencia evita duplicar toda la clase base y permite especializar solo lo necesario.
# AgenteAdmin reutiliza todo de PseudoAgente y modifica un unico metodo con override.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str = "Athena"):
        # Una variable local vive solo dentro del metodo.
        # Un atributo con self. queda guardado en el objeto para usarse en toda la sesion.
        super().__init__(nombre)
        self.nivel = "admin"

    def gestionar_historial(self, op: str, rol: str) -> str | list[Historial]:
        if op == "all":
            self.registrar_log("historial all", rol, "Admin consulto historial sin costo.")
            return self.historial_chat
        if op == "clear":
            self.historial_chat.clear()
            self.registrar_log("historial clear", rol, "Admin limpio historial sin costo.")
            return "[PseudoAgente] Historial eliminado correctamente."
        return "[PseudoAgente] Opcion de historial no reconocida."
