## Creado por: Sergio Jaramillo (SergiJaramilloL)
from datetime import datetime
from typing import Dict, List

# =====================
# CONTRATO DE MEMORIA (Type Aliasing)
# =====================
# Cuando una función actúa como "herramienta" (tool) para un modelo de IA, el modelo
# necesita saber exactamente qué estructura de datos va a recibir y retornar. Si le pasamos
# solo `list` o `dict`, la descripción es ambigua: ¿lista de qué? ¿diccionario con qué llaves?
# Al crear un Alias como `MemoriaAgente`, le damos un nombre semántico y preciso a la estructura.
# Así, cualquier función que declare `memoria: MemoriaAgente` documenta de forma legible que
# espera una lista de diccionarios {str: str}, igual a como un LLM necesita un esquema claro
# (ej. JSON Schema) para poder procesar correctamente su contexto de conversación.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]

# =====================
# FASE 0: DEFINICIÓN DE HERRAMIENTAS (TOOLS)
# =====================
# Las herramientas son funciones puras e independientes que encapsulan la lógica de cada comando.
# El bucle principal (while) solo captura el input del usuario e invoca estas funciones.
# Ninguna herramienta imprime directamente: procesa datos y retorna un string con el resultado.


def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """
    Administra el historial de comandos del agente.

    Parámetros:
        accion (str): Puede ser "all" para ver todo, "clear" para borrar,
                      o cualquier otro texto para buscar por palabra clave.
        memoria (MemoriaAgente): El historial completo de la sesión activa.

    Retorna:
        str: Texto formateado con el resultado de la acción solicitada.
    """
    # HISTORIAL ALL
    # Si la acción es "all", se arma el texto con todas las entradas del historial.
    if accion == "all":
        if len(memoria) == 0:
            return "[Sistema] El historial está vacío."
        lineas = [f"\n[Sistema] Historial completo ({len(memoria)} entradas):"]
        for i, entrada in enumerate(memoria):
            lineas.append(
                f"  {i + 1}. [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
            )
        return "\n".join(lineas)

    # HISTORIAL CLEAR
    # Si la acción es "clear", se vacía la lista en memoria y se confirma la acción.
    # Como las listas en Python se pasan por referencia, .clear() modifica el objeto original.
    elif accion == "clear":
        memoria.clear()
        return "[Sistema] Historial eliminado correctamente."

    # HISTORIAL BÚSQUEDA
    # Si la acción no es ni "all" ni "clear", se trata como término de búsqueda por palabra clave.
    else:
        clave = accion
        coincidencias = []
        # Se itera sobre cada entrada del historial para buscar la palabra clave dentro de su descripción.
        for entrada in memoria:
            # Para verificar si una palabra está dentro de un texto en Python se usa el operador "in".
            # Ejemplo: "arroz" in "Cocinar Arroz" → False, pero si aplicamos .lower() a ambos lados:
            # "arroz" in "cocinar arroz" → True. Esto hace que la búsqueda sea insensible a mayúsculas.
            if clave.lower() in entrada["descripcion"].lower():
                coincidencias.append(
                    f"  [{entrada['timestamp']}] ({entrada['rol']}) {entrada['cmd']} → {entrada['descripcion']}"
                )
        if len(coincidencias) == 0:
            return f"[PseudoAgente] No encontré registros que coincidan con '{clave}'."
        return "\n".join(coincidencias) + f"\n\n[Sistema] Se encontraron {len(coincidencias)} coincidencia(s) para '{clave}'."


def contar_letras(palabra: str) -> str:
    """
    Cuenta las vocales, consonantes y el total de letras en una palabra o frase.

    Parámetros:
        palabra (str): La palabra o frase ingresada por el usuario (ya en minúsculas).

    Retorna:
        str: Texto con el resumen del conteo de vocales, consonantes y total.
    """
    tot_letras = len(palabra)
    tot_vocales = 0
    tot_cons = 0
    for letra in palabra:
        if letra in "aeiou":
            tot_vocales += 1
        # Se usa isalpha() para contar solo letras reales como consonantes,
        # evitando que espacios o símbolos se cuenten como consonantes.
        elif letra.isalpha():
            tot_cons += 1
    return (
        f"Palabra ingresada: {palabra}\n"
        f"Total de vocales: {tot_vocales}\n"
        f"Total de consonantes: {tot_cons}\n"
        f"Total de letras: {tot_letras}"
    )


