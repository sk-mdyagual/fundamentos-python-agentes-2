from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


@dataclass
class PseudoAgente:
    nombre: str
    rol: str
    tokens: int = 100
    historial_chat: MemoriaAgente = field(default_factory=list)

    def consumir_energia(self, costo: int) -> None:
        if costo <= 0:
            return
        if self.tokens < costo:
            raise RuntimeError(
                f"Energia insuficiente para '{self.nombre}'. Requiere {costo} y tiene {self.tokens}."
            )
        self.tokens -= costo

    def completar_mision(self, energia_requerida: int) -> int:
        if energia_requerida <= 0:
            raise ValueError("La energia requerida debe ser mayor a cero")
        self.consumir_energia(energia_requerida)
        return self.tokens

    def gestionar_historial(self, accion: str) -> str:
        self.consumir_energia(5)
        accion_normalizada = accion.strip().lower()
        if accion_normalizada == "all":
            if not self.historial_chat:
                return "[PseudoAgente] El historial esta vacio."
            salida = ["=== Historial Completo ==="]
            for i, registro in enumerate(self.historial_chat, 1):
                salida.append(
                    f"[{i}] {registro.get('timestamp', '')} | {registro.get('cmd', '')} | {registro.get('descripcion', '')}"
                )
            return "\n".join(salida)

        if accion_normalizada == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        coincidencias = []
        for registro in self.historial_chat:
            if accion_normalizada in registro.get("descripcion", "").lower():
                coincidencias.append(registro)

        if not coincidencias:
            return "[PseudoAgente] No encontre registros que coincidan con esa palabra."

        salida = [f"Coincidencias: {len(coincidencias)}"]
        for i, registro in enumerate(coincidencias, 1):
            salida.append(
                f"[{i}] {registro.get('timestamp', '')} | {registro.get('rol', '')} | {registro.get('descripcion', '')}"
            )
        return "\n".join(salida)

    def registrar_recuerdo(self, cmd: str, descripcion: str) -> None:
        self.historial_chat.append(
            {
                "timestamp": datetime.now().isoformat(),
                "cmd": cmd,
                "rol": self.rol,
                "descripcion": descripcion,
            }
        )


# Heredar me evita copiar y pegar toda la clase otra vez.
# Con AgenteAdmin solo cambio lo que de verdad es distinto y reutilizo lo demas del agente base.
@dataclass
class AgenteAdmin(PseudoAgente):
    def gestionar_historial(self, accion: str) -> str:
        accion_normalizada = accion.strip().lower()
        if accion_normalizada == "all":
            if not self.historial_chat:
                return "[PseudoAgente] El historial esta vacio."
            salida = ["=== Historial Completo (Admin) ==="]
            for i, registro in enumerate(self.historial_chat, 1):
                salida.append(
                    f"[{i}] {registro.get('timestamp', '')} | {registro.get('cmd', '')} | {registro.get('descripcion', '')}"
                )
            return "\n".join(salida)

        if accion_normalizada == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        coincidencias = []
        for registro in self.historial_chat:
            if accion_normalizada in registro.get("descripcion", "").lower():
                coincidencias.append(registro)

        if not coincidencias:
            return "[PseudoAgente] No encontre registros que coincidan con esa palabra."

        salida = [f"Coincidencias: {len(coincidencias)}"]
        for i, registro in enumerate(coincidencias, 1):
            salida.append(
                f"[{i}] {registro.get('timestamp', '')} | {registro.get('rol', '')} | {registro.get('descripcion', '')}"
            )
        return "\n".join(salida)
