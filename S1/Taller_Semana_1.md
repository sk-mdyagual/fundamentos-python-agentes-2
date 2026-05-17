# 🛠️ Taller Semana 1: El Núcleo del Agente y Control de Acceso

**Fecha límite de entrega:** 16 de marzo, 2026. - 23h59

## 🎯 Objetivo del Sprint
Tu misión esta semana es tomar el bucle base que construimos en clase y convertirlo en un sistema seguro y multifuncional. Deberás programar una capa de seguridad (Login) y agregar nuevas herramientas (comandos) que requieran manipulación de texto y operaciones matemáticas, asegurando que el programa no colapse ante entradas inesperadas.

## 📋 Requerimientos Funcionales

Tu script (`main.py`) debe integrar las siguientes fases:

### Fase 1: Capa de Seguridad (Login)
Antes de que el Agente despierte y comience a escuchar comandos, debe verificar quién intenta acceder:
* El sistema debe pedir un `usuario` y una `contraseña` por consola.
* **Roles:** Define en tu código un perfil de invitado (ej. `user = "invitado"`) y un administrador (`admin = "admin"`), con sus respectivas contraseñas.
* **Sistema de Bloqueo:** El usuario tiene un máximo de **3 intentos**. Si falla 3 veces, el bucle de login se rompe, el programa imprime `[Alerta] Usuario bloqueado. Cerrando sistema.` y la ejecución termina.
* Si el inicio de sesión es exitoso, el sistema pasa a la Fase 2 y *debe recordar* con qué rol ingresó el usuario.

### Fase 2: Comandos Base (Repaso de Clase)
El menú infinito (`while`) debe mantener los comandos que exploramos en nuestra sesión interactiva:
* **`ping`:** Responde con `"pong!"`.
* **`contar`:** Pide una frase y cuenta las vocales y consonantes usando un ciclo `for`.
* **`salir`:** Rompe el bucle principal y apaga el Agente de forma elegante.

### Fase 3: Nuevas Herramientas (Tu verdadero reto)
Debes programar estos 3 comandos nuevos integrándolos a tu estructura `if/elif/else` del menú principal:

* **Comando `fecha_hoy` (Control de Acceso):** * Este comando es clasificado. Si el usuario ingresó como administrador, muestra la fecha actual *(Reto Eutagógico: investiga cómo importar el módulo `datetime` para esto)*. 
  * Si ingresó como invitado, imprime: `[Acceso Denegado] Este comando requiere privilegios de administrador.`

* **Comando `validar_pass` (Manipulación de Strings):**
  * El agente pedirá al usuario que ingrese una propuesta de contraseña nueva.
  * Debes validar dos cosas usando `if/else` y funciones de strings: 
    1. Que tenga al menos 8 caracteres de longitud (`len()`).
    2. Que no sea exactamente igual a su nombre de usuario (para esto necesitas comparar el input con la variable que guardaste en el Login).
  * Imprime un mensaje de éxito o el motivo del rechazo.

* **Comando `calculadora` (Casting y Lógica Múltiple):**
  * El agente pedirá: "Ingresa el primer número", "Ingresa el operador (+, -, *, /)", y "Ingresa el segundo número".
  * Debes convertir (`int()` o `float()`) los inputs numéricos.
  * Usando `if/elif/else` para evaluar el operador, imprime el resultado de la operación matemática. 
  * *(Opcional/Extra: ¿Qué pasa si intentan dividir por cero? Intenta manejar ese caso con un `if`).*

---

## 🤖 Política de IA (Vibecoding) y Criterios de Evaluación

En la vida real usamos la IA para acelerar el desarrollo. Puedes usar herramientas como ChatGPT, Cursor o Claude para ayudarte a codificar la sintaxis. Sin embargo, en este curso tú eres el Arquitecto (el piloto principal), no un simple transcriptor.

**Regla estricta de entrega:**
Debes incluir comentarios (`#`) escritos con **tus propias palabras** encima de los bloques más complejos de tu código:
1. Explica paso a paso cómo funciona tu lógica del contador de los 3 intentos en el Login.
2. Explica por qué tuviste que usar `int()` o `float()` en la calculadora y qué error daría el programa si no lo hicieras.

Si el código funciona perfectamente pero carece de tus explicaciones lógicas personales, el taller se considerará incompleto. ¡Demuestra que entiendes y controlas lo que el código hace!

