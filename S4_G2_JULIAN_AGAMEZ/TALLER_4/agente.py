"""
agente.py — Módulo del PseudoAgente para el Taller Semana 4

Contiene:
  - Alias de tipos (MemoriaAgente, Historial)
  - Clase PseudoAgente  (agente base)
  - Clase AgenteAdmin   (agente especializado por herencia)
  - Función login()

Uso desde main.py:
    from agente import PseudoAgente, AgenteAdmin, login
"""

import datetime
import random

# ---------------------------------------------------------------------------
# Type Aliases — Contratos de memoria del agente
# ---------------------------------------------------------------------------
type Historial = dict[str, str]
type MemoriaAgente = list[Historial]


# ---------------------------------------------------------------------------
# Clase PseudoAgente
# ---------------------------------------------------------------------------
class PseudoAgente:
    # Una variable definida con 'self.' (atributo de instancia) vive mientras exista el
    # objeto: se crea en __init__ y persiste entre llamadas a métodos. Una variable temporal
    # dentro de una función sólo existe mientras esa función se ejecuta; al retornar, Python
    # la destruye y su valor se pierde para siempre.
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens: int = 100
        self.historial_chat: MemoriaAgente = []

    # ------------------------------------------------------------------
    # Método auxiliar: marca cada acción en el historial con timestamp
    # ------------------------------------------------------------------
    def registrar_log(self, comando: str, rol: str, mensaje: str) -> None:
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol,
            "descripcion": mensaje,
        }
        self.historial_chat.append(d_log)

    # ------------------------------------------------------------------
    # ping: -2 tokens
    # ------------------------------------------------------------------
    def ping(self, rol: str) -> str:
        self.tokens -= 2
        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
        self.registrar_log("ping", rol, mensaje)
        return "pong!"

    # ------------------------------------------------------------------
    # gestionar_historial: -5 tokens (ver / borrar)
    # ------------------------------------------------------------------
    def gestionar_historial(self, op: str, rol: str) -> str:
        self.tokens -= 5
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist all", rol, mensaje)
            if not self.historial_chat:
                return f"[{self.nombre}] El historial está vacío."
            lineas = [f"[{self.nombre}] Historial completo ({len(self.historial_chat)} registro(s)):"]
            for e in self.historial_chat:
                lineas.append(f"  [{e['timestamp']}] ({e['rol']}) {e['cmd']}: {e['descripcion']}")
            return "\n".join(lineas)

        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return f"[{self.nombre}] Historial eliminado exitosamente."

        return f"[{self.nombre}] Operación '{op}' no válida. Usa: historial all | historial clear"

    # ------------------------------------------------------------------
    # contar_letras: -3 tokens
    # ------------------------------------------------------------------
    def contar_letras(self, frase: str, rol: str) -> str:
        self.tokens -= 3
        tot_vocales = sum(1 for c in frase if c.lower() in "aeiouáéíóú")
        tot_cons = sum(1 for c in frase if c.isalpha() and c.lower() not in "aeiouáéíóú")
        mensaje = f"Conteo de '{frase}': vocales={tot_vocales}, consonantes={tot_cons}"
        self.registrar_log("contar", rol, mensaje)
        return (
            f"Frase analizada: '{frase}'\n"
            f"  Vocales:      {tot_vocales}\n"
            f"  Consonantes:  {tot_cons}\n"
            f"  Total letras: {tot_vocales + tot_cons}"
        )

    # ------------------------------------------------------------------
    # calculadora: -5 tokens
    # ------------------------------------------------------------------
    def calculadora(self, num1: float, operador: str, num2: float, rol: str) -> str:
        self.tokens -= 5
        if operador == "+":
            resultado = num1 + num2
        elif operador == "-":
            resultado = num1 - num2
        elif operador == "*":
            resultado = num1 * num2
        elif operador == "/":
            if num2 == 0:
                raise ZeroDivisionError("No es posible dividir entre cero.")
            resultado = num1 / num2
        else:
            raise ValueError(f"Operador '{operador}' no reconocido. Usa +, -, * o /.")

        display = int(resultado) if resultado == int(resultado) else resultado
        mensaje = f"Operación: {num1} {operador} {num2} = {display}"
        self.registrar_log("calculadora", rol, mensaje)
        return f"Resultado: {num1} {operador} {num2} = {display}"

    # ------------------------------------------------------------------
    # fecha_hoy: -5 tokens (solo admin)
    # ------------------------------------------------------------------
    def fecha_hoy(self, rol: str) -> str:
        if rol == "invitado":
            raise PermissionError("Este comando requiere privilegios de administrador.")
        self.tokens -= 5
        hoy = datetime.date.today()
        mensaje = f"Se solicitó la fecha actual: {hoy.strftime('%d/%m/%Y')}."
        self.registrar_log("fecha_hoy", rol, mensaje)
        return f"Fecha actual: {hoy.strftime('%d/%m/%Y')}"

    # ------------------------------------------------------------------
    # validar_password: -3 tokens
    # ------------------------------------------------------------------
    def validar_password(self, propuesta: str, nombre_usuario: str, rol: str) -> str:
        self.tokens -= 3
        if len(propuesta) < 8:
            resultado = "[Rechazada] La contraseña debe tener al menos 8 caracteres."
        elif propuesta == nombre_usuario:
            resultado = "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
        else:
            resultado = "[Aceptada] Contraseña válida."
        self.registrar_log("validar_pass", rol, f"Validación de contraseña. Resultado: {resultado}")
        return resultado

    # ------------------------------------------------------------------
    # lanzar_dado: -1 token (usa módulo random)
    # ------------------------------------------------------------------
    def lanzar_dado(self, rol: str) -> str:
        self.tokens -= 1
        numero = random.randint(1, 6)
        mensaje = f"Se lanzó el dado y salió: {numero}"
        self.registrar_log("dado", rol, mensaje)
        return f"[{self.nombre}] Resultado del dado: {numero}"


