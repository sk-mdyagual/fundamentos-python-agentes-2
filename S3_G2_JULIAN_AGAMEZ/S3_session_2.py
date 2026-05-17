#Día 2: Excepciones
## Java dev: En java, el compilador de obliga a manejar los errores (Checked Exception) y 
# para validar antes de actuar)

## Python dev: En Python, la filosofia oficial se llama "Easier to ask for forgiveness 
# than permission" (EAFP - Es más fácil pedir perdón que permiso). las checked exception no existen,
# por lo tanto en tiempo de ejecución.

def calcular_division(n1, n2):
    try:
        return n1 / n2
    except ZeroDivisionError as ex:
        print("Error: No se puede dividir entre cero.", ex)

def transferir_fondos(monto, base = 1000):
    if monto <= 0:
        raise ValueError("El monto debe ser mayor que cero.")
    return f"Transferencia de {monto} realizada con éxito. Saldo restante: {base - monto}"

# try:
#     n1 = int(input("Ingrese el primer número: "))
#     n2 = int(input("Ingrese el segundo número: "))
#     resultado = calcular_division(n1, n2)
# except ValueError as ex:
#     print("Error: Entrada no válida. Por favor, ingrese números enteros.", ex)
# else:
#     print(f"Resultado: {resultado}")

ing_monto = int(input("Ingrese el monto a transferir: "))
try:
    msg = transferir_fondos(ing_monto)
except ValueError as ex:
    msg = f"Error: {ex}"
else:
    print(msg)