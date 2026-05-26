# Reto de Consolidación — La Agencia de Agentes

**Autor:** Sergio Jaramillo (SergiJaramilloL)

## Instalación y ejecución

```bash
# 1. Navegar a la carpeta
cd entregas-sergio-jaramillo/S6_reto

# 2. Crear entorno virtual e instalar dependencias
py -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 3. Crear el archivo .env (copiar la plantilla y completar la clave)
copy .env.example .env
# Editar .env y poner un valor real en AGENCIA_API_KEY

# 4. Levantar el servidor
uvicorn main:app --reload

# 5. En otra terminal, ejecutar el cliente de demostración
python cliente.py
```

La documentación interactiva Swagger UI estará disponible en `http://localhost:8000/docs`.

---

## Tabla de endpoints

| Método | Ruta                        | Protegido | Descripción                                             |
| ------ | --------------------------- | --------- | ------------------------------------------------------- |
| `GET`  | `/`                         | No        | Verifica que el servidor está activo                    |
| `GET`  | `/agentes/`                 | No        | Lista todos los agentes registrados                     |
| `GET`  | `/agente/{nombre}`          | No        | Devuelve un agente por nombre o 404                     |
| `POST` | `/agentes/`                 | **Sí**    | Crea un agente nuevo                                    |
| `POST` | `/mensajes/`                | No        | Envía un mensaje entre agentes                          |
| `GET`  | `/mensajes/{nombre}`        | No        | Lee la bandeja de entrada de un agente                  |
| `POST` | `/misiones/`                | **Sí**    | Crea una misión. Verifica que el agente asignado exista |
| `GET`  | `/misiones/{id}`            | No        | Devuelve una misión por id o 404                        |
| `GET`  | `/agente/{nombre}/misiones` | No        | Lista todas las misiones de un agente                   |
| `POST` | `/misiones/{id}/completar`  | **Sí**    | Completa la misión y descuenta energía al agente        |
| `GET`  | `/briefing/{nombre}`        | No        | Datos del agente + instrucción de una API externa       |

Los endpoints marcados como **Sí** requieren el header `X-API-KEY` con la clave configurada en `.env`.

---

## Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

Más allá del mínimo requerido, agregué dos columnas:

- **`prioridad INTEGER DEFAULT 1`** (rango 1-5): permite que `listar_misiones_agente` devuelva las misiones ordenadas por urgencia (`ORDER BY prioridad DESC`) sin lógica extra en el servidor. Es un campo operativo que cualquier agente real necesita para saber en qué orden ejecutar sus tareas.
- **`recompensa INTEGER DEFAULT 0`**: representa los tokens de energía que la Agencia promete al agente por completar la misión. Aparece en el endpoint `GET /agente/{nombre}/misiones` y da contexto para que el agente evalúe si vale la pena aceptar una misión costosa.

### 2. API pública elegida: adviceslip.com

Elegí `https://api.adviceslip.com/advice` porque es completamente gratuita, no requiere autenticación, retorna JSON simple con un consejo aleatorio (`{"slip": {"advice": "..."}}`) y no tiene límite de peticiones conocido. Encaja con la narrativa de agentes: el campo `instruccion_del_dia` del briefing es el "mensaje del cuartel general" que orienta al agente antes de enfrentar sus misiones pendientes. Es semánticamente coherente con el universo del proyecto.

### 3. Estrategia de resiliencia ante fallas de la API externa

El endpoint `GET /briefing/{nombre}` usa `requests.get(timeout=5)` dentro de un bloque `try/except Exception`. Si la API externa falla por cualquier razón (timeout, error DNS, respuesta 5xx, JSON malformado), el servidor activa un fallback: entrega igualmente el briefing con `instruccion_del_dia: "Sin instrucción disponible. Opera con criterio propio."` y `fuente_externa: "fallback"`. El cliente siempre recibe una respuesta 200 con datos locales completos. Esta decisión prioriza la disponibilidad del servidor por encima de tener la instrucción externa: un agente sin consejo externo es mejor que un servidor que no responde.

---

## Referencias consultadas

- [FastAPI — Dependencies: Header parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
- [FastAPI — Dependencies: First Steps](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [python-dotenv — Documentation](https://pypi.org/project/python-dotenv/)
- [Python logging — HOWTO](https://docs.python.org/3/howto/logging.html)
- [requests — Timeouts and Exceptions](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
- [Public APIs — GitHub list](https://github.com/public-apis/public-apis)
- [adviceslip.com API](https://api.adviceslip.com/)