def calculadora(num1: float, operador: str, num2: float) -> str:
    """
    Realiza una operación matemática básica entre dos números.

    Parámetros:
        num1 (float): El primer número de la operación.
        operador (str): El operador aritmético a aplicar (+, -, *, /).
        num2 (float): El segundo número de la operación.

    Retorna:
        str: Texto con el resultado de la operación, o mensaje de error si el operador
             no es válido o se intenta dividir entre cero.
    """
    if operador == "+":
        resultado = num1 + num2
        return f"Resultado: {num1} + {num2} = {resultado}"
    elif operador == "-":
        resultado = num1 - num2
        return f"Resultado: {num1} - {num2} = {resultado}"
    elif operador == "*":
        resultado = num1 * num2
        return f"Resultado: {num1} * {num2} = {resultado}"
    elif operador == "/":
        # Condición anidada dentro del operador "/" para verificar que el segundo número no sea cero.
        if num2 == 0:
            return "[Error] No se puede dividir entre cero."
        resultado = num1 / num2
        return f"Resultado: {num1} / {num2} = {resultado}"
    # Si el operador no es reconocido, se retorna un mensaje de error indicando los operadores válidos.
    else:
        return f"[Error] Operador '{operador}' no reconocido. Usa +, -, * o /."


def validar_password(password: str, usuario: str) -> str:
    """
    Verifica si una contraseña propuesta cumple con los requisitos mínimos de seguridad.

    Parámetros:
        password (str): La contraseña propuesta por el usuario.
        usuario (str): El nombre del usuario activo, para comparación de igualdad.

    Retorna:
        str: Mensaje indicando si la contraseña fue aceptada o el motivo de rechazo.
    """
    # Condición 1: la contraseña debe tener al menos 8 caracteres.
    if len(password) < 8:
        return "[Rechazada] La contraseña debe tener al menos 8 caracteres."
    # Condición 2: la contraseña no puede ser igual al nombre de usuario.
    elif password == usuario:
        return "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
    else:
        return "[Aceptada] Contraseña válida."


def fecha_hoy(rol: str) -> str:
    """
    Retorna la fecha y hora actual del sistema. Restringido al rol de administrador.

    Parámetros:
        rol (str): El rol del usuario activo ("admin" o "invitado").

    Retorna:
        str: Texto con la fecha y hora actual formateada.

    Lanza:
        PermissionError: Si el usuario tiene rol "invitado" (sin privilegios de admin).
    """
    # RAISE: El viaje del error desde que se lanza hasta que se atrapa.
    # Cuando un usuario con rol "invitado" llama a esta función, `raise` lanza un PermissionError
    # hacia arriba en la pila de llamadas. Como esta función no tiene ningún try/except propio,
    # Python sube un nivel y busca quién la invocó: en este caso, el bucle principal (while True).
    # Allí, el bloque `except PermissionError` lo atrapa, imprime el aviso bonito en consola
    # y el programa continúa sin crashear. Es como lanzar una pelota: `raise` la lanza hacia
    # arriba, `except` la atrapa. Si nadie la atrapara, el programa se caería por completo.
    if rol != "admin":
        raise PermissionError("Privilegios insuficientes")
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[Sistema] Fecha y hora actual: {ahora}"


# =====================
# CREDENCIALES
# =====================
# Guardo las credenciales de autenticación en variables.
user = "user"
user_pass = "user123"
admin = "admin"
admin_pass = "admin123"

# Variables de almacenamiento del usuario activo.
rol_activo = ""
user_activo = ""

