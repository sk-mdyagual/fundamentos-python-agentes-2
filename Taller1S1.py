# Tu misión esta semana es tomar el bucle base que construimos en clase y convertirlo en un sistema seguro y multifuncional. Deberás programar una capa de seguridad (Login) y agregar nuevas herramientas (comandos) que requieran manipulación de texto y operaciones matemáticas, asegurando que el programa no colapse ante entradas inesperadas.

# 📋 Requerimientos Funcionales
# Tu script (main.py) debe integrar las siguientes fases:

# Fase 1: Capa de Seguridad (Login)
# Antes de que el Agente despierte y comience a escuchar comandos, debe verificar quién intenta acceder:

# El sistema debe pedir un usuario y una contraseña por consola.
# Roles: Define en tu código un perfil de invitado (ej. user = "invitado") y un administrador (admin = "admin"), con sus respectivas contraseñas.
# Sistema de Bloqueo: El usuario tiene un máximo de 3 intentos. Si falla 3 veces, el bucle de login se rompe, el programa imprime [Alerta] Usuario bloqueado. Cerrando sistema. y la ejecución termina.
# Si el inicio de sesión es exitoso, el sistema pasa a la Fase 2 y debe recordar con qué rol ingresó el usuario.
# Fase 2: Comandos Base (Repaso de Clase)
# El menú infinito (while) debe mantener los comandos que exploramos en nuestra sesión interactiva:

# ping: Responde con "pong!".
# contar: Pide una frase y cuenta las vocales y consonantes usando un ciclo for.
# salir: Rompe el bucle principal y apaga el Agente de forma elegante.

# Fase 3: Nuevas Herramientas (Tu verdadero reto)
# Debes programar estos 3 comandos nuevos integrándolos a tu estructura if/elif/else del menú principal:

# Comando fecha_hoy (Control de Acceso): * Este comando es clasificado. Si el usuario ingresó como administrador, muestra la fecha actual (Reto Eutagógico: investiga cómo importar el módulo datetime para esto).

# Si ingresó como invitado, imprime: [Acceso Denegado] Este comando requiere privilegios de administrador.
# Comando validar_pass (Manipulación de Strings):

# El agente pedirá al usuario que ingrese una propuesta de contraseña nueva.
# Debes validar dos cosas usando if/else y funciones de strings:
# Que tenga al menos 8 caracteres de longitud (len()).
# Que no sea exactamente igual a su nombre de usuario (para esto necesitas comparar el input con la variable que guardaste en el Login).
# Imprime un mensaje de éxito o el motivo del rechazo.
# Comando calculadora (Casting y Lógica Múltiple):

# El agente pedirá: "Ingresa el primer número", "Ingresa el operador (+, -, *, /)", y "Ingresa el segundo número".
# Debes convertir (int() o float()) los inputs numéricos.
# Usando if/elif/else para evaluar el operador, imprime el resultado de la operación matemática.
# (Opcional/Extra: ¿Qué pasa si intentan dividir por cero? Intenta manejar ese caso con un if).





#Solucion


## Se crean los usuarios y su contraseña, se le asigna cada valor a cada variable
from datetime import datetime


userInvitado = "lorenzo"
contraseñaInvitado = "soyLorenzo123"

userAdmin = "sara"
contraseñaAdmin = "1000191388"


intentos = 0
rol = None ## Se pone la variable en none, osea vacia por que aun no sabemos que rol va a ingresar el usuario



## En este while se esta dando que mientras intentos sea menor que 3 entonces ejecute la logica 
# de ingrese usuario y contraseña y si se ingresa 3 veces incorrecyo entonces el programa finaliza, 
# ya que como no obtiene respuesta de la variable rol entonces esta queda vacia y rompe con el bucle
while intentos <3:
    user = input ("Ingresa tu usuario: ").strip().lower()
    password = input ("Ingresa tu contraseña: ").strip().lower()

    if user == userAdmin and password == contraseñaAdmin:
        rol="admin"
        print(f"Inicio Exitoso, Bienvenido al rol {rol}")
        break

    elif user==userInvitado and password== contraseñaInvitado:
        rol="invitado"
        print(f"Inicio Exitoso, Bienvenido al rol {rol}")
        break


    else: 
        intentos += 1
        print("Usuario o contraseña incorrectos, intente de nuevo")
if rol is None:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.") 
    exit() ## agrego exit para que finalice el programa, no pongo break por que no esta dentro de un bucle y se necesita es que cierre el programa completamente      

##al realizar este bucle se imprime el menu hasta que sea false
while True:
  print("MENU PRINCIPAL") 
  print("""
  -Ping o Pong
  -Contar
  -Fecha
  -Validar Contraseña
  -Calculadora            
  -Salir
  """)
  comando = input("Ingresa el comando de lo que desees realizar").strip().lower()  ##.strip(elimina espacios) y .lower(controla la escritura si es Aa o se equivoca) son controladores 

  if comando == "ping":
      print("Pong!")
  elif comando == "pong":
      print("Ping!")    
  elif comando== "contar":
      frase = input("Ingrese una frase: ").strip().lower()
      totalLetras = len(frase)  # funcionalidad len es para el conteno de cada letra
      
      totalVocales = 0
      totalConsonantes = 0
      vocales = "aeiouAEIOU"

      for letra in frase:
          if letra.isalpha():    ##el metodo isalpha funciona para validar si contiene solo letras sin numeros ni espacios ni simbolos para retornar un true o false
             if letra in vocales:
                 totalVocales +=1
             else:
                 totalConsonantes +=1  

      print(f"Su frase: {frase} contiene {totalVocales} Vocales y tiene {totalConsonantes} Consonantes")           
  
  elif comando=="fecha":
      if rol == "admin":
          hoy = datetime.now()  #se usa esta funcion para obtener la fecha actual
          print(f"La fecha actual es: {hoy}")
      else:
          print("[Acceso Denegado] Este comando requiere privilegios de administrador.")   
  ## para validar la contraseña se realizan condionales de validaciones para el cambo de contraseña
  elif comando=="validarcontraseña":
      nuevaContraseña = input ("Ingrese una nueva contraseña")
      if len(nuevaContraseña)<8:
          print("La contraseña debe de tener al menos 8 caracteres")

      elif nuevaContraseña==user:
          print("La contraseña no puede ser igual al nombre de usuario")
      else:
          print("Contraseña valida")
    ## para realizar la calculadora se realizan condionales de validaciones para los diferentes operadores
  elif comando == "calculadora":

      num1 = float(input("Ingrese el primer numero").strip())
      operador = input("Ingresa el operador (+, -, *, /)").strip()
      num2 = float(input("Ingresa el segundo numero: "))

      if operador =="+":
          print("Resultado: ", num1+num2)
      elif  operador == "-":        
          print("Resultado: ", num1-num2)   
      elif  operador == "*":        
          print("Resultado: ", num1*num2)   
      elif  operador == "/":        
          if num2 == 0:
              print("Error, no se puede dividir por cero") 
          else:
              print("Resultado: ", num1/num2)    
      else:
          print("Operador no valido")        
  elif comando == "salir":
      print("Apagando agente....")
      break
  else: 
      print("Comando no reconocido, digite nuevamente")       

