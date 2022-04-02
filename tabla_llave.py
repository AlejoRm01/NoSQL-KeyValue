import csv, os


class tabla_llave():
    
    def __init__(self):
        self.TABLA_LLAVES = 'llaves_nodos.csv'
        self.ESQUEMA_LLAVES = ['llave', 'servidor']
        self.dicc = [] 

    def inicializar_tabla(self):
        
        with open(self.TABLA_LLAVES, 'r') as f:
            lector = csv.DictReader(f, fieldnames=self.ESQUEMA_LLAVES)
            
            for row in lector:
                self.dicc.append(row)
            

    def guardar_llaves(self):

        tmp_tabla_llaves = '{}.tmp'.format(self.TABLA_LLAVES)
        with open(tmp_tabla_llaves, mode='w') as f:
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
        for i in self.dicc:
            if str(llave['llave']) == str(i['llave']): 
                aux = 1

        if aux == 0: 
            self.dicc.append(llave)
            return 'Se creo correctamente la llave: {} en el servidor {}'.format(llave['llave'], llave['servidor'])
        else: 
            self.eliminar_llave(llave)
            return 'Ya existe en la lista la llave: {}'.format(llave['llave'])    

                
    def ver_llave(self, llave):
        
        aux = 0
        for idx, k in enumerate(self.dicc):
            if llave == k['llave']: 
                aux = k
    
        return aux
    
    
    def eliminar_llave(self, llave):
        print(llave)
        for i in self.dicc:
            if str(llave) == str(i['llave']): 
                self.dicc.pop(i)
                return 'Se elimino correctamente: {}'.format(i)
            else:
                return 'No exite la llave: {}'.format(llave)


    

    
    
    