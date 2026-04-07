import datetime
import random
from typing import Dict, List

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


class PseudoAgente:

    # Esta variable con self pertenece al objeto y vive durante toda su existencia,
    # mientras que una variable normal dentro de una función desaparece al terminar.
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens = 100
        self.historial_chat: MemoriaAgente = []

    def consumir_tokens(self, cantidad: int) -> bool:
        if self.tokens <= 0:
            return False
        self.tokens -= cantidad
        return True

    def registrar_evento(self, cmd: str, descripcion: str) -> None:
        self.historial_chat.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cmd": cmd,
            "rol": self.nombre,
            "descripcion": descripcion
        })

    def ping(self):
        if not self.consumir_tokens(5):
            return "Agente sin energía"
        self.registrar_evento("ping", "Se envió un ping")
        return "pong"

    def fecha_hoy(self):
        if not self.consumir_tokens(15):
            return "Agente sin energía"

        if self.nombre == "invitado":
            raise PermissionError("Acceso denegado")

        fecha_actual = datetime.datetime.now()
        resultado = fecha_actual.strftime('%d/%m/%Y %H:%M:%S')
        self.registrar_evento("fecha_hoy", resultado)
        return resultado

    def contar_letras(self, palabra: str):
        if not self.consumir_tokens(15):
            return "Agente sin energía"

        total_vocales = sum(1 for p in palabra if p in "aeiou")
        total_consonantes = sum(1 for p in palabra if p in "bcdfghjklmnpqrstvwxyz")

        resultado = (f"{len(palabra)} caracteres, "
                     f"{total_vocales} vocales, "
                     f"{total_consonantes} consonantes")

        self.registrar_evento("contar", resultado)
        return resultado

    def calculadora(self, num1, num2, operador):
        if not self.consumir_tokens(15):
            return "Agente sin energía"

        try:
            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            elif operador == "/":
                if num2 == 0:
                    raise ZeroDivisionError("No se puede dividir por cero.")
                resultado = num1 / num2
            else:
                raise ValueError("Operador no válido. Usa: +, -, *, /")

            self.registrar_evento("calculadora", str(resultado))
            return resultado

        except ZeroDivisionError as e:
            self.registrar_evento("calculadora", str(e))
            return str(e)

        except ValueError as e:
            self.registrar_evento("calculadora", str(e))
            return str(e)

    def validar_pass(self, nueva_pass: str):
        if not self.consumir_tokens(10):
            return "Agente sin energía"

        if len(nueva_pass) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        elif nueva_pass == self.nombre:
            return "La contraseña no puede ser igual a tu nombre de usuario."
        else:
            return "Su contraseña cumple con los criterios."

    def lanzar_dado(self):
        if not self.consumir_tokens(10):
            return "Agente sin energía"

        numero = random.randint(1, 6)
        self.registrar_evento("dado", str(numero))
        return numero

    def gestionar_historial(self, accion="ver", palabra_clave=""):
        if accion == "ver":
            if not self.consumir_tokens(15):
                return "Agente sin energía"
            return self.historial_chat

        elif accion == "limpiar":
            if not self.consumir_tokens(5):
                return "Agente sin energía"
            self.historial_chat.clear()
            return "Historial eliminado"

        elif accion == "buscar":
            if not self.consumir_tokens(20):
                return "Agente sin energía"

            resultados = []
            contador = 0

            for item in self.historial_chat:
                descripcion = item.get("descripcion", "").lower()

                if palabra_clave.lower() in descripcion:
                    contador += 1
                    resultados.append(
                        f"[{item.get('rol', 'desconocido')}] {item.get('descripcion', '')}"
                    )

            if contador == 0:
                return "No encontré coincidencias"
            else:
                return "\n".join(resultados) + f"\nTotal: {contador}"

        else:
            return "Acción no válida"


# Heredar evita duplicar código,
# y me permite modificar lo necesario sin copiar y pegar funciones.
class AgenteAdmin(PseudoAgente):

    def __init__(self, nombre: str):
        super().__init__(nombre)

    def gestionar_historial(self, accion="ver", palabra_clave=""):

        if accion == "ver":
            return self.historial_chat

        elif accion == "limpiar":
            self.historial_chat.clear()
            return "Historial eliminado (admin)"

        elif accion == "buscar":

            resultados = []
            contador = 0

            for item in self.historial_chat:
                descripcion = item.get("descripcion", "").lower()

                if palabra_clave.lower() in descripcion:
                    contador += 1
                    resultados.append(
                        f"[{item.get('rol', 'desconocido')}] {item.get('descripcion', '')}"
                    )

            if contador == 0:
                return "No encontré coincidencias"
            else:
                return "\n".join(resultados) + f"\nTotal: {contador}"

        else:
            return "Acción no válida"