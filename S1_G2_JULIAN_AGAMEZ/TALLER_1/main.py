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
usuario_activo = ""  # guardará el nombre del usuario para usarlo luego
rol_activo     = ""  # guardará el rol leído desde el JSON

while intentos < 3:
    usuario_input = input("\nUsuario: ").strip()
    pass_input    = input("Contraseña: ").strip()

    # Verificamos si el usuario existe en el JSON y si la contraseña coincide
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
    print("  Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, salir")
    print("=" * 48)

    cmd            = ""
    sistema_activo = True

    while sistema_activo:
        cmd = input("\nAgente> ").strip().lower()

        if cmd == "salir":
            print("Apagando el Agente. ¡Hasta pronto!")
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")

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

        elif cmd == "fecha_hoy":
            if usuarios[usuario_activo]["rol"] == "administrador":
                hoy = datetime.date.today()
                print(f"Fecha actual: {hoy.strftime('%d/%m/%Y')}")
            else:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

        elif cmd == "validar_pass":
            propuesta = input("Ingresa tu propuesta de contraseña: ").strip()
            if len(propuesta) < 8:
                print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            elif propuesta == usuario_activo:
                print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
            else:
                print("[Aceptada] Contraseña válida.")

        elif cmd == "calculadora":
            try:
                num1     = float(input("Ingresa el primer número: "))
                operador = input("Ingresa el operador (+, -, *, /): ").strip()
                num2     = float(input("Ingresa el segundo número: "))
            except ValueError:
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
                    print("[Error] No es posible dividir entre cero.")
                    continue
                resultado = num1 / num2
            else:
                print(f"[Error] Operador '{operador}' no reconocido. Usa +, -, * o /.")
                continue

            if resultado == int(resultado):
                print(f"Resultado: {num1} {operador} {num2} = {int(resultado)}")
            else:
                print(f"Resultado: {num1} {operador} {num2} = {resultado}")

        else:
            print(f"[Desconocido] Comando '{cmd}' no reconocido.")
            print("  Comandos válidos: ping, contar, fecha_hoy, validar_pass, calculadora, salir")
