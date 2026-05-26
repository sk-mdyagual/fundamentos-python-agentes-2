# Taller Semana 3 - Refactorización y Blindaje del PseudoAgente
# Basado en el Taller de la Semana 2, aplicando funciones tipadas,
# Type Aliases y manejo de errores con try/except/raise.

import datetime
from typing import Dict, List

# ---------------------------------------------------------------------------
# DEFINICIÓN DEL CONTRATO DE MEMORIA (Type Aliasing)
# ---------------------------------------------------------------------------

# ¿Por qué usar un Alias de Tipo como "MemoriaAgente"?
# Cuando entrenamos o definimos herramientas para un modelo de IA (LLM), el modelo
# no recibe un bucle 'while'; recibe descripciones textuales de funciones con sus
# tipos de entrada y salida. Un alias semántico como "MemoriaAgente" le dice al
# modelo QUÉ representa ese dato (la memoria del agente), no solo cómo está formado
# (una lista de diccionarios). Esto reduce la ambigüedad y permite que el agente
# decida mejor qué herramienta invocar y con qué argumentos, sin que yo tenga que
# explicarle cada vez que "esa lista es el historial del sistema".
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]

# ---------------------------------------------------------------------------
# USUARIOS DEFINIDOS COMO DICCIONARIO (estilo JSON)
# ---------------------------------------------------------------------------

usuarios = {
    "invitado": {"password": "pass123",  "rol": "invitado"},
    "admin":    {"password": "admin123", "rol": "administrador"},
}

# ---------------------------------------------------------------------------
# TOOLS — Funciones puras (sin print interno, siempre retornan un valor)
# ---------------------------------------------------------------------------

def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """
    Tool A: Gestiona el historial del PseudoAgente.

    Permite mostrar todo el historial, confirmar su borrado, o buscar entradas
    que contengan una palabra clave. Esta función no imprime nada; devuelve
    un string formateado para que el bucle principal lo muestre.

    Args:
        accion:  'all' para mostrar todo, 'clear' para confirmar borrado,
                 o cualquier otra cadena como palabra clave de búsqueda.
        memoria: El historial completo del agente (MemoriaAgente).

    Returns:
        str: Texto con el resultado formateado de la operación solicitada.
    """
    if accion == "all":
        if not memoria:
            return "[PseudoAgente] El historial está vacío."
        lineas = [f"[PseudoAgente] Historial completo ({len(memoria)} registro(s)):"]
        for entrada in memoria:
            lineas.append(
                f"  [{entrada['timestamp']}] {entrada['usuario']} "
                f"({entrada['rol']}): {entrada['descripcion']}"
            )
        return "\n".join(lineas)

    if accion == "clear":
        return "[PseudoAgente] Historial eliminado exitosamente."

    # Modo búsqueda: 'accion' es la palabra clave a buscar
    coincidencias = [
        f"  [{e['timestamp']}] {e['usuario']}: {e['descripcion']}"
        for e in memoria
        if accion.lower() in e["descripcion"].lower()
    ]
    if not coincidencias:
        return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
    return f"[PseudoAgente] {len(coincidencias)} coincidencia(s):\n" + "\n".join(coincidencias)


def contar_letras(frase: str) -> str:
    """
    Tool B: Cuenta vocales y consonantes en una frase.

    Recorre cada carácter de la frase y clasifica las letras alfabéticas como
    vocales (incluyendo acentuadas) o consonantes. Ignora espacios y símbolos.

    Args:
        frase: La cadena de texto a analizar.

    Returns:
        str: Resumen formateado con el total de vocales, consonantes y letras.
    """
    tot_vocales = sum(1 for c in frase if c.lower() in "aeiouáéíóú")
    tot_cons    = sum(1 for c in frase if c.isalpha() and c.lower() not in "aeiouáéíóú")
    return (
        f"Frase analizada: '{frase}'\n"
        f"  Vocales:      {tot_vocales}\n"
        f"  Consonantes:  {tot_cons}\n"
        f"  Total letras: {tot_vocales + tot_cons}"
    )


def calculadora(num1: float, operador: str, num2: float) -> str:
    """
    Tool B: Ejecuta una operación aritmética básica entre dos números.

    Soporta los operadores +, -, * y /. Lanza ValueError si el operador
    no es reconocido, y ZeroDivisionError si se intenta dividir entre cero.

    Args:
        num1:     Primer operando.
        operador: Operador aritmético (+, -, *, /).
        num2:     Segundo operando.

    Returns:
        str: Resultado formateado de la operación.

    Raises:
        ValueError:        Si el operador ingresado no es válido.
        ZeroDivisionError: Si se intenta dividir entre cero.
    """
    if operador == "+":
        resultado = num1 + num2
    elif operador == "-":
        resultado = num1 - num2
    elif operador == "*":
        resultado = num1 * num2
    elif operador == "/":
        if num2 == 0:
            raise ZeroDivisionError("No es posible dividir entre cero.")
        resultado = num1 / num2
    else:
        raise ValueError(f"Operador '{operador}' no reconocido. Usa +, -, * o /.")

    display = int(resultado) if resultado == int(resultado) else resultado
    return f"Resultado: {num1} {operador} {num2} = {display}"


