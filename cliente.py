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
        # Abrir archivo, leerlo y retornarlo
        file = open(path, 'rb')
        archivo = file.read()
        file.close()

        return archivo
    
    def crear(self, llave, path):
        #Crear un registro nuevo en la bases de datos
        valor = self.leer_archivo(path)

        self.msg += str(1)
        self.msg += '/' + str(llave)
        self.msg += '/' + str(valor)
    
        self.enviar()


    def leer(self, llave):
        #Leer registro o registros de la base de datos
        self.msg += str(2)
        self.msg += '/' + str(llave)

        self.enviar()

    def actualizar(self, llave, path):
        #Actualizar registro de la base dec datos
        valor = self.leer_archivo(path)

        self.msg += str(3)
        self.msg += '/' + str(llave)
        self.msg += '/' + str(valor)

        self.enviar()

    def eliminar(self, llave):
        #Eliminar registro de la base de datos
        self.msg += str(4)
        self.msg += '/' + str(llave)

        self.enviar()

    def enviar(self):   
        #Almacenar str en un contenedor dumps y enviar este al servidor
        msg = pickle.dumps(self.msg)
        length = len(msg)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(msg)
       
    def recvall (self):
        #Recibir respueta del servidor si es necesario
        msg = self.sock.recv(17520)
           
    def cerrar_conexion(self):
        #Cerrar conexion 
        self.sock.close()
                
   
if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5050)
    c.iniciar_conexion()
    c.crear('Hola', r'Telematica.png')
    c.enviar()
    c.cerrar_conexion()
