## Creado por: Sergio Jaramillo (SergiJaramilloL)
from datetime import datetime
from typing import Dict, List
import random

# =====================
# CONTRATO DE MEMORIA (Type Aliasing)
# =====================
# Al trabajar con modelos de IA, las funciones que actúan como "herramientas" (tools)
# deben comunicar claramente qué tipo de datos aceptan y retornan. Si en cada función
# escribimos `list` a secas, quien lea el código no sabe qué hay dentro de esa lista.
# Al crear un alias como `MemoriaAgente`, le damos un nombre semántico a la estructura:
# cualquier función que reciba una `MemoriaAgente` sabe exactamente que está trabajando
# con una lista de diccionarios {str: str}, igual a cómo un modelo de IA necesita un
# esquema claro para poder procesar su contexto o historial de conversación.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


# =====================
# CLASE: PseudoAgente
# =====================
class PseudoAgente:

    def __init__(self, nombre: str) -> None:
        # Una variable "normal" dentro de una función existe solo mientras esa función se ejecuta:
        # cuando la función termina, la variable desaparece. En cambio, una variable con `self.`
        # queda "pegada" al objeto y persiste todo el tiempo que el objeto exista. Por eso guardamos
        # el nombre, los tokens y el historial como atributos de instancia: son el estado del agente
        # y deben sobrevivir entre llamadas a sus distintos métodos.
        self.nombre = nombre
        self.tokens = 100
        self.historial_chat: MemoriaAgente = []

    # =====================
    # MÉTODO: registrar_log
    # =====================
    def registrar_log(self, cmd: str, rol: str, descripcion: str) -> None:
        """
        Agrega una entrada al historial interno del agente.

        Parámetros:
            cmd (str): El comando que se ejecutó.
            rol (str): El rol del usuario que lo ejecutó.
            descripcion (str): Descripción breve del resultado del comando.
        """
        # Se crea el diccionario de log y se agrega al historial del agente usando self.historial_chat.
        d_log: Recuerdo = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol,
            "descripcion": descripcion
        }
        self.historial_chat.append(d_log)

    # =====================
    # HERRAMIENTAS (TOOLS)
    # =====================

    def ping(self) -> str:
        """
        Responde con 'pong!' para verificar que el agente está activo.

        Retorna:
            str: Confirmación de actividad del agente.
        """
        # Consumo: operación simple, bajo costo de batería.
        self.tokens -= 2
        return "pong!"

    def contar_letras(self, palabra: str) -> str:
        """
        Cuenta las vocales, consonantes y el total de letras en una palabra o frase.

        Parámetros:
            palabra (str): La palabra o frase ingresada por el usuario (ya en minúsculas).

        Retorna:
            str: Texto con el resumen del conteo de vocales, consonantes y total.
        """
        # Consumo: requiere procesar cada carácter, costo moderado.
        self.tokens -= 3
        tot_letras = len(palabra)
        tot_vocales = 0
        tot_cons = 0
        for letra in palabra:
            if letra in "aeiou":
                tot_vocales += 1
            # Se usa isalpha() para contar solo letras reales como consonantes,
            # evitando que espacios o símbolos se cuenten como consonantes.
            elif letra.isalpha():
                tot_cons += 1
        return (
            f"Palabra ingresada: {palabra}\n"
            f"Total de vocales: {tot_vocales}\n"
            f"Total de consonantes: {tot_cons}\n"
            f"Total de letras: {tot_letras}"
        )

    def calculadora(self, num1: float, operador: str, num2: float) -> str:
        """
        Realiza una operación matemática básica entre dos números.

        Parámetros:
            num1 (float): El primer número de la operación.
            operador (str): El operador aritmético a aplicar (+, -, *, /).
            num2 (float): El segundo número de la operación.

        Retorna:
            str: Texto con el resultado de la operación, o mensaje de error si no es válida.
        """
        # Consumo: operación aritmética con validación, costo moderado-alto.
        self.tokens -= 4
        if operador == "+":
            resultado = num1 + num2
            return f"Resultado: {num1} + {num2} = {resultado}"
        elif operador == "-":
            resultado = num1 - num2
            return f"Resultado: {num1} - {num2} = {resultado}"
        elif operador == "*":
            resultado = num1 * num2
            return f"Resultado: {num1} * {num2} = {resultado}"
        elif operador == "/":
            # Condición anidada dentro del operador "/" para verificar que el segundo número no sea cero.
            if num2 == 0:
                return "[Error] No se puede dividir entre cero."
            resultado = num1 / num2
            return f"Resultado: {num1} / {num2} = {resultado}"
        # Si el operador no es reconocido, se retorna un mensaje de error indicando los operadores válidos.
        else:
            return f"[Error] Operador '{operador}' no reconocido. Usa +, -, * o /."

    def validar_password(self, password: str, usuario: str) -> str:
        """
        Verifica si una contraseña propuesta cumple con los requisitos mínimos de seguridad.

        Parámetros:
            password (str): La contraseña propuesta por el usuario.
            usuario (str): El nombre del usuario activo, para comparación de igualdad.

        Retorna:
            str: Mensaje indicando si la contraseña fue aceptada o el motivo de rechazo.
        """
        # Consumo: validación de reglas sobre el texto ingresado, costo moderado.
        self.tokens -= 3
        # Condición 1: la contraseña debe tener al menos 8 caracteres.
        if len(password) < 8:
            return "[Rechazada] La contraseña debe tener al menos 8 caracteres."
        # Condición 2: la contraseña no puede ser igual al nombre de usuario.
        elif password == usuario:
            return "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
        else:
            return "[Aceptada] Contraseña válida."

    def fecha_hoy(self, rol: str) -> str:
        """
        Retorna la fecha y hora actual del sistema. Restringido al rol de administrador.

        Parámetros:
            rol (str): El rol del usuario activo ("admin" o "invitado").

        Retorna:
            str: Texto con la fecha y hora actual formateada.

        Lanza:
            PermissionError: Si el usuario tiene rol "invitado" (sin privilegios de admin).
        """
        # Consumo: consulta al sistema operativo, costo alto.
        self.tokens -= 5
        # RAISE: El viaje del error desde que se lanza hasta que se atrapa.
        # Cuando un usuario con rol "invitado" llama a este método, `raise` lanza un PermissionError
        # hacia arriba en la pila de llamadas. Como este método no tiene ningún try/except propio,
        # Python sube un nivel y busca quién lo invocó: en este caso, el bucle principal (while).
        # Allí, el bloque `except PermissionError` lo atrapa, imprime el aviso bonito en consola
        # y el programa continúa sin crashear.
        if rol != "admin":
            raise PermissionError("Privilegios insuficientes")
        ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"[Sistema] Fecha y hora actual: {ahora}"

    def gestionar_historial(self, accion: str) -> str:
        """
        Administra el historial de comandos del agente usando su memoria interna.

        Parámetros:
            accion (str): Puede ser "all" para ver todo, "clear" para borrar,
                          o cualquier otro texto para buscar por palabra clave.

        Retorna:
            str: Texto formateado con el resultado de la acción solicitada.
        """
        # Consumo: acceso y procesamiento del historial completo, costo alto.
        self.tokens -= 5

        # HISTORIAL ALL
        # Si la acción es "all", se arma el texto con todas las entradas del historial.
        if accion == "all":
            if len(self.historial_chat) == 0:
                return "[Sistema] El historial está vacío."
            lineas = [f"\n[Sistema] Historial completo ({len(self.historial_chat)} entradas):"]
            for i, entrada in enumerate(self.historial_chat):
                lineas.append(
                    f"  {i + 1}. [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
                )
            return "\n".join(lineas)

        # HISTORIAL CLEAR
        # Si la acción es "clear", se vacía la lista en memoria y se confirma la acción.
        elif accion == "clear":
            self.historial_chat.clear()
            return "[Sistema] Historial eliminado correctamente."

        # HISTORIAL BÚSQUEDA
        # Si la acción no es ni "all" ni "clear", se trata como término de búsqueda por palabra clave.
        else:
            clave = accion
            coincidencias = []
            # Se itera sobre cada entrada del historial para buscar la palabra clave dentro de su descripción.
            for entrada in self.historial_chat:
                # Para verificar si una palabra está dentro de un texto en Python se usa el operador "in".
                # Ejemplo: "arroz" in "Cocinar Arroz" → False, pero si aplicamos .lower() a ambos lados:
                # "arroz" in "cocinar arroz" → True. Esto hace que la búsqueda sea insensible a mayúsculas.
                if clave.lower() in entrada["descripcion"].lower():
                    coincidencias.append(
                        f"  [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
                    )
            if len(coincidencias) == 0:
                return f"[PseudoAgente] No encontré registros que coincidan con '{clave}'."
            return "\n".join(coincidencias) + f"\n\n[Sistema] Se encontraron {len(coincidencias)} coincidencia(s) para '{clave}'."

    def lanzar_dado(self) -> str:
        """
        Lanza un dado virtual y devuelve un número aleatorio entre 1 y 6.

        Retorna:
            str: Texto con el resultado del lanzamiento.
        """
        # Consumo: operación muy simple, mínimo costo de batería.
        self.tokens -= 1
        numero = random.randint(1, 6)
        return f"[Dado] Lanzaste el dado y salió: {numero}"