def validar_password(propuesta: str, nombre_usuario: str) -> str:
    """
    Tool B: Valida una propuesta de contraseña según las reglas del sistema.

    Verifica que la contraseña tenga al menos 8 caracteres y que no sea
    idéntica al nombre del usuario activo en la sesión.

    Args:
        propuesta:      La contraseña candidata ingresada por el usuario.
        nombre_usuario: El nombre del usuario en sesión (para comparación).

    Returns:
        str: Mensaje indicando si la contraseña fue aceptada o rechazada,
             con la razón del rechazo si aplica.
    """
    if len(propuesta) < 8:
        return "[Rechazada] La contraseña debe tener al menos 8 caracteres."
    if propuesta == nombre_usuario:
        return "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
    return "[Aceptada] Contraseña válida."


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

# ---------------------------------------------------------------------------
# FASE 2: BUCLE PRINCIPAL DEL AGENTE
# ---------------------------------------------------------------------------

if login_exitoso:
    print("=" * 48)
    print("  Agente iniciado. Escribe un comando.")
    print("  Comandos: ping, contar, fecha_hoy, validar_pass,")
    print("            calculadora, historial [all|clear|buscar], salir")
    print("=" * 48)

    historial_chat: MemoriaAgente = []
    sistema_activo = True
    mensaje        = ""

    while sistema_activo:
        cmd = input(f"\n{usuario_activo}@PseudoAgente> ").strip().lower()

        if cmd == "salir":
            print("Apagando el Agente. ¡Hasta pronto!")
            mensaje = "Se solicitó salir del sistema."
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")
            mensaje = "Se envió el comando 'ping' y se recibió 'pong!' como respuesta."

        elif cmd == "contar":
            frase_usr        = input("Ingresa una frase: ").strip()
            resultado_contar = contar_letras(frase_usr)
            print(resultado_contar)
            mensaje = f"Se contó la frase '{frase_usr}': {resultado_contar.splitlines()[-1]}."

        elif cmd == "fecha_hoy":
            # ¿Cómo viaja el error desde raise hasta except?
            # 1. El bloque try inicia la ejecución protegida.
            # 2. Si el rol es "invitado", la línea 'raise PermissionError(...)' crea un objeto
            #    de excepción y detiene el flujo normal de la función, propagándolo hacia arriba
            #    en la pila de llamadas.
            # 3. El intérprete de Python busca hacia afuera el primer 'except PermissionError'
            #    que lo pueda recibir; en este caso, está en el mismo bloque try/except.
            # 4. Ese bloque 'except' captura el objeto, lo asigna a la variable 'e', y ejecuta
            #    el código de recuperación sin que el programa crashee.
            try:
                if rol_activo == "invitado":
                    raise PermissionError("Privilegios insuficientes")
                hoy     = datetime.date.today()
                mensaje = f"Se solicitó la fecha actual: {hoy.strftime('%d/%m/%Y')}."
                print(f"Fecha actual: {hoy.strftime('%d/%m/%Y')}")
            except PermissionError as e:
                mensaje = f"Se intentó usar 'fecha_hoy' sin privilegios de administrador. Error: {e}"
                print(f"[Acceso Denegado] {e}. Este comando requiere rol de administrador.")

        elif cmd == "validar_pass":
            propuesta_usr  = input("Ingresa tu propuesta de contraseña: ").strip()
            resultado_pass = validar_password(propuesta_usr, usuario_activo)
            print(resultado_pass)
            mensaje = f"Se validó una contraseña. Resultado: {resultado_pass}"

        elif cmd == "calculadora":
            # Punto crítico: el usuario puede ingresar texto en lugar de números.
            # Usamos try/except ValueError para capturar el fallo de float() y
            # try/except ZeroDivisionError / ValueError para los errores dentro de la tool.
            try:
                n1       = float(input("Ingresa el primer número: "))
                op       = input("Ingresa el operador (+, -, *, /): ").strip()
                n2       = float(input("Ingresa el segundo número: "))
                resultado_calc = calculadora(n1, op, n2)
                print(resultado_calc)
                mensaje = f"Operación calculadora: {resultado_calc}"
            except ValueError as e:
                mensaje = f"Error en calculadora por valor inválido: {e}"
                print(f"[Error] {e}")
            except ZeroDivisionError as e:
                mensaje = f"Error en calculadora: {e}"
                print(f"[Error] {e}")

        elif cmd and cmd.split()[0] == "historial":
            partes = cmd.split()

            if len(partes) > 1 and partes[1] == "all":
                resultado_hist = gestionar_historial("all", historial_chat)
                print(resultado_hist)
                mensaje = "Se solicitó ver el historial completo con 'historial all'."

            elif len(partes) > 1 and partes[1] == "clear":
                resultado_hist = gestionar_historial("clear", historial_chat)
                historial_chat.clear()
                print(resultado_hist)
                mensaje = "Se eliminó todo el historial almacenado con 'historial clear'."

            else:
                palabra_clave  = input("Ingresa la palabra clave a buscar: ").strip()
                resultado_hist = gestionar_historial(palabra_clave, historial_chat)
                print(resultado_hist)
                mensaje = f"Se buscó '{palabra_clave}' en el historial."

        else:
            mensaje = f"Se ingresó un comando desconocido: '{cmd}'."
            print(f"[Desconocido] Comando '{cmd}' no reconocido.")
            print("  Comandos válidos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, salir")

        # Registro de la acción en la memoria del agente
        d_log: Recuerdo = {
            "timestamp":   datetime.datetime.now().isoformat(),
            "usuario":     usuario_activo,
            "cmd":         cmd,
            "rol":         rol_activo,
            "descripcion": mensaje,
        }
        historial_chat.append(d_log)
