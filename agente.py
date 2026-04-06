# ===========================================================
# Taller Semana 4: Nace la Entidad (POO y Modularización)
# Agente
# César Orlando Ríos Quiroga
# ===========================================================

import datetime
import random

# --- ALIAS DE TIPOS ---
# Un Alias lo damos a una estructura de datos compleja.
# La 'MemoriaAgente' será una lista que contiene esos diccionarios.
type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]

# --- CLASE BASE: PSEUDOAGENTE (El molde principal) ---
class PseudoAgente:
    # El método __init__ es donde "nace" el agente. 
    # decimos que una variable normal en una función es temporal y se borra al terminar.
    # Una variable que empieza con 'self.' es un ATRIBUTO: es información que el agente
    # guarda permanente y puede usar en cualquier momento de su vida.
    def __init__(self, nombre: str = "Athena"):
        self.nombre = nombre        # Atributo: El nombre que identifica al agente
        self.tokens = 100           # Atributo: El numero de Tokens disponibles inicalmente (recurso limitado)
        self.historial_chat: MemoriaAgente = [] # Atributo: Su memoria interna privada

    # MÉTODO DE REGISTRAR LOG
    # Esta función sirve para que el agente anote cada cosa que hace en su memoria.
    def registrar_log(self, comando: str, rol: str, mensaje: str):
        # Creamos un diccionario con los datos de la acción actual
        nuevo_log: Recuerdo = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol,
            "descripcion": mensaje
        }
        # Añadimos este registro a la lista "historial_chat"
        self.historial_chat.append(nuevo_log)

    # --- HERRAMIENTAS DEL AGENTE ---

    # Gestión de Historial, se le pasa la lista de memoria como parámetro externo.
    # El agente usa 'self.historial_chat' que ya tiene guardado.
    def gestionar_historial(self, op: str, rol: str):
        # El agente gasta 30 Tokens por el esfuerzo de recordar
        self.tokens -= 30 
        
        # Decisión lógica según lo que pidió el usuario
        if op == "all":
            # Si escribe "all", se muenstra toda la lista de la memoria
            self.registrar_log("historial all", rol, "Consulta de memoria completa")
            return self.historial_chat 
        elif op == "clear":
            # Si el usario escribe "clear", usamos el método .clear() para vaciar su memoria
            self.historial_chat.clear() 
            self.registrar_log("historial clear", rol, "Reseteo de memoria realizado")
            return f"[{self.nombre}] Memoria borrada con éxito."
        
        return "Opción de historial no válida."

    # Conteo de letras
    def contar_letras(self, palabra: str, rol: str):
        # Consume 10 Tokens
        self.tokens -= 10
        # Se Usa la función len() para contar el total de caracteres
        total = len(palabra)
        # Se usa un ciclo interno para contar vocales
        vocales = sum(1 for letra in palabra.lower() if letra in "aeiou")
        
        mensaje = f"Análisis de '{palabra}': {total} letras y {vocales} vocales."
        self.registrar_log("contar", rol, mensaje)
        return mensaje

    # Calculadora
    def ejecutar_calculo(self, operacion: str, n1: float, n2: float, rol: str):
        # Se gastan 15 tokens
        self.tokens -= 15 
        
        # Estructura de decisión para elegir la operación correcta
        if operacion == "+": resultado = n1 + n2
        elif operacion == "-": resultado = n1 - n2
        elif operacion == "*": resultado = n1 * n2
        elif operacion == "/":
            # Lógica de blindaje: Evitamos que el programa falle si se divide por 0
            if n2 == 0:
                mensaje = "Error: Intento de división por cero detectado."
                self.registrar_log("calculadora", rol, mensaje)
                return mensaje
            resultado = n1 / n2
        else:
            return "Operación matemática no reconocida."
        
        # Guardamos el resultado exitoso
        mensaje = f"Cálculo: {n1} {operacion} {n2} = {resultado}"
        self.registrar_log("calculadora", rol, mensaje)
        return mensaje

    # Lanzar Dado
    def lanzar_dado(self, rol: str):
        # Se gastan 5 Tokens
        self.tokens -= 5
        # Se usa random.randint para obtener un número entre 1 y 6
        resultado = random.randint(1, 6)
        mensaje = f"Lanzamiento de dado: cayó en {resultado}"
        self.registrar_log("dado", rol, mensaje)
        return mensaje

    # Validación de Password
    def validar_pass(self, password: str, rol: str):
        # Se gastan 5 Tokens 
        self.tokens -= 5
        
        # Evaluamos múltiples condiciones de seguridad
        largo_ok = len(password) >= 8
        tiene_mayus = any(c.isupper() for c in password)
        tiene_minus = any(c.islower() for c in password)
        tiene_num = any(c.isdigit() for c in password)
        
        # Decisión final basada en todos los requisitos
        if largo_ok and tiene_mayus and tiene_minus and tiene_num:
            mensaje = "Resultado: Contraseña SEGURA"
        else:
            # Si algo falla, damos la sugerencia exacta pedida en el taller
            mensaje = "Resultado: Contraseña DÉBIL\nSugerencia: Use 8+ caracteres, números y mayúsculas."
        
        self.registrar_log("validar_pass", rol, mensaje)
        return mensaje

# --- ESPECIALIZACIÓN POR HERENCIA ---

class AgenteAdmin(PseudoAgente):
    
    def __init__(self, nombre: str = "Athena-Admin"):
        # La función super() inicializa los atributos básicos (tokens, nombre) del padre
        super().__init__(nombre)

    # SOBRESCRITURA (Override):
    # El Administrador puede ver la memoria sin gastar Tokens.
    def gestionar_historial(self, op: str, rol: str):
        # Guardamos cuánta energía tiene antes de empezar
        tokens_antes = self.tokens 
        # Ejecutamos la lógica normal de ver el historial que tiene el padre
        resultado = super().gestionar_historial(op, rol)
        # Restauramos la energía (así el costo final es 0 para el Admin)
        self.tokens = tokens_antes 
        return f"[MODO ADMIN] {resultado}"