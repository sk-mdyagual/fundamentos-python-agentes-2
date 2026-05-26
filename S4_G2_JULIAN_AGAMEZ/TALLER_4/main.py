"""
main.py — Punto de entrada del PseudoAgente (Taller Semana 4)

Responsabilidades:
  - Sistema de login (hasta 3 intentos)
  - Instanciación del agente según el rol (AgenteAdmin o PseudoAgente)
  - Bucle principal de comandos con monitoreo de tokens
"""

from agente import PseudoAgente, AgenteAdmin, login

# ---------------------------------------------------------------------------
# FASE 1: AUTENTICACIÓN
# ---------------------------------------------------------------------------
print("=" * 52)
print("  Sistema de Agente — Autenticación requerida")
print("=" * 52)

intentos = 0
tiene_acceso = False
usuario_activo = ""
rol_activo = ""

while intentos < 3 and not tiene_acceso:
    usuario_input = input("\nUsuario: ").strip()
    pass_input = input("Contraseña: ").strip()

    resultado_login = login(usuario_input, pass_input)

    if resultado_login["access"]:
        tiene_acceso = True
        usuario_activo = usuario_input
        rol_activo = resultado_login["rol"]
        print(resultado_login["descripcion"])
    else:
        intentos += 1
        print(resultado_login["descripcion"])
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Alerta] Intentos restantes: {restantes}")

if not tiene_acceso:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")

# ---------------------------------------------------------------------------
# FASE 2: BUCLE PRINCIPAL
# ---------------------------------------------------------------------------
if tiene_acceso:
    # Si el usuario es "admin" se instancia AgenteAdmin (sin costo en historial).
    # Si es "invitado" se instancia PseudoAgente normal.
    if rol_activo == "admin":
        mi_agente: PseudoAgente = AgenteAdmin("Athena")
    else:
        mi_agente = PseudoAgente("Athena")

    print("\n" + "=" * 52)
    print(f"  Agente '{mi_agente.nombre}' iniciado. Bienvenido, {usuario_activo}.")
    print("  Comandos disponibles:")
    print("    ping | contar | fecha_hoy | validar_pass")
    print("    calculadora | historial [all|clear] | dado | salir")
    print("=" * 52)

    sistema_activo = True

    while sistema_activo:
        print(f"\n[{mi_agente.nombre}] Tokens disponibles: {mi_agente.tokens}")

        # El agente "muere" si se queda sin tokens; se apaga sin usar break
        if mi_agente.tokens <= 0:
            print(f"[{mi_agente.nombre}] Agente agotado. Sin tokens suficientes. Apagando...")
            sistema_activo = False
            continue

        cmd = input(f"{usuario_activo}@PseudoAgente> ").strip().lower()

        if cmd == "salir":
            mi_agente.registrar_log("salir", rol_activo, "Se ha solicitado terminar la sesión.")
            print(f"[{mi_agente.nombre}] Apagando sistemas. ¡Hasta pronto!")
            sistema_activo = False

        elif cmd == "ping":
            print(mi_agente.ping(rol_activo))

        elif cmd == "contar":
            frase_usr = input("Ingresa una frase: ").strip()
            print(mi_agente.contar_letras(frase_usr, rol_activo))

        elif cmd == "fecha_hoy":
            try:
                print(mi_agente.fecha_hoy(rol_activo))
            except PermissionError as e:
                print(f"[Acceso Denegado] {e}")

        elif cmd == "validar_pass":
            propuesta_usr = input("Ingresa tu propuesta de contraseña: ").strip()
            print(mi_agente.validar_password(propuesta_usr, usuario_activo, rol_activo))

        elif cmd == "calculadora":
            try:
                n1 = float(input("Ingresa el primer número: "))
                op = input("Ingresa el operador (+, -, *, /): ").strip()
                n2 = float(input("Ingresa el segundo número: "))
                print(mi_agente.calculadora(n1, op, n2, rol_activo))
            except ValueError as e:
                print(f"[Error] {e}")
            except ZeroDivisionError as e:
                print(f"[Error] {e}")

        elif cmd and cmd.split()[0] == "historial":
            partes = cmd.split()
            if len(partes) > 1:
                print(mi_agente.gestionar_historial(partes[1], rol_activo))
            else:
                print(f"[{mi_agente.nombre}] Especifica la operación: historial all | historial clear")

        elif cmd == "dado":
            print(mi_agente.lanzar_dado(rol_activo))

        else:
            mi_agente.registrar_log(cmd, rol_activo, f"Comando desconocido: '{cmd}'.")
            print(f"[Desconocido] Comando '{cmd}' no reconocido.")
            print("  Válidos: ping, contar, fecha_hoy, validar_pass, calculadora, historial, dado, salir")
