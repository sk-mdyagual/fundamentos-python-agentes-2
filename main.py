import datetime
from typing import Dict, List


print("-" * 40)
print(" " * 12 + "Taller semana 3" + " " * 12)
print("-" * 40)

# Credenciales guardadas en un diccionario
usuarios_validos = {"invitado": "algodificil", "admin": "algofacil"}
# Diccionario para persistir el historial

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]
historial_chat = []
historial_chat: MemoriaAgente = []

intentos = 0
max_intentos = 3
totalVocales = 0
totalConsonantes = 0

def registrar_evento(log: MemoriaAgente, cmd: str, rol: str, descripcion: str) -> None:
    """
    Este metodo lo voy a usar para registrar eventos en la memoria. 
    """
    log.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cmd": cmd,
        "rol": rol,
        "descripcion": descripcion
    })

def obtener_fecha_hoy(usuario: str) -> str:
    """
   Metodo para obtener la fecha actual.
    """
    # El error "raise" interrumpe la ejecución normal de este metodo  
    # y devuelve el error donde fue invocado
    if usuario == "invitado":
        raise PermissionError("[Acceso Denegado] Este comando requiere privilegios de administrador.")
        
    fecha_actual = datetime.datetime.now()
    return f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y %H:%M:%S')}"

def calculadora(num1: float, num2: float, operador: str) -> str:
    """
    Metodo para la calculadora.
    """
    if operador == "+":
        return f"Resultado de la suma: {num1} + {num2} = {num1 + num2}"
    elif operador == "-":
        return f"Resultado resta: {num1} - {num2} = {num1 - num2}"
    elif operador == "*":
        return f"Resultado multiplicación: {num1} × {num2} = {num1 * num2}"
    elif operador == "/":
        if num2 == 0:
            raise ZeroDivisionError("No se puede dividir por cero.")
        return f"Resultado de la división: {num1} ÷ {num2} = {num1 / num2}"
    else:
        raise ValueError("Operador no válido. Usa: +, -, *, /")

def contar_letras(palabra: str) -> str:
    """
    Este metodo lo uso para saber el total de caracteres, vocales y consonantes.
    """
    total_vocales = sum(1 for p in palabra if p in "aeiou")
    total_consonantes = sum(1 for p in palabra if p in "bcdfghjklmnpqrstvwxyz")
    
    return (f"La palabra contiene {len(palabra)} caracteres.\n"
            f"La palabra contiene {total_vocales} vocales.\n"
            f"La palabra contiene {total_consonantes} consonantes.")

def validar_pass(usuario: str, nueva_pass: str) -> str:
    """
   Metodo para validar que la nueva contraseña cumpla con los estándares de seguridad.
    """
    if len(nueva_pass) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    elif nueva_pass == usuario:
        return "La contraseña no puede ser igual a tu nombre de usuario."
    else:
        return "Su contraseña cumple con los criterios."
# El while valida que intentos sea menor a 3, porque inicie en cero
while intentos < max_intentos:
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()

    # Verificar si las credenciales son correctas
    if usuario in usuarios_validos and usuarios_validos[usuario] == contraseña:
        registrar_evento(historial_chat, "login", usuario, "Inicio de sesión exitoso")

        print(f"Inicio de sesión exitoso, Bienvenido {usuario}!")

        palabraAnalizar = "iniciar"

        while palabraAnalizar != "salir":
            palabraAnalizar = input("Ingrese un comando: ").lower().strip()

            if palabraAnalizar == "salir":
                break

            elif palabraAnalizar == "ping":
                print("pong")
                registrar_evento(historial_chat, "ping", usuario, "Se envió un ping y se devuelve un pong.")

            elif palabraAnalizar == "fecha_hoy":
                try:
                    resultado_fecha = obtener_fecha_hoy(usuario)
                    print(resultado_fecha)
                    registrar_evento(historial_chat, "fecha_hoy", usuario, "Se devolvió la fecha de hoy exitosamente.")
                except PermissionError as e:
                    print(f"{e}")
                    registrar_evento(historial_chat, "fecha_hoy", usuario, "Acceso denegado por falta de privilegios.")
        
            elif palabraAnalizar == "validar_pass":
                nueva_pass = input("Ingresa tu propuesta de contraseña nueva: ")
                validate = validar_pass(usuario,nueva_pass)
                print(validate)
                registrar_evento(historial_chat, "validar_pass", usuario, validate)

            

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
                try: 
                    resultado_calc = calculadora(num1, num2, operador)
                    print(resultado_calc)
                    registrar_evento(historial_chat, "calculadora", usuario, resultado_calc)
                except ValueError:
                    print(f"[Error de Input]operador incorrecto.")
                    registrar_evento(historial_chat, "calculadora", usuario, "[Error de Input]operador incorrecto.")

                except ZeroDivisionError as e:
                    print(f"[Error Matemático] {e}")
                    registrar_evento(historial_chat, "calculadora", usuario,"[Error Matemático] {e}")


            else:
               print(contar_letras(palabraAnalizar))
               registrar_evento(historial_chat, "por defecto", usuario, "Se analizo cuantas vocales contiene la palabra ingresada, cuantas consonantes y cuantos caracteres")

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
