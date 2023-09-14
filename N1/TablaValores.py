import os
import json

class tabla_valores():
    
    def __init__(self):
        self.TABLA_LLAVES = 'TablaValores.json'
        self.dicc = []

    def inicializar_tabla(self):
        if os.path.exists(self.TABLA_LLAVES):
            with open(self.TABLA_LLAVES, 'r', encoding='utf-8') as f:
                self.dicc = json.load(f)

    def guardar_llaves(self):
        with open(self.TABLA_LLAVES, 'w', encoding='utf-8') as f:
            json.dump(self.dicc, f, ensure_ascii=False, indent=4)

    def leer_lista_llaves(self):
        return self.dicc
    
    def buscar_por_llave(self, llave):
        for elemento in self.dicc:
            if llave in elemento:
                return elemento[llave]
        return None

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
'''
if __name__ == "__main__":
    t = tabla_valores()
    t.inicializar_tabla()
    x = t.buscar_por_llave("Arquitectura.png")
    print(x)
'''
