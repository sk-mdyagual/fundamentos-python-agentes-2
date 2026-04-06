# ===========================================================
# Taller Semana 4: Nace la Entidad (POO y Modularización)
# Login y Menú
# César Orlando Ríos Quiroga
# ===========================================================

import datetime
# Importamos las clases (moldes) que definimos en el archivo agente.py
# PseudoAgente es la base, y AgenteAdmin es la versión con privilegios.
from agente import PseudoAgente, AgenteAdmin

# --- MÓDULO DE SEGURIDAD (Sistema de Acceso) ---
# Esta función verificar quién intenta entrar al sistema.
def sistema_login():
    # Definimos los usuarios válidos y sus contraseñas.
    usuarios = {
        "admin": "admin_1234",
        "invitado": "pass_1234"
    }
    
    # Variables de control para el proceso de entrada
    intentos = 0            # inicia en 0 y se incrementa por cada intento hasta 3
    sesion_activa = False   # Inica en False y cambia a True si los datos son correctos
    rol_final = ""          # variable para almacenar el usuario 'admin' o 'invitado'

    # CICLO DE LOGIN (Bucle While): 
    # Ciclo pafa que el usuario coloque los datos bien o 
    # o hasta que se le acaben los 3 intentos permitidos.
    while intentos < 3 and not sesion_activa:
        # Mostramos dinámicamente el número de intento actual (Requerimiento Taller 3)
        print(f"\n--- INICIO DE SESIÓN (Intento {intentos + 1}/3) ---")
        
        # Pedimos los datos al usuario y se usa .strip() elimina espacios accidentales y .lower() pasa todo a minúsculas.
        user = input("Usuario: ").strip().lower()
        password = input("Contraseña: ").strip()

        # ESTRUCTURA DE DECISIÓN (Validación):
        # Primero revisamos si el nombre de usuario existe en nuestras llaves (keys)
        # y luego si la contraseña escrita coincide con el valor guardado.
        if user in usuarios and usuarios[user] == password:
            print(f"\n[Sistema] Acceso concedido. Bienvenido, {user.upper()}.")
            sesion_activa = True # Esto hará que el ciclo 'while' termine con éxito
            rol_final = user
        else:
            # Si los datos están mal, sumamos 1 al contador de errores
            intentos += 1 
            print(f"[Error] Credenciales incorrectas. Te quedan {3 - intentos} intentos.")

    # Al terminar, devolvemos el resultado: si entró y bajo qué rol
    return sesion_activa, rol_final

