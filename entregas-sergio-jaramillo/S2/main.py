## Creado por: Sergio Jaramillo (SergiJaramilloL)
from datetime import datetime

# Guardo las credenciales de autenticación en variables.
user = "user"
user_pass = "user123"
admin = "admin"
admin_pass = "admin123"

# Variables de almacenamiento del usuario activo
rol_activo = ""
user_activo = ""

# Lista de diccionarios que actúa como memoria del agente.
# Cada entrada registra el timestamp, comando ejecutado, rol del usuario y una descripción del resultado.
historial_chat = []

# =====================
# FASE 1: LOGIN
# =====================
for intento in range(3):
    # Se hace un print inicial que actúa como contador de intentos, y luego se le pide usuario y contraseña a la persona.
    print(f"\n[Login] Intento {intento + 1} de 3")
    user_input = input("Usuario: ").strip().lower()
    pass_input = input("Contraseña: ").strip().lower()

    # Se evalúan las diferentes condiciones en el siguiente orden:
    # 1. Si el usuario y contraseña coinciden con las credenciales de admin,
    # 2. Si el usuario y contraseña coinciden con las credenciales de invitado,
    # 3. Si no coinciden, se muestra un mensaje de error y se indica cuántos intentos quedan.
    #    Al final del for se muestra el mensaje de bloqueo y se termina la ejecución.
    if user_input == admin and pass_input == admin_pass:
        rol_activo = "admin"
        user_activo = admin
        print(f"[Sistema] Bienvenido, {user_activo}. Rol: administrador.")
        break
    elif user_input == user and pass_input == user_pass:
        rol_activo = "invitado"
        user_activo = user
        print(f"[Sistema] Bienvenido, {user_activo}. Rol: invitado.")
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
  6. historial | historial all | historial clear
  7. salir
