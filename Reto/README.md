# PROYECTO DE CONSOLIDACION LA AGENCIA DE AGENTES


## 1. Preparacion del entorno y efecucion del proyecto

A continuación se presenta el paso a paso para ejecutar el proyecto, iniciando con la creación de un **entorno virtual**, para aislar las dependencias requeridas de tu sistema. 

### 1.1. Abre una terminal y navega a la carpeta Reto

```bash
cd Reto
```

### 1.2. Crea el entorno virtual

```bash
python3 -m venv .venv
```

### 1.3. Activa el entorno virtual

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (cmd):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

Sabras que esta activo porque veras `(.venv)` al inicio de tu linea de terminal.

### 1.4. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 1.5. Verifica la instalacion

```bash
python -c "import fastapi; print('FastAPI', fastapi.__version__, '- OK')"
python -c "import requests; print('Requests - OK')"
```

### 1.6. Levanta el servidor FastAPI
**Archivo:** `main.py`

```bash
uvicorn main:app --reload
```

Deja esta terminal abierta durante la ejecución del proyecto. Visita: [http://localhost:8000/docs](http://localhost:8000/docs) en el navegaor para acceder a la documentación interactiva del proyecto desde Swagger UI.

### 1.7. Ejecutar el cliente
**Archivo:** `cliente.py`

Desde otra terminal ejecutar el script

```bash
python cliente.py
```
### 1.8 Limpieza

Cuando termines o quieras empezar de cero:

```bash
# Borrar la base de datos (se regenera al ejecutar de nuevo)
rm agentes.db

# Desactivar el entorno virtual
deactivate
```

## 2. Endpoints de la aplicación

| Método | Ruta | Protegido | Qué hace |
|---|---|---|---|
| `GET` | `/` | No | Devuelve el estado del sistema y mensaje de bienvenida. |
| `GET` | `/agente/{nombre}` | No | Obtiene la información de un agente específico. Si el agente no existe, responde `404`. |
| `GET` | `/agentes/` | No | Lista todos los agentes registrados en el sistema. |
| `POST` | `/agentes/` | Sí | Registra un nuevo agente con nombre, rol y energía. |
| `POST` | `/mensajes/` | Sí | Crea un mensaje entre dos agentes. Requiere remitente, destinatario y contenido. |
| `GET` | `/mensajes/{nombre}` | No | Obtiene todos los mensajes recibidos por un agente específico. |
| `POST` | `/misiones/` | Sí | Crea una misión. Si el `agente_asignado` no existe en la tabla `agentes`, responde `404`. |
| `GET` | `/misiones/{id}` | No | Devuelve la misión o `404`. |
| `GET` | `/agente/{nombre}/misiones` | No | Lista las misiones asignadas a un agente. |
| `POST` | `/misiones/{id}/completar` | Sí | Marca la misión como `"completada"`. Despierta el agente desde la DB, reconstruye la instancia correcta, descuenta `energia_requerida` a través de un método de la clase, y persiste el nuevo estado del agente. |
| `GET` | `/briefing/{nombre}` | No | Obtiene información del agente (nombre, rol, energía) y su planeta de nacimiento desde SWAPI. El `planet_id` se calcula automáticamente contando el número de letras del nombre del agente. |


## 3. Decicisiones de ingeniería

### 3.1 Esquema de la tabla `misiones` 

Añadi la columna tiempo_estimado a la tabla para monitorear el tiempo que le tomaría a cada agente realizar la misón y poder llevar un control de posibles agentes disponibles para asignar una nueva misión.

### 3.2 API Publica elegida 

Elegi la API SWAPI: The Star Wars API, ya que, los agentes de mi proyecto han tenido un perfil galáctico y del espacio. Y como información adiconal incluí el lugar de "nacimiento", dado que la información de la NASA es más compleja y trae mucha data, decidi tomar el endpoint de planetas de SWAPI para conocer el lugar de "nacimiento" del agente consultando el nombre del plante segun el id del mismo, el id se determina contando las letras del nombre del agente.

### 3.3 Estrategia de resiliencia

Para el endpoint `/briefing/{nombre}` que consume la API externa SWAPI, se implementa una **estrategia de timeout y fast-fail**:

- Se establece un timeout de `EXTERNAL_API_TIMEOUT` segundos (5 segundos por defecto) para las peticiones a SWAPI.
- Si la API no responde dentro del timeout o hay error de conexión, el endpoint retorna error HTTP `504 Gateway Timeout`. Lo que permite al usuario sepa que no se pudo completar la información y establezca su propia estrategia de reintento. No se retorna el objeto con la información disponible ya que esta información se puede consultar desde otro endpoint dado que el plus o valor agregado de este endpoint es consultar la información del nombre del lugar de nacimiento desde una fuente externa no traer esta información no aportaría al objetivo de la API.


## 4. Referencias consultadas 

| Referencia | URL | Descripción |
|---|---|---|
| Configuracion inicial logging | [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html) | Documentación oficial de logging en Python |
| Personalizacion formato logging | [https://docs.python.org/es/3/howto/logging.html](https://docs.python.org/es/3/howto/logging.html) | Documentación oficial de logging en Python (español) |
| Capturar headers | [https://medium.com/@mizutori/fastapi-study-diary-5-handling-request-headers-and-error-responses-b9d23ed48747](https://medium.com/@mizutori/fastapi-study-diary-5-handling-request-headers-and-error-responses-b9d23ed48747) | Manejo de request headers y respuestas de error en FastAPI |
| Validacion de headers en endpoints | [https://medium.com/@ddias.olv/mastering-depends-in-fastapi-unlocking-the-power-of-dependency-injection-e529c99386ea](https://medium.com/@ddias.olv/mastering-depends-in-fastapi-unlocking-the-power-of-dependency-injection-e529c99386ea) | Inyección de dependencias con Depends en FastAPI |
| Enviar header en la petición | [https://skaaptjop.medium.com/getting-clever-with-python-requests-http-methods-5eeafcd92292](https://skaaptjop.medium.com/getting-clever-with-python-requests-http-methods-5eeafcd92292) | Métodos HTTP y uso avanzado de la librería requests |
| Variables de entorno | [https://lukianovihor.medium.com/python-environment-variables-using-dotenv-library-71529ad0e9c3](https://lukianovihor.medium.com/python-environment-variables-using-dotenv-library-71529ad0e9c3) | Carga de variables de entorno usando .env y dotenv |



---
