# Día 1: Funciones
## Crear una función - def nombre (): return/print ft Type Hints

## Alcance de las variables - Funciones SIEMPRE deben ser cajas negras - Ingreso por parámetros, Salida por return.
## Retorno anticipado - Para reducir estructuras if/else

## Para revisión autónoma
### Importancia de los type hints en tiempos de IA
### Parámetros por defecto, *args, *kwargs. ¿Cuál es la diferencia con un argumento?
### Docstrings o las triple comillas para las funciones """ """

import datetime

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

        #Uso del type Historial
        d_log: Historial = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol_actual,
                "descripcion": mensaje}
        
        historial_chat.append(d_log)
        

else:
    print("Acceso denegado.")




