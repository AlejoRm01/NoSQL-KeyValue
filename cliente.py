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
    
    def crear_archivo(self, llave, path):
        #Crear un registro nuevo en la bases de datos
        valor = self.leer_archivo(path)

        valor = pickle.dumps(valor)

        self.msg['operacion'] = '1'
        self.msg['llave'] = llave
        self.msg['valor'] = valor
    
        self.enviar(self.msg)

    def crear(self, llave, valor):
        #Crear un registro nuevo en la bases de datos
        self.msg['operacion'] = '1'
        self.msg['llave'] = llave
        self.msg['valor'] = valor
    
        self.enviar(self.msg)

    def leer(self, llave):
        #Leer registro o registros de la base de datos
        self.msg['operacion'] = '2'
        self.msg['llave'] = llave

        self.enviar(self.msg)
        msg = self.recibir_datos()
        msg = pickle.loads(msg)
        print(msg)
        
    def actualizar(self, llave, valor):
        #Actualizar registro de la base dec datos
        #valor = self.leer_archivo(path)

        self.msg['operacion'] = '3'
        self.msg['llave'] = llave
        self.msg['valor'] = valor

        self.enviar(self.msg)

    def eliminar(self, llave):
        #Eliminar registro de la base de datos<
        self.msg['operacion'] = '4'
        self.msg['llave'] = llave

        self.enviar(self.msg)

    def enviar(self, msg):   
        #Almacenar str en un contenedor dumps y enviar este al servidor
        msg = pickle.dumps(msg)
        length = len(msg)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(msg)
           
    def recibir_datos(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.hostname, 4999))
        sock.listen(1)
        conn, addr = sock.accept()
        print('Leyendo datos de: ', addr)
        while True:
            # Recibir datos del nodo.
            lengthbuf = self.recvall(conn, 4)
            length, = struct.unpack('!I', lengthbuf)
            msg = self.recvall(conn, length)                 
            return msg

    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf  

if __name__ == "__main__":
    c = Cliente(hostname = 'localhost', port = 5050)
    #c.iniciar_conexion()
    #c.crear('01', 'Odio a todo el mundo')
    #c.actualizar('01', 'Telematica')
    #c.eliminar('01')
