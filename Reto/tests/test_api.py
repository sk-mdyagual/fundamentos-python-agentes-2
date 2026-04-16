from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_post_mision_sin_api_key_da_401():
    payload = {
        "titulo": "Prueba sin key",
        "descripcion": "Debe fallar por auth",
        "agente_asignado": "Atlas",
        "estado": "pendiente",
        "energia_requerida": 5,
        "prioridad": "media",
        "creado_por": "test",
    }
    response = client.post("/misiones/", json=payload)
    assert response.status_code == 401


def test_briefing_retorna_local_y_externo(monkeypatch):
    class DummyResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"fact": "Mocked external insight"}

    def fake_get(*args, **kwargs):
        return DummyResp()

    monkeypatch.setattr("main.requests.get", fake_get)

    response = client.get("/briefing/Atlas")
    assert response.status_code == 200
    data = response.json()
    assert "agente" in data
    assert "insight_externo" in data
    assert "fuente_externa" in data
    assert data["insight_externo"] == "Mocked external insight"
