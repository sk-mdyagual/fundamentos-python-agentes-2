"""
seed_data.py — Script para poblar la base de datos con datos iniciales

Crea agentes, mensajes y misiones de ejemplo para demostración.
Ejecutar una sola vez después de crear las tablas.

Uso: python seed_data.py
"""

import db

def poblar_base_datos():
    """Crea datos."""
    
    print("=" * 60)
    print("  POBLANDO BASE DE DATOS")
    print("=" * 60)
    
    # Crear tablas si no existen
    db.crear_tablas()
    print("Tablas verificadas")
    

    print("\n Creando agentes...")
    
    agentes = [
        ("Atlas", "explorador", 200),
        ("Nova", "cientifica", 180),
        ("Titan", "admin", 250),
        ("Hermes", "mensajero", 150),
    ]
    
    for nombre, rol, energia in agentes:
        resultado = db.registrar_agente(nombre, rol, energia)
        print(f"  {resultado}")
    
    # ===================================================================
    # MENSAJES (mínimo 5)
    # ===================================================================
    print("\n📨 Enviando mensajes...")
    
    mensajes = [
        ("Atlas", "Nova", "He descubierto una anomalía en el Sector Gamma. Requiero análisis científico."),
        ("Nova", "Atlas", "Datos recibidos. Analizando patrones. Resultados en 24 horas."),
        ("Titan", "Atlas", "Misión aprobada. Procede con precaución."),
        ("Hermes", "Nova", "Entrega de suministros completada en tu laboratorio."),
        ("Nova", "Hermes", "Gracias. Suministros recibidos en perfectas condiciones."),
        ("Titan", "Hermes", "Actualización del protocolo de comunicaciones en las próximas 48h."),
    ]
    
    for remitente, destinatario, contenido in mensajes:
        resultado = db.enviar_mensaje(remitente, destinatario, contenido)
        print(f"  {resultado}")
    
    # ===================================================================
    # MISIONES (mínimo 3, en estados distintos)
    # ===================================================================
    print("\n🎯 Creando misiones...")
    
    # Misión 1: Pendiente
    mision1_id = db.crear_mision(
        titulo="Explorar Sector Gamma",
        descripcion="Investigar la anomalía detectada en las coordenadas G-42-7.",
        agente_asignado="Atlas",
        energia_requerida=80,
        prioridad="alta",
        recompensa=100,
        creado_por="Titan"
    )
    print(f"  ✅ Misión #{mision1_id} creada: Explorar Sector Gamma (pendiente)")
    
    # Misión 2: Pendiente
    mision2_id = db.crear_mision(
        titulo="Análisis de muestras",
        descripcion="Analizar las muestras recolectadas en la misión anterior.",
        agente_asignado="Nova",
        energia_requerida=50,
        prioridad="media",
        recompensa=75,
        creado_por="Titan"
    )
    print(f"  ✅ Misión #{mision2_id} creada: Análisis de muestras (pendiente)")
    
    # Misión 3: Crear y completar inmediatamente
    mision3_id = db.crear_mision(
        titulo="Ruta de comunicaciones",
        descripcion="Establecer nueva ruta de comunicaciones entre bases Alpha y Beta.",
        agente_asignado="Hermes",
        energia_requerida=30,
        prioridad="baja",
        recompensa=50,
        creado_por="Titan"
    )
    print(f"  ✅ Misión #{mision3_id} creada: Ruta de comunicaciones (pendiente)")
    
    # Completar la misión de Hermes y descontar energía
    db.completar_mision(mision3_id)
    # Actualizar energía de Hermes (150 - 30 = 120)
    db.actualizar_energia_agente("Hermes", 120)
    print(f"  ✅ Misión #{mision3_id} completada por Hermes")
    
    # Misión 4: En curso (estado cambiado manualmente)
    mision4_id = db.crear_mision(
        titulo="Auditoría del sistema",
        descripcion="Revisar logs y métricas de todos los agentes activos.",
        agente_asignado="Titan",
        energia_requerida=0,  # Admin no consume energía
        prioridad="alta",
        recompensa=150,
        creado_por="sistema"
    )
    # Cambiar estado a "en_curso" manualmente
    import sqlite3
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE misiones SET estado = ? WHERE id = ?", ("en_curso", mision4_id))
    conn.commit()
    conn.close()
    print(f"  ✅ Misión #{mision4_id} creada: Auditoría del sistema (en_curso)")
    
    # ===================================================================
    # RESUMEN
    # ===================================================================
    print("\n" + "=" * 60)
    print("  ✅ BASE DE DATOS POBLADA EXITOSAMENTE")
    print("=" * 60)
    
    agentes_registrados = db.listar_agentes()
    print(f"\nTotal agentes: {len(agentes_registrados)}")
    for agente in agentes_registrados:
        print(f"  - {agente['nombre']} ({agente['rol']}) - Energía: {agente['energia']}")
    
    print(f"\nMensajes enviados: {len(mensajes)}")
    print(f"Misiones creadas: 4 (1 completada, 1 en curso, 2 pendientes)")
    
    print("\n🚀 El sistema está listo para usarse.")
    print("   Ejecuta: uvicorn main:app --reload")
    print("   Luego: python cliente.py")


if __name__ == "__main__":
    poblar_base_datos()
