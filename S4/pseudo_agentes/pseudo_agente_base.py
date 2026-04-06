
import datetime
import json
import os
import random

Historial = dict[str, str]


class PseudoAgente:
    def __init__(self, nombre: str = "Athena"):
        self.nombre = nombre
        self.historial_chat: list[Historial] = []
        self.tokens: int = 100
        self.ruta_historial: str = "historial.json"

    def comando_ping(self) -> str:
        self.tokens -= 5
        message = f"[{self.nombre}] Ping enviado, pong recibido."
        self.registrar_log("ping", "user", message)
        return "pong~"

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str):
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)

    def gestionar_historial(self, op: str, rol: str) -> str | list[Historial]:
        self.tokens -= 30
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist all", rol, mensaje)
            return self.historial_chat
        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return mensaje

    ## Nuevo: Librería random
    def lanzar_dado(self) -> str:
        """Lanza un dado de 6 caras usando random.randint()."""
        self.tokens -= 5
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"

    ## Nuevo: Librería json + os (guardar a archivo)
    def guardar_historial(self) -> str:
        """Persiste el historial_chat en un archivo JSON usando json.dump()."""
        self.tokens -= 10
        with open(self.ruta_historial, "w", encoding="utf-8") as archivo:
            json.dump(self.historial_chat, archivo, indent=2, ensure_ascii=False)
        ruta_completa = os.path.abspath(self.ruta_historial)
        return f"[{self.nombre}] Historial guardado en: {ruta_completa}"

    ## Nuevo: Librería json + os (cargar desde archivo)
    def cargar_historial(self) -> str:
        """Carga el historial_chat desde un archivo JSON usando json.load()."""
        self.tokens -= 10
        if not os.path.exists(self.ruta_historial):
            return f"[{self.nombre}] No se encontró el archivo: {self.ruta_historial}"
        with open(self.ruta_historial, "r", encoding="utf-8") as archivo:
            self.historial_chat = json.load(archivo)
        return f"[{self.nombre}] Historial cargado. {len(self.historial_chat)} registros recuperados."

    ## Nuevo: Librería os + datetime (información del sistema)
    def info_sistema(self) -> str:
        """Devuelve información del sistema usando os y datetime."""
        self.tokens -= 10
        ahora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info = (
            f"[{self.nombre}] Info del Sistema:\n"
            f"  Fecha/Hora: {ahora}\n"
            f"  Directorio: {os.getcwd()}\n"
            f"  Sistema: {os.name}\n"
            f"  Archivos: {os.listdir('.')}"
        )
        return info