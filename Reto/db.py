"""
db.py — Capa de persistencia SQLite para La Agencia de Agentes

Contiene funciones que hablan con SQLite:
  - crear_tablas            → inicializa el esquema
  - registrar_agente        → INSERT en agentes
  - despertar_agente        → SELECT por nombre (retorna dict | None)
  - listar_agentes          → SELECT todos los agentes
  - actualizar_energia      → UPDATE energia de un agente
  - enviar_mensaje          → INSERT en mensajes
  - leer_mensajes           → SELECT mensajes por destinatario
  - crear_mision            → INSERT en misiones (retorna id)
  - obtener_mision          → SELECT misión por id
  - listar_misiones_agente  → SELECT misiones por agente_asignado
  - actualizar_estado_mision → UPDATE estado de una misión

Restricción: No hay imports de fastapi aquí.
             Toda query usa parámetros ? — nunca f-strings con SQL.
"""

import sqlite3
import datetime
import os

# La base de datos vive en la misma carpeta que este archivo.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


def _conexion() -> sqlite3.Connection:
    """Abre y retorna una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)


# ---------------------------------------------------------------------------
# Inicialización del esquema
# ---------------------------------------------------------------------------

def crear_tablas() -> None:
    """
    Crea las tablas agentes, mensajes y misiones si no existen todavía.
    Se llama al arrancar el servidor para garantizar que el esquema existe
    antes de procesar cualquier petición.
    """
    conn = _conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre  TEXT PRIMARY KEY,
            rol     TEXT,
            energia INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente    TEXT,
            destinatario TEXT,
            contenido    TEXT,
            timestamp    TEXT
        )
    """)

    # Columnas extra respecto al mínimo del reto:
    #   prioridad  → permite triaje rápido de misiones (alta/media/baja)
    #   creado_por → trazabilidad: saber qué operador o sistema originó la misión
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo           TEXT NOT NULL,
            descripcion      TEXT,
            agente_asignado  TEXT,
            estado           TEXT,
            energia_requerida INTEGER,
            prioridad        TEXT,
            creado_por       TEXT,
            created_at       TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Funciones de agentes
# ---------------------------------------------------------------------------

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """
    Inserta un agente nuevo. Retorna mensaje de éxito o de error
    si el nombre ya existe (PRIMARY KEY duplicada).
    """
    conn = _conexion()
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
    """
    Busca un agente por nombre. Retorna un dict con sus datos
    o None si no existe en la base de datos.
    """
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?",
        (nombre,),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def listar_agentes() -> list[dict]:
    """Retorna una lista con todos los agentes registrados."""
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def actualizar_energia(nombre: str, nueva_energia: int) -> None:
    """Persiste la nueva energía de un agente después de ejecutar una misión."""
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Funciones de mensajes
# ---------------------------------------------------------------------------

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """
    Inserta un mensaje con timestamp automático en formato ISO.
    Retorna un string descriptivo del resultado.
    """
    conn = _conexion()
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
    """
    Retorna todos los mensajes dirigidos a un agente, ordenados
    cronológicamente por timestamp.
    """
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT remitente, destinatario, contenido, timestamp
        FROM mensajes
        WHERE destinatario = ?
        ORDER BY timestamp
        """,
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "remitente": f[0],
            "destinatario": f[1],
            "contenido": f[2],
            "timestamp": f[3],
        }
        for f in filas
    ]


# ---------------------------------------------------------------------------
# Funciones de misiones
# ---------------------------------------------------------------------------

def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    estado: str,
    energia_requerida: int,
    prioridad: str,
    creado_por: str,
) -> int:
    """
    Inserta una nueva misión y retorna el id generado (AUTOINCREMENT).
    El timestamp se genera automáticamente en el momento de la inserción.
    """
    conn = _conexion()
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO misiones
            (titulo, descripcion, agente_asignado, estado, energia_requerida,
             prioridad, creado_por, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (titulo, descripcion, agente_asignado, estado,
         energia_requerida, prioridad, creado_por, created_at),
    )
    conn.commit()
    mision_id = cursor.lastrowid
    conn.close()
    return mision_id


def obtener_mision(mision_id: int) -> dict | None:
    """Busca una misión por id. Retorna dict o None si no existe."""
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, titulo, descripcion, agente_asignado, estado,
               energia_requerida, prioridad, creado_por, created_at
        FROM misiones
        WHERE id = ?
        """,
        (mision_id,),
    )
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
        "prioridad": fila[6],
        "creado_por": fila[7],
        "created_at": fila[8],
    }


def listar_misiones_agente(nombre: str) -> list[dict]:
    """Retorna todas las misiones asignadas a un agente, ordenadas por fecha."""
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, titulo, descripcion, agente_asignado, estado,
               energia_requerida, prioridad, creado_por, created_at
        FROM misiones
        WHERE agente_asignado = ?
        ORDER BY created_at
        """,
        (nombre,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0],
            "titulo": f[1],
            "descripcion": f[2],
            "agente_asignado": f[3],
            "estado": f[4],
            "energia_requerida": f[5],
            "prioridad": f[6],
            "creado_por": f[7],
            "created_at": f[8],
        }
        for f in filas
    ]


def actualizar_estado_mision(mision_id: int, estado: str) -> None:
    """Actualiza el estado de una misión (pendiente | en_curso | completada | fallida)."""
    conn = _conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = ? WHERE id = ?",
        (estado, mision_id),
    )
    conn.commit()
    conn.close()