# =====================
# CLASE: AgenteAdmin (hereda de PseudoAgente)
# =====================
# Heredar de PseudoAgente es mejor que copiar y pegar todo el código en una clase nueva
# porque cualquier corrección o mejora que hagamos en PseudoAgente se refleja automáticamente
# en AgenteAdmin. Con copy-paste tendríamos dos versiones del mismo código que se desincronizarían
# con el tiempo: si arreglamos un bug en una, la otra sigue rota hasta que alguien lo recuerde.
class AgenteAdmin(PseudoAgente):

    def __init__(self, nombre: str) -> None:
        # super().__init__() llama al constructor de PseudoAgente para inicializar los atributos
        # comunes (nombre, tokens, historial_chat). Así no repetimos esa lógica aquí.
        super().__init__(nombre)

    def gestionar_historial(self, accion: str) -> str:
        """
        Administra el historial de comandos del agente sin consumir batería.
        Sobreescribe el método del padre para que el admin revise su historial gratis.

        Parámetros:
            accion (str): Puede ser "all" para ver todo, "clear" para borrar,
                          o cualquier otro texto para buscar por palabra clave.

        Retorna:
            str: Texto formateado con el resultado de la acción solicitada.
        """
        # Para el AgenteAdmin, revisar el historial es una operación administrativa
        # que no consume batería. Se omite el descuento de tokens y se ejecuta la lógica directamente.
        if accion == "all":
            if len(self.historial_chat) == 0:
                return "[Sistema] El historial está vacío."
            lineas = [f"\n[Sistema] Historial completo ({len(self.historial_chat)} entradas):"]
            for i, entrada in enumerate(self.historial_chat):
                lineas.append(
                    f"  {i + 1}. [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
                )
            return "\n".join(lineas)
        elif accion == "clear":
            self.historial_chat.clear()
            return "[Sistema] Historial eliminado correctamente."
        else:
            clave = accion
            coincidencias = []
            for entrada in self.historial_chat:
                if clave.lower() in entrada["descripcion"].lower():
                    coincidencias.append(
                        f"  [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
                    )
            if len(coincidencias) == 0:
                return f"[PseudoAgente] No encontré registros que coincidan con '{clave}'."
            return "\n".join(coincidencias) + f"\n\n[Sistema] Se encontraron {len(coincidencias)} coincidencia(s) para '{clave}'."

## Creado por: Sergio Jaramillo (SergiJaramilloL)
