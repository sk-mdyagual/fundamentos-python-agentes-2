import datetime
import random
from typing import Dict, List


"""Alias de Tipos: Sirven para ponerle un nombre único a una estructura de datos (como una lista de diccionarios), 
haciendo que el código sea más fácil de leer y documentar. 
Esto ayuda a la IA porque le define reglas exactas sobre qué datos debe procesar previniendo errores o confusiones."""

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


class PseudoAgente:

    def __init__(self):
        self.historial_chat: MemoriaAgente = []
        self.tokens = 100

    def gestionarHistorial(self, accion: str) -> str:
        """
            Ejecuta cada acción elegida por el usuario y devuelve un mensaje con la respuesta.
        """
        self.tokens -= 5

        if accion == "historial":
            pal = input("Ingrese palabra clave para la busqueda: ").lower()
            resultado = []
            
            for i in self.historial_chat:
                if pal in i["descripcion"].lower():
                    resultado.append(i)
            
            if len(resultado) == 0:
                return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
            else:
                return f"Total de registros: {len(resultado)} | Detalle: {resultado}"

        elif accion == "historial all":
            return f"El historial es: {self.historial_chat}"

        elif accion == "historial clear":
            self.historial_chat.clear() 
            return "Se ha eliminado el historial correctamente."

        elif accion == "salir":
            return "salir" 

        else:
            return "No eligió una opción válida."


    def contarLetras(self, pal: str) -> str:
        """
        Cuenta el total de letras, vocales y consonantes de una palabra.
        Recibe como parametro el string o palabra ingresada por el usuario y retornaun string con el mensaje para la respuesta.
        """
        self.tokens -= 2

        tot_letras = len(pal)
        tot_vocales = 0
        tot_cons = 0
        for p in pal:
            if p in "aeiou":
                tot_vocales += 1
            else:
                tot_cons += 1
    
        return f"Palabra: {pal} | Vocales: {tot_vocales} | Consonantes: {tot_cons} | Total: {tot_letras}"


    def ejecutarCalculadora(self, num1: float, operacion: str, num2: float) -> str:
        """
        Realiza la operación de matemáticas solicitada por el usuario.
        Recibe como parametros dos float para la operación y un string para identificar el tipo de operación a realizar y 
        retorna un string con el resultado de la operación o error.
        """
        
        self.tokens -= 3

        if operacion == "+":
            return f"El resultado de la suma es: {num1 + num2}"
        elif operacion == "-":
            return f"El resultado de la resta es: {num1 - num2}"
        elif operacion == "*":
            return f"El resultado de la multiplicación es: {num1*num2}"
        elif operacion == "/":
            if num2 != 0:
                return f"El resultado de la división es: {num1 / num2}"
            else:
                return "No se puede dividir entre cero."
        else:
            raise ValueError("Operador no válido.")
    
    def lanzar_dado(self) -> str:
        #Lanza un dado de 6 caras usando random.
        self.tokens -= 1  
        resultado = random.randint(1, 6)
        return f"[PseudoAgente] Resultado del dado: {resultado}"
        
    def mostrarFecha(self, rol: str)-> str:
        self.tokens -= 2

        if rol == "admin":    
            return f"Fecha y hora actual: {datetime.datetime.now()}"        
        else:
            """raise: Es una instrucción que detiene la ejecución normal para generar un error controlado cuando ocurre algo no permitido dentro de la función.
            El error viaja "hacia afuera" de la función buscando un bloque except en el programa principal donde se llamada dicha función que genero la exception,
            si lo encuentra, el error se captura y el programa muestra un mensaje en lugar de cerrarse el programa."""
            raise PermissionError("[Acceso Denegado] Este comando requiere privilegios de administrador.")

    def registrar_log(self, cmd: str, rol: str, mensaje: str):
        d_log = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)



# La herencia permite reutilizar código sin tener que copiar y pegar toda la lógica en otra clase.
# Esto facilita el mantenimiento y evita errores cuando se hacen cambios en el código fuente.
class AgenteAdmin(PseudoAgente):

    def __init__(self):
        super().__init__()

    def gestionarHistorial(self, accion: str) -> str:
        
        if accion == "historial all":
            return f"El historial es: {self.historial_chat}"
        elif accion == "historial clear":
            self.historial_chat.clear()
            return "Se ha eliminado el historial correctamente."
        elif accion == "salir":
            return "salir"
        else:
            return super().gestionarHistorial(accion)