import datetime
from agente import PseudoAgente, AgenteAdmin, Recuerdo

# 1. LÓGICA DE INICIO (LOGIN)
u_admin, p_admin = "administrador", "67890"
u_inv, p_inv = "invitado", "12345"

intentos = 0
tiene_acceso = False
usuario_actual = ""
rol_actual = ""

while intentos < 3 and not tiene_acceso:
    u = input("Ingresa tu usuario: ").strip().lower()
    p = input("Ingresa tu contraseña: ").strip().lower()

    if u == u_admin and p == p_admin:
        rol_actual = "administrador"
        usuario_actual = u
        tiene_acceso = True
        print(f"Inicio exitoso. Bienvenido, tu rol es: {rol_actual}")
    elif u == u_inv and p == p_inv:
        rol_actual = "invitado"
        usuario_actual = u
        tiene_acceso = True
        print(f"Inicio exitoso. Bienvenido, tu rol es: {rol_actual}")
    else:
        intentos += 1
        print("Datos incorrectos")

if not tiene_acceso:
    print("Alerta: Usuario bloqueado. Cerrando sistema.")
    exit()

# 2. INSTANCIACIÓN DEL AGENTE

# Si es admin, usamos la clase hija. Si es invitado, la clase padre.
if rol_actual == "administrador":
    mi_agente = AgenteAdmin(nombre="AdminBot_Pro")
else:
    mi_agente = PseudoAgente(nombre="GuestBot_Lite")

print(f"\n[Sistema] Instancia creada: {type(mi_agente).__name__}")
print(f"[Sistema] Nombre del agente: {mi_agente.nombre} | Batería: {mi_agente.tokens} tokens")

# 3. BUCLE PRINCIPAL (MONITOREA BATERÍA Y ESTADO)

ejecutando = True

# El bucle depende del estado del booleano Y de los tokens del agente. 
# Si los tokens caen a 0, el while detecta la condición y se apaga suavemente sin usar "break".
while ejecutando and mi_agente.tokens > 0:
    print(f"\n--- Batería restante: {mi_agente.tokens} ---")
    print("Comandos: ping | pong | contar | fecha | dado | validarcontraseña | calculadora | historial | salir")
    
    comando = input("Solicitud: ").strip().lower()
    
    if comando == "salir":
        print("Apagando agente por petición del usuario....")
        ejecutando = False # Termina el bucle de forma limpia
    else:
        try:
            mensaje_log = ""
            
            if comando in ["ping", "pong"]:
                mensaje_log = mi_agente.tool_ping_pong(comando)
                print(mensaje_log)
                
            elif comando == "contar":
                pal = input("Ingresa una palabra: ")
                mensaje_log = mi_agente.tool_contar(pal)
                print(mensaje_log)
                
            elif comando == "dado":
                mensaje_log = mi_agente.tool_lanzar_dado()
                print(mensaje_log)

            elif comando == "fecha":
                mensaje_log = mi_agente.tool_fecha_hoy(rol_actual)
                print(mensaje_log)

            elif comando == "validarcontraseña":
                p_in = input("Ingrese una nueva contraseña: ")
                mensaje_log = mi_agente.tool_validar_password(p_in, usuario_actual)
                print(mensaje_log)

            elif comando == "calculadora":
                try:
                    n1 = float(input("Ingrese el primer numero: "))
                    op = input("Ingresa el operador (+,-,*,/): ")
                    n2 = float(input("Ingrese el segundo numero: "))
                    mensaje_log = mi_agente.tool_calculadora(n1, op, n2)
                    print(mensaje_log)
                except ValueError:
                    mensaje_log = "Error de entrada: Valor numérico esperado."
                    print(mensaje_log)
                except ZeroDivisionError as e:
                    mensaje_log = f"Error matemático: {e}"
                    print(mensaje_log)

            elif comando == "historial":
                h_all = input("¿Ver todo (all), limpiar (clear) o buscar (search)?: ").strip().lower()
                filtro_busqueda = ""
                if h_all == "search":
                    filtro_busqueda = input("Palabra clave a buscar: ")
                
                # NOTA: Ya no le pasamos 'historial_chat', el objeto gestiona su propia memoria internamente.
                mensaje_log = mi_agente.tool_gestionar_historial(h_all, filtro_busqueda)
                print(mensaje_log)

            else:
                mensaje_log = "Comando no reconocido."
                print(mensaje_log)

            # Registro en la memoria INTERNA del agente
            nuevo_recuerdo: Recuerdo = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "comando": comando,
                "rol": rol_actual,
                "descripcion": mensaje_log
            }
            mi_agente.historial_chat.append(nuevo_recuerdo)

        # Capturamos el error disparado por la falta de permisos de Fecha
        except PermissionError as e:
            print(f"🚫 ERROR: {e}")
            mi_agente.historial_chat.append({
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "comando": comando, "rol": rol_actual, "descripcion": f"Fallo de permisos: {e}"
            })
            
        # Capturamos el error disparado cuando los tokens bajan de cero (Batería muerta)
        except SystemError as e:
            print(f"\n☠️ APAGADO DE EMERGENCIA: {e}")
            # Al llegar aquí, mi_agente.tokens ya es 0, por lo que el while no se repetirá.

# Mensaje final después de salir del while
if mi_agente.tokens <= 0:
    print("El sistema se ha apagado porque el agente se quedó sin energía.")
else:
    print("Programa finalizado correctamente.")