import os
import json

class tabla_nodos():
    
    def __init__(self):
        self.TABLA_LLAVES = 'tabla_nodos.json'
        self.dicc = []

    def inicializar_tabla(self):
        if os.path.exists(self.TABLA_LLAVES):
            with open(self.TABLA_LLAVES, 'r') as f:
                self.dicc = json.load(f)

    def guardar_llaves(self):
        with open(self.TABLA_LLAVES, 'w') as f:
            json.dump(self.dicc, f, indent=4)

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
                return i['nodo']

    def eliminar(self, llave):
        for i in self.dicc:
            if str(llave) == str(i['llave']):
                self.dicc.remove(i)