# ---------------------------------------------------------------------------
# Clase AgenteAdmin — Hereda de PseudoAgente
# ---------------------------------------------------------------------------
# Heredar de PseudoAgente es mejor que copiar y pegar el código en una clase nueva
# porque cualquier corrección o mejora hecha en PseudoAgente se propaga
# automáticamente a AgenteAdmin, evitando duplicación y posibles inconsistencias.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str):
        # super().__init__ delega la inicialización al constructor del padre,
        # evitando repetir la lógica de self.tokens, self.historial_chat, etc.
        super().__init__(nombre)

    # Override: gestionar_historial SIN consumo de tokens para el administrador
    def gestionar_historial(self, op: str, rol: str) -> str:
        # El administrador no paga tokens por revisar o limpiar el historial
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado (sin costo - Admin)"
            self.registrar_log("hist all", rol, mensaje)
            if not self.historial_chat:
                return f"[{self.nombre}] El historial está vacío."
            lineas = [f"[{self.nombre}] Historial completo ({len(self.historial_chat)} registro(s)):"]
            for e in self.historial_chat:
                lineas.append(f"  [{e['timestamp']}] ({e['rol']}) {e['cmd']}: {e['descripcion']}")
            return "\n".join(lineas)

        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado (sin costo - Admin)"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return f"[{self.nombre}] Historial eliminado exitosamente."

        return f"[{self.nombre}] Operación '{op}' no válida. Usa: historial all | historial clear"


# ---------------------------------------------------------------------------
# Función login
# ---------------------------------------------------------------------------
def login(user: str, passwrd: str) -> dict:
    if user == "admin" and passwrd == "admin123":
        return {
            "rol": user,
            "access": True,
            "descripcion": "[Sistema] Acceso concedido. Privilegios de Administrador activados.",
        }
    if user == "invitado" and passwrd == "1234":
        return {
            "rol": user,
            "access": True,
            "descripcion": "[Sistema] Acceso concedido. Modo Invitado.",
        }
    return {
        "rol": "",
        "access": False,
        "descripcion": "[Sistema] Credenciales incorrectas.",
    }
