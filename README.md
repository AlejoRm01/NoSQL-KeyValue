# Base de datos NoSQL basada en Key-Value

## Realizado por Alejandro Rodriguez Muñoz, Camila Mejia y Daniel Solano 

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
Se necesita un puerto diferente por nodo, si se va a ejecutar un solo nodo por default estara en el
puerto 5000, se puede ejecutar de la siguiente manera: 
```
$ py nodo.py
```
De lo contrario si se quiere mas de un nodo al tiempo se debe ejecutar en diferentes consolas añadiendo como argumento el puerto
ejemplo:
```
$ py nodo.py 5000
$ py nodo.py 5001
$ py nodo.py 5002
$ py nodo.py 5003
```
#### Segundo balanceardor de carga
Si solo de dispone un nodo se ejecuta asi:
```
$ py balanceador_de_carga.py
```
Si hay mas de un nodo debes adiccionar los puertos de los nodos de esta manera:
```
$ py balanceador_de_carga.py 5000 5001 5002 5003
```

#### Tercero cliente
El cliente puede crear, leer, actualizar y eliminar.

#### Crear
```
c.crear('01', 'Juan Carlos es el mejor profesor') 
```
#### Leer 
```
c.leer('01')
``` 
#### Actualizar
```
#c.actualizar('01', 'Telematica')
```
#### Eliminar
```
#c.eliminar('01')
```
Solo es cambiar la llave por una de su elección, y el valor por uno de su elección.
#### Ejecutar de la siguiente forma:
```
$ py cliente.py 
```
