import os
import json

class tablaNodos():
    
    def __init__(self):
        self.TABLA_LLAVES = 'TablaNodos.json'
        self.dicc = {}

    def inicializar_tabla(self):
        if os.path.exists(self.TABLA_LLAVES):
            with open(self.TABLA_LLAVES, 'r') as f:
                self.dicc = json.load(f)

    def guardar_llaves(self):
        with open(self.TABLA_LLAVES, 'w') as f:
            json.dump(self.dicc, f, indent=4)

    def crear_llave(self, llave, particiones):
        self.dicc[llave] = particiones

    def obtener_particiones(self, llave):
        return self.dicc.get(llave, [])

    def eliminar(self, llave):
        if llave in self.dicc:
            del self.dicc[llave]