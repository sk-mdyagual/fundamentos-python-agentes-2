# 🏛️ La Agencia de Agentes

Sistema de gestión de agentes inteligentes con persistencia SQLite, API REST, autenticación, y conexión con el mundo exterior.

## 📋 Descripción

Este proyecto integra los conceptos de las Semanas 4 y 5 (POO, SQLite, FastAPI) y añade cuatro nuevas capacidades de nivel profesional:
- 🔐 Autenticación con API key
- 🌐 Consumo de APIs públicas externas
- 🗝️ Configuración con variables de entorno
- 📝 Observabilidad con logging estructurado

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env con tu editor favorito y configura:
# - AGENCIA_API_KEY: tu clave secreta para autenticación
# - EXTERNAL_API_URL: URL de la API externa (por defecto Advice Slip API)
```

### 3. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

### 4. Ejecutar el cliente de demostración

En otra terminal:

```bash
python cliente.py
```

Este script ejecuta un flujo completo end-to-end sin intervención manual.

## 📚 Documentación de Endpoints

La documentación interactiva está disponible en: `http://localhost:8000/docs`

### Endpoints disponibles

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| `GET` | `/` | No | Verificación del servidor |
| `GET` | `/agentes/` | No | Lista todos los agentes |
| `GET` | `/agente/{nombre}` | No | Obtiene información de un agente |
| `POST` | `/agentes/` | ✅ Sí | Crea un nuevo agente |
| `POST` | `/mensajes/` | ✅ Sí | Envía un mensaje entre agentes |
| `GET` | `/mensajes/{nombre}` | No | Lee la bandeja de mensajes |
| `POST` | `/misiones/` | ✅ Sí | Crea una nueva misión |
| `GET` | `/misiones/{id}` | No | Obtiene una misión por ID |
| `GET` | `/agente/{nombre}/misiones` | No | Lista misiones de un agente |
| `POST` | `/misiones/{id}/completar` | ✅ Sí | Completa una misión |
| `GET` | `/briefing/{nombre}` | No | Briefing con inteligencia externa |

**Nota:** Los endpoints marcados con ✅ requieren el header `X-API-KEY` con la clave configurada en `.env`

## 🧭 Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

**Columnas agregadas más allá del mínimo:**
- `prioridad` (TEXT): Permite clasificar misiones como "baja", "media" o "alta". Útil para sistemas futuros de priorización automática donde los agentes puedan elegir qué misiones atender primero.
- `recompensa` (INTEGER): Representa el beneficio que obtiene un agente al completar la misión. Puede usarse para sistemas de incentivos o economía interna de la agencia.
- `creado_por` (TEXT): Auditoría de quién creó la misión. Importante en sistemas multiusuario para rastrear responsabilidades y flujos de trabajo.
- `completed_at` (TEXT): Timestamp de cuándo se completó la misión. Permite analizar tiempos de ejecución y productividad de agentes.

**Justificación:** Estas columnas convierten la tabla de misiones en un sistema robusto de gestión de tareas con auditoría completa, métricas de desempeño y capacidad de priorización. No es solo un registro pasivo, sino una herramienta de administración activa.

### 2. API pública elegida: Advice Slip API

**URL:** `https://api.adviceslip.com/advice`

**Por qué esta API:**
- **Sin autenticación:** No requiere registro ni API keys, ideal para una demostración funcional inmediata.
- **Formato JSON simple:** Respuesta fácil de parsear (`{"slip": {"advice": "..."}}`)
- **Narrativa coherente:** Los agentes de la Agencia necesitan "sabiduría externa" antes de iniciar misiones. Cada vez que consultan su briefing, reciben un consejo motivacional del mundo exterior.

**Qué añade al briefing:**
El endpoint `/briefing/{nombre}` combina los datos locales del agente (nombre, rol, energía, misiones pendientes) con un consejo externo que actúa como "inteligencia contextual". Esto simula cómo un sistema real podría enriquecerse con datos externos: clima, noticias, indicadores económicos, etc.

**Alternativas consideradas:**
- OpenWeatherMap (requiere API key)
- JSONPlaceholder (datos ficticios, menos narrativa)
- Public APIs de citas (menos diversidad de contenido)

### 3. Estrategia de resiliencia ante fallos de API externa

**Decisión implementada:** Fallback gracioso con timeout de 3 segundos.

**Comportamiento:**
- Si la API externa responde correctamente: se incluye el consejo en el briefing.
- Si la API externa tarda más de 3 segundos (timeout): se activa un mensaje de fallback predefinido y se registra una WARNING en los logs.
- Si la API externa devuelve un error HTTP: se usa un fallback y se registra WARNING.
- Si ocurre cualquier excepción inesperada: se captura, se registra ERROR, y se continúa con fallback.

**Justificación:**
Un servicio de la Agencia NO puede depender de la disponibilidad de servicios externos. El servidor debe ser autónomo y resiliente. El timeout de 3 segundos es un balance entre dar tiempo razonable a la API externa y no hacer esperar demasiado al cliente. Los mensajes de fallback son contextualmente apropiados ("When external sources fail, rely on your inner strength") y mantienen la experiencia del usuario fluida.

**Qué NO se hace:**
- ❌ Dejar que el servidor se cuelgue esperando una respuesta que nunca llega
- ❌ Lanzar un error 500 al usuario cuando la API externa falla
- ❌ Bloquear otros endpoints dependiendo de un servicio externo

## 🔐 Autenticación

**Endpoints protegidos:** Todos los de escritura (`POST`, `PUT`, `DELETE`)

**Endpoints libres:** Todos los de lectura (`GET`)

