# 🛠️ Taller Semana 4: Nace la Entidad (POO y Modularización)
# Lina María Ramírez

from taller4.agente import PseudoAgente, AgenteAdmin
#Tipado
type UserInfo = dict[str, str]
type Credentials = dict[str, UserInfo]

def get_agent(logged_user: UserInfo):
    """Return the appropriate agent instance based on user role.
    
    Args:
        logged_user: Dictionary containing user information including role.
        
    Returns:
        An AgenteAdmin or PseudoAgente instance based on the user's role.
    """
    current_rol: str = logged_user["rol"]
    if current_rol == "admin":
        agent = AgenteAdmin()
    else:
        agent = PseudoAgente()
    
    print(f"\n----------------- Agente {agent.name} activado. Tipo: {type(agent).__name__} ----------------- ")
    return agent


print("\n-----------------Iniciando el pseudoagente estilo consola-----------------\n")

ACTIVE_SYSTEM = False
LOGIN_ATTEMPTS = 0
LOGIN_SUCCESS = False
MAX_ATTEMPTS = 3

#Diccionario que simula la base de datos de usuarios registrados
user_credentials: Credentials = {
    "administrador": {"password": "admin_pass", "rol": "admin"},
    "invitado": {"password": "user_pass", "rol": "guest"},
}
logged_user_data: UserInfo = {}
user_input: str = ""
my_agent: PseudoAgente

# Bloque de autenticación
# Mientras el login no sea exitoso se consultara al usuario por el nombre y contraseña
while not LOGIN_SUCCESS:
    # Sin embargo, si el numero de intentos alcanza el máximo, el sistema se cierra y con break salimos del la estructura while
    if LOGIN_ATTEMPTS == MAX_ATTEMPTS:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        break

    user_input = input("\nEscriba su usuario: ").strip()
    pass_input = input("Digite su contraseña: ").strip()
    # Cada vez que el usuario digite las credenciales se cuenta como un intento de login
    LOGIN_ATTEMPTS += 1
    IS_CREDENTIAL_VALID = False

    # El manejo delkey error se realiza en el bloque except permitiendo un mensaje personalizado si el usuario no esta registrado
    try:
        logged_user_data = user_credentials[user_input]
        # La contraseña se encuentra almacenada en el value de la key "password" para el diccionario asociado al usuario
        real_pass = logged_user_data["password"]
        IS_CREDENTIAL_VALID = real_pass == pass_input
    except KeyError:
        print(f"[Error] El usuario {user_input} no se encuentra registrado. Inteno No. {LOGIN_ATTEMPTS} de {MAX_ATTEMPTS}")
        continue

    # Si las credenciales son validas, es decir, el usuario esta registrado en el diccionario y la contraseña ingresada coincide con la registrada
    # Se define que el usuario esta loggeado y se activa el sistema del agente
    if IS_CREDENTIAL_VALID:
        LOGIN_SUCCESS = True
        ACTIVE_SYSTEM = True
        print(f"Bienvenido {user_input}. Despertando al agente.\n")
        my_agent = get_agent(logged_user_data)
    # De lo contrario se da mensaje informativo y se reptie el bucle
    else:
        print(
            f"\n🚫 Usuario o contraseña incorrecto. Inteno No. {LOGIN_ATTEMPTS} de {MAX_ATTEMPTS}"
        )


# Bloque menu de control pseudoagente
# Estructura de control while que indica el estado de la sesión del pseudoagente y presenta el menú de acciones posibles a ejecutar
# El sistema solo se activa si las credenciales de acceso son validas
while ACTIVE_SYSTEM:
    MESSAGE: str = ""
    CMD = ""
    if my_agent.tokens <= 0:
        print("\n******* Token agotados. Finalizando la sesión.")
        ACTIVE_SYSTEM = False
        continue
    print(f"\nTokens disponibles: {my_agent.tokens} *****")
    try:
        CMD = input("\nPseudoAgente>: ").lower().strip()

        if CMD == "salir":
            print("Finalizando la sesión")
            MESSAGE = "Se ha solicitado terminar la sesión"
            ACTIVE_SYSTEM = False
        elif CMD == "ping":
            my_agent.tokens -= 5
            print("pong")
            MESSAGE = "Se envió un ping y se devuelve un pong"
        elif CMD == "contar":
            input_word = input("Ingrese una palabra: ").lower()
            MESSAGE = my_agent.count_word(input_word)
        elif CMD == "fecha_hoy":
            try:
                MESSAGE = my_agent.get_todays_date()
            except PermissionError as error:
                MESSAGE = str(error)
                print(MESSAGE)
        elif CMD == "validar_pass":
            new_pass = input("Ingrese nueva contraseña a validar: ")
            MESSAGE = my_agent.validate_pass(new_pass, logged_user_data)
        elif CMD == "calculadora":
            first = input("Ingrese el primer numero: ")
            op = input("Ingrese el operador: ")
            second = input("Ingrese el segundo numero: ")
            try:
                MESSAGE = my_agent.handle_calculator_operations(first, op, second)
            except ValueError:
                MESSAGE = "Uno de los valores ingresados no es númerico."
            except ZeroDivisionError:
                MESSAGE = "Para el operador '/' el segundo numero no puede ser 0"
            print(MESSAGE)
        elif CMD.startswith("historial"):
            ##El while solo prepara la acción y delega la lógica a la Tool de historial
            history_action:str = CMD.removeprefix("historial").strip()
            OUTPUT_HISTORIAL:str = ""    
            if history_action == "all":
                OUTPUT_HISTORIAL = my_agent.gestionar_historial(history_action)
                MESSAGE = "Se consultó el historial completo."
            elif history_action == "clear":
                OUTPUT_HISTORIAL = my_agent.gestionar_historial(history_action)
                MESSAGE = "Se solicitó borrar el historial completo."
            elif history_action == "":
                input_word = input("\nIngresa la palabra clave a buscar: ")
                OUTPUT_HISTORIAL = my_agent.gestionar_historial(history_action, input_word)
                MESSAGE = f"Se buscó la palabra '{input_word}' en el historial."
            else:
                MESSAGE = "Comando de historial no especificado. Usa: historial all | historial clear | historial."
                OUTPUT_HISTORIAL = MESSAGE
            print(OUTPUT_HISTORIAL)
        elif CMD == "lanzar_dado":
            random_number = my_agent.throw_a_dice()
            MESSAGE = f"El número aleatorio obtenido del dado es {random_number}"
            print(MESSAGE)
        else:
            MESSAGE = "Comando desconocido, intente nuevamente"
            print(MESSAGE)

        # Guarda el comando en el historial
        my_agent.add_log_entry(logged_user_data, user_input, MESSAGE, CMD)    
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Finalizando la sesión.")
        ACTIVE_SYSTEM = False
