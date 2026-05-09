#Taller Semana 1 Fundamentos de Python para Agentes - Doris Mosquera Lozano
#doris.mosquera@sofka.com.co - DMosqueraLSofka

# Importaciones
import hashlib # Libreria para el manejo de usuarios y contraseñas almacenadas
import getpass # Libería para ocultar los caracteres de la contraseña ingresada por consola
from datetime import date # Librería para el manejo de fechas y horas


# Funciones
## Función para solicitar  al usuario números para el comando calculadora, controlando el error que si el usuario ingresa letras y/o caracteres especiales, le indique que ingrese un número váldido
def ingresar_numero(num):
    while True:
        try:            
            ## Se selecciona el tipo de dato float dado que el taller no especifica el tipo numérico y además, la división puede tener resultado número decimales y usar el tipo int
            ## no sería correcto el resultado. Igual permite operaciones con todo número que ingrese el usuario
            ## El usuario podrá ingresar números con comas (ej: 7,9), indicando que es un número decimal (7.9) y el sistema reemplazará la coma por un punto (método replace)
            return float(input(num).replace(",", "."))
        except ValueError: ## Con la ayuda de IA se implenta el control de errores, cuando el usuario no proporcione un número válido
            print("❌ El número ingresado no es válido. Intenta de nuevo\n")


## Función para ejecutar la calculadora, cuando el comando cmd sea igual a calculador
def calculadora():
    calculadora_activa = True
    while calculadora_activa:
        print("\n\t...::Menú de operaciones::...")
        print("\t\t1. ➕ Suma")
        print("\t\t2. ➖ Resta")
        print("\t\t3. ✖️  Multiplicación")
        print("\t\t4. ➗ División")
        print("\t\t5. 🏁 Salir")

        opcion = input("\nSelecciona una opción (1-5): ")

        match opcion: ##Se implementa el match/case para las distintas opciones de la calculadora.
            case "1":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("-------------------------------------------")
                print(f"Resultado: {num1} + {num2} = {num1 + num2} 📌")
                print("-------------------------------------------")
            case "2":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("-------------------------------------------")
                print(f"Resultado: {num1} - {num2} = {num1 - num2} 📌")
                print("-------------------------------------------")
            case "3":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("-------------------------------------------")
                print(f"Resultado: {num1} × {num2} = {num1 * num2} 📌")
                print("-------------------------------------------")
            case "4":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("-------------------------------------------")
                if num2 != 0:
                    print(f"Resultado: {num1} ÷ {num2} = {num1 / num2} 📌")
                    print("-------------------------------------------")
                else:
                    # Control de la división por cero. Es una indeterminanción matemática 
                    # por lo que al presentarse no hay un resultado para dicha operación
                    print("❌ ¡Upppppssss! No está permitida la división por cero.")
                    print("-------------------------------------------")
            case "5":
                print("\n😁  Gracias por usar nuesta calculadora 😁\n")
                calculadora_activa = False
            case _:
                print("⚠️ Opción inválida. Seleccione una opción")


# Usuarios y contraseñas
usuarios = {"admin": "1234", "user": "abcd", "ejecutivo": "4321"}

# Hash --- Con la ayuda de la IA se implementa el hash para hacer más profesional el código y el manejo de los usuarios y sus contraseñas
for u in usuarios:
    usuarios[u] = hashlib.sha256(usuarios[u].encode()).hexdigest()

login_exitoso = False
usuario_actual = ""
intento = 0
max_intentos = 3

# Fase 1: Capa de Seguridad (Login)
print("""
      \n..::Bienvenid@ a tu PythonAgente::..\n
      Iniciemos sesión. 😎\n
    ---------------------------------------------------------------------------------------------------------------------------- 
    🚨 Ten presente que sólo cuentas con 3 intentos de inicio de sesión. Superado estos intentos, tu usuario será bloqueado. 🚨
    ----------------------------------------------------------------------------------------------------------------------------
    """)
