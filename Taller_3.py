import datetime
from typing import Dict, List

# Definimos el contrato de memoria para el agente, que es una lista de registros (recuerdos).
Recuerdo = Dict[str, str] 
# Cada recuerdo tiene un timestamp, el comando ejecutado, el rol del usuario y una descripción del resultado o acción tomada.
MemoriaAgente = List[Recuerdo]

#Funciones de herramientas (Tools) para cada comando, con validaciones y blindajes necesarios.
# Funcion para contar vocales y consonantes en una palabra, con validación de caracteres alfabéticos.
def tool_contar(palabra: str) -> str:
    """Cuenta vocales y consonantes en una palabra."""
    vocales_validas = "aeiouáéíóú"
    v = sum(1 for letra in palabra if letra.isalpha() and letra in vocales_validas)
    c = sum(1 for letra in palabra if letra.isalpha() and letra not in vocales_validas)
    return f"La palabra '{palabra}' tiene {v} vocales y {c} consonantes."

#Funcion para mostrar la fecha actual, con validación de rol (solo administrador puede acceder).
def tool_fecha_hoy(rol_usuario: str) -> str:
    """Retorna la fecha o lanza PermissionError si el rol no es administrador."""
    if rol_usuario != "administrador":
        raise PermissionError("Privilegios insuficientes: Solo el administrador puede ver la fecha.")
    
    hoy = datetime.datetime.now()
    return f"Fecha actual: {hoy.strftime('%Y-%m-%d %H:%M:%S')}"

#Funcion para validar la seguridad de una contraseña, con requisitos de longitud y comparación con el nombre de usuario.
def tool_validar_password(password: str, usuario: str) -> str:
    """Valida requisitos de seguridad de una contraseña."""
    if len(password) < 8:
        return "Error: La contraseña debe tener al menos 8 caracteres."
    if password == usuario:
        return "Error: La contraseña no puede ser igual al usuario."
    return "Contraseña válida y segura."

#Funcion para realizar operaciones matemáticas, con validación de operador y manejo de división por cero.
def tool_calculadora(num1: float, operador: str, num2: float) -> str:
    """Realiza operaciones matemáticas con blindaje ZeroDivisionError."""
    if operador == "+": return f"Resultado: {num1 + num2}"
    elif operador == "-": return f"Resultado: {num1 - num2}"
    elif operador == "*": return f"Resultado: {num1 * num2}"
    elif operador == "/":
        if num2 == 0:
            raise ZeroDivisionError("No se puede dividir por cero.")
        return f"Resultado: {num1 / num2}"
    else:
        raise ValueError(f"Operador '{operador}' no reconocido.")

#Funcion para gestionar el historial del agente, con opciones para ver todo, limpiar o buscar por palabra clave.
def tool_gestionar_historial(accion: str, memoria: MemoriaAgente, filtro: str = "") -> str:
    """Gestiona el historial: ver todo, limpiar o buscar coincidencias."""
    if accion == "all":
        if not memoria: return "El historial está vacío."
        cuerpo = f"\n--- Historial completo ({len(memoria)} registros) ---\n"
        for reg in memoria:
            cuerpo += f"Timestamp: {reg['timestamp']}, Comando: {reg['comando']}, Rol: {reg['rol']}, Descripción: {reg['descripcion']}\n"
        return cuerpo.strip()
    
    elif accion == "clear":
        memoria.clear()
        return "Historial actual limpiado."
    
    elif accion == "search":
        if not filtro: return "Debe ingresar una palabra para buscar."
        res = [r for r in memoria if filtro.lower() in r["descripcion"].lower()]
        if not res: return f"No encontré registros con: '{filtro}'"
        cuerpo = f"\n--- Se encontraron {len(res)} resultado(s) ---\n"
        for reg in res:
            cuerpo += f"Rol: {reg['rol']}, Descripción: {reg['descripcion']}\n"
        return cuerpo.strip()
    
    return "Acción de historial no reconocida."

# LÓGICA DE INICIO (LOGIN)

usuario_invitado = "invitado"
contraseña_invitado = "12345"
usuario_administrador = "administrador"
contraseña_administrador = "67890"

