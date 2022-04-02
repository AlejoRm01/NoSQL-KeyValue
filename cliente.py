import socket, pickle, struct, sys

class Cliente():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port 
        self.msg = {}
     
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

        self.msg['operacion'] = '1'
        self.msg['llave'] = llave
        self.msg['valor'] = valor
    
        self.enviar(self.msg)


    def leer(self, llave):
        #Leer registro o registros de la base de datos
        self.msg['operacion'] = '2'
        self.msg['llave'] = llave

        self.enviar(self.msg)

    def actualizar(self, llave, path):
        #Actualizar registro de la base dec datos
        valor = self.leer_archivo(path)

        self.msg['operacion'] = '3'
        self.msg['llave'] = llave
        self.msg['valor'] = valor

        self.enviar(self.msg)

    def eliminar(self, llave):
        #Eliminar registro de la base de datos
        self.msg['operacion'] = '4'
        self.msg['llave'] = llave

        self.enviar(self.msg)

    def enviar(self, msg):   
        #Almacenar str en un contenedor dumps y enviar este al servidor
        msg = pickle.dumps(msg)
        length = len(msg)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(msg)
       
    def recvall (self):
        #Recibir respueta del servidor si es necesario
        msg = self.sock.recv(17520)
           
    def cerrar_conexion(self):
        #Cerrar conexion 
        self.sock.close()

llave = sys.argv[0]                
documento = sys.argv[1]   
if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5000)
    c.iniciar_conexion()
    c.crear(llave, documento)
    c.cerrar_conexion()