# --- PROGRAMA PRINCIPAL (Lógica de Ejecución) ---
# Esta es la estructura principal del progrma una vez que el usuario ha sido validado.
def main():
    # Primero llamamos al sistema de seguridad y esperamos su respuesta
    acceso, rol = sistema_login()

    # Si el acceso es verdadero (True), procedemos a llamar al agente
    if acceso:
        # Se crea el el objeto basándonos segun el rol del usuario.
        # Si es admin, usamos la clase especializada; si no, la clase normal.
        if rol == "admin":
            mi_agente = AgenteAdmin("Athena-Alpha")
        else:
            mi_agente = PseudoAgente("Athena-Beta")

        print(f"Agente {mi_agente.nombre} activado y listo para recibir órdenes.\n")

        # BUCLE DE CONTROL (Ciclo de Vida):
        # El agente funcionará en un ciclo hasta que se apague o se acaben los Tokens.
        # No se uasará 'break' para salir; usaremos una variable booleana de control.
        sistema_encendido = True
        
        while sistema_encendido:
            # Se moestra cuánta "batería" cuantos Tokens le queda
            print(f"\n⚡ Energía del Agente: {mi_agente.tokens} tokens")

            # Si el agente se queda sin tokens (0 o menos), se apaga automáticamente.
            if mi_agente.tokens <= 0:
                print(f"[{mi_agente.nombre}] Mi energía ha llegado al límite. Apagando sistemas...")
                sistema_encendido = False # Cambiamos el estado para que el 'while' no se repita
                continue # Regresa a la evaluación del bucle para salir limpiamente

            # MENÚ DE OPCIONES: Mostramos al usuario los comandos que puede escribir
            print("-" * 60) # muetra por pantalla el "-" 60 veces
            print("Comandos: ping, contar, fecha_hoy, validar_pass, calculadora, lanzar_dado, historial, salir")
            cmd = input(f"{rol}@{mi_agente.nombre}>: ").strip().lower()

            # LÓGICA DE COMANDOS: se valida segun la selección del usuario

            # Opción "Salir" del programa de forma voluntaria
            if cmd == "salir":
                print(f"[{mi_agente.nombre}] Desactivando protocolos. ¡Hasta pronto!")
                mi_agente.registrar_log(cmd, rol, "El usuario finalizó la sesión manualmente")
                sistema_encendido = False 

            # Opción "ping"
            elif cmd == "ping":
                mi_agente.tokens -= 20 # Realizar acciones consume 20 Tokens
                print("pong")
                mi_agente.registrar_log(cmd, rol, "Respuesta de red exitosa")

            # Opción "Contar" letras y vocales de una palabra
            elif cmd == "contar":
                palabra = input("Ingresa la palabra a contar: ").strip()
                # Le pedimos al objeto agente que procese la palabra
                print(mi_agente.contar_letras(palabra, rol))

            # Opción "lanzar_Dado"
            elif cmd == "lanzar_dado":
                print(mi_agente.lanzar_dado(rol))

            # Opción validación de contraseñas
            elif cmd == "validar_pass":
                # Mostramos el mensaje exacto solicitado para guiar al usuario
                pwd = input("Ingrese contraseña a evaluar (mínimo 8 caracteres, incluir mayúscula, minúscula y número): ").strip()
                print(mi_agente.validar_pass(pwd, rol))

            # Opción de "Calculadora"
            elif cmd == "calculadora":
                # Primero solicitamos la operación que desea realizar
                print("\n--- Módulo de Calculadora ---")
                op = input("Operación (+, -, *, /): ").strip()
                
                # MANEJO DE ERRORES (Try-Except):
                # Si el usuario escribe letras en vez de números, 
                # se toma el error para que el programa no se cierre bruscamente.
                try:
                    num1 = float(input("Número 1: "))
                    num2 = float(input("Número 2: "))
                    # El agente procesa el cálculo y maneja internamente la división por cero
                    print(mi_agente.ejecutar_calculo(op, num1, num2, rol))
                except ValueError:
                    print("[Error] Entrada inválida. Por favor, ingresa solo números.")

            # Opción "fecha_hoy" solo para le Administrador
            elif cmd == "fecha_hoy":
                # Solo el administrador tiene permiso para ver la fecha
                if rol == "admin":
                    hoy = datetime.datetime.now().strftime('%d/%m/%Y')
                    print(f"La fecha del sistema es: {hoy}")
                    mi_agente.registrar_log(cmd, rol, f"Consulta exitosa de fecha: {hoy}")
                else:
                    # Si el rol es 'invitado', no se le presenta la opción
                    print("[Bloqueado] Acceso Denegado. Se requieren privilegios de Administrador.")
                    mi_agente.registrar_log(cmd, rol, "Intento de acceso a fecha sin permisos")

            # Opción "historial"
            elif cmd.startswith("historial"):
                # Verificamos si escribieron algo como 'historial clear' o solo 'historial'
                sub_op = cmd.split(" ")[-1] if " " in cmd else "all"
                # Gracias a la herencia, si es admin, el costo de tokens será 0
                print(mi_agente.gestionar_historial(sub_op, rol))

            # Si el usuario escribe algo que no está en la lista
            else:
                print(f"[{mi_agente.nombre}] Comando desconocido. Por favor, intenta de nuevo.")

    else:
        # Si el ciclo de login terminó pero la sesión no se activó
        print("\n[Sistema] ALERTA: Se han agotado los 3 intentos. Sistema bloqueado por seguridad.")

# Esta línea asegura que el programa solo comience si ejecutamos este archivo directamente.
if __name__ == "__main__":
    main()