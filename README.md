# Base de datos NoSQL basada en Key-Value

## Realizado por Alejandro Rodriguez Muñoz

### Materia Topicos de telematica de la universidad EAFIT 2022-1

### Instalacción y ejecución
***
```
$ git clone https://github.com/AlejoRm01/NoSQL-KeyValue
$ cd ../path/to/the/file/NoSQL-KeyValue
```
### Ejecución
***
#### Primero ejecutas el balanceardor de cargar de la siguiente forma:
```
py balanceador_de_carga.py
```
#### Seguido los nodos que desea tener
Se necesitan un argumento para la ejecucion el cual es el puerto que tendra este nodo
```
py nodo.py 6000
```
#### Por ultimo ejecutas el cliente
Se necesitan dos argumentos para la ejecucion los cuales son en su respectivo orden llave y 
path del archivo de la siguiente manera 
```
py cliente.py 3043 C:\NoSQL-KeyValue\Telematica.png
```
