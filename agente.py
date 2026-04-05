import datetime
import random
from typing import Dict, List

# ALIAS DE TIPOS
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]

# CLASE BASE

class PseudoAgente:
    # AUDITORÍA: Una variable temporal (como una declarada directamente dentro de una función) 
    # desaparece de la memoria en cuanto la función termina de ejecutarse. 
    # En cambio, una variable con 'self.' es un Atributo de Instancia: pertenece al objeto 
    # y su valor "vive" y se mantiene en el tiempo, permitiendo que todos los métodos del objeto 
    # accedan a él y lo modifiquen durante todo el ciclo de vida del programa.
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens = 100
        self.historial_chat: MemoriaAgente = []

    def _consumir_bateria(self, costo: int):
        """Método interno para gestionar la batería. Lanza error si se agota."""
        self.tokens -= costo
        if self.tokens <= 0:
            self.tokens = 0
            raise SystemError(f"[{self.nombre}] Batería agotada. El agente ha muerto de cansancio.")

    def tool_ping_pong(self, comando: str) -> str:
        self._consumir_bateria(2)
        return "pong" if comando == "ping" else "ping!"

    def tool_contar(self, palabra: str) -> str:
        self._consumir_bateria(5)
        vocales_validas = "aeiouáéíóú"
        v = sum(1 for letra in palabra if letra.isalpha() and letra in vocales_validas)
        c = sum(1 for letra in palabra if letra.isalpha() and letra not in vocales_validas)
        return f"La palabra '{palabra}' tiene {v} vocales y {c} consonantes."

    def tool_fecha_hoy(self, rol_usuario: str) -> str:
        self._consumir_bateria(3)
        if rol_usuario != "administrador":
            raise PermissionError("Privilegios insuficientes: Solo el administrador puede ver la fecha.")
        hoy = datetime.datetime.now()
        return f"Fecha actual: {hoy.strftime('%Y-%m-%d %H:%M:%S')}"

    def tool_validar_password(self, password: str, usuario: str) -> str:
        self._consumir_bateria(4)
        if len(password) < 8:
            return "Error: La contraseña debe tener al menos 8 caracteres."
        if password == usuario:
            return "Error: La contraseña no puede ser igual al usuario."
        return "Contraseña válida y segura."

    def tool_calculadora(self, num1: float, operador: str, num2: float) -> str:
        self._consumir_bateria(5)
        if operador == "+": return f"Resultado: {num1 + num2}"
        elif operador == "-": return f"Resultado: {num1 - num2}"
        elif operador == "*": return f"Resultado: {num1 * num2}"
        elif operador == "/":
            if num2 == 0:
                raise ZeroDivisionError("No se puede dividir por cero.")
            return f"Resultado: {num1 / num2}"
        else:
            raise ValueError(f"Operador '{operador}' no reconocido.")

    def tool_lanzar_dado(self) -> str:
        """Nueva herramienta que consume poca batería."""
        self._consumir_bateria(1)
        resultado = random.randint(1, 6)
        return f"Has lanzado un dado. El resultado es: {resultado}"

    def tool_gestionar_historial(self, accion: str, filtro: str = "") -> str:
        """Gestiona el historial consumiendo batería y usando self.historial_chat."""
        self._consumir_bateria(10) # Revisar la memoria es costoso
        
        if accion == "all":
            if not self.historial_chat: return "El historial está vacío."
            return "\n".join([f"[{r['timestamp']}] {r['rol']}: {r['descripcion']}" for r in self.historial_chat])
        
        elif accion == "clear":
            self.historial_chat.clear()
            return "Historial actual limpiado."
        
        elif accion == "search":
            if not filtro: return "Debe ingresar una palabra para buscar."
            res = [r for r in self.historial_chat if filtro.lower() in r["descripcion"].lower()]
            if not res: return f"No encontré registros con: '{filtro}'"
            return "\n".join([f"-> {r['descripcion']}" for r in res])
        
        return "Acción de historial no reconocida."

# RETO EUTAGÓGICO: HERENCIA

# AUDITORÍA: Usar herencia es mejor que copiar y pegar el código porque nos permite aplicar 
# el principio DRY (Don't Repeat Yourself). Al heredar, AgenteAdmin obtiene automáticamente todas las 
# funciones de PseudoAgente, y solo necesitamos reescribir lo que cambia (en este caso, el historial).
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str):
        # super().__init__() llama al constructor de la clase padre para inicializar nombre, tokens e historial
        super().__init__(nombre)

    def tool_gestionar_historial(self, accion: str, filtro: str = "") -> str:
        """Versión PRO: No consume batería para revisar el historial."""
        # Se omitió self._consumir_bateria(10)
        
        if accion == "all":
            if not self.historial_chat: return "El historial está vacío."
            return "\n".join([f"[{r['timestamp']}] {r['rol']}: {r['descripcion']}" for r in self.historial_chat])
        elif accion == "clear":
            self.historial_chat.clear()
            return "Historial actual limpiado."
        elif accion == "search":
            if not filtro: return "Debe ingresar una palabra para buscar."
            res = [r for r in self.historial_chat if filtro.lower() in r["descripcion"].lower()]
            return "\n".join([f"-> {r['descripcion']}" for r in res]) if res else "Sin coincidencias."
        return "Acción no reconocida."