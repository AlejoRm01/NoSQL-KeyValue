from importlib.resources import path
from msilib.schema import File


class llaves_servidores():
    
    def __init__(self, llave):
        self.dicc = {}
        self.llave = llave
        path = b'llaves_servidores.txt'

        #Verificar si el txt existe, si no existe se crea
        self.file = self.verificar_txt(path)
        if self.file == None:
            self.crear_documento(path)
        self.datos = self.file.read()

    def recibir_llave(self, llave):
        pass
    
    def adiccionar_llave(self, llave):
        pass

    def lista_llaves_servidores(self):
        pass

    def eliminar_llave(self, llave):
        pass
    
    def enviar(self):
        pass

    def verificar_txt(self, path):
        try: 
            with open(path, 'r') as file:
                return file
                
        except FileNotFoundError as e:
                return None

    def crear_documento(self):
        file = open(path, 'w')
        return file 

    def cerrar_documento(self):
        self.file.close()
    