intentos = 0
rol = None
tiene_acceso = False
usuario_actual = ""

# BUCLE DE LOGIN: El usuario tiene 3 intentos para ingresar credenciales correctas. Si falla, el sistema se bloquea.
while intentos < 3 and not tiene_acceso:
    usuario = input("ingresa tu usuario: ").strip().lower()
    contraseña = input("ingresa tu contraseña: ").strip().lower()

    if usuario == usuario_administrador and contraseña == contraseña_administrador:
        rol = "administrador"
        usuario_actual = usuario
        print("inicio exitoso bienvenido")
        print(f"tu rol es: {rol}")
        tiene_acceso = True
        break
    elif usuario == usuario_invitado and contraseña == contraseña_invitado:
        rol = "invitado"
        usuario_actual = usuario
        print("inicio exitoso bienvenido")
        print(f"tu rol es: {rol}")
        tiene_acceso = True
        break
    else:
        intentos += 1
        print("datos incorrectos")

if not tiene_acceso:
    print("alerta usuario bloqueado. cerrando sistema")
    exit()

# BUCLE PRINCIPAL (PSEUDOAGENTE)
historial_chat: MemoriaAgente = []

while True:
    print("\n--- Home de entrada ---")
    print("ping | pong | contar | fecha | validarcontraseña | calculadora | historial | salir")

    comando = input("\nIngrese su solicitud: ").strip().lower()
    
    if comando == "salir":
        print("Apagando agente....")
        break

    try:
        mensaje_log = ""

        if comando == "ping":
            print("pong")
            mensaje_log = "se ha solicitado el comando ping"
        
        elif comando == "pong":
            print("ping!")
            mensaje_log = "se ha solicitado el comando pong"

        elif comando == "contar":
            pal = input("ingresa una palabra: ")
            mensaje_log = tool_contar(pal)
            print(mensaje_log)

        elif comando == "fecha":
            # Si el rol es 'invitado', tool_fecha_hoy lanzará el raise PermissionError
            mensaje_log = tool_fecha_hoy(rol)
            print(mensaje_log)

        elif comando == "validarcontraseña":
            p_in = input("Ingrese una nueva contraseña: ")
            mensaje_log = tool_validar_password(p_in, usuario_actual)
            print(mensaje_log)

        elif comando == "calculadora":
            # BLINDAJE: Capturamos fallos de escritura del usuario
            try:
                n1 = float(input("Ingrese el primer numero: "))
                op = input("Ingresa el operador (+,-,*,/): ")
                n2 = float(input("Ingrese el segundo numero: "))
                mensaje_log = tool_calculadora(n1, op, n2)
                print(mensaje_log)
            except ValueError:
                mensaje_log = "Error: Se esperaba un valor numérico."
                print(mensaje_log)
            except ZeroDivisionError as e:
                mensaje_log = f"Error: {e}"
                print(mensaje_log)

        elif comando == "historial":
            h_all = input("¿Desea ver todo el historial? (s/n): ").lower()
            if h_all == "s":
                res_h = tool_gestionar_historial("all", historial_chat)
                print(res_h)
            else:
                limp = input("¿Desea limpiar el historial? (s/n): ").lower()
                if limp == "s":
                    res_h = tool_gestionar_historial("clear", historial_chat)
                    print(res_h)
                else:
                    pal_bus = input("Palabra clave a buscar: ")
                    res_h = tool_gestionar_historial("search", historial_chat, pal_bus)
                    print(res_h)
            mensaje_log = "Consulta de historial realizada"

        else:
            print("Comando no reconocido.")
            mensaje_log = "Comando no reconocido"

    except PermissionError as e:
        # Aquí atrapamos el error que viene desde la Tool de fecha
        print(f"🚫 ERROR DE ACCESO: {e}")
        mensaje_log = f"Fallo de permisos: {e}"

    # Registro de auditoría
    recuerdo: Recuerdo = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comando": comando,
        "rol": str(rol),
        "descripcion": mensaje_log
    }
    historial_chat.append(recuerdo)