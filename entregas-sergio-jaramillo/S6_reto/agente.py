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

    def __init__(self, nombre: str, energia: int = 100) -> None:
        # Una variable "normal" dentro de una función existe solo mientras esa función se ejecuta:
        # cuando la función termina, la variable desaparece. En cambio, una variable con `self.`
        # queda "pegada" al objeto y persiste todo el tiempo que el objeto exista. Por eso guardamos
        # el nombre, la energía y el historial como atributos de instancia: son el estado del agente
        # y deben sobrevivir entre llamadas a sus distintos métodos.
        # En este reto `energia` recibe el valor almacenado en la base de datos cuando el agente
        # se "despierta", de modo que su estado real persiste entre reinicios del servidor.
        self.nombre = nombre
        self.energia = energia
        self.historial_chat: MemoriaAgente = []

    def consumir_energia(self, cantidad: int) -> int:
        """
        Descuenta energía del agente y retorna el nivel resultante.
        La energía nunca baja de 0.

        Parámetros:
            cantidad (int): Cantidad de energía a consumir.

        Retorna:
            int: Nivel de energía tras el descuento.
        """
        # El descuento se hace sobre self.energia para que el resultado sea persistible en la DB.
        self.energia -= cantidad
        if self.energia < 0:
            self.energia = 0
        return self.energia

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
        """Responde con 'pong!' para verificar que el agente está activo."""
        self.energia -= 2
        return "pong!"

    def lanzar_dado(self) -> str:
        """Lanza un dado virtual y devuelve un número aleatorio entre 1 y 6."""
        self.energia -= 1
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

    def __init__(self, nombre: str, energia: int = 100) -> None:
        # super().__init__() llama al constructor de PseudoAgente para inicializar los atributos
        # comunes (nombre, energia, historial_chat). Así no repetimos esa lógica aquí.
        super().__init__(nombre, energia)

    def consumir_energia(self, cantidad: int) -> int:
        """
        El AgenteAdmin completa misiones con un descuento reducido (50% del costo normal).
        Sobreescribe el método del padre para darle ventaja operativa al administrador.

        Parámetros:
            cantidad (int): Energía base requerida por la misión.

        Retorna:
            int: Nivel de energía tras el descuento reducido.
        """
        # El admin descuenta solo la mitad de la energía requerida.
        # Esto ilustra cómo la herencia permite que dos clases respondan diferente
        # al mismo mensaje (consumir_energia) sin cambiar el código que las llama.
        costo_real = max(1, cantidad // 2)
        self.energia -= costo_real
        if self.energia < 0:
            self.energia = 0
        return self.energia

## Creado por: Sergio Jaramillo (SergiJaramilloL)
