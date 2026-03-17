from datetime import datetime

# --- Fase 1: Capa de Seguridad (Login) ---

USUARIO_ADMIN = "admin"
CONTRASENA_ADMIN = "adminpass"
USUARIO_INVITADO = "invitado"
CONTRASENA_INVITADO = "invitadopass"

MAX_INTENTOS = 3
rol = usuario = None


for intento in range(1, MAX_INTENTOS + 1):
    usuario = input("Usuario: ")
    password = input("Contraseña: ")
    if (usuario == USUARIO_ADMIN and password == CONTRASENA_ADMIN) or (usuario == USUARIO_INVITADO and password == CONTRASENA_INVITADO):
        rol = usuario
        print(f"[Login Exitoso] Bienvenido, {usuario}.")
        break
    else:
        if intento == 1:
            print("[Error] Primer intento fallido. Verifica tus datos e inténtalo de nuevo.")
        elif intento == 2:
            print("[Error] Segundo intento fallido. Asegúrate de escribir correctamente usuario y contraseña .")
        elif intento == 3:
            print(f"[Error] Tercer intento fallido. Intento {intento}/{MAX_INTENTOS}. daño critico explotara")
else:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

# --- Fase 2: Comandos Base y Fase 3: Menú de Comandos ---
# IMPLEMENTACION DEL wHILE PARA QUE SEA UN BUCLE LAS OPCIONES
while True:
    print("\n+-----------------------+")
    print("|  Comandos disponibles  |")
    print("+-------------------------+")
    print("|   ping             |\n|   contar           |\n|   calculadora      |\n|   fecha_hoy        |\n|   validar_pass     |\n|   salir            |")
    print("+---------------------+\n")
# .strip().lower() CONTROLA QUE LAS OPCIONES RESPONDAN ASI TENGAN ALGUN ESPACIO O MAYUSCULAS     
    comando = input("Ingresa un comando: ").strip().lower()
    print(f"la opcion seleccionada fue......................................................................... {comando}")

    if comando == "ping":
        print("pong!")
    elif comando == "pong":
        print("ping!")

    elif comando == "contar":

        frase = input("Escribe una frase: ")

        vocales = 0
        consonantes = 0

        for c in frase:
            #compara cada caracter en miniscula con las vocales y las incrementa
            if c.lower() in "aeiou":
                vocales += 1
            #sino es vocal revisa que sea una letra y si es asi incrementa consonantes    
            elif c.isalpha():
                consonantes += 1

        print(f"Vocales: {vocales}, Consonantes: {consonantes}")

    elif comando == "fecha_hoy":

        if rol == "admin":
            #uso de la libreria datetime para mostrar la fecha y hora actual formateada Fecha actual: Monday, 16 de March de 2026, 00:00:00
            print("Fecha actual:", datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S"))
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

    elif comando == "validar_pass":

        nueva_pass = input("Propuesta de contraseña nueva: ")
        if len(nueva_pass) < 8:
            print("[Rechazo] La contraseña debe tener al menos 8 caracteres.")
        elif nueva_pass == usuario:
            print("[Rechazo] La contraseña no puede ser igual al nombre de usuario.")
        else:
            print("[Éxito] Contraseña válida.")

    elif comando == "calculadora":
        try:

            num1 = float(input("Ingresa el primer número: "))
            operador = input("Ingresa el operador (+, -, *, /): ")
            num2 = float(input("Ingresa el segundo número: "))
            match operador:
                case "+":
                    print(f"Resultado: {num1 + num2}")
                case "-":
                    print(f"Resultado: {num1 - num2}")
                case "*":
                    print(f"Resultado: {num1 * num2}")
                case "/":
                    if num2 == 0:
                        print("[Error] No se puede dividir por cero.")
                    else:
                        print(f"Resultado: {num1 / num2}")
                case _:
                    print("[Error] Operador no válido.")
        except ValueError:
            print("[Error] Entrada numérica inválida.")

    elif comando == "salir":
        print("Apagando el Agente. ¡Hasta luego!")
        break
    else:
        print("[Comando no reconocido] Intenta de nuevo.")
