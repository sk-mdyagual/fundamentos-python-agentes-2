import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")

# -----------------------------------------------------------#
# SECCION A: Funciones del modulo (siempre disponibles)
# -----------------------------------------------------------#
# Estas funciones NO estan comentadas porque otros archivos
# las importan. No las modifiques a menos que se indique.
# -----------------------------------------------------------#


def crear_tablas() -> None:
    """Crea las tablas agentes y mensajes si no existen."""
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
            estado TEXT,
            tiempo_estimado INTEGER,
            energia_requerida INTEGER,
            created_at TEXT
)
    """)
    conn.commit()
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
        resultado = f"El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str) -> dict | None:
    """Busca un agente por nombre. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,)
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


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
    return (
        f"[DB] Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."
    )


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
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def registrar_mision(
    titulo: str, descripcion: str, agente_asignado: str, tiempo:int ,energia: int
) -> str | None:

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM agentes WHERE nombre = ?", (agente_asignado,))
    fila = cursor.fetchone()
    if fila is None:
        conn.close()
        return None

    timestamp = datetime.datetime.now().isoformat()
    estado: str = "pendiente"
    cursor.execute(
        "INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, tiempo_estimado, energia_requerida, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (titulo, descripcion, agente_asignado, estado, tiempo, energia, timestamp),
    )
    conn.commit()
    resultado = f"[DB] Mision '{titulo}' registrada con exito."
    conn.close()
    return resultado


def obtener_mision(mision_id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, agente_asignado, estado, tiempo_estimado, energia_requerida, created_at FROM misiones WHERE id = ?",
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
        "tiempo_estimado": fila[5],
        "energia_requerida": fila[6],
        "fecha_creacion": fila[7],
    }


def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, agente_asignado, estado, tiempo_estimado, energia_requerida, created_at FROM misiones WHERE agente_asignado = ? ORDER BY id",
        (nombre_agente,),
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
            "tiempo_estimado": f[5],
            "energia_requerida": f[6],
            "created_at": f[7],
        }
        for f in filas
    ]


def actualizar_estado_mision(mision_id: int, estado: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE misiones SET estado = ? WHERE id = ?", (estado, mision_id))
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    return filas_afectadas > 0


def actualizar_energia_agente(nombre: str, energia: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE agentes SET energia = ? WHERE nombre = ?", (energia, nombre))
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    return filas_afectadas > 0
