# BackUp

## Realizado por Alejandro Rodriguez Muñoz

### Materia Sistemas operativos de la universidad EAFIT 2023-1


### Arquitectura

![Arquitectura del sistema](https://github.com/AlejoRm01/NoSQL-KeyValue/blob/8875a5b315c54383679fc322c6a3e9d95d618338/Arquitectura.png)

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
$ cd N2/python3 Nodo.py
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
Se ejecuta y salen varias opciones, en este momento esta funcional la opción 1 y 2 solamente
