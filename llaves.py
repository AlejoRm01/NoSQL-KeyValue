import csv, os


class llaves():
    

    def __init__(self):
        self.TABLA_LLAVES = 'llaves.csv'
        self.ESQUEMA_LLAVES = ['llave', 'servidor']
        self.llaves = [] 

    def inicializar_tabla(self):
        with open(self.TABLA_LLAVES, 'a+') as f:
            lector = csv.DictReader(f, fieldnames=self.ESQUEMA_LLAVES)

            for row in lector:
                self.llaves.append(row)

    def guardar_llaves(self):

        tmp_tabla_llaves = '{}.tmp'.format(self.TABLA_LLAVES)
        with open(tmp_tabla_llaves, mode='a+') as f:
            escritor = csv.DictWriter(f, fieldnames=self.ESQUEMA_LLAVES)
            escritor.writerows(self.llaves)
            os.remove(self.TABLA_LLAVES)
        os.rename(tmp_tabla_llaves, self.TABLA_LLAVES)
            

    def ver_lista_llaves(self):
        aux = ''
        for idx, llave in enumerate(self.llaves):
            aux += ('{llave} | {servidor}\n').format(
                llave = llave['llave'],
                servidor = llave['servidor']
            )
        return aux

    def crear_llave(self, llave):
        
        if llave not in self.llaves:
            self.llaves.append(llave)
            return 'Se creo correctamente la llave: {}'.format(llave)
        else: 
            return 'Ya existe en la lista la llave: {}'.format(llave)

    def eliminar_llave(self, llave):
        if llave not in self.llaves:
            return 'No exite la llave: {}'.format(llave)
        else: 
            aux = self.llaves.index(llave)
            self.llaves.pop(aux)
            return 'Se elimino correctamente: {}'.format(llave)

if __name__=='__main__':

    llave1 = {
            'llave': 1,
            'servidor': 20
        }
    llave2= {
            'llave': 2,
            'servidor': 4
        }
    llave3 ={
            'llave': 3,
            'servidor': 6
        }
    llave4 ={
            'llave': 3,
            'servidor': 5
        }
        
    tabla = llaves()
    
    tabla.inicializar_tabla()
    
    tabla.crear_llave(llave1)
    tabla.crear_llave(llave2)
    tabla.crear_llave(llave3)
    tabla.crear_llave(llave4)
   
    tabla.ver_lista_llaves()

    tabla.guardar_llaves()

    
    
    