import sqlite3
import datetime
import os
from agente import PseudoAgente, AgenteAdmin

"""Este script se encarga de toda la comunicación con la base de datos. Aquí creo las tablas, guardo agentes, mensajes y misiones, 
y también reconstruye los agentes como objetos usando POO cuando se necesita."""


DB_PATH = "agentes.db"

def crear_tablas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre TEXT PRIMARY KEY,
            rol TEXT,
            energia INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente TEXT,
            destinatario TEXT,
            contenido TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT,
            energia_requerida INTEGER,
            created_at TEXT
        )
    """)
    # guardar cambios
    conn.commit()
    # cerrar conexión  
    conn.close()   


def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """Registra un agente en la base de datos. Retorna mensaje de exito o error."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia),
        )
        conn.commit()
        resultado = f"[DB] Agente '{nombre}' registrado con exito."
    except sqlite3.IntegrityError:
        resultado = f"[DB] Error: El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado



def despertar_agente(nombre: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()

    if fila is None:
        return None

    nombre, rol, energia = fila

    if rol == "admin":
        agente = AgenteAdmin()
    else:
        agente = PseudoAgente()

    agente.nombre = nombre
    agente.energia = energia

    return agente


def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """Inserta un mensaje en la tabla mensajes con timestamp automatico."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, timestamp),
    )
    conn.commit()
    conn.close()
    return f"[DB] Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."


def leer_mensajes(nombre_agente: str) -> list[dict]:
    """Lee todos los mensajes dirigidos a un agente, ordenados por timestamp."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT remitente, destinatario, contenido, timestamp FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {"remitente": f[0], "destinatario": f[1], "contenido": f[2], "timestamp": f[3]}
        for f in filas
    ]





def listar_agentes() -> list[dict]:
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [
        {"nombre": f[0], "rol": f[1], "energia": f[2]}
        for f in filas
    ]

def crear_mision(titulo, descripcion, agente, energia):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, energia_requerida, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descripcion, agente, "pendiente", energia, timestamp))

    conn.commit()
    conn.close()

    return "[DB] Misión creada correctamente"


def obtener_mision(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM misiones WHERE id = ?", (id,))
    fila = cursor.fetchone()
    conn.close()

    if fila is None:
        return None

    return {
        "id": fila[0],
        "titulo": fila[1],
        "descripcion": fila[2],
        "agente_asignado": fila[3],
        "estado": fila[4],
        "energia_requerida": fila[5],
        "created_at": fila[6]
    }


def listar_misiones_agente(nombre):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM misiones WHERE agente_asignado = ?", (nombre,))
    filas = cursor.fetchall()
    conn.close()

    return [
        {
            "id": f[0],
            "titulo": f[1],
            "descripcion": f[2],
            "estado": f[4]
        }
        for f in filas
    ]


def completar_mision(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT agente_asignado, energia_requerida FROM misiones WHERE id = ?", (id,))
    fila = cursor.fetchone()

    if fila is None:
        conn.close()
        return None

    agente_nombre, energia = fila

    cursor.execute("UPDATE misiones SET estado = 'completada' WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return agente_nombre, energia


def actualizar_energia(nombre, nueva_energia):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre)
    )

    conn.commit()
    conn.close()