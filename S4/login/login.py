def login(user: str, passwrd: str) -> dict:
    if user == "admin" and passwrd == "admin123":
        return {
            "rol": user,
            "access": True,
            "descripcion": "[Sistema] Acceso concedido. Privilegios de Administrador activados.",
        }
    if user == "invitado" and passwrd == "1234":
        return {
            "rol": user,
            "access": True,
            "descripcion": "[Sistema] Acceso concedido. Modo Invitado.",
        }
    # Fix: retorno explícito cuando las credenciales son incorrectas
    # (En S4_sesion_1.py esto retornaba None y causaba un crash)
    return {
        "rol": "",
        "access": False,
        "descripcion": "[Sistema] Credenciales incorrectas.",
    }