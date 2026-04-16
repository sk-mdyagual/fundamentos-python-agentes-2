# Reto de Consolidación — La Agencia de Agentes

Integración de S4 (POO/Herencia) + S5 (SQLite + FastAPI) con 4 saltos de investigación:
autenticación por API Key, API externa, variables de entorno y logging estructurado.

---

## Instalación y ejecución

### 1. Instalar dependencias

```bash
pip install -r Reto/requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Desde la carpeta Reto/
cp .env.example .env
# Edita .env y define tu AGENCIA_API_KEY
```

### 3. Levantar el servidor

```bash
cd Reto
uvicorn main:app --reload
```

### 4. Explorar la API

Abre `http://localhost:8000/docs` en el navegador.

### 5. Ejecutar la demo completa

```bash
python Reto/cliente.py
```

---

## Tabla de endpoints

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| GET | `/` | No | Estado del servidor |
| GET | `/agentes/` | No | Listar todos los agentes |
| GET | `/agente/{nombre}` | No | Obtener agente por nombre |
| POST | `/agentes/` | No | Registrar nuevo agente |
| POST | `/mensajes/` | No | Enviar mensaje entre agentes |
| GET | `/mensajes/{nombre}` | No | Leer bandeja de un agente |
| POST | `/misiones/` | **Sí (X-API-KEY)** | Crear misión asignada a un agente |
| GET | `/misiones/{id}` | No | Obtener misión por id |
| GET | `/agente/{nombre}/misiones` | No | Listar misiones de un agente |
| POST | `/misiones/{id}/completar` | **Sí (X-API-KEY)** | Completar misión y descontar energía |
| GET | `/briefing/{nombre}` | No | Datos del agente + consejo de API externa |

Los endpoints protegidos requieren el header: `X-API-KEY: <tu_clave>`

---

## Decisiones de Ingeniería

### 1. Columna `prioridad` en la tabla `misiones`

Se agregó la columna `prioridad` con los valores posibles `'baja'`, `'media'` y `'alta'`
(valor por defecto: `'media'`). La decisión se tomó porque en un sistema real de gestión
de misiones es necesario poder distinguir urgencia sin depender solo del campo `energia_requerida`,
que mide costo operativo pero no criticidad temporal. Tener prioridad como campo explícito
facilita filtros futuros (ej. listar solo misiones de alta prioridad), alertas automáticas
y extensiones como deadlines o escalados sin necesidad de migrar el esquema.

### 2. API pública elegida: `api.adviceslip.com/advice`

Se eligió la API pública `https://api.adviceslip.com/advice`, que devuelve un consejo aleatorio
en inglés en formato JSON (`{"slip": {"id": N, "advice": "..."}}`) sin necesidad de autenticación
ni registro. Encaja con la narrativa de la Agencia porque cada agente puede recibir un "consejo
del día" al consultar su briefing, añadiendo un elemento de contexto narrativo. La API es simple,
estable, gratuita y no requiere configuración adicional, lo que la hace ideal para un entorno
educativo donde el foco debe estar en la integración y no en la gestión de credenciales externas.

### 3. Estrategia de resiliencia ante fallos de la API externa

Si la API externa no responde (timeout, error de red, respuesta inesperada), el endpoint
`GET /briefing/{nombre}` devuelve igualmente los datos completos del agente y sus misiones
activas, con el campo `dato_externo` conteniendo `{"mensaje": "sin datos externos disponibles"}`.
Se eligió esta estrategia de **degradación elegante** en lugar de propagar el error (500)
porque el dato primario del briefing es la información local del agente, y la API externa es
enriquecimiento opcional. Bloquear el servidor por un servicio de terceros introduciría
dependencia innecesaria. El timeout está configurado en 3 segundos para no penalizar la
experiencia del usuario. Todos los fallos se registran con `logger.warning()` para trazabilidad.