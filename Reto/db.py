# Reto de Consolidación - Agencia del Olimpo
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# db.py — Funciones SQLite (NO tiene FastAPI)

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


# Crear tablas

def crear_tablas() -> None:
    """Crea las tablas agentes, mensajes y misiones si no existen."""
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
            titulo TEXT NOT NULL,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT DEFAULT 'pendiente',
            energia_requerida INTEGER,
            prioridad TEXT DEFAULT 'media',
            recompensa INTEGER DEFAULT 0,
            reintentos INTEGER DEFAULT 0,
            created_at TEXT,
            completed_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# Funciones de agentes

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """Registra un agente en la base de datos. Retorna mensaje de éxito o error."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia),
        )
        conn.commit()
        resultado = f"Agente '{nombre}' registrado con éxito."
    except sqlite3.IntegrityError:
        resultado = f"Error: El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str) -> dict | None:
    """Busca un agente por nombre. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def listar_agentes() -> list[dict]:
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def actualizar_energia_agente(nombre: str, nueva_energia: int) -> None:
    """Actualiza la energía de un agente en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre))
    conn.commit()
    conn.close()


# Funciones de mensajes

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """Inserta un mensaje en la tabla mensajes con timestamp automático."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, timestamp),
    )
    conn.commit()
    conn.close()
    return f"Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."


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


# Funciones de misiones

def crear_mision(titulo: str, descripcion: str, agente_asignado: str,
                 energia_requerida: int, prioridad: str = "media",
                 recompensa: int = 0) -> int:
    """Crea una misión con estado 'pendiente'. Retorna el id generado."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO misiones
           (titulo, descripcion, agente_asignado, estado, energia_requerida,
            prioridad, recompensa, reintentos, created_at, completed_at)
           VALUES (?, ?, ?, 'pendiente', ?, ?, ?, 0, ?, NULL)""",
        (titulo, descripcion, agente_asignado, energia_requerida,
         prioridad, recompensa, created_at),
    )
    conn.commit()
    mision_id = cursor.lastrowid
    conn.close()
    return mision_id


def obtener_mision(mision_id: int) -> dict | None:
    """Busca una misión por id. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado,
                  energia_requerida, prioridad, recompensa, reintentos,
                  created_at, completed_at
           FROM misiones WHERE id = ?""",
        (mision_id,),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {
        "id": fila[0], "titulo": fila[1], "descripcion": fila[2],
        "agente_asignado": fila[3], "estado": fila[4],
        "energia_requerida": fila[5], "prioridad": fila[6],
        "recompensa": fila[7], "reintentos": fila[8],
        "created_at": fila[9], "completed_at": fila[10]
    }


def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    """Lista todas las misiones asignadas a un agente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado,
                  energia_requerida, prioridad, recompensa, reintentos,
                  created_at, completed_at
           FROM misiones WHERE agente_asignado = ? ORDER BY created_at""",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0], "titulo": f[1], "descripcion": f[2],
            "agente_asignado": f[3], "estado": f[4],
            "energia_requerida": f[5], "prioridad": f[6],
            "recompensa": f[7], "reintentos": f[8],
            "created_at": f[9], "completed_at": f[10]
        }
        for f in filas
    ]


def completar_mision_db(mision_id: int) -> bool:
    """Marca una misión como 'completada' con timestamp. Retorna True si existía."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    completed_at = datetime.datetime.now().isoformat()
    cursor.execute(
        "UPDATE misiones SET estado = 'completada', completed_at = ? WHERE id = ? AND estado != 'completada'",
        (completed_at, mision_id),
    )
    conn.commit()
    cambios = cursor.rowcount
    conn.close()
    return cambios > 0


def reintentar_mision_db(mision_id: int) -> bool:
    """Reintenta una misión fallida: estado → 'pendiente', reintentos + 1."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = 'pendiente', reintentos = reintentos + 1 WHERE id = ? AND estado = 'fallida'",
        (mision_id,),
    )
    conn.commit()
    cambios = cursor.rowcount
    conn.close()
    return cambios > 0


def fallar_mision_db(mision_id: int) -> bool:
    """Marca una misión como 'fallida'."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = 'fallida' WHERE id = ? AND estado IN ('pendiente', 'en_curso')",
        (mision_id,),
    )
    conn.commit()
    cambios = cursor.rowcount
    conn.close()
    return cambios > 0
