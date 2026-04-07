from datetime import date, datetime
import random

# Tipado
type Recuerdo = dict[str, str]
# Permite controlar que operaciones o métodos podemos realizar sobre datos recopilados teniendo certeza de posibles excepciones que puedan ocurrir y darles manejo desde el codigo sin
# esperar alguna sorpresa al correr la applicacion. Adicionalmente, hay menos ambiguedad en el codigo permitiendo ajustes más claros y prompts más definidos
type MemoriaAgente = list[Recuerdo]
type UserInfo = dict[str, str]


# Clase generica pseudoagente que centraliza y controla la sesión de uso de un agente
class PseudoAgente:
    """
    Clase genérica pseudoagente que centraliza y controla la sesión de uso de un agente.
    Proporciona funcionalidades básicas como gestión de memoria, conteo de palabras,
    validación de contraseñas, operaciones de calculadora e historial de chat.
    """
    # Una variable dentro de una función solo se puede utilizar dentro del scope de la función fuera de esta no puedo acceder a ella y una vez se ha llamado y terminado la funcion, el valor de la función deja de existir
    # Por el contrario, una variable que tiene el prefijo 'self' es una variable de instancia, de clase, va a existir mientras la instancia de la clase exista y se puede acceder a ella a través de la clase, además, puede ser utilizada en diferentes métodos de la función sin pasarla commo argumento
    def __init__(self, name: str = "Slave"):
        self.name = name
        self.chat_history: MemoriaAgente = [
            {
                "timestamp": "21-03-2026 21:06:16",
                "cmd": "ping",
                "author": "administrador",
                "rol": "admin",
                "description": "Se envió un ping y se devuelve un pong",
            }
        ]
        self.tokens: int = 100

        # Metodo para contar letras, vocales y consonantes de una palabara

    def count_word(self, word: str) -> str:
        """
        Cuenta e imprime el número total de letras, vocales y consonantes en la
        palabra proporcionada. El resultado se muestra en la consola.
        """
        self.tokens -= 10
        tot_letter = len(word)
        tot_vowels = 0
        tot_consts = 0

        for p in word:
            # valida si la letra es una vocal, de lo contrario es una consonante
            if p in "aeiou":
                tot_vowels += 1
            else:
                tot_consts += 1
        # Resultados del conteo
        print(f"\nPalabra ingresada: {word}")
        print(f"Total letras: {tot_letter}")
        print(f"Total vocales: {tot_vowels}")
        print(f"Total constonantes: {tot_consts}")
        return f"La palabra ingresada fue {word} con {tot_letter} letras, {tot_vowels} vocales y {tot_consts} constantes"

    # Metodo para ejecutar el comando "fecha_hoy"
    def get_todays_date(self) -> str:
        """
        Muestra la fecha actual en formato dd/mm/yyyy si el usuario conectado tiene
        el rol de administrador; de lo contrario, imprime un mensaje de acceso denegado.
        """
        self.tokens -= 5
        # Si el rol del usuario loggeado no corresponde al admin, se lanza un error (parando la ejecución normal de la función), que se propaga através de la función getTodaysDate hasta el bloque del menu de control del seudoagente
        # donde esta siendo llamada, alli el error es capturado por el bloque try-except donde se imprime el mensaje del error
        raise PermissionError(
            "[Acceso Denegado] Este comando requiere privilegios de administrador."
        )

    # Metodo para validar la contraseña
    def validate_pass(self, password: str, logged_user: str) -> str:
        """
        Valida una contraseña verificando que tenga al menos 8 caracteres y que no
        sea igual al nombre de usuario.
        Imprime los resultados de la validación en la consola.
        """
        self.tokens -= 15
        message = ""
        valid_password = password.strip()
        # Valida la longitudo de la contraseña sin considerar espacios
        is_length_valid = len(valid_password) >= 8
        # Valida si la contraseña es igual al nombre de usuario
        is_equal_to_user_name = valid_password == logged_user

        # Si incumple las dos validaciones, se indica con mensaje al usuario
        if not is_length_valid and is_equal_to_user_name:
            message = """
        La contraseña no cumple con las validaciones:
        - La longitud no es de minimo 8 carácteres
        - La contraseña es igual al nombre de usuario
            """
        # Si incumple solo con la validacion de longitud minima
        elif not is_length_valid:
            message = "La contraseña no cumple con la longitud mínima de 8 caracteres."
        # Si incumple solo con la validacion de que no sea ingual al usuario
        elif is_equal_to_user_name:
            message = "La contraseña no puede ser igual al nombre de usuario."
        # Si cumple con la longitud y no es igual al nombre de usuario, se considera exitosa
        else:
            message = "La nueva contraseña cumple con las validaciones"
        print(message)
        return message

    # Metodo que gestiona las operaciones de la calculadora
    def handle_calculator_operations(
        self, first_number: str, operator: str, second_number: str
    ) -> str:
        """
        Gestiona operaciones básicas de calculadora (+, -, *, /) en dos números proporcionados
        como cadenas.
        """
        self.tokens -= 20
        first_number_float = float(first_number)
        second_number_float = float(second_number)
        result: float = 0.0

        match operator:
            case "+":
                result = first_number_float + second_number_float
            case "-":
                result = first_number_float - second_number_float
            case "*":
                result = first_number_float * second_number_float
            case "/":
                result = first_number_float / second_number_float
            case _:
                message = f"El operador {operator} no es válido."
                return message

        return f"La operación {first_number}{operator}{second_number} da como resultado {result}"

    def gestionar_historial_all(self) -> str:
        """Construye y devuelve el historial completo del chat."""
        return_message = "[PseudoAgente] Historial completo:\n"
        for entry in self.chat_history:
            return_message += f"{entry['timestamp']} | Command: {entry['cmd']} | Rol: {entry['rol']} | Autor: {entry['author']} | Mensaje: {entry['description']}\n"
        return return_message

    def gestionar_historial_clear(self) -> str:
        """Borra el historial y devuelve el mensaje de confirmación."""
        self.chat_history.clear()
        return "[PseudoAgente] Borrando el historial de la memoria del pseudoagente"

    def gestionar_historial_busqueda(self, word_to_search: str) -> str:
        """Busca una palabra clave en el historial y devuelve coincidencias."""
        return_message = ""
        # Lista de logs cuya descripcion contiene la palabra a buscar
        conincidences = []

        # Antes de la busqueda se ajusta la palabra a buscar a minuscula y se eliminan espacios finales
        word_processed = word_to_search.strip().lower()

        for log in self.chat_history:
            # Antes de la busqueda se ajusta la descripción a minuscula y se eliminan espacios finales
            description_processed = log["description"].strip().lower()
            # Usando el comando 'in' se identifica si la palabra está en la descripcion
            if word_processed in description_processed:
                conincidences.append(log)

        if len(conincidences) == 0:
            return_message += "No encontré registros que coincidan con esa palabra."
        else:
            number_of_coincidences = len(conincidences)
            return_message += f"Se encontraron {number_of_coincidences} registros de la palabra '{word_to_search}' en el historial"
            for coincidence in conincidences:
                return_message += f"\n Autor: {coincidence['author']} | Mensaje: {coincidence['description']}"

        return return_message

    # Metodo para gestionar las acciones relacionadas con el historial
    def gestionar_historial(self, action: str, word: str = "") -> str:
        """
        Gestiona las operaciones del historial de chat: muestra todas las entradas del historial,
        borra el historial, o busca una palabra clave específica en las descripciones del historial.
        """
        self.tokens -= 15
        # El comando recibe una accion concreta: all, clear o palabra clave
        if action == "all":
            return self.gestionar_historial_all()
        elif action == "clear":
            return self.gestionar_historial_clear()
        elif action.strip() == "":
            return self.gestionar_historial_busqueda(word)
        else:
            return "Comando de historial no especificado. Usa: historial all | historial clear | historial."

    def add_log_entry(
        self, user_data: UserInfo, author_name: str, log_description: str, command: str
    ) -> None:
        """
        Crea un diccionario de entrada de registro con marca de tiempo, comando, autor, rol y descripción.
        Se utiliza para registrar acciones del usuario en el historial de chat.
        """
        new_log: Recuerdo = {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "cmd": command,
            "author": author_name,
            "rol": user_data["rol"],
            "description": log_description,
        }

        self.chat_history.append(new_log)

    def throw_a_dice(self) -> int:
        """
        Lanza un dado virtual y devuelve un número aleatorio entre 1 y 6.
        """
        self.tokens -= 2
        return random.randint(1, 6)


