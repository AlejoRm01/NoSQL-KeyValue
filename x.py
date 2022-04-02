import random
from tabla_llave import * 

def crear(llave):
    #Iniciar proceso de crear registro en la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
    servidor = random.randrange(0, 3)
    t = tabla_llave()
    t.inicializar_tabla()
    t.crear_llave(llave)
    t.eliminar_llave(llave)
    t.guardar_llaves()

msg = {
    'llave':231,
    'servidor':2323
}    


crear(msg)