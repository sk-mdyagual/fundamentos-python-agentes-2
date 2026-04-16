##Temas de la semana
##Día 1 - Listas y Diccionarios
### Listas [] Mutable (modificable) >> Colección ordenada de elementos
# -indexación (índices | posicionamiento) >> str inmutable (no modificable) >> Colección ordenada de caracteres
# Positivos 0, 1, ...
# Negativos -1, -2, ...
notas = [80, 65,60, 96, 74, 45]
nombre = "Julian Agamez"
info = ["Julian", 2002, True, 18.5]

print(f"Total de elementos: {len(notas)}")
print(f"Primer elemento: {notas[0]}")
print(f"Último elemento: {notas[-1]}")
print(f"Total de caracteres: {len(nombre)}")
print(f"Primer caracter: {nombre[0]}")
print(f"Último caracter: {nombre[-1]}")

#Funcione típicas de listas

#append() >> Agrega un elemento al final de la lista
print(f"Notas antes: {notas}")
notas.append(85)
print(f"Notas después: {notas}")
print("##################")

#lower() >> Convierte una cadena a minúsculas
print(f"Nombre antes: {nombre}")
nombre = nombre.lower()
print(f"Nombre después: {nombre}")

#concatenación - ' + ' >> Unir dos o más cadenas o listas
nombre_completo = "Julian " + "Agamez"
notas_2 = [88, 92]
todas_notas = notas + notas_2

print(f"Nombre completo: {nombre_completo}")
print(f"Todas las notas: {todas_notas}")

#extend() >> Agrega los elementos de una lista al final de otra lista
print(f"Notas antes de extend: {notas}")
notas.extend(notas_2)
print(f"Notas después de extend: {notas}")

#TO-DO
# ¿Cómo agregar elementos a una lista en una posición específica?

#insert() >> Agrega un elemento en una posición específica
print(f"Notas antes de insert: {notas}")
notas.insert(2, 77) # Agrega 77 en la posición 2
print(f"Notas después de insert: {notas}")

# Otras funciones para usar en las listas

#reverse() >> Invierte el orden de los elementos de la lista
print(f"Notas antes de reverse: {notas}")
notas.reverse()
print(f"Notas después de reverse: {notas}")

#count() >> Cuenta cuántas veces aparece un elemento en la lista
print(f"Notas: {notas}")
print(f"El número 85 aparece {notas.count(85)} veces en la lista")

#index() >> Devuelve el índice de la primera aparición de un elemento en la lista
print(f"Notas: {notas}")
print(f"El índice de la primera aparición de 85 es {notas.index(85)}")

#remove() >> Elimina la primera aparición de un elemento en la lista
print(f"Notas antes de remove: {notas}")
notas.remove(85)
print(f"Notas después de remove: {notas}")

#pop() >> Elimina y devuelve el elemento en una posición específica
print(f"Notas antes de pop: {notas}")
notas.pop(2) # Elimina el elemento en la posición 2
print(f"Notas después de pop: {notas}")

#clear() >> Elimina todos los elementos de la lista
print(f"Notas antes de clear: {notas}")
notas.clear()
print(f"Notas después de clear: {notas}")

# ¿Cómo ordenamos una lista?

#sort() >> Ordena los elementos de la lista
print(f"Notas antes de sort: {notas}")
notas.sort()
print(f"Notas después de sort: {notas}")

###Diccionarios: { } - par clave-valor
estudiantes = {"M0421": "Julian Agamez", "M0422": "Camila Rojas", "M0423": "Sofia Vargas"}
calificaciones = {"M0421": [80, 85, 90], "M0422": [75, 88, 92], "M0423": [60, 70, 80]}

# .update()
print("################")
print(f"Estudiantes antes de update: {estudiantes}")
estudiantes.update({"M0424": "Andres Perez"})
print(f"Estudiantes después de update: {estudiantes}")

#Acceder a un valor por su clave
print(f"Calificaciones de M0421: {estudiantes['M0421']}")
print(f"Calificaciones de M0422: {estudiantes.get('M0422')}")

#TO-DO: .keys(), .values(), ...

print(f"Claves de estudiantes: {estudiantes.keys()}")
print(f"Valores de estudiantes: {estudiantes.values()}")
print(f"Items de estudiantes: {estudiantes.items()}")

#for - listas
for n in notas: #n en cada vuelta, va a ser un elemento de la lista notas
    print(f"Nota: {n}")

for i in range(len(notas)): #i en cada vuelta, va a ser un índice de la lista notas
    print(f"Nota: {notas[i]}")

#for - diccionarios
for key, value in estudiantes.items(): #value en cada vuelta, va a ser un valor del diccionario estudiantes
    print(f"Matricula: {key}, Nombre: {value}")

