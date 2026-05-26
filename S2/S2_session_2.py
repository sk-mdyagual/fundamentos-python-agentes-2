# Día 1: Listas y Diccionarios 
## Día 2: Anidaciones - [[],[],[],[]], [{}, {}, {}], {"a": {1: [] }, "b": {1: [] }}

import datetime
print("-----------Iniciando el pseudoagente estilo consola--------------------")

##Login
intentos = 0
rol_actual = ""
tiene_acceso = False

while intentos < 3 and not tiene_acceso:
    usuario = input("Usuario: ").strip().lower()
    password = input("Contraseña: ").strip()
    
    if usuario == "admin" and password == "admin123":
        rol_actual = "admin"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Privilegios de Administrador activados.")
        
    elif usuario == "invitado" and password == "1234":
        rol_actual = "invitado"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Modo Invitado.")
        
    else:
        intentos += 1
        print(f"[Error] Credenciales incorrectas. Te quedan {3 - intentos} intentos.")

## Pseudoagente
if tiene_acceso:
    #TO-DO: Agregar una memoria al pseudo agente utilizando listas y diccionarios
    historial_chat=[{'timestamp': '2026-03-19 07:47:36', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se envió un ping y se devuelve un pong.'}, {'timestamp': '2026-03-19 07:47:40', 'cmd': 'fecha_hoy', 'rol': 'invitado', 'descripcion': 'Este comando requiere privilegios de administrador.'}, {'timestamp': '2026-03-19 07:47:46', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se envió un ping y se devuelve un pong.'}, {'timestamp': '2026-03-19 07:47:57', 'cmd': 'contar', 'rol': 'invitado', 'descripcion': 'La palabra ingresada fue computadora y se obtuvo como resultado: Vocales - 5 | Consonantes 6 siendo el total: 11'}, {'timestamp': '2026-03-19 07:47:46', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se envió un ping y se devuelve un pong.'}, {'timestamp': '2026-03-19 07:47:57', 'cmd': 'contar', 'rol': 'invitado', 'descripcion': 'La palabra ingresada fue computadora y se obtuvo como resultado: Vocales - 5 | Consonantes 6 siendo el total: 11 '}, {'timestamp': '2026-03-19 07:48:07', 'cmd': 'salir', 'rol': 'invitado', 'descripcion': 'Se ha solicitado terminar la sesión.'}] 
    pseudo_activo = True
    mensaje = ""

    while pseudo_activo:
        cmd = input(f"\n{usuario}@PseudoAgente>: ").strip().lower() 

        if cmd == "salir":
            print("[PseudoAgente] Apagando sistemas...")
            mensaje = "Se ha solicitado  terminar la sesión."
            pseudo_activo = False
        elif cmd == "ping":
            print("pong~")
            mensaje = "Se envió un ping y se devuelve un pong."  
        elif cmd == "contar":
            pal = input("Ingrese una palabra: ").strip().lower()
            tot_letras = len(pal)
            tot_vocales = 0
            tot_cons = 0
            for p in pal:
                if p in "aeiou":
                    tot_vocales += 1
                elif p.isalpha(): 
                    tot_cons += 1                    
            print(f"Palabra ingresada: {pal}")
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
            print(f"Total de letras: {tot_letras}")
            mensaje = f"La palabra ingresada fue {pal} y se obtuvo como resultado: Vocales - {tot_vocales} | Consonantes {tot_cons} siendo el total: {tot_letras} "
        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                ahora = datetime.datetime.now()
                mensaje = f"La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
                print("[PseudoAgente]" + mensaje)
                
            else:
                mensaje = "Este comando requiere privilegios de administrador."
                print("[PseudoAgente]" + mensaje)

        elif cmd == "validar_pass":
            print("Validar pass")
            mensaje = ""
        elif cmd == "calculadora":
            print("Calculadora")
            mensaje = ""
        else:
            mensaje = "Comando no existe. Intente de nuevo"
            print("[PseudoAgente]" + mensaje)
            
        #TO-DO: Taller de la semana - Búsqueda de memoria
        d_log = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol_actual,
                "descripcion": mensaje}
        
        historial_chat.append(d_log)
        print(historial_chat)

else:
    print("Acceso denegado.")
