#Día 1
##Entrada y salida de datos
###Entrada: input()
###Salida: print()

#variables
nom_per = input("¿Cuál es tu nombre?: ")
anio = input("Ingresa tu anio de nacimiento: ")
edad = 2026 - int(anio)
#Funciones para str 
#.upper()/.lower()/.capitalize()... ¿Qué otras más existen?
genero = input("Ingresa (M) para masculino o (F) para femenino: ").upper()
#Formas de hacer print/presentar por pantalla
#1. Por comas
#2. Concatenación (+)
#3. Por placeholders
#-----------------------------------------------------------#

#Tipos de datos primitivos - ¿Qué otros tipos de datos primitivos existen?
##%s: str - String - Texto
##%d: int - Integer - Numérico entero
##%f: float - Float - Numérico decimal
## bool - Boolean - Valor de verdad: Verdadero (true) o Falso (false)

#---------------------------------------------------------#
#4. .format()
#5. f

#print("Hola,",nom_per, "mucho gusto~")
#print("Hola, "+nom_per+" mucho gusto~")
#print("Hola %s, mucho gusto. Tu edad es %d años" %(nom_per, anio))
#print("Hola {}. Tu edad es {}".format(nom_per,edad))
#print("Hola {fnom}. Tu edad es {fedad}".format(fnom=nom_per, fedad=edad))
print(f"Hola, {nom_per}. Tu edad es {edad}")

#Lógica booleana - if/else |if/elif/else 
##Operadores I: and, or, not 
##Operadores II: >,<, >=, <=, ==, !=

if edad >=18 and genero == "M":
    print(f"Bienvenido al club, Sr. {nom_per}")
elif edad>=18 and genero == "F":
    print(f"Bienvenido al club, Srita/Sra. {nom_per}")
else:
    print("No eres mayor de edad. Vaya pa' su casa.")

##Ejemplo para estudios autónomos
print("--- Sistema de Seguridad Nivel 1 ---")

# 1. Recolección de datos (I/O)
nombre = input("Identifícate. ¿Cuál es tu nombre?: ")

# Demostrar la conversión explícita
edad_str = input("Ingresa tu edad: ")
edad = int(edad_str) 

tiene_credencial = input("¿Tienes credencial VIP? (si/no): ").lower() == "si"

# 2. Lógica Booleana y Control de Flujo (if/elif/else)
print("\nAnalizando credenciales...")

if edad >= 18 and tiene_credencial:
    # Uso de f-strings para formateo moderno
    print(f"Acceso Concedido. Bienvenido a la terminal, {nombre}.")
elif edad >= 18 and not tiene_credencial:
    print(f"Acceso Denegado. {nombre}, eres mayor de edad pero requieres pase VIP.")
else:
    # Se calcula cuánto falta para los 18
    print(f"Alerta de intruso. Te faltan {18 - edad} años para ingresar.")


##Mini-taller I: Ejercicio para práctica autónoma
### La IA generó un sistema de cálculo de bonos, pero está crasheando y 
# tomando decisiones ilógicas. ¿Puedes encontrar los 3 errores, 
# arreglarlos y mejorar los prints usando f-strings?
sueldo = input("Ingresa tu sueldo base: ")
anios_empresa = input("¿Cuántos años llevas en la empresa?: ")

bono = sueldo * 0.10 

if anios_empresa > 5:
    print("¡Felicidades! Tienes un bono extra por antigüedad.")
    total = sueldo + bono + 500
else:
    print("No hay bono de antigüedad.")
    total = sueldo + bono

print("Tu total a recibir es:")
print(total)
