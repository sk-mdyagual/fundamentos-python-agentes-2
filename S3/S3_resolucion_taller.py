import datetime
from typing import Dict, List



print("-----------Iniciando el pseudoagente estilo consola--------------------")

### Se crea un usuario raíz para el pseudoagente, con su nombre, contraseña y rol
rootUser = {
    "name": "Root",
    "password": "123456",
    "Role": "Admin",
}
### Se crea una lista de usuarios, se inicializa con el usuario raiz 
users = [rootUser]
active_user = None #Variable para almacenar el usuario activo, None si no hay ninguno

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]
historial_chat : MemoriaAgente = [] 


def login():
    global active_user
    retries = 0
    user_found = False
    while user_found == False and retries < 4:    
        if active_user is not None:
            print(f"Ya hay un usuario activo: {active_user['name']}")
            user_found = True
        elif retries >= 3:
            print("[Alerta] Usuario bloqueado. Cerrando sistema")
            retries += 1
            sistema_activo = False
        else:   
            name = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            #Validación de credenciales                    
            for user in users:
                if user["name"] == name and user["password"] == password:
                    role = user["Role"]
                    active_user = user
                    print(f"Bienvenido {user['name']}! Has iniciado sesión como {role}.")
                    user_found = True
                    break
            if not user_found:
                retries += 1
                print("Credenciales incorrectas, intente de nuevo.")

def user():
    if active_user is not None:
        print(f"Usuario activo: {active_user['name']} - Rol: {active_user['Role']}")
    else:
        print("No hay ningún usuario activo.")

def logout():
    global active_user
    if active_user is not None:
        print(f"Usuario {active_user['name']} ha cerrado sesión.")
        active_user = None
    else:
        print("No hay ningún usuario activo para cerrar sesión.")

def create_user():
    if active_user is not None and active_user["Role"] == "Admin":
        user_name = input("Ingrese el nombre del nuevo usuario: ")
        valid_password = False
        while valid_password == False:
            user_password = input("Ingrese la contraseña del nuevo usuario: ")
            if user_password == user_name:
                print("La contraseña no puede ser igual al nombre de usuario. Usuario no creado.")
            elif(len(user_password) < 8):
                print("La contraseña debe tener al menos 8 caracteres. Usuario no creado.")
            else:
                valid_password = True
        new_user = {
            "name": user_name,
            "password": user_password,
            "Role": "User",
        }
        users.append(new_user)
        print(f"Usuario {user_name} creado exitosamente con rol User.")
    else:
        raise PermissionError("Privilegios insuficientes")

def fecha_hoy():
    if active_user is not None and active_user["Role"] == "Admin":
        fecha_actual = datetime.datetime.now()
        print(f"La fecha de hoy es: {fecha_actual}")
    else:
        raise PermissionError("Privilegios insuficientes")
    
def calculadora():
    if active_user is not None:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))            
        operacion = input("Ingrese el operador (+, -, *, /): ").lower()
        if operacion == "+":
            resultado = num1 + num2
            print(f"El resultado de la suma es: {resultado}")
        elif operacion == "-":
            resultado = num1 - num2
            print(f"El resultado de la resta es: {resultado}")
        elif operacion == "*":
            resultado = num1 * num2
            print(f"El resultado de la multiplicación es: {resultado}")
        elif operacion == "/":
            if num2 != 0:
                resultado = num1 / num2
                print(f"El resultado de la división es: {resultado}")
            else:
                print("Error: No se puede dividir por cero.")
        else:
            print("Operación no reconocida. Por favor, intente de nuevo.")
    else:
        raise PermissionError("Privilegios insuficientes")
    
def command_validation(cmd: str):
    valid_commands = ["salir", "ping", "contar", "login", "user", "logout", "create user", "fecha hoy", "calculadora"]
    if cmd in valid_commands:
        return True
    else:
        return False
    
def save_command(cmd: str) :
    command : Recuerdo = {
        "role": active_user["Role"] if active_user is not None else "None",
        "command": cmd
    }
    historial_chat.append(command)


def gestionar_historial(accion: str):
    if accion == "all":
        if not historial_chat:
            print("No hay comandos en el historial.")
        else:
            for i, recuerdo in enumerate(historial_chat):
                print(f"{i}. [{recuerdo['role']}] {recuerdo['command']}")
    elif accion == "clear":
        historial_chat.clear()
        print("Historial limpiado exitosamente.")
    elif accion == "search":
        keyword = input("Ingrese la palabra clave para buscar en el historial: ")
        results = [recuerdo for recuerdo in historial_chat if keyword in recuerdo["command"]]
        if results:
            print(f"Comandos que contienen '{keyword}':")
            for i, recuerdo in enumerate(results):
                print(f"{i}. [{recuerdo['role']}] {recuerdo['command']}")
        else:
            print(f"No se encontraron comandos que contengan '{keyword}'.")



#Banderas/Banderines - Booleanos
def pseudo_agente():
    cmd = ""
    sistema_activo = True
    while sistema_activo:
        cmd = input("PseudoAgente>: ").lower() #salir

         

        if command_validation(cmd):
            save_command(cmd)

        if cmd == "salir":
            sistema_activo = False

        elif cmd == "ping":
            print("pong~")

        elif cmd == "contar":
            pal = input("Ingrese una palabra: ").strip().lower()
            tot_letras = len(pal)
            #Conteo
            tot_vocales = 0
            tot_cons = 0
            for p in pal:
                if p in "aeiou":
                    tot_vocales +=1
                else:
                    tot_cons +=1
            #Resultados del conteo
            print(f"Palabra ingresada: {pal}")
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
            print(f"Total de letras: {tot_letras}")

        #Se añade el comando login, para iniciar sesion
        elif cmd == "login" :
            login()

        #Se añade el comando active User para mostrar el usuario activo
        elif cmd == "user":
            user()

        # se añade el comando logout para cerrar sesión del usuario activo, si no hay usuario activo se muestra un mensaje
        elif cmd == "logout":
            logout()

        # se añade el comando create user, este comando solo lo puede ejecutar un rol admin
        elif cmd == "create user":
            create_user()

        # se añade el comando fecha hoy, este comando solo lo puede ejecutar un rol admin
        elif cmd == "fecha hoy":
            fecha_hoy()

        # se añade el comando calculadora, este comando solo lo puede ejecutar cualquier usuario que haya iniciado sesión
        elif cmd == "calculadora" :
            calculadora()
        
        elif cmd == "all" or cmd == "clear" or cmd == "search":
            gestionar_historial(cmd)

        else:
            print("Comando desconocido, intente de nuevo.")

def run_pseudo_agente():
    try:
        pseudo_agente()
    except PermissionError as e:
        print(f"[Acceso Denegado] {e}")
        run_pseudo_agente() 

run_pseudo_agente()
