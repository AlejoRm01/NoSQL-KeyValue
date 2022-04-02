import csv, os


class Tabla_llaves():
    
    def __init__(self):
        self.TABLA_LLAVES = 'llaves_nodos.csv'
        self.ESQUEMA_LLAVES = ['llave', 'servidor']
        self.dicc = [] 

    def inicializar_tabla(self):
        
        with open(self.TABLA_LLAVES, 'a+') as f:
            lector = csv.DictReader(f, fieldnames=self.ESQUEMA_LLAVES)

            for row in lector:
                self.dicc.append(row)

    def guardar_llaves(self):

        tmp_tabla_llaves = '{}.tmp'.format(self.TABLA_LLAVES)
        with open(tmp_tabla_llaves, mode='a+') as f:
            escritor = csv.DictWriter(f, fieldnames=self.ESQUEMA_LLAVES)
            escritor.writerows(self.dicc)
            os.remove(self.TABLA_LLAVES)
        os.rename(tmp_tabla_llaves, self.TABLA_LLAVES)
            

    def ver_lista_llaves(self):
        
        aux = ''
        for idx, llave in enumerate(self.dicc):
            aux += ('{llave} | {servidor}\n').format(
                llave = llave['llave'],
                servidor = llave['servidor']
            )
        return aux

    def crear_llave(self, llave):
        
        aux = 0
        for idx, k in enumerate(self.dicc):
            if llave['llave'] == k['llave']: 
                aux += 1

        if aux == 0: 
            self.dicc.append(llave)
            return 'Se creo correctamente la llave: {} en el servidor {}'.format(llave['llave'], llave['servidor'])
        else: 
            self.eliminar_llave(llave)
            return 'Ya existe en la lista la llave: {}'.format(llave['llave'])    


    def eliminar_llave(self, llave):
        
        if llave not in self.dicc:
            return 'No exite la llave: {}'.format(llave)
        else: 
            
            self.dicc.pop(llave)
            return 'Se elimino correctamente: {}'.format(llave)
    
    def ver_llave(self, llave):
        
        aux = 0
        for idx, k in enumerate(self.dicc):
            if llave == k['llave']: 
                aux = k
    
        return aux
    
    
'''
if __name__=='__main__':

    llave1 = {
            'llave': 1,
            'servidor': 4
        }
    llave2 = {
            'llave': 2,
            'servidor': 2
        }
    llave3 = {
            'llave': 3,
            'servidor': 4
        }
    llave4 = {
            'llave': 2,
            'servidor': 5
        }
        
    tabla = Tabla_llaves()
    
    tabla.inicializar_tabla()
    
    print(tabla.crear_llave(llave1))
    print(tabla.crear_llave(llave2))
    print(tabla.crear_llave(llave3))
    print(tabla.crear_llave(llave4))
    tabla.guardar_llaves()
    tabla.ver_lista_llaves()
'''
    

    
    
    