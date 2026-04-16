## Creado por: Sergio Jaramillo (SergiJaramilloL)
# -----------------------------------------------------------#
# db.py — Capa de acceso a datos (SQLite)
# -----------------------------------------------------------#
# Este módulo es el único lugar del proyecto que habla con la
# base de datos. Ningún otro archivo escribe SQL en crudo.
# Regla: siempre usar parámetros `?` en las queries — nunca
# construir SQL con f-strings para evitar inyección SQL.
# -----------------------------------------------------------#

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


# =====================
# CREAR TABLAS
# =====================

def crear_tablas() -> None:
    """Crea las tablas agentes, mensajes y misiones si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla agentes: misma estructura que S5.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre TEXT PRIMARY KEY,
            rol TEXT,
            energia INTEGER
        )
    """)

    # Tabla mensajes: misma estructura que S5.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente TEXT,
            destinatario TEXT,
            contenido TEXT,
            timestamp TEXT
        )
    """)

    # Tabla misiones: esquema mínimo del reto + columnas extras.
    # `prioridad` (1-5): permite ordenar misiones por urgencia sin lógica extra en el servidor.
    # `recompensa`: tokens que el agente ganará al completar la misión — incentivo visible en el briefing.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT,
            energia_requerida INTEGER,
            prioridad INTEGER DEFAULT 1,
            recompensa INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# =====================
# AGENTES
# =====================

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
        resultado = f"[DB] Agente '{nombre}' registrado con éxito."
    except sqlite3.IntegrityError:
        resultado = f"[DB] Error: El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str) -> dict | None:
    """Busca un agente por nombre. Retorna dict con sus datos o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def actualizar_energia_agente(nombre: str, nueva_energia: int) -> None:
    """Actualiza el nivel de energía de un agente en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # UPDATE con parámetros `?` para evitar inyección SQL.
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre),
    )
    conn.commit()
    conn.close()


def listar_agentes() -> list[dict]:
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


# =====================
# MENSAJES
# =====================

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


# =====================
# MISIONES
# =====================

def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    estado: str,
    energia_requerida: int,
    prioridad: int,
    recompensa: int,
) -> int:
    """
    Inserta una misión nueva y retorna el id generado.

    Retorna:
        int: Id de la misión recién creada.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO misiones
           (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, recompensa, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, recompensa, created_at),
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id


def obtener_mision(mision_id: int) -> dict | None:
    """Busca una misión por id. Retorna dict con sus datos o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, recompensa, created_at FROM misiones WHERE id = ?",
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
        "recompensa": fila[7], "created_at": fila[8],
    }


def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    """Retorna todas las misiones asignadas a un agente, ordenadas por prioridad descendente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, recompensa, created_at
           FROM misiones WHERE agente_asignado = ? ORDER BY prioridad DESC""",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0], "titulo": f[1], "descripcion": f[2],
            "agente_asignado": f[3], "estado": f[4],
            "energia_requerida": f[5], "prioridad": f[6],
            "recompensa": f[7], "created_at": f[8],
        }
        for f in filas
    ]


def marcar_mision_completada(mision_id: int) -> None:
    """Actualiza el estado de una misión a 'completada'."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = 'completada' WHERE id = ?",
        (mision_id,),
    )
    conn.commit()
    conn.close()

## Creado por: Sergio Jaramillo (SergiJaramilloL)
