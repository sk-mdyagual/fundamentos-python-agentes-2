# db.py — Capa de persistencia SQLite para Cyber-Mercs
# AUDITORÍA: Este archivo concentra TODA la interacción con la base de datos.
# Ningún otro módulo ejecuta SQL directamente, garantizando el principio
# de responsabilidad única (SRP).

import sqlite3
import logging
from contextlib import contextmanager
from config import DB_PATH

logger = logging.getLogger(__name__)


@contextmanager
def _conn():
    """Context manager que garantiza commit + close incluso ante excepciones."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def reset_db() -> None:
    """Elimina todas las tablas. Solo se invoca vía DELETE /reset (no en arranque)."""
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS implantes")
        cur.execute("DROP TABLE IF EXISTS comunicaciones")
        cur.execute("DROP TABLE IF EXISTS contratos")
        cur.execute("DROP TABLE IF EXISTS mercs")
    logger.info("Base de datos corporativa reseteada.")


def crear_tablas() -> None:
    """Crea las 4 tablas si no existen. Idempotente."""
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mercs (
                alias TEXT PRIMARY KEY,
                clase_nombre TEXT,
                hp INTEGER,
                creditos INTEGER,
                estado_vital TEXT DEFAULT 'vivo'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                tipo_contrato TEXT,
                mercenario_asignado TEXT,
                dano_estimado INTEGER,
                pago_base INTEGER,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY(mercenario_asignado) REFERENCES mercs(alias)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comunicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente TEXT,
                destinatario TEXT,
                contenido TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # UNIQUE evita que un mercenario acumule duplicados del mismo implante.
        cur.execute("""
            CREATE TABLE IF NOT EXISTS implantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mercenario_alias TEXT,
                nombre_implante TEXT,
                FOREIGN KEY(mercenario_alias) REFERENCES mercs(alias),
                UNIQUE(mercenario_alias, nombre_implante)
            )
        """)
    logger.info("Tablas de la corporación verificadas/creadas.")


def hay_mercenarios() -> bool:
    """Indica si la tabla mercs ya tiene registros (para evitar reseed innecesario)."""
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM mercs LIMIT 1")
        return cur.fetchone() is not None


def registrar_merc(alias: str, clase_nombre: str, hp: int, creditos: int) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO mercs (alias, clase_nombre, hp, creditos) VALUES (?, ?, ?, ?)",
            (alias, clase_nombre, hp, creditos),
        )


def obtener_merc(alias: str) -> dict | None:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT alias, clase_nombre, hp, creditos, estado_vital FROM mercs WHERE alias = ?",
            (alias,),
        )
        fila = cur.fetchone()
    if fila is None:
        return None
    return {"alias": fila[0], "clase_nombre": fila[1], "hp": fila[2], "creditos": fila[3], "estado_vital": fila[4]}


def listar_mercs() -> list[dict]:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT alias, clase_nombre, hp, creditos, estado_vital FROM mercs")
        filas = cur.fetchall()
    return [{"alias": f[0], "clase_nombre": f[1], "hp": f[2], "creditos": f[3], "estado_vital": f[4]} for f in filas]


def actualizar_hp(alias: str, nuevo_hp: int) -> None:
    with _conn() as conn:
        conn.execute("UPDATE mercs SET hp = ? WHERE alias = ?", (nuevo_hp, alias))


def actualizar_creditos(alias: str, nuevos_creditos: int) -> None:
    """Setter directo. Para descuentos condicionados usar descontar_creditos_atomico."""
    with _conn() as conn:
        conn.execute("UPDATE mercs SET creditos = ? WHERE alias = ?", (nuevos_creditos, alias))


def descontar_creditos_atomico(alias: str, monto: int) -> bool:
    """Descuenta `monto` créditos solo si el saldo alcanza, en una sola sentencia SQL.
    Retorna True si se aplicó el descuento, False si no había fondos.
    Cierra la race condition entre dos sobornos concurrentes."""
    with _conn() as conn:
        cur = conn.execute(
            "UPDATE mercs SET creditos = creditos - ? WHERE alias = ? AND creditos >= ?",
            (monto, alias, monto),
        )
        return cur.rowcount > 0


def actualizar_estado_vital(alias: str, nuevo_estado: str) -> None:
    with _conn() as conn:
        conn.execute("UPDATE mercs SET estado_vital = ? WHERE alias = ?", (nuevo_estado, alias))


def crear_contrato_db(titulo: str, tipo_contrato: str, merc_asignado: str, dano_estimado: int, pago_base: int) -> int:
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO contratos (titulo, tipo_contrato, mercenario_asignado, dano_estimado, pago_base) VALUES (?, ?, ?, ?, ?)",
            (titulo, tipo_contrato, merc_asignado, dano_estimado, pago_base),
        )
        return cur.lastrowid


def obtener_contrato_db(contrato_id: int) -> dict | None:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, titulo, tipo_contrato, mercenario_asignado, dano_estimado, pago_base, estado FROM contratos WHERE id = ?",
            (contrato_id,),
        )
        fila = cur.fetchone()
    if fila is None:
        return None
    return {"id": fila[0], "titulo": fila[1], "tipo_contrato": fila[2], "mercenario_asignado": fila[3], "dano_estimado": fila[4], "pago_base": fila[5], "estado": fila[6]}


def completar_contrato_db(contrato_id: int) -> None:
    with _conn() as conn:
        conn.execute("UPDATE contratos SET estado = 'completado' WHERE id = ?", (contrato_id,))


def fallar_contrato_db(contrato_id: int) -> None:
    with _conn() as conn:
        conn.execute("UPDATE contratos SET estado = 'fallido' WHERE id = ?", (contrato_id,))


def obtener_contratos_por_merc(alias: str) -> list[dict]:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, estado FROM contratos WHERE mercenario_asignado = ?", (alias,))
        filas = cur.fetchall()
    return [{"id": f[0], "titulo": f[1], "estado": f[2]} for f in filas]


def guardar_mensaje(remitente: str, destinatario: str, contenido: str) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO comunicaciones (remitente, destinatario, contenido) VALUES (?, ?, ?)",
            (remitente, destinatario, contenido),
        )


def leer_mensajes(alias: str) -> list[dict]:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT remitente, contenido, timestamp FROM comunicaciones WHERE destinatario = ?",
            (alias,),
        )
        filas = cur.fetchall()
    return [{"remitente": f[0], "contenido": f[1], "timestamp": f[2]} for f in filas]


def agregar_implante(alias: str, implante: str) -> bool:
    """Inserta un implante. Si el mercenario ya lo posee (UNIQUE), no lo duplica.
    Retorna True si se insertó, False si era duplicado."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO implantes (mercenario_alias, nombre_implante) VALUES (?, ?)",
                (alias, implante),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def listar_implantes(alias: str) -> list[dict]:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT nombre_implante FROM implantes WHERE mercenario_alias = ?", (alias,))
        filas = cur.fetchall()
    return [{"nombre_implante": f[0]} for f in filas]
