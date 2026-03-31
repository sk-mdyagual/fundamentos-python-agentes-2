
# Importar datetime para manejo de fechas
from datetime import datetime
from typing import Dict, List

# Se usan Alias de tipo para mejorar la legibilidad del código, especialmente en la gestión del historial del agente.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


def contar_letras(texto_entrada: str) -> str:
    """Cuenta vocales y consonantes en una frase y retorna el resultado formateado.
    El método itera sobre cada caracter de la frase, usando .lower() para comparar sin importar mayúsculas/minúsculas.
    Se utiliza .isalpha() para asegurarse de contar solo letras como consonantes, excluyendo espacios, números o signos de puntuación."""
    vocales = 0
    consonantes = 0

    for c in texto_entrada:
        # compara cada caracter en miniscula con las vocales y las incrementa
        if c.lower() in "aeiou":
            vocales += 1
        # sino es vocal revisa que sea una letra y si es asi incrementa consonantes
        elif c.isalpha():
            consonantes += 1

    return f"Vocales: {vocales}, Consonantes: {consonantes}"


def validar_password(propuesta_clave: str, usuario_actual: str) -> str:
    """Valida reglas mínimas de contraseña y retorna el mensaje de estado.
    Reglas:
    - Al menos 8 caracteres
    - No puede ser igual al nombre de usuario
    """

    if len(propuesta_clave) < 8:
        return "[Rechazo] La contraseña debe tener al menos 8 caracteres."
    if propuesta_clave == usuario_actual:
        return "[Rechazo] La contraseña no puede ser igual al nombre de usuario."
    return "[Éxito] Contraseña válida."


def calculadora(numero_a: float, operador_math: str, numero_b: float) -> float:
    """Ejecuta una operación aritmética básica y retorna el resultado numérico.
    Soporta suma (+), resta (-), multiplicación (*) y división (/).
    Lanza ValueError para operadores no válidos y ZeroDivisionError para división por cero."""
    match operador_math:
        case "+":
            return numero_a + numero_b
        case "-":
            return numero_a - numero_b
        case "*":
            return numero_a * numero_b
        case "/":
            if numero_b == 0:
                raise ZeroDivisionError("No se puede dividir por cero.")
            return numero_a / numero_b
        case _:
            raise ValueError("Operador no válido.")


def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """Gestiona historial: mostrar todo, limpiar o buscar por palabra clave.
     - 'all': muestra todo el historial formateado.
     - 'clear': limpia el historial.
     - cualquier otra cadena: busca en las descripciones del historial."""
    if accion == "all":
        if len(memoria) == 0:
            return "[PseudoAgente] No hay registros en el historial."

        lineas = ["--- Historial completo ---"]
        for h in memoria:
            lineas.append(f"[{h['timestamp']}] ({h['rol']}) {h['cmd']}: {h['descripcion']}")
        return "\n".join(lineas)

    if accion == "clear":
        memoria.clear()
        return "[PseudoAgente] Historial eliminado correctamente."

    termino_busqueda = accion.strip().lower()
    coincidencias = []
    for h in memoria:
        # .lower() para comparar sin tener en cuenta mayúsculas/minúsculas
        # Utilicé el operador 'in' para verificar si la palabra clave está contenida en la descripción (ambos en minúsculas)
        if termino_busqueda in h["descripcion"].lower():
            coincidencias.append(f"[{h['timestamp']}] ({h['rol']}) {h['cmd']}: {h['descripcion']}")

    if len(coincidencias) == 0:
        return "--- Resultados de búsqueda ---\n[PseudoAgente] No encontré registros que coincidan con esa palabra."

    return (
        "--- Resultados de búsqueda ---\n"
        + "\n".join(coincidencias)
        + f"\n[PseudoAgente] Se encontraron {len(coincidencias)} coincidencia(s)."
    )


