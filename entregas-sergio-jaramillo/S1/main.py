## Creado por: Sergio Jaramillo (SergiJaramilloL)
from datetime import date

# Guardo las credenciales de autenticación en variables.
user = "user"
user_pass = "user123"
admin = "admin"
admin_pass = "admin123"

# Variables de almacenamiento del usuario activo
rol_activo = ""
usuario_activo = ""

# =====================
# FASE 1: LOGIN
# =====================
for intento in range(3):
    # Se hace un print inicial que actua como contador de intentos, y luego se le pide usuario y contraseña a la persona.
    print(f"\n[Login] Intento {intento + 1} de 3")
    user_input = input("Usuario: ").strip().lower()
    pass_input = input("Contraseña: ").strip().lower()

    # Se evalúan las diferentes condiciones en el siguiente orden:
    # 1. Si el usuario y contraseña coinciden con las credenciales de admin,
    # 2. Si el usuario y contraseña coinciden con las credenciales de invitado,
    # 3. Si no coinciden, se muestra un mensaje de error y se indica
    #    Al final del for se muestra el mensaje de bloqueo y se termina la ejecución. 
    if user_input == admin and pass_input == admin_pass:
        rol_activo = "admin"
        usuario_activo = admin
        print(f"[Sistema] Bienvenido, {usuario_activo}. Rol: administrador.")
        break
    elif user_input == user and pass_input == user_pass:
        rol_activo = "invitado"
        usuario_activo = user
        print(f"[Sistema] Bienvenido, {usuario_activo}. Rol: invitado.")
        break
    else:
        restantes = 2 - intento
        if restantes > 0:
            print(f"[Error] Credenciales incorrectas. Te quedan {restantes} intento(s).")
else:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

# =====================
# FASE 2 & 3: BUCLE PRINCIPAL
# =====================
# Se inicia el bucle infinito y se muestra el menú de comandos disponibles.
while True:
    print("""
-----------------------------
  Hola soy tu agente. Puedo ayudarte con lo siguiente:
  1. ping
  2. contar
  3. fecha_hoy
  4. validar_pass
  5. calculadora
  6. salir
-----------------------------""")
    ### --- Fase 2: Comandos existentes ---
    # Se le pide al usuario el comando a ejecutar.
    comando = input(">> ").strip().lower()

    # PING
    # Condiciones comando ping. Responde con pong.
    if comando == "ping":
        print("pong!")
    # Condiciones comando contar. Cuenta vocales y consonantes en una frase dada por el usuario.

    # CONTAR
    # Condiciones comando contar. Cuenta vocales y consonantes en una frase dada por el usuario.
    elif comando == "contar":
        pal = input("Ingrese una palabra: ").strip().lower()
        tot_letras = len(pal)
        # Conteo
        tot_vocales = 0
        tot_cons = 0
        for p in pal:
            if p in "aeiou":
                tot_vocales +=1
            else:
                tot_cons +=1
        # Resultados del conteo
        print(f"Palabra ingresada: {pal}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras: {tot_letras}")

    # SALIR
    # Condiciones comando salir. Termina el bucle y apaga el agente.
    elif comando == "salir":
        print("Apagando agente. 👋 Chao! Bye! Ciao! Au revoir! Tchao! Tschüss! До свидания! 再见! 👋")
        break

    ### --- Fase 3: Nuevas herramientas ---

    # FECHA_HOY
    # Condición para comando fecha_hoy.
    elif comando == "fecha_hoy":
        # Condición anidada dentro de fecha_hoy para verificar si el usuario tiene rol de admin y luego se muetra la fecha actual, con ayuda de la librería datatime.
        if rol_activo == "admin":
            print(f"[Sistema] Fecha actual: {date.today()}")
        # Si el usuario no tiene rol de admin, se muestra un mensaje de acceso denegado.
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

    # VALIDAR_PASS
    # Condición para comando validar_pass.
    elif comando == "validar_pass":
        # Pide al usuario ingresar una contraseña nueva.
        nueva_pass = input("Ingresa tu nueva contraseña propuesta: ")
        # Condición anidada dentro de validar_pass para verificar si la contraseña nueva cumple con los requisitos de seguridad:
        # 1. Al menos 8 caracteres
        # 2. No ser igual al nombre de usuario.
        # 3. Si no entra en ninguna condición de rechazo, se acepta la contraseña y se muestra un mensaje de contraseña válida.
        if len(nueva_pass) < 8:
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
        elif nueva_pass == usuario_activo:
            print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
        else:
            print("[Aceptada] Contraseña válida.")

    # CALCULADORA
    # Condición para comando calculadora.
    elif comando == "calculadora":
        # Se le pide al usuario ingresar dos números y un operador matemático.
        num1_str = input("Ingresa el primer número: ")
        operador = input("Ingresa el operador (+, -, *, /): ").strip()
        num2_str = input("Ingresa el segundo número: ")

        # Se convierten las entradas "string" con float() para que sea tipo númerico:
        # El float en python acepta enteros y decimales, sí uso int() y el usuario ingresa un número decimal, se generará un error.
        num1 = float(num1_str)
        num2 = float(num2_str)

        # Condición anidada dentro de calculadora para verificar el operador ingresado y realizar la operación matemática correspondiente.
        # Condición para cada uno de los operadores devolviendo el resultado correspondiente al operador
        if operador == "+":
            print(f"Resultado: {num1 + num2}")
        elif operador == "-":
            print(f"Resultado: {num1 - num2}")
        elif operador == "*":
            print(f"Resultado: {num1 * num2}")
        elif operador == "/":
            # Condición anidada dentro del operador "/" para verificar que el segundo número no sea cero.
            if num2 == 0:
                print("[Error] No se puede dividir entre cero.")
            else:
                print(f"Resultado: {num1 / num2}")
        # Sí el operador no es reconocido, se muestra un mensaje de error indicando que el operador no es válido.
        else:
            print("[Error] Operador no reconocido. Usa +, -, * o /.")

    # Condición final por defecto. Sí no encuentra ninguna coincidencia con los comandos reconocidos, se muestra un mensaje de error indicando que el comando no es reconocido.
    else:
        print("[Error] Comando no reconocido. Escribe uno de los comandos disponibles.")

## Creado por: Sergio Jaramillo (SergiJaramilloL)
