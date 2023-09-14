# BackUp

## Realizado por Alejandro Rodriguez Muñoz

### Materia Sistemas operativos de la universidad EAFIT 2023-1


### Arquitectura

![Arquitectura del sistema](https://github.com/AlejoRm01/NoSQL-KeyValue/blob/e0589cfa6dbcc5eeb54c7762da5390d806984e2e/Arquitectura.png)

### Instalacción
***
```
$ git clone https://github.com/AlejoRm01/NoSQL-KeyValue
$ cd ../path/to/the/file/NoSQL-KeyValue
```
### Ejecución
***
#### Primero nodos
Se ejecutan los nodos de la siguiente manera: 
```
$ cd N0/python3 Nodo.py
$ cd N1/python3 Nodo.py
$ cd N1/python3 Nodo.py
```

#### Segundo balanceardor
Se ejecuta asi:
```
$ python3 Balanceador.py -a 2020 2021 2022
```

#### Tercero cliente
El cliente puede crear, leer, actualizar y eliminar.
```
$ python3  Cliente.py
```
Se ejecuta y salen varias opciones, en este momento esta funcional la opcion 1 y 2 solamente
