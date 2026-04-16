# Programación orientada a objetos

import datetime

from S3.S3_sesion_1 import Historial

# Día 1: POO in a nutshell
## Clases: Para instanciar/crear objetos
## Objetos: Representaciones a partir de una clase

## Calse Carro (Huella) -> Carro_1, Carro_2, Carro_3 (Instancias)

## Constructor: __init__
## self, siempre va con el constructor, self.attribute después. Es un tema de entender el proposito de self
### En resumen: self funciona como incicador de sitio, para saber a donde debes ir cuando utilizas las funciones de una clase o accedes a los atributos
## No existen modificaciones de acceso (public/private/protected) pero existe el "_" para hacer ._attribute: uso interno

#TO-DO: Construir una clase PseudoAgente
## Atributos de entradad: nombre
## Atributos adicionales: tokens, historial_chat
###Metodos/Funciones
#registrar_log()
#gestionar_hisotrial()

type Historial = dict[str, str]

class PseudoAgente:
    #constructor
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens = 100
        self.historial_chat: list[Historial] = []

    #Funciones
    def registrar_log(self, cmd: str, rol: str, descripcion: str):
        d_log: Historial = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol,
                "descripcion": descripcion}
        
        self.historial_chat.append(d_log)

    def gestionar_historial(self, op: str, rol: str):
        self.tokens -= 30

        if op == "all":
            self.registrar_log("historial " + op, rol, f"[PseudoAgente] Se muestra el historial actual hasta las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")
            return self.historial_chat
        if op == "clear":
            self.registrar_log("historial " + op, rol, f"[PseudoAgente] Se borró el historial actual a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ")
            self.historial_chat.clear()
            return self.historial_chat

#TO-DO 1: Función para validar el acceso
def login(user, passwrd):
    if user == "admin" and passwrd == "admin123":
        return {"rol": user, "access": True, "description":"[Sistema] Acceso concedido. Privilegios de Administrador activados."}
    if user == "invitado" and passwrd == "1234":
        return {"rol": user, "access": True, "description": "[Sistema] Acceso concedido. Modo Invitado."}
    
    return {"rol": user, "access": False, "description": "[Error] Credenciales incorrectas."}


#TO-DO 2: Funciones para procesar cada comando
#Propuesta: Dividir las funcionalidades del comando historial
def hist_sing(l_hist, op="all"):

    if op == "all":
        return {"result": l_hist, "description": f"[PseudoAgente] Se muestra el historial actual hasta las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} " }
                    
    if op == "clear":
        return {"result": [], "description": f"[PseudoAgente] Se borró el historial actual a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} " }
            

#Para estudios autónomos: Busqueda sobre el historial

#Para estudios autónomos - TO-DO 3: Función para guardar la memoria del agente




##Login
print("-----------Iniciando el pseudoagente estilo consola--------------------")
intentos = 0
rol_actual = ""
tiene_acceso = False

while intentos < 3 and not tiene_acceso:
    usuario = input("Usuario: ").strip().lower()
    password = input("Contraseña: ").strip()
    
    login_attemp = login(usuario, password)
    rol_actual = login_attemp["rol"]
    tiene_acceso = login_attemp["access"]

    if not tiene_acceso:
        intentos += 1
        print(f"{login_attemp["description"]} Te quedan {3 - intentos} intentos.")
    else:
        print(login_attemp["description"])



## Pseudoagente
if tiene_acceso:    
    historial_chat: list[Historial] = [] 
    #{'timestamp': '2026-03-18 13:50:51', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se ha enviado un ping y de respuesta se devolvió un pong.'}, {'timestamp': '2026-03-18 13:50:56', 'cmd': 'fecha_hoy', 'rol': 'invitado', 'descripcion': '[Acceso Denegado] Este comando requiere privilegios de administrador.'}, {'timestamp': '2026-03-18 13:51:02', 'cmd': 'dormir', 'rol': 'invitado', 'descripcion': 'Comando no existe. Intente de nuevo'}, {'timestamp': '2026-03-18 13:51:07', 'cmd': 'salir', 'rol': 'invitado', 'descripcion': 'Se ha solicitado terminar la sesión.'}
    pseudo_activo = True
    mensaje = ""

    mi_agente: PseudoAgente = PseudoAgente("Harvis")

    while pseudo_activo:
        print(f"[{mi_agente.nombre}] Tokens disponibles: {mi_agente.tokens}")

        if mi_agente.tokens <= 0:
            print(f"[{mi_agente.nombre}] No tienes tokens disponibles. Por favor, recarga para seguir usando el agente.")
            break

        cmd = input(f"\n{usuario}@PseudoAgente>: ").strip().lower()

        if cmd == "salir":
            print("[PseudoAgente] Apagando sistemas...")
            pseudo_activo = False
            mi_agente.registrar_log(cmd, rol_actual, "Se ha solicitado terminar la sesión.")

        elif cmd == "ping":
            print("pong~")
            mi_agente.tokens -= 10
            mi_agente.registrar_log(cmd, rol_actual, "Se ha enviado un ping y de respuesta se devolvió un pong.")

        elif cmd == "contar":
            pal = input("Ingrese una palabra: ").strip().lower()
            #Para revisión autónoma: List comprehesion - Ejemplo de uso
            #Antes
            """tot_letras = len(pal)
            tot_vocales = 0
            tot_cons = 0
            for p in pal:
                if p in "aeiou":
                    tot_vocales += 1
                elif p.isalpha(): 
                    tot_cons += 1    """
            #Ahora
            vocales = [l for l in pal if l in "aeiou"]
            consonantes = [l for l in pal if l not in "aeiou"] 

            tot_vocales = len(vocales)
            tot_cons = len(consonantes)  
            tot_letras = len(pal)
        
            mensaje = f"""Se solicitó el conteo de la palabra {pal}, dando como resultados:
            Vocales: {tot_vocales}
            Consonantes: {tot_cons}
            Total: {tot_letras}"""

            print(mensaje)
        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                ahora = datetime.datetime.now()
                mensaje = f"[PseudoAgente] La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
                print(mensaje)
                
            else:
                mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
                print(mensaje)

        elif cmd == "validar_pass":
            print("Validar pass")
            mensaje = ""
        elif cmd == "calculadora":
            print("Calculadora")
            mensaje = ""
        elif cmd.startswith("hist"):
            if " " in cmd:
                sing = cmd.split(" ")[-1]
                hist_result = hist_sing(historial_chat)
                historial_chat = hist_result["result"]
                print(hist_result["description"])
                print(historial_chat)
                
                
            else:
                found = []
                word = input("Ingresa la palabra clave a buscar: ").lower()
                #Para revisión autónoma: enumerate()
                for i, elem in enumerate(historial_chat, sing):
                    if(word in elem["descripcion"]):
                        found.append(elem)
                mensaje = f" [PseudoAgente] Total de concidencias: {len(found)}"
                print(mensaje)
                if len(found) > 0:                    
                    for i, elem in enumerate(found):
                        print(f"{i+1} >>> {elem}")
                else:
                    print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")

        else:
            mensaje = " [PseudoAgente] Comando no existe. Intente de nuevo"
            print(mensaje)

        print(mi_agente.registrar_log(cmd, rol_actual, mensaje))        

else:
    print("Acceso denegado.")
