# Reto Final: La Agencia de Agentes

## Cómo ejecutar

1. Entrar a la carpeta:

```bash
cd Reto
```

2. Crear y activar entorno virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear archivo `.env` local a partir de `.env.example` y completar valores.
5. Levantar servidor:

```bash
uvicorn main:app --reload
```

6. Probar cliente de demostracion:

```bash
python cliente.py
```

## Endpoints implementados

| Metodo | Ruta                        | Protegido | Descripcion                                   |
| ------ | --------------------------- | --------- | --------------------------------------------- |
| GET    | `/`                         | No        | Estado del servidor                           |
| GET    | `/agente/{nombre}`          | No        | Despierta y reconstruye instancia por rol     |
| GET    | `/agentes/`                 | No        | Lista agentes                                 |
| POST   | `/agentes/`                 | Si        | Crea agente                                   |
| POST   | `/mensajes/`                | Si        | Envia mensaje                                 |
| GET    | `/mensajes/{nombre}`        | No        | Lee bandeja de entrada                        |
| POST   | `/misiones/`                | Si        | Crea mision                                   |
| GET    | `/misiones/{id}`            | No        | Obtiene mision por id                         |
| GET    | `/agente/{nombre}/misiones` | No        | Lista misiones de agente                      |
| POST   | `/misiones/{id}/completar`  | Si        | Completa mision, descuenta energia y persiste |
| GET    | `/briefing/{nombre}`        | No        | Combina datos locales + API publica           |

# Evidencias Swagger:
### OBTENER AGENTES
![Consumo swagger](https://github.com/user-attachments/assets/2714cb92-e7c2-40de-9c97-5e41c485cc68)
### OBTENER MISONES POR AGENTE
![Consumo swagger](https://github.com/user-attachments/assets/9e337a10-bb99-4b27-866c-a0b6809acc3d)
### COMPLETAR MISION CON API KEY DE AUTORIZACIÓN
![Consumo swagger](https://github.com/user-attachments/assets/55fa0af8-926e-4094-a24f-dfa1c5f3b05e)
### CONECTANDO AGENTE CON API EXTERNA - BRIEFING 
![Consumo swagger](https://github.com/user-attachments/assets/26d4bcd6-096f-45a8-90a7-7a212ea6a877)


## Decisiones de ingenieria

### 1) Esquema de tabla `misiones`

Agregue columnas extras: `prioridad`, `deadline` y `creado_por`.
Así puedo ordenar mejor las misiones y saber quien las pide.

### 2) API publica elegida

Se uso `https://catfact.ninja/fact` porque es simple y no pide login. El dato externo queda dentro del briefing.
La idea fue integrar una API externa sin complicar la lógica principal.

### 3) Estrategia de resiliencia

El endpoint `/briefing/{nombre}` usa timeout y `try/except` sobre requests.
Si la API externa falla, el sistema sigue respondiendo con un respaldo local `contingencia_activada=true`.
Preferí que siga funcionando aunque el servicio externo se caiga.

## Tests implementados (+extra)

Se implementaron dos tests con `pytest` y `TestClient`:

- `POST /misiones/` sin API key retorna `401`.
- `GET /briefing/{nombre}` retorna estructura local + dato externo mockeado.

Ejecucion de tests:

```bash
pytest -q
```

## Datos semilla

Al iniciar el servidor se insertan datos semilla automaticamente si la DB esta vacia:

- 3 agentes (`Atlas`, `Nova`, `admin`)
- 5 mensajes
- 3 misiones con estados distintos

## Evidencia visual solicitada

Tomar capturas en Swagger UI de:

1. Endpoint protegido con `401` sin API key.
2. Mismo endpoint con `200/201` con API key valida.
3. `GET /briefing/{nombre}` devolviendo datos combinados.

## Referencias consultadas

- FastAPI dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- FastAPI Header params: https://fastapi.tiangolo.com/tutorial/header-params/
- Python logging: https://docs.python.org/3/library/logging.html
- python-dotenv: https://pypi.org/project/python-dotenv/
- Requests timeouts/exceptions: https://requests.readthedocs.io/en/latest/user/quickstart/
- SQLite with Python: https://docs.python.org/3/library/sqlite3.html
- Pytest + TestClient: https://fastapi.tiangolo.com/tutorial/testing/
