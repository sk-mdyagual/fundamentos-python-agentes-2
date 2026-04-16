# 🏛️ Agencia del Olimpo — Reto de Consolidación
**Doris Mosquera Lozano** — doris.mosquera@sofka.com.co — DMosqueraLSofka

## 📋 Descripción
Sistema de gestión de agentes del Olimpo que integra:
**POO con herencia** (S4): PseudoAgente y AgenteAdmin con polimorfismo
**Persistencia SQLite** (S5): datos que sobreviven al cierre del programa
**API HTTP con FastAPI** (S5): 12 endpoints accesibles desde cualquier cliente
**Autenticación**, **logging**, **variables de entorno** y **API externa** (Reto)

### La Agencia
**5 agentes** del Olimpo (Zeus, Atenea, Hermes, Apolo, Artemisa) ejecutan **7 misiones épicas**.
Destaca la misión "Negociar tregua con Cronos", donde Apolo es enviado como diplomático
pero el bando de los Titanes lo convence de unirse a sus filas — la misión queda como **FALLIDA**.

## 🚀 Instalación y ejecución

### 1. Crear entorno virtual
bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

### 2. Instalar dependencias
bash
pip install -r requirements.txt

### 3. Configurar variables de entorno
Copia .env.example a .env y llena los valores:
bash
copy .env.example .env
Edita .env con tus propios valores:
AGENCIA_API_KEY=tu-clave-secreta-aqui
EXTERNAL_API_URL=https://uselessfacts.jsph.pl/api/v2/facts/random
 **IMPORTANTE:** La API key es secreta. No la compartas ni la subas a Git.

### 4. Levantar el servidor
bash
uvicorn main:app --reload
Swagger UI disponible en: http://localhost:8000/docs

### 5. Ejecutar el cliente de demostración
En otra terminal (con el servidor corriendo):
bash
python cliente.py

## 📡 Tabla de endpoints

| Método | Ruta | Protegido | Descripción |
|---|---|---|---|
| GET | / | ❌ | Status del servidor |
| GET | /agentes/ | ❌ | Lista todos los agentes |
| GET | /agente/{nombre} | ❌ | Consulta un agente por nombre |
| POST | /agentes/ | ✅ API key | Crea un agente nuevo |
| POST | /mensajes/ | ✅ API key | Envía un mensaje entre agentes |
| GET | /mensajes/{nombre} | ❌ | Lee la bandeja de un agente |
| POST | /misiones/ | ✅ API key | Crea una misión asignada a un agente |
| GET | /misiones/{id} | ❌ | Consulta una misión por ID |
| GET | /agente/{nombre}/misiones | ❌ | Lista las misiones de un agente |
| POST | /misiones/{id}/completar | ✅ API key | Completa misión (descuenta energía + recompensa) |
| POST | /misiones/{id}/fallar | ✅ API key | Marca una misión como fallida |
| GET | /briefing/{nombre} | ❌ | Briefing + código de confusión para los Titanes |

**Autenticación:** Enviar header X-API-KEY con el valor configurado en .env.

## 🧭 Decisiones de Ingeniería

### 1. Esquema de la tabla misiones

Además de las columnas mínimas requeridas (id, titulo, descripcion, agente_asignado, estado, energia_requerida, created_at), agregué **4 columnas extras**:

| Columna | Tipo | Por qué |
|---|---|---|
| prioridad | TEXT (alta/media/baja) | No todas las misiones del Olimpo tienen la misma urgencia. Defender contra Titanes es más urgente que entregar un pergamino. Permite al admin priorizar recursos. |
| recompensa | INTEGER | Si un agente solo gasta energía, eventualmente se agota. La recompensa cierra el ciclo: el agente invierte energía pero recupera parte al completar. Es un incentivo narrativo y mecánico. |
| reintentos | INTEGER | Los dioses también fallan. Registrar cuántas veces se reintentó una misión permite medir la dificultad real de cada tarea. |
| completed_at | TEXT | Junto con created_at, permite calcular el tiempo de ejecución (completed_at - created_at). No guardé "tiempo de ejecución" como columna porque es un dato derivado que se calcula al consultar. |

### 2. API pública elegida

Elegí **Useless Facts API** (`https://uselessfacts.jsph.pl/api/v2/facts/random`) por tres razones:
**Sin autenticación:** no requiere API key, registro ni cuenta. Solo GET y devuelve JSON.
**Respuesta simple:** retorna {"text": "Un dato curioso..."}, fácil de parsear.
**Encaje narrativo:** cada agente recibe un **"código de confusión"** en su briefing — un dato tan aleatorio y absurdo que la Agencia lo transmite en abierto. Los Titanes lo interceptan pero **no logran descifrarlo** porque no tiene sentido. Es guerra psicológica pura.

### 3. Estrategia de resiliencia

Mi estrategia es **fallback con mensaje** — si la API externa falla, el endpoint /briefing **NUNCA falla**:
**Timeout:** requests.get(url, timeout=5) — máximo 5 segundos de espera.
**Sin conexión:** except ConnectionError → retorna "Fuente externa no disponible (sin conexión)".
**Error HTTP:** Si status_code != 200 → retorna "No disponible".
**Justificación:** Un agente del Olimpo debe recibir su briefing siempre, incluso si la inteligencia externa está comprometida. El campo inteligencia_del_dia mostrará el fallback y fuente_externa indicará de dónde se intentó obtener.

## 📁 Estructura del proyecto

```bash
Reto/
├── agente.py        # Clases PseudoAgente y AgenteAdmin (dominio)
├── db.py            # Funciones SQLite (persistencia)
├── config.py        # Variables de entorno (configuración)
├── main.py          # Servidor FastAPI — 12 endpoints, logging, auth
├── cliente.py       # Demo end-to-end
├── .env             # Secretos (NO versionado)
├── .env.example     # Plantilla de secretos
├── .gitignore       # Excluye .env, agentes.db, __pycache__
├── requirements.txt # fastapi, uvicorn, requests, python-dotenv
└── README.md        # Este archivo
```

## 📊 Datos semilla (generados por cliente.py)

| Entidad | Cantidad | Detalle |
|---|---|---|
| Agentes | **5** | Zeus (admin), Atenea (estratega), Hermes (mensajero), Apolo (diplomático), Artemisa (cazadora) |
| Misiones | **7** | 4 completadas, 2 pendientes, 1 fallida |
| Mensajes | **8** | Comunicación entre los agentes del Olimpo |

## 📚 Referencias consultadas

[FastAPI - Security / API Key](https://fastapi.tiangolo.com/reference/security/?h=api+key) — para implementar APIKeyHeader y Depends.
[python-dotenv (PyPI)](https://pypi.org/project/python-dotenv/) — documentación oficial de load_dotenv() y os.getenv().
[Python logging — Basic Logging Tutorial](https://docs.python.org/3/howto/logging.html) — para basicConfig, niveles y formateo.
[Useless Facts API](https://uselessfacts.jsph.pl/) — API pública elegida para el briefing.
[Requests: HTTP for Humans](https://docs.python-requests.org/) — para requests.get(), timeout y manejo de excepciones.