# Lista de diccionarios que actúa como memoria del agente.
# Cada entrada registra el timestamp, comando ejecutado, rol del usuario y una descripción del resultado.
# Ahora tipada con el alias MemoriaAgente para mayor claridad sobre su estructura.
historial_chat: MemoriaAgente = []

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
    # Condiciones comando contar. Delega el conteo a la función contar_letras().
    elif comando == "contar":
        pal = input("Ingrese una palabra: ").strip().lower()
        resultado_contar = contar_letras(pal)
        print(resultado_contar)
        mensaje = f"La palabra ingresada fue '{pal}': conteo de vocales, consonantes y total completado."

    # SALIR
    # Condiciones comando salir. Termina el bucle y apaga el agente.
    elif comando == "salir":
        print("Apagando agente. 👋 Chao! Bye! Ciao! Au revoir! Tchao! Tschüss! До свидания! 再见! 👋")
        mensaje = "Se solicitó terminar la sesión."
        # Se guarda el log antes de salir para que el historial quede completo.
        d_log: Recuerdo = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        historial_chat.append(d_log)
        break

    ### --- Fase 3: Nuevas herramientas ---

    # FECHA_HOY
    # Condición para comando fecha_hoy. Delega a fecha_hoy() que lanza PermissionError si el rol es invitado.
    # El try/except aquí en el bucle es quien atrapa ese error y lo muestra como mensaje amigable.
    elif comando == "fecha_hoy":
        try:
            resultado_fecha = fecha_hoy(rol_activo)
            print(resultado_fecha)
            mensaje = f"La fecha y hora actual fue consultada exitosamente."
        except PermissionError as e:
            print(f"[Acceso Denegado] {e}")
            mensaje = "Se intentó acceder a fecha_hoy sin privilegios de administrador."

    # VALIDAR_PASS
    # Condición para comando validar_pass. Delega la validación a validar_password().
    elif comando == "validar_pass":
        # Pide al usuario ingresar una contraseña nueva.
        nueva_pass = input("Ingresa tu nueva contraseña propuesta: ")
        resultado_pass = validar_password(nueva_pass, user_activo)
        print(resultado_pass)
        # Se extrae el veredicto del resultado para guardarlo en el historial.
        if "Aceptada" in resultado_pass:
            mensaje = "Contraseña propuesta validada exitosamente."
        else:
            mensaje = f"Contraseña rechazada: {resultado_pass.split('] ')[1]}"

    # CALCULADORA
    # Condición para comando calculadora. Delega la operación a calculadora().
    # Punto crítico: el usuario podría ingresar texto en lugar de números, generando un ValueError
    # al intentar convertir con float(). El try/except aquí lo atrapa y muestra un mensaje claro.
    elif comando == "calculadora":
        try:
            # Se le pide al usuario ingresar dos números y un operador matemático.
            num1_str = input("Ingresa el primer número: ")
            operador = input("Ingresa el operador (+, -, *, /): ").strip()
            num2_str = input("Ingresa el segundo número: ")

            # Se convierten las entradas "string" con float() para que sea tipo numérico:
            # El float en python acepta enteros y decimales, si uso int() y el usuario ingresa un número decimal, se generará un error.
            num1 = float(num1_str)
            num2 = float(num2_str)

            resultado_calc = calculadora(num1, operador, num2)
            print(resultado_calc)
            mensaje = f"Operación ejecutada: {num1_str} {operador} {num2_str}."
        except ValueError:
            # Si el usuario ingresa algo como "dos" o "abc" en lugar de un número, float() lanza ValueError.
            # Lo atrapamos aquí para mostrar un mensaje útil sin que el programa se caiga.
            print("[Error] Entrada inválida. Asegúrate de ingresar números válidos (ej. 3, 4.5).")
            mensaje = "Operación fallida: el usuario ingresó un valor no numérico en la calculadora."

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

            # Para el modo búsqueda, se pide la palabra clave antes de invocar la función.
            if sub_cmd == "":
                sub_cmd = input("Ingresa la palabra clave a buscar: ").strip()

            # Se delega toda la lógica de historial a gestionar_historial() y se imprime su resultado.
            resultado_historial = gestionar_historial(sub_cmd, historial_chat)
            print(resultado_historial)
            mensaje = f"Comando historial ejecutado con acción: '{sub_cmd}'."
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
    d_log: Recuerdo = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cmd": comando,
        "rol": rol_activo,
        "descripcion": mensaje
    }
    historial_chat.append(d_log)

## Creado por: Sergio Jaramillo (SergiJaramilloL)
