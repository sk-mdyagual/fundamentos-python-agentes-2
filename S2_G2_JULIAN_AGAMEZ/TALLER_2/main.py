# Taller Semana 2 - Motor de Búsqueda del Agente
# Basado en S2_session_2.py con el comando 'historial' extendido.

import datetime

# ---------------------------------------------------------------------------
# USUARIOS DEFINIDOS COMO DICCIONARIO (estilo JSON)
# ---------------------------------------------------------------------------

usuarios = {
    "invitado": {"password": "pass123",  "rol": "invitado"},
    "admin":    {"password": "admin123", "rol": "administrador"}
}

# ---------------------------------------------------------------------------
# FASE 1: CAPA DE SEGURIDAD (LOGIN)
# ---------------------------------------------------------------------------

print("=" * 48)
print("  Sistema de Agente - Autenticación requerida")
print("=" * 48)

intentos       = 0
login_exitoso  = False
usuario_activo = ""
rol_activo     = ""

while intentos < 3:
    usuario_input = input("\nUsuario: ").strip()
    pass_input    = input("Contraseña: ").strip()

    if usuario_input in usuarios and usuarios[usuario_input]["password"] == pass_input:
        login_exitoso  = True
        usuario_activo = usuario_input
        rol_activo     = usuarios[usuario_input]["rol"]
        print(f"\n[OK] Bienvenido, {usuario_activo}. Rol: {rol_activo}.\n")
        break
    else:
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Error] Credenciales incorrectas. Intentos restantes: {restantes}")

if not login_exitoso:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")

if login_exitoso:
    print("=" * 48)
    print("  Agente iniciado. Escribe un comando.")
    print("  Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")
    print("=" * 48)

    cmd            = ""
    sistema_activo = True
    historial_chat = []
    mensaje        = ""

    while sistema_activo:
        cmd = input("\nAgente> ").strip().lower()

        if cmd == "salir":
            print("Apagando el Agente. ¡Hasta pronto!")
            mensaje = "He solicitado salir del sistema."
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")
            mensaje = "Se envió el comando 'ping' y se recibió 'pong!' como respuesta."

        elif cmd == "contar":
            frase       = input("Ingresa una frase: ").strip()
            tot_vocales = 0
            tot_cons    = 0
            for caracter in frase:
                if caracter.isalpha():
                    if caracter.lower() in "aeiouáéíóú":
                        tot_vocales += 1
                    else:
                        tot_cons += 1
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
            mensaje = f"Se contó la frase '{frase}' y se encontraron {tot_vocales} vocales y {tot_cons} consonantes."

        elif cmd == "fecha_hoy":
            if usuarios[usuario_activo]["rol"] == "administrador":
                hoy = datetime.date.today()
                mensaje = f"Se solicitó la fecha actual y se mostró: {hoy.strftime('%d/%m/%Y')}."
                print(f"Fecha actual: {hoy.strftime('%d/%m/%Y')}")
            else:
                mensaje = "Se intentó usar el comando 'fecha_hoy' sin privilegios de administrador."
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

        elif cmd == "validar_pass":
            propuesta = input("Ingresa tu propuesta de contraseña: ").strip()
            if len(propuesta) < 8:
                mensaje = f"Se propuso la contraseña '{propuesta}' y fue rechazada por ser menor a 8 caracteres."
                print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            elif propuesta == usuario_activo:
                mensaje = f"Se propuso la contraseña '{propuesta}' y fue rechazada por ser igual al nombre de usuario."
                print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
            else:
                mensaje = f"Se propuso la contraseña '{propuesta}' y fue aceptada como válida."
                print("[Aceptada] Contraseña válida.")

        elif cmd == "calculadora":
            try:
                num1     = float(input("Ingresa el primer número: "))
                operador = input("Ingresa el operador (+, -, *, /): ").strip()
                num2     = float(input("Ingresa el segundo número: "))
            except ValueError:
                mensaje = "Se ingresaron valores no numéricos en la calculadora."
                print("[Error] Debes ingresar valores numéricos.")
                continue

            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            elif operador == "/":
                if num2 == 0:
                    mensaje = "Se intentó dividir entre cero en la calculadora."
                    print("[Error] No es posible dividir entre cero.")
                    continue
                resultado = num1 / num2
            else:
                mensaje = f"Se ingresó un operador no reconocido: '{operador}'."
                print(f"[Error] Operador '{operador}' no reconocido. Usa +, -, * o /.")
                continue

            if resultado == int(resultado):
                mensaje = f"Se realizó la operación {num1} {operador} {num2} y el resultado fue {int(resultado)}."
                print(f"Resultado: {num1} {operador} {num2} = {int(resultado)}")
            else:
                mensaje = f"Se realizó la operación {num1} {operador} {num2} y el resultado fue {resultado}."
                print(f"Resultado: {num1} {operador} {num2} = {resultado}")

        # Usé .split() para separar el comando base ("historial") de sus argumentos opcionales
        # ("all", "clear" o ninguno), lo que me permite manejar las tres singularidades del comando
        # desde una sola condición principal.
        elif cmd.split()[0] == "historial":
            partes = cmd.split()

            if len(partes) > 1 and partes[1] == "all":
                # Mostrar todo el historial almacenado
                if not historial_chat:
                    print("[PseudoAgente] El historial está vacío.")
                else:
                    print(f"[PseudoAgente] Historial completo ({len(historial_chat)} registro(s)):")
                    for entrada in historial_chat:
                        print(f"  [{entrada['timestamp']}] {entrada['usuario']} ({entrada['rol']}): {entrada['descripcion']}")
                mensaje = "Se solicitó ver el historial completo con 'historial all'."

            elif len(partes) > 1 and partes[1] == "clear":
                # Eliminar todo el historial almacenado
                historial_chat.clear()
                print("[PseudoAgente] Historial eliminado exitosamente.")
                mensaje = "Se eliminó todo el historial almacenado con 'historial clear'."

            else:
                # Modo búsqueda: se ingresa solo "historial" sin argumentos
                palabra_clave = input("Ingresa la palabra clave a buscar: ").strip()
                coincidencias = 0

                for entrada in historial_chat:
                    # Verifico si la palabra clave está "contenida" dentro de la descripcion del
                    # diccionario usando el operador 'in' de Python (ej: "arroz" in "Cocinar Arroz").
                    # Aplico .lower() a ambos lados para que la búsqueda no distinga entre
                    # mayúsculas y minúsculas. La separacion del argumento la resolví con .split().
                    if palabra_clave.lower() in entrada["descripcion"].lower():
                        coincidencias += 1
                        print(f"  [{entrada['timestamp']}] {entrada['usuario']}: {entrada['descripcion']}")

                if coincidencias == 0:
                    print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                else:
                    print(f"[PseudoAgente] Se encontraron {coincidencias} coincidencia(s).")

                mensaje = f"Se realizó una búsqueda con la palabra clave '{palabra_clave}' y se encontraron {coincidencias} coincidencia(s)."

        else:
            mensaje = f"Se ingresó un comando desconocido: '{cmd}'."
            print(f"[Desconocido] Comando '{cmd}' no reconocido.")
            print("  Comandos válidos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")

        d_log = {
            "timestamp":   datetime.datetime.now().isoformat(),
            "usuario":     usuario_activo,
            "cmd":         cmd,
            "rol":         usuarios[usuario_activo]["rol"],
            "descripcion": mensaje
        }
        historial_chat.append(d_log)
