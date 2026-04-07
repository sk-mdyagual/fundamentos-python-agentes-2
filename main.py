from agente import PseudoAgente, AgenteAdmin

usuarios_validos = {"invitado": "algodificil", "admin": "algofacil"}

intentos = 0
max_intentos = 3

while intentos < max_intentos:

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    if usuario in usuarios_validos and usuarios_validos[usuario] == contraseña:

        if usuario == "admin":
            agente = AgenteAdmin(usuario)
        else:
            agente = PseudoAgente(usuario)

        print("Bienvenido", usuario)

        comando = ""

        while agente.tokens > 0 and comando != "salir":

            comando = input("Comando: ")

            if comando == "ping":
                print(agente.ping())

            elif comando == "fecha_hoy":
                try:
                    print(agente.fecha_hoy())
                except Exception as e:
                    print(e)

            elif comando == "contar":
                texto = input("Texto: ")
                print(agente.contar_letras(texto))

            elif comando == "calculadora":
                # Necesitamos convertir los inputs (que son strings) a números
                # se hace para poder aplicar las operaciones matematicas
                # asi nos considera los datos como numero y no string
                # float por si desean usar numeros decimales o enteros,
                # solo int lo limita a enteros
                # sino se hace la conversión puede generar error,
                # o concatenar en el caso de suma
                # use el try para manejar una excepción, en caso de que me agreguen letras
                # el while para pedir hasta que me de un numero uno valido
                while True:
                    try:
                        # de esta manera se convierte a float la entrada
                        num1 = float(input("Ingresa el primer número: "))
                        # si es valido, corta el while
                        break
                    except ValueError:
                        # en caso de que ingrese letras u otro caracter, controlo el error
                        # el while continua
                        print("Error: ingrese un número válido.")
                        
                operador = input("Ingresa el operador (+, -, *, /): ").strip()
                
                # el while para pedir hasta que me de un numero dos valido
                # aca, se repite al while inicial o del primer numero,
                # solo que para el numero dos
                while True:
                    try:
                        num2 = float(input("Ingresa el segundo número: "))
                        break
                    except ValueError:
                        print("Error: ingrese un número válido.")
                        
                
                print(agente.calculadora(num1, num2, operador))
                       
                
            elif comando == "validar_pass":
                nueva = input("Nueva contraseña: ")
                print(agente.validar_pass(nueva))

            elif comando == "historial":
                    print("Opciones: ver / limpiar / buscar")
                    opcion = input("Opción: ").strip()

                    if opcion == "buscar":
                        palabra = input("Palabra clave: ").strip()
                        print(agente.gestionar_historial("buscar", palabra))
                    else:
                        print(agente.gestionar_historial(opcion))
            elif comando == "dado":
                print(agente.lanzar_dado())

            elif comando == "salir":
                print("Apagando agente...")

            else:
                print(agente.contar_letras(comando))

        if agente.tokens <= 0:
            print("El agente murió de cansancio")

        break

    else:
        intentos += 1
        print("Credenciales incorrectas")

print("Sistema finalizado")