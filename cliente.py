import socket, pickle, os, colorama

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
        archivo = file.read()
        file.close()

        return archivo
    
    def crear(self, llave, path):

        valor = self.leer_archivo(path)

        self.dicc['operacion'] = 1
        self.dicc['llave'] = llave
        self.dicc['valor'] = valor
    
        self.enviar()


    def leer(self, llave):

        self.dicc['operacion'] = 2
        self.dicc['llave'] = llave

        self.enviar()

    def actualizar(self, llave, path):
        
        valor = self.leer_archivo(path)

        self.dicc['operacion'] = 3
        self.dicc['llave'] = llave
        self.dicc['valor'] = valor

        self.enviar()

    def eliminar(self, llave):

        self.dicc['operacion'] = 4
        self.dicc['llave'] = llave

        self.enviar()

    def enviar(self):
       # Enviar datos al servidor sendall usa UDP
        x = self.dicc
        length = len(x) 
        self.sock.sendall(length)
        self.sock.sendall(x)

       
    def recvall (self):
        msg = self.sock.recv(17520)
        if(msg != None ):
            f = open(msg['llave'],'wb')
            f.write(msg['valor'])
            f.close()
           
    def cerrar_conexion(self):
        self.sock.close()
                
   
if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5050)
    c.iniciar_conexion()
    c.cerrar_conexion()
