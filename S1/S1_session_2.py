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