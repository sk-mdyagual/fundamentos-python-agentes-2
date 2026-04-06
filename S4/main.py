from login.login import login
from pseudo_agentes.pseudo_agente_base import PseudoAgente
from pseudo_agentes.agente_admin import AgenteAdmin

intentos = 0
rol_actual = ""
tiene_acceso = False

while intentos < 3 and not tiene_acceso:
    usuario = input("Usuario: ").strip().lower()
    password = input("Contraseña: ").strip()

    login_attempt = login(usuario, password)
    rol_actual = login_attempt["rol"]
    tiene_acceso = login_attempt["access"]

    if not tiene_acceso:
        intentos += 1
        print(f"[Error] Credenciales incorrectas. Te quedan {3 - intentos} intentos.")
    else:
        print(login_attempt["descripcion"])

## Instanciación según rol: Admin obtiene AgenteAdmin, Invitado obtiene PseudoAgente
## Ambas clases comparten la misma interfaz (mismos métodos), pero se comportan diferente
## Esto es polimorfismo en acción
if tiene_acceso:
    if rol_actual == "admin":
        mi_agente = AgenteAdmin()
    else:
        mi_agente = PseudoAgente()

    print(f"\n[Sistema] Agente {mi_agente.nombre} activado. Tipo: {type(mi_agente).__name__}")

    ## Intentar cargar historial previo (librería json + os)
    print(mi_agente.cargar_historial())

    ## Bucle principal: SIN break, usamos bandera pseudo_activo
    pseudo_activo = True

    while pseudo_activo:
        print(f"\n[{mi_agente.nombre}] Tokens disponibles: {mi_agente.tokens}")

        ## Verificar tokens: si se agotan, apagar sin break
        if mi_agente.tokens <= 0:
            message = f"[{mi_agente.nombre}] Muriendo de cansancio. Apagando..."
            print(message)
            mi_agente.registrar_log("sistema", rol_actual, message)
            pseudo_activo = False
            continue

        cmd = input(f"\n{usuario}@{mi_agente.nombre}>: ").strip().lower()

        if cmd == "salir":
            print(f"[{mi_agente.nombre}] Apagando sistemas...")
            mi_agente.registrar_log(cmd, rol_actual, "Sesión finalizada")
            pseudo_activo = False

        elif cmd == "ping":
            resultado = mi_agente.comando_ping()
            print(resultado)
            mi_agente.registrar_log(cmd, rol_actual, "Ping enviado, pong recibido.")

        ## hist: all, clear, o búsqueda por palabra
        elif cmd.startswith("hist"):
            if " " in cmd:
                sub = cmd.split(" ")[-1]
                resultado = mi_agente.gestionar_historial(sub, rol_actual)
                print(resultado)
            else:
                found = []
                word = input("Ingresa la palabra clave a buscar: ").strip().lower()
                for elem in mi_agente.historial_chat:
                    if word in elem["descripcion"].lower():
                        found.append(elem)
                print(f"[{mi_agente.nombre}] Total de coincidencias: {len(found)}")
                if len(found) > 0:
                    for i, elem in enumerate(found):
                        print(f"  {i+1} >>> {elem}")
                else:
                    print(f"[{mi_agente.nombre}] No encontré registros que coincidan.")

        ## Nuevo comando: dado (librería random)
        elif cmd == "dado":
            resultado = mi_agente.lanzar_dado()
            print(resultado)
            mi_agente.registrar_log(cmd, rol_actual, resultado)

        ## Nuevo comando: guardar (librería json - persistir a archivo)
        elif cmd == "guardar":
            resultado = mi_agente.guardar_historial()
            print(resultado)
            mi_agente.registrar_log(cmd, rol_actual, "Historial guardado en archivo JSON")

        ## Nuevo comando: cargar (librería json + os - leer desde archivo)
        elif cmd == "cargar":
            resultado = mi_agente.cargar_historial()
            print(resultado)
            mi_agente.registrar_log(cmd, rol_actual, "Historial cargado desde archivo JSON")

        ## Nuevo comando: exportar (json.dumps para ver el historial formateado)
        elif cmd == "exportar":
            mi_agente.tokens -= 15
            historial_json = json.dumps(mi_agente.historial_chat, indent=2, ensure_ascii=False)
            print(f"[{mi_agente.nombre}] Historial exportado como JSON:")
            print(historial_json)
            mi_agente.registrar_log(cmd, rol_actual, "Historial exportado como JSON formateado")

        ## Nuevo comando: info (librería os + datetime, solo admin)
        elif cmd == "info":
            if rol_actual == "admin":
                resultado = mi_agente.info_sistema()
                print(resultado)
                mi_agente.registrar_log(cmd, rol_actual, "Info del sistema consultada")
            else:
                print(f"[{mi_agente.nombre}] Acceso Denegado. Requiere privilegios de administrador.")
                mi_agente.registrar_log(cmd, rol_actual, "[Denegado] Intento de acceso a info del sistema")

        else:
            print(f"[{mi_agente.nombre}] Comando no existe. Intente de nuevo.")
            mi_agente.registrar_log(cmd, rol_actual, "Comando no reconocido")

    ## Al salir: mostrar historial final y guardar automáticamente
    print(f"\n--- Historial final ({len(mi_agente.historial_chat)} registros) ---")
    for reg in mi_agente.historial_chat:
        print(f"  [{reg['timestamp']}] {reg['cmd']} -> {reg['descripcion']}")

    print(mi_agente.guardar_historial())
    print(f"[Sistema] Sesión terminada. Tokens restantes: {mi_agente.tokens}")

else:
    print("[Sistema] Acceso denegado. Sistema bloqueado.")
