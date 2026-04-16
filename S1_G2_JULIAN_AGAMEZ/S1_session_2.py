#Día 2 - Estructuras de control
## while, for
#Estructura y lógica: while
##while condición:
#  ...
#  ...
#  if(...):
#    break
# Cuidado con los bucles infinitos! Truco? la actualización/gestión de la condición

# nombre = input("¿Cuál es tu nombre?: ")
# print(f"Hola, {nombre}, adiós")

saldo = 100

#Falta colocar (tarea autonoma):
# - Mostrar el saldo disponible
# - Indicar al usuario que ya no dispone de saldo para continuar comprando
# - Gestionar el saldo negativo

# while saldo > 0:
#     print("""
#     Predas disponibles y con stock:
#         - Vestido (50)
#         - Zapatos (50)
#         - Jeans (30)
#         - Camisa (20)
#         - Medias (5)
#     """)

#     op = input("Selecciona tu prenda: ").lower()

#     if(op.startswith("v") or op.startswith("z")):
#         saldo -= 50
#     elif(op.startswith("j")):
#         saldo -= 30
#     elif(op.startswith("c")):
#         saldo -= 20
#     elif(op.startswith("m")):
#         saldo -= 5
#     else:
#         print("Opción no válida, intenta de nuevo")

#Previa para el taller de la semana: Hacer un pseudoagente estilo consola
## - ¿Qué podrá hacer este pseudoagente por medio de comandos?
### - Terminar la sesión - salir
### - Responder un ping con un pong - ping
### - Contar letras en una palabra: Total, vocales, consonantes - contar

print("-------------------- Iniciando al pseudoagente de consola. --------------------")
print("Bienvenido al pseudoagente de consola. Escribe 'salir' para terminar la sesión.")

sesion = True

while sesion:
    comando = input("PseudoAgente> ").lower()
    if comando == "salir":
        sesion = False
    elif comando == "ping":
        print("pong")
    elif comando == "contar":
        palabra = input("Ingresa una palabra: ").strip().lower()
        total_letras = len(palabra)
        t_vocales, t_consonantes = 0, 0
        for letra in palabra:
            if letra in "aeiou":
                t_vocales += 1
            else:
                t_consonantes += 1
        print(f"Palabra ingresada: {palabra}")
        print(f"Total vocales: {t_vocales}")
        print(f"Total consonantes: {t_consonantes}")
        print(f"Total letras: {total_letras}")
    else:
        print("Comando desconocido, intenta de nuevo.")