# Clase especializada de Pseudoagente para ejecutar funciones de admin
# Es mejor utilizar la herencia en este caso para: 1. Principio DRY: No repetir código reutilizando código existente
# 2. Centralización de lógica: Si se ajusta el código común entre las clases no debo hacer el ajuste 2 veces y elimino el riesgo de mantener codigo legacy en una parte y favorece la mantenibilidad
# 3. Mejora la simplicidad y lectura del código
class AgenteAdmin(PseudoAgente):
    """
    Clase especializada que hereda de PseudoAgente para ejecutar funciones administrativas.
    Proporciona funcionalidades extendidas como acceso a la fecha actual y gestión de historial
    con privilegios de administrador.
    """
    def __init__(self, name="Oráculo"):
        super().__init__(name)

    # Metodo para ejecutar el comando "fecha_hoy"
    def get_todays_date(self) -> str:
        """
        Muestra la fecha actual en formato dd/mm/yyyy si el usuario conectado tiene
        el rol de administrador; de lo contrario, imprime un mensaje de acceso denegado.
        """
        self.tokens -= 10
        # Se formatea la fecha a formato mas convencional de día/mes/año
        today_formatted = date.today().strftime("%d/%m/%Y")
        message = f"La fecha de hoy es {today_formatted}"
        print(message)
        return message

        # Metodo para gestionar las acciones relacionadas con el historial

    def gestionar_historial(self, action: str, word: str = "") -> str:
        """
        Gestiona las operaciones del historial de chat: muestra todas las entradas del historial,
        borra el historial, o busca una palabra clave específica en las descripciones del historial.
        """
        # El comando recibe una accion concreta: all, clear o palabra clave
        if action == "all":
            return self.gestionar_historial_all()
        elif action == "clear":
            return self.gestionar_historial_clear()
        elif action.strip() == "":
            return self.gestionar_historial_busqueda(word)
        else:
            return "Comando de historial no especificado. Usa: historial all | historial clear | historial."
