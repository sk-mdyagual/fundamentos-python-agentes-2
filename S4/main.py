from agente import PseudoAgente, AgenteAdmin
import datetime

rol = ""
i = 0
# Para evaluar los intentos se define el ciclo while, ya que sé cuantos intentos voy a realizar, la variable i inicia en 0 y se va a ir incrementando hasta llegar a 3 cada vez que se ingresa mal el usuario o contraseña.
# Seguido por la solicitud de usuario y contraseña.
# Si el usuario y contraseña son validos el ciclo se rompe y guarda el rol en la variable rol.

while i < 3:
    usuario = input("Ingresa tu usuario: ")
    contrasena = input("Ingresa tu contraseña: ")

    if usuario == "invitado" and contrasena == "1234":
        print("Bienvenido, invitado.")
        rol = "invitado"
        agente = PseudoAgente()
        break

    elif usuario == "admin" and contrasena == "admin123":
        print("Bienvenido, admin.")
        rol = "admin"
        agente = AgenteAdmin()
        break

    # Contador que se va incrementando cada vez que el usuario ingresa un usuario o contraseña incorrectos.
    i += 1


if rol == "invitado" or rol == "admin":
    print("-----------Iniciando el pseudoagente estilo consola--------------------")

    # Banderas/Banderines - Booleanos
    cmd = ""
    sistema_activo = True
    mensaje = ""

    while sistema_activo:
        
        #Control de tokens        
        if agente.tokens <= 0:
            print("[PseudoAgente] No tiene tokens disponibles.")
            sistema_activo = False
        else:
            cmd = input("PseudoAgente>: ").lower()            

            if cmd == "salir":
                mensaje = "Se ha solicitado  terminar la sesión."
                print("[PseudoAgente] Apagando sistemas...")
                sistema_activo = False

            elif cmd == "ping":
                if agente.tokens >= 25:
                    agente.tokens -= 25
                    print("pong~")            
                    mensaje = "Se envió un ping y se devuelve un pong."
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...")

            elif cmd == "contar":
                if agente.tokens >= 2:
                    pal = input("Ingrese una palabra: ").strip().lower()
                    mensaje = agente.contarLetras(pal)
                    print(f"[PseudoAgente] {mensaje}") 
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...")

            elif cmd == "dado":
                if agente.tokens >= 1:
                    mensaje = agente.lanzar_dado()
                    print(f"[PseudoAgente] {mensaje}")
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...")  

            elif cmd == "fecha":
                if agente.tokens >= 2:
                    try:
                        mensaje = agente.mostrarFecha(rol)
                        print(f"[PseudoAgente] {mensaje}")
                    except PermissionError as e:
                        print(e)
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...")      

            elif cmd == "contraseña":
                if agente.tokens >= 2:
                    agente.tokens -= 2
                    contrasena = input("Ingrese una opción de contraseña").lower()
                    if len(contrasena) >= 8 and contrasena != usuario:
                        print("Contraseña válida.")
                        mensaje = "Se ha ingreado la contraseña correctamente"
                    else:
                        mensaje = "La contraseña ingresada no cumple con las condiciones"
                        print(
                            "Debe tener al menos 8 caracteres y no ser igual al nombre de usuario."
                        )
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...") 

            elif cmd == "historial":
                
                    activo = True        

                    while activo:
                        historial = input("Ingrese una de las siguientes opciones: \nHistorial\nHistorial all\nHistorial clear\n o salir ").lower()
                        
                        respuesta = agente.gestionarHistorial(historial)

                        if respuesta == "salir":
                            activo = False
                        else:
                            print(f"[PseudoAgente] {respuesta}")
                            mensaje = respuesta
             

            elif cmd == "calculadora":

                if agente.tokens >= 3:
                    # Se convierte los valores ingresados a float porque input() siempre devuelve texto (string). Y si no se realiza, al realizar la operación en la ejecución genera error por el tipo de dato, el cual debe se int o float.
                    # Error generado: TypeError: unsupported operand type(s) for /: 'float' and 'str'
                    try:
                        numero_uno = float(input("Ingrese el primer número:"))
                        operador = input("Ingrese el operador (+, -, *, /):")
                        numero_dos = float(input("Ingrese el segundo número:"))

                        mensaje = agente.ejecutarCalculadora(numero_uno, operador, numero_dos)
                        print(f"[PseudoAgente] {mensaje}")

                    except ValueError as e:
                        print(e)
                else:
                    print("[PseudoAgente] No tiene tokens suficientes...") 

        #Guardar log en el agente
        agente.registrar_log(cmd, rol, mensaje)      


# Sí el usuario agotó los tres intentos en el Login, se muestra mensaje de cuenta bloqueada.
else:
    print("Acceso denegado. Cuenta bloqueada.")
    mensaje = "Se intento igresar a la cuenta con data errada"

print("-----------Fin del taller--------------------")