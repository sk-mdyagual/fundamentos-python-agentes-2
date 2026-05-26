# La Agencia de Agentes

API REST para gestión de agentes inteligentes con persistencia SQLite, autenticación por API key, logging estructurado e inteligencia externa.

## Instalación y ejecución

### 1. Instalar dependencias

```bash
cd Reto
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y completa tus valores:

```bash
cp .env.example .env
```

Edita `.env`:
```
AGENCIA_API_KEY=tu-clave-secreta-aqui
EXTERNAL_API_URL=https://api.adviceslip.com/advice
```

### 3. Poblar la base de datos con datos de semilla

```bash
python seed.py
```

Esto crea `agentes.db` con 3 agentes, 5 mensajes y 3 misiones en estados distintos.

### 4. Levantar el servidor

```bash
uvicorn main:app --reload
```

El servidor escucha en `http://localhost:8000`. La documentación interactiva está en `http://localhost:8000/docs`.

### 5. Ejecutar el cliente de demostración

Con el servidor corriendo en otra terminal:

```bash
python cliente.py
```

---

## Tabla de endpoints

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| `GET`  | `/` | No | Estado del servidor |
| `GET`  | `/agente/{nombre}` | No | Obtener agente por nombre |
| `GET`  | `/agentes/` | No | Listar todos los agentes |
| `POST` | `/agentes/` | **Sí** | Crear nuevo agente |
| `POST` | `/mensajes/` | **Sí** | Enviar mensaje entre agentes |
| `GET`  | `/mensajes/{nombre}` | No | Bandeja de mensajes de un agente |
| `POST` | `/misiones/` | **Sí** | Crear nueva misión |
| `GET`  | `/misiones/{id}` | No | Obtener misión por id |
| `GET`  | `/agente/{nombre}/misiones` | No | Listar misiones de un agente |
| `POST` | `/misiones/{id}/completar` | **Sí** | Completar una misión |
| `GET`  | `/briefing/{nombre}` | No | Briefing del agente con intel externo |

Los endpoints protegidos requieren el header `X-API-KEY: <tu-clave>`.

---

## Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

Más allá del mínimo requerido (`id`, `titulo`, `descripcion`, `agente_asignado`, `estado`, `energia_requerida`, `created_at`), agregué dos columnas:

- **`prioridad TEXT`** (alta / media / baja): permite triaje inmediato sin necesidad de abrir la descripción. Un sistema de despacho real necesita saber cuáles misiones atender primero, y codificar eso en una columna hace las consultas más simples y eficientes.
- **`creado_por TEXT`**: trazabilidad de auditoría. Saber qué operador u origen (sistema, otro agente, cliente.py) originó cada misión es indispensable para investigar incidentes y distribuir responsabilidades dentro de la Agencia.

### 2. API pública elegida

Elegí **Advice Slip API** (`https://api.adviceslip.com/advice`) porque:

- Es completamente pública, sin autenticación, con respuesta JSON limpia y predecible.
- El concepto de "consejo" encaja con la narrativa de agentes: cada vez que se consulta el briefing, el agente recibe un fragmento de inteligencia táctica para guiar su próxima misión. Transforma un dato genérico en algo narrativamente coherente con el mundo de La Agencia.
- Tiene alta disponibilidad y no requiere registro ni tokens.

### 3. Estrategia de resiliencia ante fallos externos

Si la API externa falla o tarda, el endpoint `GET /briefing/{nombre}` **nunca bloquea al cliente**:

- Se aplica un timeout de **3 segundos**. Suficientemente generoso para conexiones lentas, suficientemente estricto para no degradar la experiencia de usuario.
- En caso de `Timeout`, se activa un mensaje de fallback específico y se registra un `logger.warning` (situación inusual pero no rota).
- Cualquier otra excepción (red caída, respuesta malformada) activa un segundo fallback genérico y se registra con `logger.error` (fallo real).
- El campo `fuente_externa` siempre aparece en la respuesta para que el consumidor sepa qué API se intentó consultar.

Esta estrategia garantiza que un servidor de terceros nunca puede tumbar tu API.

---

## Arquitectura de módulos

```
Reto/
├── agente.py       # Clases de dominio puras (PseudoAgente, AgenteAdmin)
├── db.py           # Capa de persistencia SQLite (sin FastAPI)
├── config.py       # Carga de variables de entorno con python-dotenv
├── main.py         # Aplicación FastAPI + endpoints + logging
├── cliente.py      # Script de demostración end-to-end
├── seed.py         # Poblar base de datos con datos de semilla
├── requirements.txt
├── .env.example    # Plantilla de variables de entorno (sí se versiona)
├── .env            # Valores reales (NO se versiona — ver .gitignore)
└── .gitignore
```

---

## Referencias consultadas

- [FastAPI — Dependencias y Header](https://fastapi.tiangolo.com/tutorial/header-params/)
- [FastAPI — Security: API Key](https://fastapi.tiangolo.com/tutorial/security/http-basic-auth/)
- [FastAPI — Depends](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [python-dotenv — Documentación](https://saurabh-kumar.com/python-dotenv/)
- [Python logging — HOWTO](https://docs.python.org/3/howto/logging.html)
- [requests — Timeouts y excepciones](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
- [Advice Slip API](https://api.adviceslip.com/)
- [SQLite — Python sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
