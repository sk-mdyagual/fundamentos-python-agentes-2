# 🛠️ Taller Semana 4: Nace la Entidad (POO y Modularización)
# Oscar Danilo Sanabria Sogamoso

from agente import AgenteAdmin, PseudoAgente

print("----- Sistema de Agente Seguro -----")

# Perfiles del sistema (usuario, password, rol)
# Esta constante esteblece un diccionario de datos con las credenciales de acceso.
CREDENCIALES = {
    "invitado": {"password": "user12", "rol": "invitado"},
    "admin": {"password": "admon12", "rol": "admin"},
}

usuario_actual = ""
rol_actual = ""
acceso_concedido = False
intentos = 0
agente = None

# Este contador evita intentos infinitos: cada falla suma 1, y al llegar a 3
# cortamos el login para proteger el sistema de intentos repetidos.
while intentos < 3 and not acceso_concedido:
    usuario_ingresado = input("Usuario: ").strip().lower()
    password_ingresada = input("Contrasena: ").strip()
    # El método strip() elimina espacios en blanco al inicio y al final de la cadena, lo que ayuda a evitar errores de ingreso por espacios accidentales. El método lower() convierte el texto a minúsculas, permitiendo que el ingreso del usuario no sea sensible a mayúsculas o minúsculas.
    if (
        usuario_ingresado in CREDENCIALES
        and password_ingresada == CREDENCIALES[usuario_ingresado]["password"]
    ):
        acceso_concedido = True
        usuario_actual = usuario_ingresado
        rol_actual = CREDENCIALES[usuario_ingresado]["rol"]
        print(f"[OK] Bienvenido, {usuario_actual}. Rol: {rol_actual}")
    else:
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Error] Credenciales invalidas. Intentos restantes: {restantes}")

if not acceso_concedido:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
else:
    if rol_actual == "admin":
        agente = AgenteAdmin(usuario_actual)
    else:
        agente = PseudoAgente(usuario_actual)

    print("\nAgente activo. Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, lanzar_dado, historial, salir")
    sistema_activo = True
    mensaje = ""

    while sistema_activo:
        if agente.tokens <= 0:
            print(f"[Alerta] {agente.nombre} se quedó sin tokens. Cerrando sistema.")
            sistema_activo = False
            continue

        cmd_entrada = input("PseudoAgente>: ").strip().lower()
        partes_cmd = cmd_entrada.split()
        try:
            cmd = partes_cmd[0]
        except IndexError:
            print("[Error] Debes ingresar un comando.")
            mensaje = "Entrada vacía de comando."
            continue

        registrar_en_historial = True

        if cmd == "salir":
            print("Apagando agente. Hasta luego.")
            mensaje = "Se ha solicitado terminar la sesión."
            sistema_activo = False

        elif cmd == "ping":
            try:
                mensaje = agente.ping()
                print(mensaje)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "contar":
            frase = input("Ingresa una frase: ").strip().lower()
            try:
                mensaje = agente.contar_letras(frase)
                print(mensaje)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "fecha_hoy":
            try:
                fecha_actual = agente.fecha_hoy(rol_actual)
                print(f"Fecha actual: {fecha_actual}")
                mensaje = f"La fecha actual es: {fecha_actual}"
            except PermissionError as e:
                print(f"[Acceso Denegado] {e}")
                mensaje = str(e)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "validar_pass":
            nueva_password = input("Ingresa una nueva propuesta de contrasena: ").strip()
            try:
                mensaje = agente.validar_password(nueva_password, usuario_actual)
                print(mensaje)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "calculadora":
            # La función input() retorna texto. Si no convertimos a float, Python intentaria
            # sumar/castear strings y tendriamos errores de tipo en operaciones matematicas.
            n1_txt = input("Ingresa el primer numero: ").strip()
            operador = input("Ingresa el operador (+, -, *, /): ").strip()
            n2_txt = input("Ingresa el segundo numero: ").strip()

            # El bloque try-except captura errores de conversion (por ejemplo, si el usuario ingresa "abc" en lugar de un numero)
            try:
                mensaje = agente.calculadora(n1_txt, operador, n2_txt)
                print(mensaje)
            except ValueError as e:
            # Si ocurre un error de conversion, mostramos un mensaje de error y usamos 'continue' para saltar a la siguiente iteracion del bucle, evitando que el programa se caiga.
                print(f"[Error] {e}")
                mensaje = str(e)
            except ZeroDivisionError as e:
                print(f"[Error] {e}")
                mensaje = str(e)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "lanzar_dado":
            try:
                mensaje = agente.lanzar_dado()
                print(mensaje)
            except RuntimeError as e:
                print(f"[Alerta] {e}")
                mensaje = str(e)
                sistema_activo = False

        elif cmd == "historial":
            # Usando .split() podemos dividir el comando en sus partes para verificar si hay parámetros
            if len(partes_cmd) > 1:
                parametro = partes_cmd[1].lower()
                if parametro == "clear":
                    resultado_historial = agente.gestionar_historial("clear")
                    print(resultado_historial)
                    mensaje = "Historial eliminado."
                    registrar_en_historial = False
                elif parametro == "all":
                    try:
                        resultado_historial = agente.gestionar_historial("all")
                        print(resultado_historial)
                        mensaje = "Se mostró el historial completo."
                    except RuntimeError as e:
                        print(f"[Alerta] {e}")
                        mensaje = str(e)
                        sistema_activo = False
                else:
                    print("[PseudoAgente] Parámetro desconocido. Use 'historial all' o 'historial clear'.")
                    mensaje = "Parámetro de historial desconocido."
            else:
                # Modo búsqueda: el usuario ingresa una palabra clave
                palabra_clave = input("Ingresa la palabra clave a buscar: ").strip().lower()
                try:
                    resultado_historial = agente.gestionar_historial(palabra_clave)
                    print(resultado_historial)
                    if "No encontré" in resultado_historial:
                        mensaje = f"Búsqueda realizada por: {palabra_clave} (sin resultados)."
                    else:
                        mensaje = f"Búsqueda realizada por: {palabra_clave} (con resultados)."
                except RuntimeError as e:
                    print(f"[Alerta] {e}")
                    mensaje = str(e)
                    sistema_activo = False

        else:
            print("Comando desconocido, intenta de nuevo.")
            mensaje = "Comando desconocido."

        # Registrar cada acción en el historial del agente (excepto historial clear que ya lo maneja)
        if registrar_en_historial and mensaje and agente is not None:
            agente.registrar_log(cmd_entrada, rol_actual, mensaje)

        if agente.tokens <= 0:
            print(f"[Alerta] {agente.nombre} se quedó sin tokens. Cerrando sistema.")
            sistema_activo = False
