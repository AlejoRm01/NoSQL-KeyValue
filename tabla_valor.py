import csv, os


class Tabla_valor():
    
    def __init__(self):
        self.TABLA_DATOS = 'llaves_valores.csv'
        self.ESQUEMA_LLAVES = ['llave', 'valor']
        self.dicc = [] 

    def inicializar_tabla(self):
        
        with open(self.TABLA_DATOS, 'a+') as f:
            lector = csv.DictReader(f, fieldnames=self.ESQUEMA_LLAVES)
            for row in lector:
                self.dicc.append(row)

    def guardar_llaves(self):

        tmp_tabla_datos = '{}.tmp'.format(self.TABLA_DATOS)
        with open(tmp_tabla_datos, mode='a+') as f:
            escritor = csv.DictWriter(f, fieldnames=self.ESQUEMA_LLAVES)
            escritor.writerows(self.dicc)
            os.remove(self.TABLA_DATOS)
        os.rename(tmp_tabla_datos, self.TABLA_DATOS)
            

    def ver_lista_llaves(self):
        
        aux = ''
        for idx, llave in enumerate(self.dicc):
            aux += ('{llave} | {servidor}\n').format(
                llave = llave['llave'],
                servidor = llave['valor']
            )
        return aux

    def crear_llave(self, llave):
        
        aux = 0
        for idx, k in enumerate(self.dicc):
            if llave['llave'] == k['llave']: 
                aux += 1

        if aux == 0: 
            self.dicc.append(llave)
            return 'Se creo correctamente la llave: {} en el servidor {}'.format(llave['llave'], llave['valor'])
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