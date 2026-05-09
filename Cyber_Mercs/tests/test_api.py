# tests/test_api.py — Tests automatizados para Cyber-Mercs
# Usa pytest + FastAPI TestClient para verificar el comportamiento de los endpoints
# sin necesidad de levantar uvicorn manualmente.

import pytest
from fastapi.testclient import TestClient

# Importamos la app de FastAPI
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)
API_KEY = "zaun-key-2026"
HEADERS = {"X-API-KEY": API_KEY}


# =====================================================
# TEST 1: Endpoint protegido rechaza peticiones sin API Key (401)
# =====================================================
def test_registrar_merc_sin_api_key_retorna_401():
    """Verifica que POST /mercs/ sin header X-API-KEY retorna 401."""
    response = client.post("/mercs/", json={
        "alias": "TestMerc",
        "clase_nombre": "hacker",
        "hp": 100
    })
    assert response.status_code == 422 or response.status_code == 401
    # 422 si falta el header obligatorio, 401 si llega vacío


# =====================================================
# TEST 2: Endpoint protegido acepta peticiones con API Key válida (200/201)
# =====================================================
def test_registrar_merc_con_api_key_retorna_200():
    """Verifica que POST /mercs/ con API Key válida registra exitosamente."""
    # Primero reseteamos la DB para tener un entorno limpio
    client.delete("/reset", headers=HEADERS)
    
    response = client.post("/mercs/", json={
        "alias": "TestMerc",
        "clase_nombre": "hacker",
        "hp": 100,
        "creditos": 500
    }, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["alias"] == "TestMerc"


# =====================================================
# TEST 3: Validadores Pydantic rechazan datos inválidos (422)
# =====================================================
def test_validador_hp_negativo_retorna_422():
    """Verifica que enviar HP <= 0 es rechazado por el validador."""
    response = client.post("/mercs/", json={
        "alias": "MercInvalido",
        "clase_nombre": "hacker",
        "hp": -50
    }, headers=HEADERS)
    assert response.status_code == 422


def test_validador_clase_invalida_retorna_422():
    """Verifica que enviar una clase que no existe es rechazada."""
    response = client.post("/mercs/", json={
        "alias": "MercInvalido",
        "clase_nombre": "mago",
        "hp": 100
    }, headers=HEADERS)
    assert response.status_code == 422


def test_validador_tirada_fuera_de_rango():
    """Verifica que una tirada D20 fuera de rango (1-20) es rechazada."""
    # Primero necesitamos un merc y un contrato
    client.delete("/reset", headers=HEADERS)
    client.post("/mercs/", json={"alias": "DadoTest", "clase_nombre": "novato", "hp": 100}, headers=HEADERS)
    r = client.post("/contratos/", json={"titulo": "Test", "mercenario_asignado": "DadoTest"}, headers=HEADERS)
    cid = r.json()["id"]
    
    # Intentar ejecutar con tirada = 25 (inválida, D20 max es 20)
    response = client.post(f"/contratos/{cid}/ejecutar", json={"tirada_dado": 25}, headers=HEADERS)
    assert response.status_code == 422


# =====================================================
# TEST 4: Alias duplicado retorna 409
# =====================================================
def test_alias_duplicado_retorna_409():
    """Verifica que registrar dos mercenarios con el mismo alias da conflicto."""
    client.delete("/reset", headers=HEADERS)
    client.post("/mercs/", json={"alias": "Jinx", "clase_nombre": "hacker", "hp": 100}, headers=HEADERS)
    
    response = client.post("/mercs/", json={"alias": "Jinx", "clase_nombre": "tanque", "hp": 150}, headers=HEADERS)
    assert response.status_code == 409


# =====================================================
# TEST 5: Flujo completo de contrato (crear -> ejecutar -> verificar)
# =====================================================
def test_flujo_contrato_completo():
    """Verifica el ciclo de vida completo de un contrato exitoso."""
    client.delete("/reset", headers=HEADERS)
    
    # Registrar mercenario
    client.post("/mercs/", json={"alias": "FlowTest", "clase_nombre": "tanque", "hp": 200}, headers=HEADERS)
    
    # Crear contrato
    r = client.post("/contratos/", json={
        "titulo": "Misión de prueba",
        "mercenario_asignado": "FlowTest",
        "dano_estimado": 10,
        "pago_base": 1000
    }, headers=HEADERS)
    assert r.status_code == 200
    cid = r.json()["id"]
    
    # Ejecutar con tirada alta (éxito garantizado)
    r = client.post(f"/contratos/{cid}/ejecutar", json={"tirada_dado": 18}, headers=HEADERS)
    assert r.status_code == 200
    data = r.json()
    assert "pago_recibido" in data
    assert data["hp_actual"] > 0


# =====================================================
# TEST 6: Servidor responde correctamente en raíz
# =====================================================
def test_raiz_retorna_200():
    """Verifica que GET / retorna status online."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema Online" in response.json()["mensaje"]
