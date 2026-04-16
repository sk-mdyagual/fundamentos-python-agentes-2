## Creado por: Sergio Jaramillo (SergiJaramilloL)
from agente import PseudoAgente, AgenteAdmin

# =====================
# CREDENCIALES
# =====================
# Guardo las credenciales de autenticación en variables.
user = "user"
user_pass = "user123"
admin = "admin"
admin_pass = "admin123"

# Variables de almacenamiento del usuario activo.
# El historial ya no flota aquí: vive encapsulado dentro del objeto agente.
rol_activo = ""
user_activo = ""

# Variable que almacena la instancia del agente. Se asigna después del login.
agente = None

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
        # El admin recibe un AgenteAdmin: tiene los mismos poderes que PseudoAgente pero
        # con el beneficio extra de revisar el historial sin consumir batería.
        agente = AgenteAdmin("AgentePro")
        print(f"[Sistema] Bienvenido, {user_activo}. Rol: administrador. Agente: {agente.nombre}.")
        break
    elif user_input == user and pass_input == user_pass:
        rol_activo = "invitado"
        user_activo = user
        # El invitado recibe un PseudoAgente estándar con acceso limitado a comandos.
        agente = PseudoAgente("Agente")
        print(f"[Sistema] Bienvenido, {user_activo}. Rol: invitado. Agente: {agente.nombre}.")
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
# Se inicia el bucle usando agente.tokens > 0 como condición de vida del agente.
# Cuando los tokens llegan a 0 o menos, el while deja de iterar naturalmente sin usar break.
# La variable en_sesion maneja la salida voluntaria del usuario con el comando "salir".
en_sesion = True
while en_sesion and agente.tokens > 0:
    print(f"""
-----------------------------
  Hola soy tu agente. Puedo ayudarte con lo siguiente:
  1. ping
  2. contar
  3. fecha_hoy
  4. validar_pass
  5. calculadora
  6. historial | historial all | historial clear
  7. lanzar_dado
  8. salir
  [Batería: {agente.tokens} tokens]
-----------------------------""")

    # Se le pide al usuario el comando a ejecutar. El prompt muestra el nombre de usuario activo.
    comando = input(f"{user_activo}>> ").strip().lower()

    # Variable que almacena la descripción del resultado de cada comando para guardarlo en el historial.
    mensaje = ""

    ### --- Fase 2: Comandos existentes ---

    # PING
    # Condiciones comando ping. Delega a agente.ping() y muestra el resultado.
    if comando == "ping":
        resultado = agente.ping()
        print(resultado)
        mensaje = "Se envió un ping y se devuelve un pong."

    # CONTAR
    # Condiciones comando contar. Delega el conteo a agente.contar_letras().
    elif comando == "contar":
        pal = input("Ingrese una palabra: ").strip().lower()
        resultado = agente.contar_letras(pal)
        print(resultado)
        mensaje = f"La palabra ingresada fue '{pal}': conteo de vocales, consonantes y total completado."

    # SALIR
    # Condiciones comando salir. Pone en_sesion en False para terminar el bucle sin usar break.
    elif comando == "salir":
        print("Apagando agente. 👋 Chao! Bye! Ciao! Au revoir! Tchao! Tschüss! До свидания! 再见! 👋")
        mensaje = "Se solicitó terminar la sesión."
        # Se registra el log antes de salir para que el historial quede completo.
        agente.registrar_log(comando, rol_activo, mensaje)
        en_sesion = False
        # Usamos continue para saltar el registrar_log del final del bucle y evitar duplicado.
        continue

    ### --- Fase 3: Nuevas herramientas ---

    # FECHA_HOY
    # Condición para comando fecha_hoy. Delega a agente.fecha_hoy() que lanza PermissionError si el rol es invitado.
    elif comando == "fecha_hoy":
        try:
            resultado = agente.fecha_hoy(rol_activo)
            print(resultado)
            mensaje = "La fecha y hora actual fue consultada exitosamente."
        except PermissionError as e:
            print(f"[Acceso Denegado] {e}")
            mensaje = "Se intentó acceder a fecha_hoy sin privilegios de administrador."

    # VALIDAR_PASS
    # Condición para comando validar_pass. Delega la validación a agente.validar_password().
    elif comando == "validar_pass":
        nueva_pass = input("Ingresa tu nueva contraseña propuesta: ")
        resultado = agente.validar_password(nueva_pass, user_activo)
        print(resultado)
        if "Aceptada" in resultado:
            mensaje = "Contraseña propuesta validada exitosamente."
        else:
            mensaje = f"Contraseña rechazada: {resultado.split('] ')[1]}"

    # CALCULADORA
    # Condición para comando calculadora. Delega la operación a agente.calculadora().
    # Punto crítico: el usuario podría ingresar texto en lugar de números, generando un ValueError
    # al intentar convertir con float(). El try/except aquí lo atrapa y muestra un mensaje claro.
    elif comando == "calculadora":
        try:
            num1_str = input("Ingresa el primer número: ")
            operador = input("Ingresa el operador (+, -, *, /): ").strip()
            num2_str = input("Ingresa el segundo número: ")
            # Se convierten las entradas "string" con float() para que sea tipo numérico:
            # El float en python acepta enteros y decimales, si uso int() y el usuario ingresa un número decimal, se generará un error.
            num1 = float(num1_str)
            num2 = float(num2_str)
            resultado = agente.calculadora(num1, operador, num2)
            print(resultado)
            mensaje = f"Operación ejecutada: {num1_str} {operador} {num2_str}."
        except ValueError:
            # Si el usuario ingresa algo como "dos" o "abc" en lugar de un número, float() lanza ValueError.
            print("[Error] Entrada inválida. Asegúrate de ingresar números válidos (ej. 3, 4.5).")
            mensaje = "Operación fallida: el usuario ingresó un valor no numérico en la calculadora."

    # LANZAR_DADO
    # Condición para el nuevo comando lanzar_dado. Delega a agente.lanzar_dado().
    elif comando == "lanzar_dado":
        resultado = agente.lanzar_dado()
        print(resultado)
        mensaje = f"Se lanzó el dado. Resultado: {resultado.split(': ')[1]}"

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

            # Para el modo búsqueda, se pide la palabra clave antes de invocar el método.
            if sub_cmd == "":
                sub_cmd = input("Ingresa la palabra clave a buscar: ").strip()

            # Se delega toda la lógica de historial a agente.gestionar_historial() y se imprime su resultado.
            resultado = agente.gestionar_historial(sub_cmd)
            print(resultado)
            mensaje = f"Comando historial ejecutado con acción: '{sub_cmd}'."
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            mensaje = "Se intentó acceder al historial sin privilegios de administrador."

    # Condición final por defecto. Si no encuentra ninguna coincidencia con los comandos reconocidos, se muestra un mensaje de error.
    else:
        print("[Error] Comando no reconocido. Escribe uno de los comandos disponibles.")
        mensaje = f"Comando '{comando}' no reconocido."

    # REGISTRO EN HISTORIAL
    # Al finalizar cada comando, el agente guarda el evento en su memoria interna.
    # Esto permite que el agente tenga memoria de todo lo que ocurrió en la sesión.
    agente.registrar_log(comando, rol_activo, mensaje)

# =====================
# FIN DE SESIÓN
# =====================
# Si el bucle terminó porque los tokens llegaron a 0, se muestra el mensaje de agotamiento.
# Si terminó porque en_sesion fue puesto en False (comando "salir"), no se muestra nada extra.
if agente.tokens <= 0:
    print(f"\n[Sistema] {agente.nombre} se quedó sin batería. Apagando sesión automáticamente.")

## Creado por: Sergio Jaramillo (SergiJaramilloL)