**Justificación:** En una arquitectura de API pública, los datos de solo lectura pueden ser consultados libremente para facilitar la integración. Sin embargo, las operaciones que modifican el estado del sistema requieren autenticación para prevenir:
- Creación de agentes fantasma
- Manipulación de misiones ajenas
- Spam de mensajes
- Consumo de recursos por actores no autorizados

## 📝 Logging

**Niveles usados:**
- **INFO:** Eventos normales del ciclo de vida (agente creado, misión completada, servidor iniciado)
- **WARNING:** Situaciones anómalas pero no críticas (API externa lenta, timeout activado, intento de acceso con API key inválida)
- **ERROR:** Fallos que impiden completar una operación (constraints SQL violados, agente inexistente, excepciones no esperadas)

**Formato:** `[timestamp] [nivel] mensaje`

**Por qué estos niveles:**
- INFO permite auditar todas las operaciones exitosas sin ruido excesivo
- WARNING alerta sobre situaciones que deben monitorearse pero no rompen el sistema
- ERROR marca fallos reales que requieren investigación

**No se usa DEBUG en producción** porque generaría volúmenes masivos de logs. Se puede activar temporalmente cambiando `logging.INFO` a `logging.DEBUG` en `main.py`.

## 🗄️ Estructura del Proyecto

```
Reto/
├── agente.py           # Clases de dominio (PseudoAgente, AgenteAdmin)
├── db.py               # Capa de persistencia con SQLite
├── main.py             # Aplicación FastAPI y endpoints
├── cliente.py          # Cliente de demostración end-to-end
├── config.py           # Gestión de variables de entorno
├── requirements.txt    # Dependencias del proyecto
├── .env                # Variables de entorno (NO versionado)
├── .env.example        # Plantilla de variables (SÍ versionado)
├── .gitignore          # Archivos excluidos de Git
├── README.md           # Este archivo
└── agentes.db          # Base de datos SQLite (generada automáticamente)
```

## 📦 Principios de Arquitectura

### Separación de responsabilidades

- **agente.py:** Lógica de negocio pura. No conoce SQL ni HTTP.
- **db.py:** Operaciones de base de datos. No conoce FastAPI ni clases de dominio directamente (recibe/retorna dicts).
- **main.py:** Orquestación HTTP. Importa de agente.py y db.py, nunca define clases de dominio ni SQL crudo.
- **config.py:** Punto único de verdad para configuración. Todos los módulos importan desde aquí.

### Herencia polimórfica (R2)

Al despertar un agente desde la DB, el sistema reconstruye la clase correcta:
- Si `rol == "admin"` → instancia `AgenteAdmin`
- Si `rol != "admin"` → instancia `PseudoAgente`

Esto se verifica con `isinstance()` y garantiza que el comportamiento del agente (p. ej., consumo de energía) sea el correcto según su rol.

### Inmutabilidad de secretos

Ningún secreto está hardcodeado en el código fuente. Todo se carga desde variables de entorno. El archivo `.env` está excluido de Git.

## 📚 Referencias Consultadas

### Documentación oficial
- [FastAPI Documentation - Security](https://fastapi.tiangolo.com/tutorial/security/)
- [FastAPI - Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Pydantic - Field Validation](https://docs.pydantic.dev/latest/usage/validators/)
- [Python Logging - HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python-dotenv - Usage](https://pypi.org/project/python-dotenv/)
- [Requests - Timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)

### APIs y recursos externos
- [Advice Slip API Documentation](https://api.adviceslip.com/)
- [Public APIs List (GitHub)](https://github.com/public-apis/public-apis)

### Patrones y buenas prácticas
- [12 Factor App - Config](https://12factor.net/config)
- [REST API Best Practices - Authentication](https://restfulapi.net/security-essentials/)
- [SQLite - SQL Injection Prevention](https://www.sqlite.org/lang_expr.html#varparam)

## ✅ Auto-auditoría (Checklist)

- [x] El servidor levanta sin errores con `uvicorn main:app --reload`
- [x] Todos los endpoints aparecen en `http://localhost:8000/docs`
- [x] Los endpoints protegidos rechazan peticiones sin `X-API-KEY` válido (código 401)
- [x] `GET /briefing/{nombre}` retorna datos locales + información de API externa
- [x] `cliente.py` ejecuta el flujo completo sin intervención manual
- [x] Los datos persisten entre reinicios del servidor
- [x] En `main.py` no hay llamadas a `print`, todo registro pasa por `logger.*`
- [x] El archivo `.env` no está versionado, pero sí existe `.env.example`
- [x] Al despertar un agente con rol "admin", `isinstance(agente, AgenteAdmin)` devuelve `True`
- [x] El README justifica las tres Decisiones de Ingeniería
- [x] El README lista las referencias consultadas

## 🎯 Próximos Pasos (Ideas para Extensión)

- [ ] Implementar CRUD completo para agentes (PUT, DELETE)
- [ ] Agregar validadores custom de Pydantic para campos de misiones
- [ ] Tests automatizados con pytest y TestClient
- [ ] Autenticación basada en usuarios (JWT)
- [ ] Dashboard web con visualización de métricas
- [ ] Sistema de notificaciones en tiempo real (WebSockets)
- [ ] Exportación de logs a archivos rotando por fecha
- [ ] Caché de respuestas de API externa (Redis)

## 📄 Licencia

Proyecto educativo - Reto de Consolidación Semana 5

---

**Autor:** [Tu nombre]  
**Fecha:** Abril 2026  
**Curso:** Fundamentos de Python para Agentes
