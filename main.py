import datetime

print("-" * 40)
print(" " * 12 + "Taller semana 1" + " " * 12)
print("-" * 40)

# Credenciales guardadas en un diccionario
usuarios_validos = {
    "invitado": "algodificil",
    "admin": "algofacil"
}

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
        print(f"Inicio de sesión exitoso, Bienvenido {usuario}!")

        palabraAnalizar = "iniciar"

        while palabraAnalizar != "salir":
            palabraAnalizar = input("Ingrese un comando: ").lower().strip()

            if palabraAnalizar == "salir":
                break

            elif palabraAnalizar == "ping":
                print("pong")
            elif palabraAnalizar == "fecha_hoy":
                # Control de acceso basado en el rol del usuario
                if usuario == "admin":
                    fecha_actual = datetime.datetime.now()
                    print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y %H:%M:%S')}")
                else:
                    print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            elif palabraAnalizar == "validar_pass":
                    nueva_pass = input("Ingresa tu propuesta de contraseña nueva: ")

                    # Validar longitud mínima de 8 caracteres
                    if len(nueva_pass) < 8:
                        print("La contraseña debe tener al menos 8 caracteres.")
            
                    # Comparación propuesta contraseña con la variable usuario que guardamos del login
                    elif nueva_pass == usuario:
                        print("La contraseña no puede ser igual a tu nombre de usuario.")
                    else: 
                        print("Su contraseña cumple con los criterios")
            elif palabraAnalizar == "calculadora":
                            
                    # Necesitamos convertir los inputs (que son strings) a números
                    #se hace para poder aplicar las operaciones matematicas
                    #asi nos considera los datos como numero y no string
                    #float por si desean usar numeros decimales o enteros, 
                    # solo int lo limita a enteros
                    # sino se hace la conversión puede generar error,
                    #  o concatenar en el caso de suma
                    #use el try para manejar una excepción, en caso de que me agreguen letras
                    # el while para pedir hasta que me de un numero uno valido
                    while True:
                        try:
                            #de esta manera se convierte a float la entrada
                            num1 = float(input("Ingresa el primer número: "))
                            # si es valido, corta el while
                            break
                        except ValueError:
                            #en caso de que ingrese letras u otro caracter, controlo el error
                            #el while continua
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
                    elif operador == "-":
                        resultado = num1 - num2
                        print(f"Resultado: {num1} - {num2} = {resultado}")
                    elif operador == "*":
                        resultado = num1 * num2
                        print(f"Resultado: {num1} × {num2} = {resultado}")
                    elif operador == "/":
                        # Manejo especial para división por cero
                        if num2 == 0:
                            print("Error: No se puede dividir por cero.")
                        else:
                            resultado = num1 / num2
                            print(f"Resultado: {num1} ÷ {num2} = {resultado}")
                    else:
                        print("Operador no válido. Usa: +, -, *, /")

            else:
                print("La palabra contiene " + str(len(palabraAnalizar)) + " caracteres.")

                for p in palabraAnalizar:
                    if p in "aeiou":
                        totalVocales += 1
                print("La palabra contiene " + str(totalVocales) + " vocales.")

                for p in palabraAnalizar:
                    if p in "bcdfghjklmnpqrstvwxyz":
                        totalConsonantes += 1
                print("La palabra contiene " + str(totalConsonantes) + " consonantes.")

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