def obtener_fecha_hoy(rol_actual: str) -> str:
    """Retorna la fecha/hora actual para admin y lanza excepción para invitado.
     - Si el rol no es 'admin', se lanza una excepción PermissionError con un mensaje específico.
     - Si el rol es 'admin', se retorna la fecha y hora actual formateada. El formato es: 'Monday, 16 de March de 2026, 00:00:00'.  
     - El formato se logra usando strftime con los especificadores adecuados para día de la semana, día del mes, mes, año, hora, minuto y segundo."""
    # El error se lanza aquí con raise y sube al menú principal, donde un except específico lo captura para mostrar una alerta sin romper el programa.
    if rol_actual != "admin":
        raise PermissionError("Privilegios insuficientes")
    return datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S")

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
historial_chat: MemoriaAgente = []

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

        frase_usuario = input("Escribe una frase: ")
        resultado_conteo = contar_letras(frase_usuario)
        print(resultado_conteo)
        mensaje = f"La frase ingresada fue '{frase_usuario}' y se obtuvo: {resultado_conteo.replace(', ', ' | ')}"

    # --- Comando fecha_hoy ---
    elif comando == "fecha_hoy":

        try:
            #uso de la libreria datetime para mostrar la fecha y hora actual formateada Fecha actual: Monday, 16 de March de 2026, 00:00:00
            fecha_actual = obtener_fecha_hoy(rol)
            print("Fecha actual:", fecha_actual)
            mensaje = f"La fecha y hora actual es: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        except PermissionError as e:
            print(f"[Acceso Denegado] {e}.")
            mensaje = "Este comando requiere privilegios de administrador."

    # --- Comando validar_pass ---
    elif comando == "validar_pass":

        pass_propuesta = input("Propuesta de contraseña nueva: ")
        resultado_validacion = validar_password(pass_propuesta, usuario)
        print(resultado_validacion)

        if resultado_validacion.startswith("[Rechazo] La contraseña debe"):
            mensaje = "La contraseña propuesta es demasiado corta."
        elif resultado_validacion.startswith("[Rechazo] La contraseña no puede"):
            mensaje = "La contraseña no puede ser igual al usuario."
        else:
            mensaje = "Contraseña válida."

    # --- Comando calculadora ---
    elif comando == "calculadora":
        try:
            primer_numero = float(input("Ingresa el primer número: "))
            operador_input = input("Ingresa el operador (+, -, *, /): ")
            segundo_numero = float(input("Ingresa el segundo número: "))

            resultado = calculadora(primer_numero, operador_input, segundo_numero)
            print(f"Resultado: {resultado}")

            if operador_input == "+":
                mensaje = f"Se realizó suma: {primer_numero} + {segundo_numero} = {resultado}"
            elif operador_input == "-":
                mensaje = f"Se realizó resta: {primer_numero} - {segundo_numero} = {resultado}"
            elif operador_input == "*":
                mensaje = f"Se realizó multiplicación: {primer_numero} * {segundo_numero} = {resultado}"
            else:
                mensaje = f"Se realizó división: {primer_numero} / {segundo_numero} = {resultado}"
        except ValueError:
            print("[Error] Entrada numérica inválida u operador no válido.")
            mensaje = "Operador no válido o entrada numérica inválida."
        except ZeroDivisionError as e:
            print(f"[Error] {e}")
            mensaje = "Error: división por cero."

  # --- Comando historial (motor de búsqueda) ---
    elif comando.startswith("historial"):

        # Usamos .split() para separar el comando y sus argumentos
        partes = comando.split()
        if len(partes) == 2 and partes[1] == "all":

            # Mostrar todo el historial
            print("\n" + gestionar_historial("all", historial_chat))
            mensaje = "Se mostró todo el historial."

        elif len(partes) == 2 and partes[1] == "clear":
            # Limpiar todo el historial
            print(gestionar_historial("clear", historial_chat))
            mensaje = "Se eliminó todo el historial."

        elif len(partes) == 1:

            # Modo búsqueda por palabra clave
            palabra_busqueda = input("Ingresa la palabra clave a buscar: ").strip().lower()
            print("\n" + gestionar_historial(palabra_busqueda, historial_chat))
            mensaje = f"Se realizó búsqueda en historial con la palabra clave '{palabra_busqueda}'."

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