"""
seed.py — Poblar la base de datos con datos de semilla

Crea:
  - 3 agentes con distintos roles y niveles de energía
  - 5 mensajes entre agentes
  - 3 misiones en estados distintos (pendiente, en_curso, completada)

Ejecutar UNA sola vez antes de entregar el PR:
    python seed.py   (desde la carpeta Reto/)
"""

import sys
import os

# Asegura que los imports de db.py funcionen desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import (
    crear_tablas,
    registrar_agente,
    enviar_mensaje,
    crear_mision,
    actualizar_estado_mision,
)

print("Inicializando esquema de base de datos...")
crear_tablas()

# ---------------------------------------------------------------------------
# Agentes
# ---------------------------------------------------------------------------
print("\n[Agentes]")
agentes = [
    ("Athena", "admin", 150),
    ("Atlas",  "explorador", 100),
    ("Orion",  "explorador", 80),
]
for nombre, rol, energia in agentes:
    msg = registrar_agente(nombre, rol, energia)
    print(f"  {msg}")

# ---------------------------------------------------------------------------
# Mensajes (5 en total)
# ---------------------------------------------------------------------------
print("\n[Mensajes]")
mensajes = [
    ("Athena", "Atlas",  "Informe de sector norte recibido. Buen trabajo."),
    ("Atlas",  "Athena", "Perifereo norte despejado. Iniciando retorno."),
    ("Orion",  "Base",   "Solicitud de suministros para misión larga duración."),
    ("Athena", "Orion",  "Suministros aprobados. Lista de entrega adjunta."),
    ("Atlas",  "Orion",  "Nos vemos en el punto de extracción a las 18:00."),
]
for rem, dest, contenido in mensajes:
    msg = enviar_mensaje(rem, dest, contenido)
    print(f"  {msg}")

# ---------------------------------------------------------------------------
# Misiones en 3 estados distintos
# ---------------------------------------------------------------------------
print("\n[Misiones]")

# Misión 1: pendiente
id1 = crear_mision(
    titulo="Infiltración en Sector Delta",
    descripcion="Recopilar información sobre movimientos en el sector Delta sin ser detectado.",
    agente_asignado="Orion",
    estado="pendiente",
    energia_requerida=30,
    prioridad="alta",
    creado_por="Athena",
)
print(f"  Misión id={id1} creada (estado: pendiente)")

# Misión 2: en_curso
id2 = crear_mision(
    titulo="Reconocimiento Zona Alpha",
    descripcion="Explorar el perímetro norte e informar hallazgos al cuartel central.",
    agente_asignado="Atlas",
    estado="en_curso",
    energia_requerida=20,
    prioridad="media",
    creado_por="Athena",
)
print(f"  Misión id={id2} creada (estado: en_curso)")

# Misión 3: completada
id3 = crear_mision(
    titulo="Extracción de Agente en Campo",
    descripcion="Extraer al agente Orion del sector comprometido antes del amanecer.",
    agente_asignado="Athena",
    estado="pendiente",
    energia_requerida=15,
    prioridad="alta",
    creado_por="sistema",
)
actualizar_estado_mision(id3, "completada")
print(f"  Misión id={id3} creada (estado: completada)")

print("\n✓ Semilla completada. La base de datos agentes.db está lista.")
