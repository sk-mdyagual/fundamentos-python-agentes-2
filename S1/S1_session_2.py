import datetime

#Dia 2 - Estructuras de control 
## while, for | match/case**
#Estructura y lógica: while
## while condicion:
#   ...
#   ...
#   if(....):
#       break
#   Cuidado los bucles infinitos! Truco? La actualización/gestión de la condición

#nom_per = input("¿Cuál es tu nombre?: ")
#print(f"Hola {nom_per}, adiós~")


#Previa para el taller de la semana: Hacer un pseudoagente estilo consola
## - ¿Qué podrá hacer este pseudoagente por medio de comandos?
### - Terminar la sesión - salir
### - Responder un ping con un pong - ping
### - Contar letras en una palabra: Total, vocales y consonantes - contar

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



#Banderas/Banderines - Booleanos
cmd = ""
sistema_activo = True
while sistema_activo:
    cmd = input("PseudoAgente>: ").lower() #salir

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
    elif cmd == "login":
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
    #Se añade el comando active User para mostrar el usuario activo
    elif cmd == "user":
        if active_user is not None:
            print(f"Usuario activo: {active_user['name']} - Rol: {active_user['Role']}")
        else:
            print("No hay ningún usuario activo.")
    # se añade el comando logout para cerrar sesión del usuario activo, si no hay usuario activo se muestra un mensaje
    elif cmd == "logout":
        if active_user is not None:
            print(f"Usuario {active_user['name']} ha cerrado sesión.")
            active_user = None
        else:
            print("No hay ningún usuario activo para cerrar sesión.")
    # se añade el comando create user, este comando solo lo puede ejecutar un rol admin
    elif cmd == "create user":
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
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
    # se añade el comando fecha hoy, este comando solo lo puede ejecutar un rol admin
    elif cmd == "fecha hoy":
        if(active_user is not None and active_user["Role"] == "Admin") : 
            fecha_actual = datetime.datetime.now()
            print(f"La fecha de hoy es: {fecha_actual}")
        else :
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
    # se añade el comando calculadora, este comando solo lo puede ejecutar cualquier usuario que haya iniciado sesión
    elif cmd == "calculadora" :
        if(active_user is not None) : 
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
            print("[Acceso Denegado] Debe iniciar sesión para usar la calculadora.")

    else:
        print("Comando desconocido, intente de nuevo.")


#Falta colocar (Tarea autónoma):
# - Mostrar el saldo disponible
# - Indicar al usuario que ya no dispone de saldo para continuar
# - Gestionar el saldo negativo
saldo = 100
while saldo > 0:
    print("""
Prendas disponibles y con stock:
    - Vestido (50)
    - Zapatos (50)
    - Jeans (30)
    - Camiseta (20)
    - Medias/Calcetines (5)
    """)
    op = input("Selecciona una prenda: ").lower() #vestido, VESTIDO, vEStido, vstido
    if(op.startswith("v") or op.startswith("z")):
        saldo -= 50
    elif (op.startswith("j")):
        saldo -= 30
    elif (op.startswith("c")):
        saldo -=20
    elif (op.startswith("m")):
        saldo -=5
    else:
        print("Selección inválida, intente de nuevo")
