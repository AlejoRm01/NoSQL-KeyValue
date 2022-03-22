import socket, pickle, struct,os, colorama

class Cliente():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port 
        self.dicc = {}
     
    def iniciar_conexion(self):
        # Iniciar servicio
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.hostname, self.port))
        except Exception as e:
            print(e)
    
    def leer_archivo(self, path):
        file = open(path, 'rb')
        self.dicc['value'] = file.read()
        file.read()
        key = format(id(os.path.split(path)[1]))
        self.dicc['key'] = key
        file.close()
    
    def enviar_archivo(self):
        # Enviar datos al servidor sendall usa UDP
        x = self.dicc
        length = len(x)
        self.sock.sendall(length)
        self.sock.sendall(x)

       
    def recvall (self):
        msg = self.sock.recv(17520)
        msgg = pickle.loads(msg)
        print(colorama.Back.BLUE+colorama.Fore.RED+ msgg['mensaje']+colorama.Style.RESET_ALL)
        if(msgg['archivo'] != "no"):
            f = open(msgg['nombreArchivo'],'wb')
            f.write(msgg['archivo'])
            f.close()

    def recvallfile(self):
        
        msg = self.sock.recv(17520)
        msgg = pickle.loads(msg)
        print(colorama.Back.BLUE+colorama.Fore.RED+ msgg['mensaje']+colorama.Style.RESET_ALL)
        if(msgg['mensaje'] != (f"No existe el bucket {self.dicc['bucket']}")):
            for fichero in msgg['lista']:
                print(fichero)    

    def cerrar_conexion(self):
        self.sock.close()
                
   
if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5050)
    c.iniciar_conexion()
    c.cerrar_conexion()
