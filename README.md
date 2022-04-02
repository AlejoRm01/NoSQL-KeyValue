# Base de datos NoSQL basada en Key-Value

## Realizado por Alejandro Rodriguez Muñoz

### Materia Topicos de telematica de la universidad EAFIT 2022-1

### Instalacción
***
```
$ git clone https://github.com/AlejoRm01/NoSQL-KeyValue
$ cd ../path/to/the/file/NoSQL-KeyValue
```
### Ejecución
***
#### Primero nodos
Se necesita un puerto diferente por nodo, encontraremos en la linea 88 de la clase nodo.py lo siguiente:
```
 s = nodo( hostname = 'localhost', port = 5000)
```
Solo es cambiar el puerto por uno que no este repetido y ejecutar de la siguiente forma:
```
$ py nodo.py
```

#### Segundo balanceardor de carga
```
$ py balanceador_de_carga.py
```

#### Tercero cliente
Se necesitan una llave y una ruta de algun archivo, el archivo es de libre eleccion dejamos uno por defecto, 
pero se puede cambiar, encontraremos en la linea 80 de la clase cliente.py lo siguiente:
```
c.crear('Llave_01', 'Telematica.png') 
```
Solo es cambiar la llave por una de su elección, y el path del archivo por uno de su elección y 
ejecutar de la siguiente forma:
```
$ py cliente.py 
```
