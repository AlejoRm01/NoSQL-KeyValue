import csv, sys, os

class tabla_valores():
    
    def __init__(self):
        self.TABLA_LLAVES = 'tabla_valores.csv'
        self.ESQUEMA_LLAVES = ['llave', 'valor']
        self.dicc = [] 

    def inicializar_tabla(self):
        
        with open(self.TABLA_LLAVES, 'r') as f:
            lector = csv.DictReader(f, fieldnames=self.ESQUEMA_LLAVES)
            
            for row in lector:
                self.dicc.append(row)
            

    def guardar_llaves(self):

        tmp_tabla_llaves = '{}.tmp'.format(self.TABLA_LLAVES)

        with open(tmp_tabla_llaves, mode='w', encoding = 'utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=self.ESQUEMA_LLAVES)
            escritor.writerows(self.dicc)
            os.remove(self.TABLA_LLAVES)
        os.rename(tmp_tabla_llaves, self.TABLA_LLAVES)
                    

    def leer_lista_llaves(self):
        return self.dicc

    def crear_llave(self, llave):
        aux = 0
        for i in self.dicc:
            if str(llave['llave']) == str(i['llave']): 
                aux = 1

        if aux == 0: 
            self.dicc.append(llave)
               

    def leer_llave(self, llave):
        for i in self.dicc:
            if str(llave) == str(i['llave']): 
                return i

    def actualizar_llave(self, llave):
        for i in self.dicc:
            if str(llave['llave']) == str(i['llave']): 
                i['valor'] = llave['valor']
    
    def eliminar(self, llave):
        for i in self.dicc:
            if str(llave) == str(i['llave']): 
                self.dicc.remove(i)
    