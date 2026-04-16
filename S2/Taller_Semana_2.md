# 🛠️ Taller Semana 2: Motor de Búsqueda del Agente

**Fecha límite de entrega:** Lunes 23 marzo, 23h59.

**Forma de entrega:** Pull-Request a la rama semana_2 desde sus repositorios forkeados

## 🎯 Contexto
Durante las sesiones en vivo (Día 1 y Día 2), logramos que nuestro PseudoAgente guardara recuerdos (Diccionarios) en su banco de memoria (Listas) y pudiera imprimirlos todos. Sin embargo, si el agente tiene 1,000 recuerdos, leerlos todos es ineficiente. 

Tu misión es programar un **Motor de Búsqueda** interno.

## 📋 Requerimientos Funcionales

Debes agregar un **nuevo comando** a tu bucle `if/elif` del menú principal:

**Comando `historial`:** Para visualizar las acciones realizadas con el pseudoagente. El comando tiene algunas singularidades que permiten hacer algunas acciones en concreto:

  - `historial all`: Muestra todo el historial almacenado por el pesudoagente.

  - `historial clear`: Elimina todo el historial almacenado por el pseudoagente.
  
De no presentarse esto (es decir, sólo se ingresa `historial`), el pseudoagente entra en modo búsqueda:

  1. El pesudoagente debe pedir al usuario: `"Ingresa la palabra clave a buscar: "`.
  2. El programa debe iterar sobre la lista `historial_chat` usando un bucle `for` (similar a lo que hicimos en clase).
  3. Dentro del bucle, debes usar una condición `if` para verificar si la palabra clave ingresada por el usuario **está contenida** dentro del valor `"descripcion"` del diccionario actual.
  4. Si la palabra existe, cuenta cuántas coincidencias se encontraron e imprime dichas memorias (con su autor y mensaje). Caso contrario, debe devolver el mensaje  `[PseudoAgente] No encontré registros que coincidan con esa palabra.`


## 🧠 Reto Eutagógico (Autodidacta)
Las búsquedas deben ser **insensibles a mayúsculas y minúsculas**. Si guardé el mensaje "Cocinar Arroz", y busco "arroz", el sistema debería encontrarlo. *Pista: Investiga y aplica la función `.lower()` tanto a la palabra clave como al mensaje antes de compararlos.*

## 🤖 Política de Vibecoding y Evaluación
Puedes usar ChatGPT/Cursor para que te ayude a armar la lógica de búsqueda. 

**Regla de Auditoría:** Debes dejar un comentario con tus propias palabras exactamente encima de la línea del `if` donde comparas la palabra clave con el mensaje. Explica:
* ¿Cómo lograste saber si una palabra estaba "dentro" de otra en Python?
* ¿Cómo resolviste el reto de las singularidades que tiene el comando? **HINT:** función `.split()`

*Nota: Solo se revisarán los talleres que no crasheen al intentar buscar en una memoria vacía.*