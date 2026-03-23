import datetime

print("-" * 40)
print(" " * 12 + "Taller semana 1" + " " * 12)
print("-" * 40)

# Credenciales guardadas en un diccionario
usuarios_validos = {"invitado": "algodificil", "admin": "algofacil"}
# Diccionario para persistir el historial

historial_chat = []

intentos = 0
max_intentos = 3
totalVocales = 0
totalConsonantes = 0

# El while valida que intentos sea menor a 3, porque inicie en cero
while intentos < max_intentos:
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()

    # Verificar si las credenciales son correctas
    if usuario in usuarios_validos and usuarios_validos[usuario] == contraseña:
        historial_chat.append(
            {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cmd": "login",
                "rol": {usuario},
                "descripcion": "Inicio de sesión exitoso.",
            }
        )
        print(f"Inicio de sesión exitoso, Bienvenido {usuario}!")

        palabraAnalizar = "iniciar"

        while palabraAnalizar != "salir":
            palabraAnalizar = input("Ingrese un comando: ").lower().strip()

            if palabraAnalizar == "salir":
                break

            elif palabraAnalizar == "ping":
                print("pong")
                historial_chat.append(
                    {
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "cmd": "ping",
                        "rol": {usuario},
                        "descripcion": "Se envió un ping y se devuelve un pong.",
                    }
                )
            elif palabraAnalizar == "fecha_hoy":
                # Control de acceso basado en el rol del usuario
                if usuario == "admin":
                    fecha_actual = datetime.datetime.now()
                    print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y %H:%M:%S')}")
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "fecha_hoy",
                            "rol": {usuario},
                            "descripcion": "Se envió fecha_hoy y se devuelve un mensaje con la fecha de hoy",
                        }
                    )
                else:
                    print(
                        "[Acceso Denegado] Este comando requiere privilegios de administrador."
                    )
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "fecha_hoy",
                            "rol": {usuario},
                            "descripcion": "Se envió fecha_hoy y se devuelve un mensaje indicando que el usuario no tiene privilegio para ejecutar esa acción",
                        }
                    )
            elif palabraAnalizar == "validar_pass":
                nueva_pass = input("Ingresa tu propuesta de contraseña nueva: ")

                # Validar longitud mínima de 8 caracteres
                if len(nueva_pass) < 8:
                    print("La contraseña debe tener al menos 8 caracteres.")
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "validar_pass",
                            "rol": {usuario},
                            "descripcion": "Se envió validar_pass y se devuelve un mensaje indicando que La contraseña debe tener al menos 8 caracteres",
                        }
                    )
                # Comparación propuesta contraseña con la variable usuario que guardamos del login
                elif nueva_pass == usuario:
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "validar_pass",
                            "rol": {usuario},
                            "descripcion": "Se envió validar_pass y se devuelve un mensaje que indica que La contraseña no puede ser igual a tu nombre de usuario",
                        }
                    )
                    print("La contraseña no puede ser igual a tu nombre de usuario.")
                else:
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "validar_pass",
                            "rol": {usuario},
                            "descripcion": "Se envió validar_pass y se devuelve un mensaje que indica que Su contraseña cumple con los criterios",
                        }
                    )
                    print("Su contraseña cumple con los criterios")

            elif palabraAnalizar == "historial":
                print("Si desea ver el historial completo escriba: historial all")
                print("Si desea borrar el histroial: historial clear")
                print("Si quiere hacer una busqueda: historial")
                historial = input("Escriba su opción ").strip()

                if historial == "historial all":
                    print(historial_chat)
                elif historial == "historial clear":
                    historial_chat.clear()
                    print ("Historial eliminado")
                elif historial == "historial":
                    palabra_clave = (
                        input("Escriba la palabra a buscar: ").strip().lower()
                    )

                    contador = 0
                    # In verifica si una palabra, letra o en este caso entrada está contenida dentro de descripción.

                    for item in historial_chat:
                        # aca controlo para que no se rompa en caso de estar vacio
                        descripcion = item.get(
                            "descripcion", ""
                        ).lower()  # evita errores

                        if palabra_clave in descripcion:
                            contador += 1
                            print(
                                f"[{item.get('rol', 'desconocido')}] {item.get('descripcion', '')}"
                            )

                    if contador == 0:
                        print(
                            "[PseudoAgente] No encontré registros que coincidan con esa palabra."
                        )
                    else:
                        print(f"\nTotal de coincidencias: {contador}")
                else:
                    print("Opción no valida, se retornara al menú principal")
            elif palabraAnalizar == "calculadora":

                # Necesitamos convertir los inputs (que son strings) a números
                # se hace para poder aplicar las operaciones matematicas
                # asi nos considera los datos como numero y no string
                # float por si desean usar numeros decimales o enteros,
                # solo int lo limita a enteros
                # sino se hace la conversión puede generar error,
                #  o concatenar en el caso de suma
                # use el try para manejar una excepción, en caso de que me agreguen letras
                # el while para pedir hasta que me de un numero uno valido
                while True:
                    try:
                        # de esta manera se convierte a float la entrada
                        num1 = float(input("Ingresa el primer número: "))
                        # si es valido, corta el while
                        break
                    except ValueError:
                        # en caso de que ingrese letras u otro caracter, controlo el error
                        # el while continua
                        print("Error: ingrese un número válido.")
                operador = input("Ingresa el operador (+, -, *, /): ").strip()

                # el while para pedir hasta que me de un numero dos valido
                # aca, se repite al while inicial o del primer numero,
                #  solo que para el numero dos
                while True:
                    try:
                        num2 = float(input("Ingresa el segundo número: "))
                        break
                    except ValueError:
                        print("Error: ingrese un número válido.")

                # Evaluamos qué operación realizar usando
                if operador == "+":
                    resultado = num1 + num2
                    print(f"Resultado: {num1} + {num2} = {resultado}")
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "calcauladora",
                            "rol": {usuario},
                            "descripcion": "El usuario realizo una suma",
                        }
                    )

                elif operador == "-":
                    resultado = num1 - num2
                    print(f"Resultado: {num1} - {num2} = {resultado}")
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "calcauladora",
                            "rol": {usuario},
                            "descripcion": "El usuario realizo una resta",
                        }
                    )
                elif operador == "*":
                    resultado = num1 * num2
                    print(f"Resultado: {num1} × {num2} = {resultado}")
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "calcauladora",
                            "rol": {usuario},
                            "descripcion": "El usuario realizo una multiplicación",
                        }
                    )
                elif operador == "/":
                    historial_chat.append(
                        {
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cmd": "calcauladora",
                            "rol": {usuario},
                            "descripcion": "El usuario realizo una división",
                        }
                    )
                    # Manejo especial para división por cero
                    if num2 == 0:
                        print("Error: No se puede dividir por cero.")
                    else:
                        resultado = num1 / num2
                        print(f"Resultado: {num1} ÷ {num2} = {resultado}")
                else:
                    print("Operador no válido. Usa: +, -, *, /")

            else:
                print(
                    "La palabra contiene " + str(len(palabraAnalizar)) + " caracteres."
                )

                for p in palabraAnalizar:
                    if p in "aeiou":
                        totalVocales += 1
                print("La palabra contiene " + str(totalVocales) + " vocales.")

                for p in palabraAnalizar:
                    if p in "bcdfghjklmnpqrstvwxyz":
                        totalConsonantes += 1
                print("La palabra contiene " + str(totalConsonantes) + " consonantes.")
                historial_chat.append(
                    {
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "cmd": "por defecto",
                        "rol": {usuario},
                        "descripcion": "Se analizo cuantas vocales contiene la palabra ingresada, cuantas consonantes y cuantos caracteres",
                    }
                )
        break

    else:
        # si no es correcto, se aumenta el contador
        intentos += 1
        # si los intentos no supera el maximo (3)
        if intentos < max_intentos:
            print("Credenciales incorrectas. Intente nuevamente.")
        else:
            # entra aca cuando tenga 3, indica que completo los intentos,
            #  regresa al while y termina
            print("\n [Alerta] Usuario bloqueado. Cerrando sistema.")

print("Programa terminado.")
