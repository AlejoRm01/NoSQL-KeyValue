import socket, pickle, struct, os

class Cliente():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port 
        self.msg = ''
     
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

        self.msg += str(1)
        self.msg += '/' + str(llave)
        self.msg += '/' + str(valor)
    
        self.enviar()


    def leer(self, llave):

        self.arr.append(2)
        self.arr.append(llave)

        self.enviar()

    def actualizar(self, llave, path):

        valor = self.leer_archivo(path)

        self.arr.append(3)
        self.arr.append(llave)
        self.arr.append(valor)

        self.enviar()

    def eliminar(self, llave):

        self.arr.append(4)
        self.arr.append(llave)

        self.enviar()

    def enviar(self):   
        x = pickle.dumps(self.msg)
        length = len(x)
        self.sock.sendall(struct.pack('!I', length))
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
    c.crear('Hola', r'Telematica.png')
    c.enviar()
    c.cerrar_conexion()
