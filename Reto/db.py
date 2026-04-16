"""
db.py — Capa de persistencia con SQLite

Todas las operaciones con la base de datos están aquí.
Este módulo NO conoce FastAPI ni las clases de dominio (solo recibe/retorna dicts).

Funciones para:
- Agentes: crear, registrar, despertar, listar, actualizar
- Mensajes: enviar, leer bandeja
- Misiones: crear, obtener, listar por agente, completar
"""

import sqlite3
import datetime
from typing import Dict, List, Optional
from config import DB_PATH


def crear_tablas() -> None:
    """Crea las tablas agentes, mensajes y misiones si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla agentes (de Semana 5)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre TEXT PRIMARY KEY,
            rol TEXT NOT NULL,
            energia INTEGER NOT NULL
        )
    """)
    
    # Tabla mensajes (de Semana 5)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente TEXT NOT NULL,
            destinatario TEXT NOT NULL,
            contenido TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    # Tabla misiones (NUEVA para el reto)
    # Columnas extra agregadas: prioridad, recompensa, creado_por
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            energia_requerida INTEGER NOT NULL,
            prioridad TEXT DEFAULT 'media',
            recompensa INTEGER DEFAULT 0,
            creado_por TEXT,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (agente_asignado) REFERENCES agentes(nombre)
        )
    """)
    
    conn.commit()
    conn.close()


# ===================================================================
# FUNCIONES PARA AGENTES (reutilizadas de Semana 5)
# ===================================================================

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


def despertar_agente(nombre: str) -> Optional[Dict]:
    """Busca un agente por nombre. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    
    if fila is None:
        return None
    
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def actualizar_energia_agente(nombre: str, nueva_energia: int) -> bool:
    """Actualiza la energía de un agente. Retorna True si tuvo éxito."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre)
    )
    filas_afectadas = cursor.rowcount
    conn.commit()
    conn.close()
    return filas_afectadas > 0


def listar_agentes() -> List[Dict]:
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes ORDER BY nombre")
    filas = cursor.fetchall()
    conn.close()
    
    return [
        {"nombre": f[0], "rol": f[1], "energia": f[2]}
        for f in filas
    ]


# ===================================================================
# FUNCIONES PARA MENSAJES (reutilizadas de Semana 5)
# ===================================================================

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


def leer_mensajes(nombre_agente: str) -> List[Dict]:
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


# ===================================================================
# FUNCIONES PARA MISIONES (NUEVAS para el reto)
# ===================================================================

def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    energia_requerida: int,
    prioridad: str = "media",
    recompensa: int = 0,
    creado_por: str = "sistema"
) -> int:
    """
    Crea una nueva misión en la base de datos.
    Retorna el ID de la misión creada.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    
    cursor.execute(
        """INSERT INTO misiones 
        (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, recompensa, creado_por, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (titulo, descripcion, agente_asignado, "pendiente", energia_requerida, prioridad, recompensa, creado_por, timestamp)
    )
    
    mision_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return mision_id


def obtener_mision(mision_id: int) -> Optional[Dict]:
    """Obtiene una misión por su ID. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida, 
        prioridad, recompensa, creado_por, created_at, completed_at 
        FROM misiones WHERE id = ?""",
        (mision_id,)
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
        "recompensa": fila[7],
        "creado_por": fila[8],
        "created_at": fila[9],
        "completed_at": fila[10]
    }


def listar_misiones_agente(nombre_agente: str) -> List[Dict]:
    """Lista todas las misiones asignadas a un agente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida,
        prioridad, recompensa, creado_por, created_at, completed_at
        FROM misiones WHERE agente_asignado = ? ORDER BY created_at DESC""",
        (nombre_agente,)
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
            "recompensa": f[7],
            "creado_por": f[8],
            "created_at": f[9],
            "completed_at": f[10]
        }
        for f in filas
    ]


def completar_mision(mision_id: int) -> bool:
    """
    Marca una misión como completada.
    Retorna True si tuvo éxito, False si no existe o ya estaba completada.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    
    cursor.execute(
        "UPDATE misiones SET estado = ?, completed_at = ? WHERE id = ? AND estado != 'completada'",
        ("completada", timestamp, mision_id)
    )
    
    filas_afectadas = cursor.rowcount
    conn.commit()
    conn.close()
    
    return filas_afectadas > 0
