#Día 2: Excepciones
## Java dev: En Java, el compilador te obliga a manejar los errores (Checked Exceptions) y 
# la filosofía suele ser "Look Before You Leap" (LBYL - Mira antes de saltar: usar muchos if 
# para validar antes de actuar).

## Python dev: En Python, la filosofía oficial se llama EAFP: "Easier to Ask for Forgiveness 
# than Permission" (Es más fácil pedir perdón que pedir permiso). Las checked exceptions no existen,
# por lo tanto todo sucede en tiempo de ejecución.

def calcular_division(x,y):   
    try:
        return x/y
    except ZeroDivisionError as e:
        print(e)
        return -1

def transferir_fondos(monto):
    if monto <= 0:
        raise ValueError("El monto a transferir tiene que ser mayor a cero")
    return f"Se transfirieron {monto} exitosamente"

"""
try:
    n1 = int(input("N1: "))
    n2 = int(input("N2: "))
    res = calcular_division(n1,n2)
except ValueError as e:
    print(e)
    
else:
    print(f"Result: {res}")
    """

ing_monto = int(input("Ingrese monto: ")) 

try:
    msg = transferir_fondos(ing_monto)
except ValueError as e:
    print(e)
else:
    print(msg)