-----------------------------""")

    # Se le pide al usuario el comando a ejecutar. El prompt muestra el nombre de usuario activo.
    comando = input(f"{user_activo}>> ").strip().lower()

    # Variable que almacena la descripción del resultado de cada comando para guardarlo en el historial.
    mensaje = ""

    ### --- Fase 2: Comandos existentes ---

    # PING
    # Condiciones comando ping. Responde con pong.
    if comando == "ping":
        print("pong!")
        mensaje = "Se envió un ping y se devuelve un pong."

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
                tot_vocales += 1
            # Se usa isalpha() para contar solo letras reales como consonantes,
            # evitando que espacios o símbolos se cuenten como consonantes.
            elif p.isalpha():
                tot_cons += 1
        # Resultados del conteo
        print(f"Palabra ingresada: {pal}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras: {tot_letras}")
        mensaje = f"La palabra ingresada fue '{pal}': Vocales - {tot_vocales} | Consonantes - {tot_cons} | Total - {tot_letras}."

    # SALIR
    # Condiciones comando salir. Termina el bucle y apaga el agente.
    elif comando == "salir":
        print("Apagando agente. 👋 Chao! Bye! Ciao! Au revoir! Tchao! Tschüss! До свидания! 再见! 👋")
        mensaje = "Se solicitó terminar la sesión."
        # Se guarda el log antes de salir para que el historial quede completo.
        d_log = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        historial_chat.append(d_log)
        break

    ### --- Fase 3: Nuevas herramientas ---

    # FECHA_HOY
    # Condición para comando fecha_hoy.
    elif comando == "fecha_hoy":
        # Condición anidada dentro de fecha_hoy para verificar si el usuario tiene rol de admin.
        # Si lo tiene, se muestra la fecha y hora actual usando datetime.
        if rol_activo == "admin":
            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[Sistema] Fecha y hora actual: {ahora}")
            mensaje = f"La fecha y hora actual es: {ahora}."
        # Si el usuario no tiene rol de admin, se muestra un mensaje de acceso denegado.
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            mensaje = "Se intentó acceder a fecha_hoy sin privilegios de administrador."

    # VALIDAR_PASS
    # Condición para comando validar_pass.
    elif comando == "validar_pass":
        # Pide al usuario ingresar una contraseña nueva.
        nueva_pass = input("Ingresa tu nueva contraseña propuesta: ")
        # Condición anidada dentro de validar_pass para verificar si la contraseña nueva cumple con los requisitos de seguridad:
        # 1. Al menos 8 caracteres.
        # 2. No ser igual al nombre de usuario.
        # 3. Si no entra en ninguna condición de rechazo, se acepta la contraseña.
        if len(nueva_pass) < 8:
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            mensaje = "Contraseña rechazada: menos de 8 caracteres."
        elif nueva_pass == user_activo:
            print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
            mensaje = "Contraseña rechazada: igual al nombre de usuario."
        else:
            print("[Aceptada] Contraseña válida.")
            mensaje = "Contraseña propuesta validada exitosamente."

    # CALCULADORA
    # Condición para comando calculadora.
    elif comando == "calculadora":
        # Se le pide al usuario ingresar dos números y un operador matemático.
        num1_str = input("Ingresa el primer número: ")
        operador = input("Ingresa el operador (+, -, *, /): ").strip()
        num2_str = input("Ingresa el segundo número: ")

        # Se convierten las entradas "string" con float() para que sea tipo numérico:
        # El float en python acepta enteros y decimales, si uso int() y el usuario ingresa un número decimal, se generará un error.
        num1 = float(num1_str)
        num2 = float(num2_str)

        # Condición anidada dentro de calculadora para verificar el operador ingresado y realizar la operación matemática correspondiente.
        if operador == "+":
            resultado = num1 + num2
            print(f"Resultado: {resultado}")
            mensaje = f"Operación: {num1} + {num2} = {resultado}."
        elif operador == "-":
            resultado = num1 - num2
            print(f"Resultado: {resultado}")
            mensaje = f"Operación: {num1} - {num2} = {resultado}."
        elif operador == "*":
            resultado = num1 * num2
            print(f"Resultado: {resultado}")
            mensaje = f"Operación: {num1} * {num2} = {resultado}."
        elif operador == "/":
            # Condición anidada dentro del operador "/" para verificar que el segundo número no sea cero.
            if num2 == 0:
                print("[Error] No se puede dividir entre cero.")
                mensaje = f"Operación fallida: división de {num1} entre cero."
            else:
                resultado = num1 / num2
                print(f"Resultado: {resultado}")
                mensaje = f"Operación: {num1} / {num2} = {resultado}."
        # Si el operador no es reconocido, se muestra un mensaje de error indicando que el operador no es válido.
        else:
            print("[Error] Operador no reconocido. Usa +, -, * o /.")
            mensaje = f"Operador '{operador}' no reconocido."

    ### --- Fase 4: Motor de búsqueda ---

    # HISTORIAL
    # Condición para comando historial. Solo disponible para el rol admin.
    # El comando soporta tres variantes: "historial", "historial all" y "historial clear".
    # Para distinguir entre ellas se usa .split(), que divide el string en una lista de palabras.
    # Ejemplo: "historial all".split() → ["historial", "all"]. Luego se revisa si hay un segundo elemento.
    elif comando.split()[0] == "historial":
        if rol_activo == "admin":
            # Se extraen las partes del comando y se determina la sub-acción si existe.
            # Ejemplo: "historial clear" → partes = ["historial", "clear"] → sub_cmd = "clear".
            # Si solo se escribe "historial" → partes = ["historial"] → sub_cmd = "" (modo búsqueda).
            partes = comando.split()
            sub_cmd = partes[1] if len(partes) > 1 else ""

            # HISTORIAL ALL
            # Muestra todas las entradas del historial almacenadas en la sesión.
            if sub_cmd == "all":
                if len(historial_chat) == 0:
                    print("[Sistema] El historial está vacío.")
                    mensaje = "Se consultó el historial completo: estaba vacío."
                else:
                    print(f"\n[Sistema] Historial completo ({len(historial_chat)} entradas):")
                    for i, entrada in enumerate(historial_chat):
                        print(f"  {i + 1}. [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}")
                    mensaje = f"Se mostró el historial completo: {len(historial_chat)} entradas."

            # HISTORIAL CLEAR
            # Elimina todas las entradas del historial almacenadas en la sesión.
            elif sub_cmd == "clear":
                historial_chat.clear()
                print("[Sistema] Historial eliminado correctamente.")
                mensaje = "Se eliminó todo el historial de comandos."

            # HISTORIAL (modo búsqueda)
            # Sin sub-acción, el agente entra en modo búsqueda por palabra clave.
            else:
                clave = input("Ingresa la palabra clave a buscar: ").strip()
                coincidencias = 0
                # Se itera sobre cada entrada del historial para buscar la palabra clave dentro de su descripción.
                for entrada in historial_chat:
                    # Para verificar si una palabra está dentro de un texto en Python se usa el operador "in".
                    # Ejemplo: "arroz" in "Cocinar Arroz" → False, pero si aplicamos .lower() a ambos lados:
                    # "arroz" in "cocinar arroz" → True. Esto hace que la búsqueda sea insensible a mayúsculas.
                    if clave.lower() in entrada["descripcion"].lower():
                        coincidencias += 1
                        print(f"  [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}")
                # Si no se encontró ninguna coincidencia, se muestra el mensaje de resultado vacío.
                if coincidencias == 0:
                    print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                    mensaje = f"Búsqueda de '{clave}': sin coincidencias en el historial."
                else:
                    print(f"\n[Sistema] Se encontraron {coincidencias} coincidencia(s) para '{clave}'.")
                    mensaje = f"Búsqueda de '{clave}': {coincidencias} coincidencia(s) encontradas."
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            mensaje = "Se intentó acceder al historial sin privilegios de administrador."

    # Condición final por defecto. Si no encuentra ninguna coincidencia con los comandos reconocidos, se muestra un mensaje de error.
    else:
        print("[Error] Comando no reconocido. Escribe uno de los comandos disponibles.")
        mensaje = f"Comando '{comando}' no reconocido."

    # REGISTRO EN HISTORIAL
    # Al finalizar cada comando, se crea un diccionario con los datos del evento y se agrega a historial_chat.
    # Esto permite que el agente tenga memoria de todo lo que ocurrió en la sesión.
    d_log = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cmd": comando,
        "rol": rol_activo,
        "descripcion": mensaje
    }
    historial_chat.append(d_log)

## Creado por: Sergio Jaramillo (SergiJaramilloL)
