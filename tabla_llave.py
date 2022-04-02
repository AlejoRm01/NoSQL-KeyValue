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
               

    def eliminar(self, llave):
        for i in self.dicc:
            if str(llave['llave']) == str(i['llave']): 
                print('entre')
                self.dicc.remove(i)
                
                
    def ver_llave(self, llave):
        for i in self.dicc:
            if str(llave) == str(i['llave']): 
                self.dicc.remove(i)
                return i

    


    

    
    
    