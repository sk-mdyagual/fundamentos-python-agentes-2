from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "agentes.db"


def _get_conn() -> sqlite3.Connection:
    # Esta función la uso para no repetir la conexion en cada funcion
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Aquí tengo todas las funciones relacionadas con la base de datos. Crear tablas, insertar datos, consultar, etc.

# La función crear_tablas se asegura de que las tablas necesarias existan antes de que el servidor empiece a manejar solicitudes.
def crear_tablas() -> None:
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agentes (
                nombre TEXT PRIMARY KEY,
                rol TEXT NOT NULL,
                energia INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente TEXT NOT NULL,
                destinatario TEXT NOT NULL,
                contenido TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS misiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                agente_asignado TEXT,
                estado TEXT,
                energia_requerida INTEGER,
                prioridad TEXT,
                deadline TEXT,
                creado_por TEXT,
                created_at TEXT
            )
            """
        )

# Registro de agentes, mensajes y misiones. Consultas para listar agentes, leer mensajes, obtener misiones, etc.
def registrar_agente(nombre: str, rol: str, energia: int) -> bool:
    now = datetime.now().isoformat()
    try:
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO agentes (nombre, rol, energia, created_at) VALUES (?, ?, ?, ?)",
                (nombre, rol, energia, now),
            )
        return True
    except sqlite3.IntegrityError:
        return False
 
def listar_agentes() -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT nombre, rol, energia, created_at FROM agentes ORDER BY nombre"
        ).fetchall()
    return [dict(row) for row in rows]

# La función despertar_agente se encarga de cargar los datos de un agente específico desde la base de datos, lo que permite que el servidor pueda acceder a su información cuando sea necesario.
def despertar_agente(nombre: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT nombre, rol, energia, created_at FROM agentes WHERE nombre = ?",
            (nombre,),
        ).fetchone()
    return dict(row) if row else None

# La función actualizar_energia_agente se utiliza para modificar la cantidad de energía de un agente específico, lo que es fundamental para gestionar las misiones y acciones que el agente puede realizar.
def actualizar_energia_agente(nombre: str, energia: int) -> bool:
    with _get_conn() as conn:
        cursor = conn.execute(
            "UPDATE agentes SET energia = ? WHERE nombre = ?",
            (energia, nombre),
        )
    return cursor.rowcount > 0


def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    timestamp = datetime.now().isoformat()
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
            (remitente, destinatario, contenido, timestamp),
        )
    return f"Mensaje de '{remitente}' a '{destinatario}' enviado."

# La función leer_mensajes permite recuperar todos los mensajes dirigidos a un agente específico, lo que es esencial para que el agente pueda procesar su correspondencia y responder adecuadamente.
def leer_mensajes(nombre_agente: str) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, remitente, destinatario, contenido, timestamp
            FROM mensajes
            WHERE destinatario = ?
            ORDER BY timestamp
            """,
            (nombre_agente,),
        ).fetchall()
    return [dict(row) for row in rows]

# La función crear_mision se encarga de insertar una nueva misión en la base de datos, asignándola a un agente específico.
def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    estado: str,
    energia_requerida: int,
    prioridad: str,
    deadline: Optional[str],
    creado_por: str,
) -> int:
    created_at = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO misiones
            (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, deadline, creado_por, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                titulo,
                descripcion,
                agente_asignado,
                estado,
                energia_requerida,
                prioridad,
                deadline,
                creado_por,
                created_at,
            ),
        )
    return int(cursor.lastrowid)

# La función obtener_mision permite recuperar los detalles de una misión específica utilizando su ID, lo que es crucial para que el agente pueda conocer las tareas asignadas y su estado actual.
def obtener_mision(mision_id: int) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            """
            SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida,
                   prioridad, deadline, creado_por, created_at
            FROM misiones
            WHERE id = ?
            """,
            (mision_id,),
        ).fetchone()
    return dict(row) if row else None

# La función listar_misiones_por_agente permite obtener todas las misiones asignadas a un agente específico, lo que es fundamental para que el agente pueda gestionar sus tareas y prioridades de manera efectiva.
def listar_misiones_por_agente(nombre: str) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida,
                   prioridad, deadline, creado_por, created_at
            FROM misiones
            WHERE agente_asignado = ?
            ORDER BY id DESC
            """,
            (nombre,),
        ).fetchall()
    return [dict(row) for row in rows]

# La función actualizar_estado_mision se utiliza para modificar el estado de una misión específica, lo que es fundamental para gestionar el progreso de las tareas asignadas.
def actualizar_estado_mision(mision_id: int, estado: str) -> bool:
    with _get_conn() as conn:
        cursor = conn.execute(
            "UPDATE misiones SET estado = ? WHERE id = ?",
            (estado, mision_id),
        )
    return cursor.rowcount > 0

# La función agente_existe se utiliza para verificar si un agente específico existe en la base de datos.
def agente_existe(nombre: str) -> bool:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT nombre FROM agentes WHERE nombre = ?",
            (nombre,),
        ).fetchone()
    return row is not None

# La función eliminar_mision se encarga de eliminar una misión específica de la base de datos utilizando su ID, lo que puede ser necesario para gestionar misiones canceladas o incorrectas.
def insertar_datos_semilla() -> None:
    crear_tablas()
    with _get_conn() as conn:
        agentes_count = conn.execute("SELECT COUNT(*) FROM agentes").fetchone()[0]
        mensajes_count = conn.execute("SELECT COUNT(*) FROM mensajes").fetchone()[0]
        misiones_count = conn.execute("SELECT COUNT(*) FROM misiones").fetchone()[0]

        if agentes_count == 0:
            now = datetime.now().isoformat()
            conn.executemany(
                "INSERT INTO agentes (nombre, rol, energia, created_at) VALUES (?, ?, ?, ?)",
                [
                    ("Atlas", "operativo", 120, now),
                    ("Nova", "analista", 110, now),
                    ("admin", "admin", 200, now),
                ],
            )

        if mensajes_count == 0:
            now = datetime.now().isoformat()
            conn.executemany(
                "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
                [
                    ("Atlas", "Nova", "Reporte de zona norte listo.", now),
                    ("Nova", "Atlas", "Recibido. Inicia validacion.", now),
                    ("admin", "Atlas", "Prioriza mision alfa.", now),
                    ("Atlas", "admin", "Mision alfa en progreso.", now),
                    ("Nova", "admin", "Analisis de riesgo enviado.", now),
                ],
            )

        if misiones_count == 0:
            now = datetime.now().isoformat()
            conn.executemany(
                """
                INSERT INTO misiones
                (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, deadline, creado_por, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        "Reconocimiento sector A",
                        "Levantar mapa de riesgos.",
                        "Atlas",
                        "pendiente",
                        15,
                        "alta",
                        None,
                        "admin",
                        now,
                    ),
                    (
                        "Correlacion de datos",
                        "Cruzar telemetria y logs.",
                        "Nova",
                        "en_curso",
                        10,
                        "media",
                        None,
                        "admin",
                        now,
                    ),
                    (
                        "Entrega informe inicial",
                        "Consolidar hallazgos de campo.",
                        "Atlas",
                        "completada",
                        8,
                        "baja",
                        None,
                        "admin",
                        now,
                    ),
                ],
            )
