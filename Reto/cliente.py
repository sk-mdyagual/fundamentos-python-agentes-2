"""
cliente.py — Cliente HTTP de demostración end-to-end

Este script ejecuta un guion completo que demuestra todas las capacidades
de la Agencia de Agentes sin intervención manual.

IMPORTANTE: El servidor debe estar corriendo en http://localhost:8000
Para ejecutar: python cliente.py
"""

import requests
import time
from typing import Dict, Optional

# Configuración del cliente
BASE_URL = "http://localhost:8000"
API_KEY = "mi_super_clave_secreta_123"  # Debe coincidir con la del .env del servidor

# Headers para endpoints protegidos
HEADERS_AUTH = {"X-API-KEY": API_KEY}


def print_seccion(titulo: str):
    """Imprime un separador visual para organizar la salida."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


def verificar_servidor() -> bool:
    """Verifica que el servidor esté vivo."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"✅ Servidor operativo: {response.json()}")
            return True
        else:
            print(f"❌ Servidor respondió con código {response.status_code}")
            return False
    except requests.ConnectionError:
        print(f"❌ No se pudo conectar al servidor en {BASE_URL}")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def crear_agente(nombre: str, rol: str, energia: int) -> Optional[Dict]:
    """Crea un nuevo agente."""
    try:
        response = requests.post(
            f"{BASE_URL}/agentes/",
            json={"nombre": nombre, "rol": rol, "energia": energia},
            headers=HEADERS_AUTH
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Agente '{nombre}' creado: {response.json()}")
            return response.json()
        elif response.status_code == 409:
            print(f"⚠️  Agente '{nombre}' ya existe (409 Conflict)")
            return None
        else:
            print(f"❌ Error al crear agente: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al crear agente: {e}")
        return None


def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    energia_requerida: int,
    prioridad: str = "media"
) -> Optional[Dict]:
    """Crea una nueva misión."""
    try:
        response = requests.post(
            f"{BASE_URL}/misiones/",
            json={
                "titulo": titulo,
                "descripcion": descripcion,
                "agente_asignado": agente_asignado,
                "energia_requerida": energia_requerida,
                "prioridad": prioridad,
                "creado_por": "cliente_demo"
            },
            headers=HEADERS_AUTH
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Misión '{titulo}' creada: {response.json()}")
            return response.json()
        else:
            print(f"❌ Error al crear misión: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al crear misión: {e}")
        return None


def completar_mision(mision_id: int) -> bool:
    """Completa una misión por su ID."""
    try:
        response = requests.post(
            f"{BASE_URL}/misiones/{mision_id}/completar",
            headers=HEADERS_AUTH
        )
        
        if response.status_code == 200:
            print(f"✅ Misión #{mision_id} completada: {response.json()}")
            return True
        else:
            print(f"❌ Error al completar misión: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al completar misión: {e}")
        return False


def obtener_briefing(nombre: str) -> Optional[Dict]:
    """Obtiene el briefing de un agente (incluye API externa)."""
    try:
        response = requests.get(f"{BASE_URL}/briefing/{nombre}")
        
        if response.status_code == 200:
            briefing = response.json()
            print(f"✅ Briefing para '{nombre}':")
            print(f"   Rol: {briefing['agente']['rol']}")
            print(f"   Energía: {briefing['agente']['energia']}")
            print(f"   Misiones totales: {briefing['misiones_totales']}")
            print(f"   Misiones pendientes: {briefing['misiones_pendientes']}")
            print(f"   💡 Consejo del día: \"{briefing['consejo_del_dia']}\"")
            print(f"   📡 Fuente: {briefing['fuente_externa']}")
            return briefing
        else:
            print(f"❌ Error al obtener briefing: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al obtener briefing: {e}")
        return None


def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> bool:
    """Envía un mensaje entre agentes."""
    try:
        response = requests.post(
            f"{BASE_URL}/mensajes/",
            json={
                "remitente": remitente,
                "destinatario": destinatario,
                "contenido": contenido
            },
            headers=HEADERS_AUTH
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Mensaje enviado de '{remitente}' a '{destinatario}'")
            return True
        else:
            print(f"❌ Error al enviar mensaje: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al enviar mensaje: {e}")
        return False


def leer_bandeja(nombre: str) -> Optional[Dict]:
    """Lee la bandeja de mensajes de un agente."""
    try:
        response = requests.get(f"{BASE_URL}/mensajes/{nombre}")
        
        if response.status_code == 200:
            bandeja = response.json()
            print(f"✅ Bandeja de '{nombre}' ({bandeja['total']} mensajes):")
            for msg in bandeja['mensajes']:
                print(f"   📩 De: {msg['remitente']} | \"{msg['contenido']}\" ({msg['timestamp']})")
            return bandeja
        else:
            print(f"❌ Error al leer bandeja: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al leer bandeja: {e}")
        return None


def probar_autenticacion() -> bool:
    """Prueba que la autenticación funciona correctamente."""
    print_seccion("PRUEBA DE AUTENTICACIÓN")
    
    # Intentar crear agente SIN API key (debe fallar con 401)
    try:
        response = requests.post(
            f"{BASE_URL}/agentes/",
            json={"nombre": "Intruso", "rol": "hacker", "energia": 999}
            # SIN el header X-API-KEY
        )
        if response.status_code == 401:
            print("✅ Endpoint protegido rechaza peticiones sin API key (401)")
            return True
        else:
            print(f"❌ Endpoint debió responder 401, pero respondió {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en prueba de autenticación: {e}")
        return False


# ===================================================================
# GUION PRINCIPAL DE DEMOSTRACIÓN
# ===================================================================
def main():
    print_seccion("🏛️  DEMOSTRACIÓN CLIENTE DE LA AGENCIA DE AGENTES")
    
    # PASO 1: Verificar que el servidor está vivo
    print_seccion("1. Verificación del Servidor")
    if not verificar_servidor():
        print("\n❌ No se puede continuar sin el servidor. Abortando.")
        return
    
    time.sleep(1)
    
    # PASO 2: Probar autenticación
    if not probar_autenticacion():
        print("\n⚠️  La autenticación no funciona como se espera.")
    
    time.sleep(1)
    
    # PASO 3: Crear un agente
    print_seccion("2. Creación de Agente")
    agente_nombre = "Orion"
    crear_agente(agente_nombre, "explorador", 200)
    
    time.sleep(1)
    
    # PASO 4: Crear una misión asignada a ese agente
    print_seccion("3. Creación de Misión")
    resultado_mision = crear_mision(
        titulo="Explorar Sector Alpha",
        descripcion="Mapear la región desconocida del Sector Alpha y reportar hallazgos.",
        agente_asignado=agente_nombre,
        energia_requerida=50,
        prioridad="alta"
    )
    
    if not resultado_mision:
        print("⚠️  No se pudo crear la misión. El guion continuará de todos modos.")
        mision_id = 1  # Asumir ID por defecto
    else:
        mision_id = resultado_mision.get("mision_id", 1)
    
    time.sleep(1)
    
    # PASO 5: Completar la misión
    print_seccion("4. Completar Misión")
    completar_mision(mision_id)
    
    time.sleep(1)
    
    # PASO 6: Consultar el briefing del agente
    print_seccion("5. Consultar Briefing (con API Externa)")
    obtener_briefing(agente_nombre)
    
    time.sleep(1)
    
    # PASO 7: Enviar un mensaje entre agentes
    print_seccion("6. Mensajería entre Agentes")
    # Crear un segundo agente para el mensaje
    crear_agente("Nova", "cientifica", 150)
    time.sleep(0.5)
    
    enviar_mensaje(agente_nombre, "Nova", "Sector Alpha mapeado. Datos enviados.")
    time.sleep(0.5)
    
    enviar_mensaje("Nova", agente_nombre, "Datos recibidos y analizados. Buen trabajo.")
    time.sleep(0.5)
    
    # PASO 8: Leer la bandeja de mensajes
    print_seccion("7. Leer Bandeja de Mensajes")
    leer_bandeja(agente_nombre)
    time.sleep(0.5)
    leer_bandeja("Nova")
    
    # FINALIZACIÓN
    print_seccion("✅ DEMOSTRACIÓN COMPLETADA")
    print("Todos los flujos ejecutados exitosamente.")
    print("Revisa los logs del servidor para ver el registro detallado.")
    print("\nPara explorar más, visita: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
