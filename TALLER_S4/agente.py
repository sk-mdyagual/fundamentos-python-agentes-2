# 🛠️ Taller Semana 4: Nace la Entidad (POO y Modularización)
# Oscar Danilo Sanabria Sogamoso
"""
agente.py — Módulo del PseudoAgente para la Semana 4

Este archivo contiene la clase PseudoAgente, la clase AgenteAdmin y los alias
de tipos necesarios para encapsular el estado del agente en un solo lugar.
"""

import datetime
import random

# Darle un alias a la memoria ayuda porque deja clara la forma exacta de cada recuerdo
# y hace que la estructura del agente sea más fácil de leer, mantener y reutilizar.
Recuerdo = dict[str, str]
MemoriaAgente = list[Recuerdo]


class PseudoAgente:
    # Una variable temporal vive solo dentro de un método, pero self.nombre,
    # self.tokens y self.historial_chat se quedan guardadas en el objeto para que el agente recuerde su estado.
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens = 100
        self.historial_chat: MemoriaAgente = []

    def _consumir_tokens(self, costo: int) -> None:
        """Descuenta tokens y lanza un error si el agente se queda sin energía."""
        self.tokens -= costo
        if self.tokens <= 0:
            raise RuntimeError(f"{self.nombre} se quedó sin tokens.")

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str) -> None:
        """Guarda un recuerdo de la acción ejecutada por el agente."""
        d_log: Recuerdo = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje,
        }
        self.historial_chat.append(d_log)

    def ping(self) -> str:
        """Responde al comando ping consumiendo pocos tokens."""
        self._consumir_tokens(20)
        return "pong!"

    def contar_letras(self, frase: str) -> str:
        """Cuenta vocales, consonantes y total de letras en una frase."""
        self._consumir_tokens(20)
        total_vocales = 0
        total_consonantes = 0

        for ch in frase.lower():
            if ch.isalpha():
                if ch in "aeiou":
                    total_vocales += 1
                else:
                    total_consonantes += 1

        total_letras = total_vocales + total_consonantes
        return (
            f"Frase: {frase}\n"
            f"Vocales: {total_vocales}\n"
            f"Consonantes: {total_consonantes}\n"
            f"Total de letras: {total_letras}"
        )

    def fecha_hoy(self, rol_actual: str) -> str:
        """Retorna la fecha actual solo si el usuario tiene rol admin."""
        self._consumir_tokens(20)
        if rol_actual != "admin":
            # Aquí lanzamos el error y ese error viaja al menú principal,
            # donde el except lo atrapa para mostrar una alerta elegante sin crashear.
            raise PermissionError("Privilegios insuficientes")
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def validar_password(self, nueva_password: str, usuario_actual: str) -> str:
        """Valida longitud mínima y evita que la contraseña sea igual al usuario."""
        self._consumir_tokens(20)
        if len(nueva_password) < 8:
            return "[Rechazada] Debe tener al menos 8 caracteres."
        if nueva_password.lower() == usuario_actual.lower():
            return "[Rechazada] La contrasena no puede ser igual al nombre de usuario."
        return "[OK] Contrasena valida."

    def calculadora(self, n1_txt: str, operador: str, n2_txt: str) -> str:
        """Ejecuta operaciones matemáticas básicas y retorna el resultado."""
        self._consumir_tokens(20)
        try:
            n1 = float(n1_txt)
            n2 = float(n2_txt)
        except ValueError as exc:
            raise ValueError("Debes ingresar valores numericos validos.") from exc

        if operador == "+":
            return f"Resultado: {n1 + n2}"
        if operador == "-":
            return f"Resultado: {n1 - n2}"
        if operador == "*":
            return f"Resultado: {n1 * n2}"
        if operador == "/":
            if n2 == 0:
                raise ZeroDivisionError("No se puede dividir entre cero.")
            return f"Resultado: {n1 / n2}"
        raise ValueError("Operador no valido.")

    def lanzar_dado(self) -> str:
        """Lanza un dado de 6 caras usando random.randint()."""
        self._consumir_tokens(20)
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"

    def gestionar_historial(self, accion: str) -> str:
        """Muestra, limpia o busca en el historial del agente usando su memoria interna."""
        accion_normalizada = accion.strip().lower()
        if accion_normalizada == "all":
            self._consumir_tokens(20)
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] El historial está vacío."
            salida = ["=== Historial Completo ==="]
            for i, registro in enumerate(self.historial_chat, 1):
                salida.append(f"\n[{i}] Timestamp: {registro['timestamp']}")
                salida.append(f"    Comando: {registro['cmd']}")
                salida.append(f"    Rol: {registro['rol']}")
                salida.append(f"    Descripción: {registro['descripcion']}")
            return "\n".join(salida)

        if accion_normalizada == "clear":
            self._consumir_tokens(20)
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        self._consumir_tokens(20)
        palabra_clave = accion_normalizada
        if len(self.historial_chat) == 0:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        coincidencias: MemoriaAgente = []
        for registro in self.historial_chat:
            # Para saber si una palabra está "dentro" de otra usamos el operador in,
            # y con lower() hacemos la búsqueda insensible a mayúsculas y minúsculas.
            if palabra_clave in registro["descripcion"].lower():
                coincidencias.append(registro)

        if len(coincidencias) == 0:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        salida = [
            f"=== Resultados de búsqueda para '{palabra_clave}' ===",
            f"Se encontraron {len(coincidencias)} coincidencia(s):",
        ]
        for i, registro in enumerate(coincidencias, 1):
            salida.append(f"\n[{i}] Autor: {registro['rol']}")
            salida.append(f"    Mensaje: {registro['descripcion']}")
            salida.append(f"    Timestamp: {registro['timestamp']}")
        return "\n".join(salida)


# Heredar evita copiar y pegar toda la clase porque solo cambiamos el comportamiento específico del administrador.
# Así reutilizamos la base común del agente y mantenemos el código más corto, limpio y fácil de modificar.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str):
        super().__init__(nombre)

    def gestionar_historial(self, accion: str) -> str:
        """Versión administrativa de historial: revisar no consume batería."""
        accion_normalizada = accion.strip().lower()
        if accion_normalizada == "all":
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] El historial está vacío."
            salida = ["=== Historial Completo ==="]
            for i, registro in enumerate(self.historial_chat, 1):
                salida.append(f"\n[{i}] Timestamp: {registro['timestamp']}")
                salida.append(f"    Comando: {registro['cmd']}")
                salida.append(f"    Rol: {registro['rol']}")
                salida.append(f"    Descripción: {registro['descripcion']}")
            return "\n".join(salida)

        if accion_normalizada == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        palabra_clave = accion_normalizada
        if len(self.historial_chat) == 0:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        coincidencias: MemoriaAgente = []
        for registro in self.historial_chat:
            if palabra_clave in registro["descripcion"].lower():
                coincidencias.append(registro)

        if len(coincidencias) == 0:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        salida = [
            f"=== Resultados de búsqueda para '{palabra_clave}' ===",
            f"Se encontraron {len(coincidencias)} coincidencia(s):",
        ]
        for i, registro in enumerate(coincidencias, 1):
            salida.append(f"\n[{i}] Autor: {registro['rol']}")
            salida.append(f"    Mensaje: {registro['descripcion']}")
            salida.append(f"    Timestamp: {registro['timestamp']}")
        return "\n".join(salida)
