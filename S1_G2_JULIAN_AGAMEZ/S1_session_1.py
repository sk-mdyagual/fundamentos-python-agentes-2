#Día 1
##Entrada y salida de datos
###Entrada: input()
###Salida: print()

#variables
nombre = input("¿Cuál es tu nombre?: ")
anio = input("¿En qué año naciste?: ")
edad = 2026 - int(anio)
#Funciones para str
#upper() - Mayúscula
#lower() - Minúscula
#capitalize() - Primera letra mayúscula

genero = input("¿Cuál es tu género? (M/F): ").upper()

#Formas de hacer print/presentar en pantalla
#1. Por comas
#2. Concatenación (+)
#3. Por Placehorders - Tipos de datos primitivo
###str - String - Texto: %s
###int - Integer - Númerico entero: %d
###float - Float - Númerico decimal: %f

#4. .format()
#5. f

# print("Hola,", nombre, "mucho gusto")
# print("Hola, "+ nombre + " mucho gusto ")
# print("Hola, %s mucho gusto. Naciste en %s. Tienes %d años." % (nombre, anio, edad))
# print("Hola, {} mucho gusto. Naciste en {}. Tienes {} años.".format(nombre, anio, edad))
print(f"Hola, {nombre} mucho gusto. Naciste en {anio}. Tienes {edad} años.")

#logica booleana - if/else | if/elif/else
##operadores I: and, or, not
##Operadores II: >, <, >=, <=, ==, !=

if edad >= 18 and genero == "M":
    print(f"Bienvenido al club, Sr. {nombre}")
elif edad >= 18 and genero == "F":
    print(f"Bienvenida al club, Sra. {nombre}")
else:
    print("No eres mayor de edad, no puedes entrar al club")

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
sueldo = float(input("Ingresa tu sueldo base: "))
anios_empresa = int(input("¿Cuántos años llevas en la empresa?: "))

bono = sueldo * 0.10 

if anios_empresa > 5:
    print("¡Felicidades! Tienes un bono extra por antigüedad de $500.")
    total = sueldo + bono + 500
else:
    print("No hay bono de antigüedad.")
    total = sueldo + bono

print(f"Tu total a recibir es: ${total:.2f}")