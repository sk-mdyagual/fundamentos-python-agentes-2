#Día  2 Líbrerias, Modulos y Herencias
## ¿Qué es un modulo? Un archivo .py que contine codigo reutilizable (funciones, clases, variables)
## ¿Qué es una librería? Una colección de modulos agrupados
## ¿Por qué modularizar? Para organizar el código, facilitar su mantenimiento y reutilización



## 1. import completo: accedes con prefijo del modulo.funcion

import math
print(math.sqrt(144))
print(math.pi)

## 2. import especifico: accedes directamente a la función sin prefijo

## Para revisión autónoma:
### ¿Qué es un entorno virtual (venv) y por qué es importante?
### Es un entorno aislado que permite gestionar las dependencias de un proyecto sin afectar al sistema global. Es importante para evitar conflictos entre paquetes y mantener un entorno limpio.
### ¿Qué hace: pip freeze > requirements.txt?
### Genera un archivo con la lista de paquetes instalados y sus versiones, útil para replicar el entorno en otro sistema.
### ¿Qué es pyproject.toml?
### Es un archivo de configuración que define las dependencias y la configuración del proyecto, utilizado por herramientas como Poetry para gestionar el proyecto.

## Para revisión autónoma:
### ¿Qué es herencia múltiple? class Hijo(Padre1, Padre2):
### Es una característica de la programación orientada a objetos donde una clase puede heredar de más de una clase padre, lo que permite combinar funcionalidades de ambas clases.
### ¿Qué son las clases abstractas (ABC)?
### Son clases que no pueden ser instanciadas directamente y que definen métodos que deben ser implementados por las clases hijas.
### ¿Qué es polimorfismo y cómo se relaciona con override?
### El polimorfismo es la capacidad de una función o método para procesar objetos de diferentes clases. El override es una técnica que permite a una clase hija proporcionar una implementación específica de un método que ya está definido en su clase padre, lo que facilita el polimorfismo.