# Día 1: Funciones
## Crear una función - def nombre(): return/print ft Type Hints
def coordenadas(x, y):
    print(f"({x}, {y})")

## Alcance de las variables - Funciones SIEMPRE deben ser cajas negras - Ingreso por parámetros, Salida por return.
## Para revisión autónoma
### Importancia de los type hints en tiempos de IA
### Parámetros por defecto, *args, *kwargs. ¿Cuál es la diferencia con un argumento?
### Docstrings o las triple comillas para las funciones """ """

import datetime
import json
import re

#Para revisión autónoma: Alias Type (Modelo de datos)
type Historial = dict[str,str]

## FUNCIONES

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

#TO-DO 3: Función para guardar la memoria del agente
def guardar_memoria(historial: list, archivo: str = "memoria_agente.json") -> dict:
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)
    return {"result": archivo, "description": f"[PseudoAgente] Memoria guardada en '{archivo}' a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}

def validar_pass(contrasena: str) -> dict:
    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_minuscula = any(c.islower() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    tiene_especial = any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for c in contrasena)
    longitud_ok = len(contrasena) >= 8
    puntaje = sum([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial, longitud_ok])
    nivel = "Fuerte" if puntaje == 5 else ("Media" if puntaje >= 3 else "Débil")
    return {"nivel": nivel, "puntaje": puntaje, "description": f"[PseudoAgente] Contraseña evaluada. Nivel: {nivel} ({puntaje}/5 criterios)."}

def calculadora_eval(expr: str) -> dict:
    if not re.fullmatch(r'[\d\s\+\-\*\/\.\(\)]+', expr):
        return {"resultado": None, "description": "[PseudoAgente] Expresión inválida. Solo se permiten números y operadores (+, -, *, /, ())."}
    try:
        resultado = eval(expr)  # nosec - entrada validada por regex antes del eval
        return {"resultado": resultado, "description": f"[PseudoAgente] {expr} = {resultado}"}
    except ZeroDivisionError:
        return {"resultado": None, "description": "[PseudoAgente] Error: División entre cero."}
    except (ValueError, TypeError, SyntaxError):
        return {"resultado": None, "description": "[PseudoAgente] Error al evaluar la expresión."}

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

    while pseudo_activo:
        cmd = input(f"\n{usuario}@PseudoAgente>: ").strip().lower()

        if cmd == "salir":
            print("[PseudoAgente] Apagando sistemas...")
            pseudo_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        elif cmd == "ping":
            print("pong~")
            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."            
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
            pw = input("Ingresa la contraseña a validar: ").strip()
            vp_result = validar_pass(pw)
            mensaje = vp_result["description"]
            print(mensaje)
        elif cmd == "calculadora":
            expresion = input("Ingresa la expresión (ej: 5 + 3 * 2): ").strip()
            calc_result = calculadora_eval(expresion)
            mensaje = calc_result["description"]
            print(mensaje)
        elif cmd == "guardar_memoria":
            mem_result = guardar_memoria(historial_chat)
            mensaje = mem_result["description"]
            print(mensaje)
        elif cmd.startswith("hist"):
            if " " in cmd:
                sing = cmd.split(" ")[-1]
                hist_result = hist_sing(historial_chat, sing)
                historial_chat = hist_result["result"]
                print(hist_result["description"])
                print(historial_chat)
                
                
            else:
                found = []
                word = input("Ingresa la palabra clave a buscar: ").lower()
                #Para revisión autónoma: enumerate()
                for i, elem in enumerate(historial_chat, 1):
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

        #Uso del type Historial
        d_log: Historial = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol_actual,
                "descripcion": mensaje}
        
        historial_chat.append(d_log)

else:
    print("Acceso denegado.")