while intento < max_intentos and not login_exitoso:
    print("\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")
    usuario = input("\n👤  Usuario: ").lower()
    ## Usando la librería getpass, permite que el usuario mientras escribe la contraseña esta se oculte (no muestra los carácteres de la contraseña en pantalla)
    password = getpass.getpass(" ░  Contraseña: ")
    hash_password_ingresada = hashlib.sha256(password.encode()).hexdigest()
    rol = "admin" if usuario == "admin" else "invitado"

    if usuario in usuarios and hash_password_ingresada == usuarios[usuario]:
        print(f"\n🎉 ¡Acceso Concedido! 🎉 - Bienvenido/a {usuario.capitalize()}")
        login_exitoso = True        
    else:
        intento += 1
        if intento < max_intentos:
            print(
                f"\n❌ Datos incorrectos. Te quedan {max_intentos - intento} intento(s) para iniciar de sesión."
            )
        else:
            print("\n❌ ¡Acceso Denegado!. Superaste la cantidad máxima de intentos.\n")

if not login_exitoso:
    print("🚫 Usuario bloqueado 🚫 Cerrando sistema.\n")
else:
    print("\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n")
    print(f"🤗  {rol.capitalize()}, ¿Qué deseas hacer hoy?\n")
    usuario_actual = usuario

    # Fase 2: Comandos Base

    cmd = ""
    sistema_activo = True

    while sistema_activo:
        cmd = input("Comando>: ").lower()

        ## Salir del sistema
        if cmd == "salir":
            print("\n💖  Gracias por usar nuesto PythonAgente 💖 \n")
            sistema_activo = False

        ## El sistema responde pong si recibe del usuario el comando ping
        elif cmd == "ping":
            print("\n¡pong!\n")

        ## Contar la cantidad de vocales, consonantes y letras que contiene una palabra ingresada por el usuario
        elif cmd == "contar":
            palabra = input("\nIngrese una palabra: ").strip().lower()
            ## Usando el método isalpha(), el sistema valida que la palabra ingresada por el usuario corresponde a los carácteres del alfabeto
            validando_palabra = palabra.isalpha()
            tot_letras = len(palabra)

            if (validando_palabra):
                # Conteo
                tot_vocales = 0
                tot_cons = 0
                for p in palabra:
                    if p in "aeiou":
                        tot_vocales += 1
                    else:
                        tot_cons += 1
                # Resultados del conteo
                print(f"\n\t✍️  Palabra ingresada: {palabra}")
                print(f"\n\t✏️  Total de vocales: {tot_vocales}")
                print(f"\t✏️  Total de consonantes: {tot_cons}")
                print(f"\t✏️  Total de letras: {tot_letras}\n")  
            else:
                print("\n🙅 La palabra ingresada no es válida\n")          

        # Fase 3: Nuevas Herramientas

        ## Casting y Lógica Múltiple
        elif cmd == "calculadora":
            calculadora()

        ## Control de Acceso
        elif cmd == "fecha_hoy":
            if rol == "admin":
                hoy = date.today()
                print(f"\n🗓️  Hoy es: {hoy.strftime('%d %B %Y')}\n")
            else:
                print(
                    "\n⛔ Acceso Denegado. Este comando requiere privilegios de administrador ⛔\n"
                )

        ## Manipulación de Strings
        elif cmd == "validar_pass":
            pass_nueva = input("\nIngrese la contraseña nuevaa validar: ").strip()
            no_permitido = usuario_actual
            no_usar = no_permitido in pass_nueva

            if (len(pass_nueva) < 8):
                print("\n📢 La contraseña debe ser al menos de 8 caracteres.\n")
            elif (no_usar or pass_nueva == no_permitido):
                print("\n📢 La contraseña no debe contener o ser igual al usuario con que inicias sesión.\n")
            else:
                print("""\n👌 La contraseña que ingresaste cumple las condiciones establecidas:\n
                      ✔️  Tiene al menos 8 carácteres
                      ✔️  No usa el usuario de inicio de sesión\n""")

        else:
            print("\n🤷 Comando desconocido, intente de nuevo.\n")