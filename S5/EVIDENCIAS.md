# Evidencias - Semana 5: Fundamentos Python Agentes

## Sesion 2 - Servidor FastAPI y Cliente HTTP

### Capitulo 3: Mi primer endpoint

**Prueba:** `GET /` desde Swagger UI  
**Resultado:**
```json
{
  "status": "online",
  "mensaje": "Bienvenido al sistema de agentes"
}
```
**Codigo HTTP:** 200 OK  
**Conclusion:** El servidor FastAPI esta corriendo y respondiendo correctamente. Swagger UI genera documentacion interactiva automaticamente a partir del codigo Python.

---

### Capitulo 4: GET con parametros

**Prueba:** `GET /agente/{nombre}` con agente existente y no existente  
**Resultado agente existente:**
```json
{
  "nombre": "Orion",
  "rol": "estratega",
  "energia": 130
}
```
**Resultado agente no existente:**
```json
{
  "detail": "Agente 'Oriona' no encontrado"
}
```
**Conclusion:** Los path parameters `{nombre}` en la URL permiten que el cliente especifique exactamente que recurso quiere. Cuando el agente existe, el servidor retorna sus datos con codigo 200. Cuando no existe, FastAPI lanza una `HTTPException` con codigo 404, lo que comunica claramente al cliente que el recurso no fue encontrado sin romper el servidor. 

---

### Capitulo 5: POST endpoints

**Prueba:** `POST /agentes/` para crear un agente  
**Body enviado:**
```json
{
  "nombre": "Orion",
  "rol": "estratega",
  "energia": 130
}
```
**Resultado:**
```json
{
  "mensaje": "[DB] Agente 'Orion' registrado con exito."
}
```
**Prueba:** `POST /mensajes/` y luego `GET /mensajes/{nombre}`  
**Resultado:**
```json
 {'mensaje': "[DB] Mensaje de 'Orion' a 'Atlas' enviado a las 2026-04-14T19:53:50.313554."}
```
**Conclusion:** GET y POST cumplen roles opuestos: GET lee datos sin modificar el estado del servidor, POST envia datos nuevos y los persiste. Pydantic valida automaticamente el cuerpo del request antes de que llegue a la logica del negocio: si un campo tiene el tipo incorrecto (por ejemplo `energia="hola"`), FastAPI rechaza la peticion con un error 422 sin necesidad de escribir validacion manual. 

---

### Capitulo 6: El agente como cliente HTTP

**Prueba:** Enviar mensaje via script Python, luego consultar en Swagger UI con `GET /mensajes/{nombre}`  
**Resultado en Swagger UI:**
```json
{
  "status": "online",
  "mensaje": "Bienvenido al sistema de agentes"
}
```
**Codigo HTTP:** 200 OK  
**Conclusion:** El protocolo HTTP es el puente universal. No importa si se usa Python (`requests`) o el navegador (Swagger UI): ambos son clientes que hablan el mismo idioma HTTP con el servidor. El resultado es el mismo porque llegan al mismo lugar.

---

### Capitulo 7: El circuito completo

**Prueba:** Ejecutar `python S5_cliente.py` con el circuito completo descomentado  
**Output del script:**
``` json
Servidor: {'status': 'online', 'mensaje': 'Bienvenido al sistema de agentes'}
Registrar agente: {'mensaje': "[DB] Agente 'Orion' registrado con exito."}
Agente consultado: {'nombre': 'Orion', 'rol': 'estratega', 'energia': 130}
Mensaje enviado: {'mensaje': "[DB] Mensaje de 'Orion' a 'Atlas' enviado a las 2026-04-14T19:53:50.313554."}

--- Bandeja de Atlas (5 mensajes) ---
  [2026-04-09T14:35:17.977171] Nova -> Excelente. Enviare un drone de analisis.
  [2026-04-09T14:37:11.184229] Nova -> Excelente. Enviare un drone de analisis.
  [2026-04-09T14:40:57.719480] Nova -> Excelente. Enviare un drone de analisis.
  [2026-04-09T14:41:59.462295] Nova -> Excelente. Enviare un drone de analisis.
  [2026-04-14T19:53:50.313554] Orion -> Solicito reporte de la mision.
```
**Verificacion en Swagger UI:** `GET /mensajes/Atlas`  
**Resultado:**
```json
[
  {
    "remitente": "Nova",
    "destinatario": "Atlas",
    "contenido": "Excelente. Enviare un drone de analisis.",
    "timestamp": "2026-04-09T14:35:17.977171"
  },
  {
    "remitente": "Nova",
    "destinatario": "Atlas",
    "contenido": "Excelente. Enviare un drone de analisis.",
    "timestamp": "2026-04-09T14:37:11.184229"
  },
  {
    "remitente": "Nova",
    "destinatario": "Atlas",
    "contenido": "Excelente. Enviare un drone de analisis.",
    "timestamp": "2026-04-09T14:40:57.719480"
  },
  {
    "remitente": "Nova",
    "destinatario": "Atlas",
    "contenido": "Excelente. Enviare un drone de analisis.",
    "timestamp": "2026-04-09T14:41:59.462295"
  },
  {
    "remitente": "Orion",
    "destinatario": "Atlas",
    "contenido": "Solicito reporte de la mision.",
    "timestamp": "2026-04-14T19:53:50.313554"
  }
]
```
**Conclusion:** El circuito completo demuestra que una aplicacion real es una cadena de peticiones HTTP coordinadas: verificar disponibilidad, crear recursos, consultarlos, enviar datos y leerlos. Todo desde codigo Python puro, sin intervension del navegador. Este es el patron base de los microservicios y las integraciones entre sistemas: cada actor es un cliente HTTP que habla con otros a traves de endpoints bien definidos.

