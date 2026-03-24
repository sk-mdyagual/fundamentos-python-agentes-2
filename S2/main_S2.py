
# Importar datetime para manejo de fechas
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


# --- Inicializar historial de acciones (memoria del agente) ---
# Cada acción será un diccionario con timestamp, comando, rol y descripción
historial_chat = []

# --- Fase 2: Comandos Base y Fase 3: Menú de Comandos ---
# IMPLEMENTACION DEL wHILE PARA QUE SEA UN BUCLE LAS OPCIONES
while True:
    print("\n+-----------------------+")
    print("|  Comandos disponibles  |")
    print("+-------------------------+")
    print("|   ping             |\n|   contar           |\n|   calculadora      |\n|   fecha_hoy        |\n|   validar_pass     |\n|   historial        |\n|   salir            |")
    print("+---------------------+\n")
    comando = input("Ingresa un comando: ").strip().lower()
    print(f"la opcion seleccionada fue......................................................................... {comando}")

    mensaje = ""
    # --- Comando ping ---
    if comando == "ping":
        print("pong!")
        mensaje = "Se envió un ping y se devuelve un pong."
    # --- Comando pong ---
    elif comando == "pong":
        print("ping!")
        mensaje = "Se envió un pong y se devuelve un ping."

    # --- Comando contar ---
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
        mensaje = f"La frase ingresada fue '{frase}' y se obtuvo: Vocales - {vocales} | Consonantes - {consonantes}"

    # --- Comando fecha_hoy ---
    elif comando == "fecha_hoy":

        if rol == "admin":
            #uso de la libreria datetime para mostrar la fecha y hora actual formateada Fecha actual: Monday, 16 de March de 2026, 00:00:00
            print("Fecha actual:", datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S"))
            mensaje = f"La fecha y hora actual es: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            mensaje = "Este comando requiere privilegios de administrador."

    # --- Comando validar_pass ---
    elif comando == "validar_pass":

        nueva_pass = input("Propuesta de contraseña nueva: ")
        if len(nueva_pass) < 8:
            print("[Rechazo] La contraseña debe tener al menos 8 caracteres.")
            mensaje = "La contraseña propuesta es demasiado corta."
        elif nueva_pass == usuario:
            print("[Rechazo] La contraseña no puede ser igual al nombre de usuario.")
            mensaje = "La contraseña no puede ser igual al usuario."
        else:
            print("[Éxito] Contraseña válida.")
            mensaje = "Contraseña válida."

    # --- Comando calculadora ---
    elif comando == "calculadora":
        try:

            num1 = float(input("Ingresa el primer número: "))
            operador = input("Ingresa el operador (+, -, *, /): ")
            num2 = float(input("Ingresa el segundo número: "))
            match operador:
                case "+":
                    print(f"Resultado: {num1 + num2}")
                    mensaje = f"Se realizó suma: {num1} + {num2} = {num1 + num2}"
                case "-":
                    print(f"Resultado: {num1 - num2}")
                    mensaje = f"Se realizó resta: {num1} - {num2} = {num1 - num2}"
                case "*":
                    print(f"Resultado: {num1 * num2}")
                    mensaje = f"Se realizó multiplicación: {num1} * {num2} = {num1 * num2}"
                case "/":
                    if num2 == 0:
                        print("[Error] No se puede dividir por cero.")
                        mensaje = "Error: división por cero."
                    else:
                        print(f"Resultado: {num1 / num2}")
                        mensaje = f"Se realizó división: {num1} / {num2} = {num1 / num2}"
                case _:
                    print("[Error] Operador no válido.")
                    mensaje = "Operador no válido."
        except ValueError:
            print("[Error] Entrada numérica inválida.")

  # --- Comando historial (motor de búsqueda) ---
    elif comando.startswith("historial"):

        # Usamos .split() para separar el comando y sus argumentos
        partes = comando.split()
        if len(partes) == 2 and partes[1] == "all":

            # Mostrar todo el historial
            print("\n--- Historial completo ---")

            if len(historial_chat) == 0:
                print("[PseudoAgente] No hay registros en el historial.")
            else:
                for h in historial_chat:
                    print(f"[{h['timestamp']}] ({h['rol']}) {h['cmd']}: {h['descripcion']}")
            mensaje = "Se mostró todo el historial."

        elif len(partes) == 2 and partes[1] == "clear":
            # Limpiar todo el historial
            historial_chat.clear()
            print("[PseudoAgente] Historial eliminado correctamente.")
            mensaje = "Se eliminó todo el historial."

        elif len(partes) == 1:

            # Modo búsqueda por palabra clave
            palabra = input("Ingresa la palabra clave a buscar: ").strip().lower()
            coincidencias = 0
            print("\n--- Resultados de búsqueda ---")

            for h in historial_chat:
                # .lower() para comparar sin tener en cuenta mayúsculas/minúsculas
                # Utilicé el operador 'in' para verificar si la palabra clave está contenida en la descripción (ambos en minúsculas)
                if palabra in h["descripcion"].lower():
                    print(f"[{h['timestamp']}] ({h['rol']}) {h['cmd']}: {h['descripcion']}")
                    coincidencias += 1

            if coincidencias == 0:
                print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")

            else:
                print(f"[PseudoAgente] Se encontraron {coincidencias} coincidencia(s).")
            mensaje = f"Se realizó búsqueda en historial con la palabra clave '{palabra}'."

        else:
            print("[PseudoAgente] Opción de historial no reconocida. Usa 'historial', 'historial all' o 'historial clear'.")
            mensaje = "Opción de historial no reconocida."            

    elif comando == "salir":
        print("Apagando el Agente. ¡Hasta luego!")
        mensaje = "Se ha solicitado terminar la sesión."
        # Registrar la acción antes de salir
        d_log = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol,
            "descripcion": mensaje
        }
        historial_chat.append(d_log)
        break

    else:
        print("[Comando no reconocido] Intenta de nuevo.")
        mensaje = "Comando no reconocido."

    # --- Guardar cada acción en el historial (memoria del agente) ---
    d_log = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cmd": comando,
        "rol": rol,
        "descripcion": mensaje
    }
    historial_chat.append(d_log)