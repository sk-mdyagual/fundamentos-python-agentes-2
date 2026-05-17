##Temas de la seaman
##Día 1 - Listas y Diccionarios
### Listas: [] Mutable
# -indexación (índices | posicionamiento) >> str: Inmutables
#Positivos: 0, ...
#Negativos: -1, ....
notas = [80, 65, 60, 96, 74, 45] # 0 - 80, 1 - 65, .... 5 - 45

info = ["Mishell", 1995, True, 18.5]

# -1 ~ 45, -2 ~ 74,.... -6 ~ 80
nombre = "Mishell"
#print(f"Total de elementos: {len(notas)}") #6
#print(f"Primera elemento: {notas[-len(notas)]}")
#print(f"Ultimo elemento: {notas[-1]}")

#Funciones típicas
#append(): Agregar 1 elemento al final de la lista
print(notas)
notas.append(90)
print(notas)
print("###############")
print(nombre)
nombre.lower()
print(nombre)

print("###############")

#Concatenación - '+'
nombre = "Mishell "+ "Yagual"
notas_2 = [66, 85]
res = notas + notas_2

print(nombre)
print(res)

print(notas)
notas.extend(notas_2)
print(notas)

#TO-DO
# ¿Cómo agregar elementos a una lista en una posición especifica?
# Otras funciones para usar en las listas
# ¿Cómo ordenamos una lista?

### Diccionarios: { } - Par clave, valor 
estudiantes = {"M14531":"Mishell Yagual Mendoza", "M14538": "Adriana Rojas"}
calificaciones = {"M14531": [98, 55, 80], "M14538":[94, 56, 84]}
#.update()

print("###############")
print(estudiantes)
estudiantes.update({"M14534": "Caroline Alvarado"})
print(estudiantes)

## Acceder a un valor
#print(f"Acceder a un valor: {estudiantes['M14530']}")
#print(f"Acceder a un valor: {estudiantes.get('M14530')}")

#TO-DO: .keys(), .values(), ...

#for - Listas
for n in notas: #n en cada vuelta, va a ser un elemento de la lista notas
    print(n)

for i in range(len(notas)): #i en cada vuelta va a ser un indice disponible de la lista notas - i: [0 ... 5]
    print(notas[i])

#for - Diccionarios
for value in calificaciones.values(): # items() - [("M14531","Mishell Yagual Mendoza"), .... ] 
    for i in range(len(value)): #i en cada vuelta va a ser un indice disponible de la lista notas - i: [0 ... 5]
        print(value)
