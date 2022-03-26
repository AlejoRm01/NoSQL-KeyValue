import socket, multiprocessing, struct, pickle, os

class Server():

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.arr = []
        self.connected = True
        
    def iniciar_conexion(self):
        # Iniciar servicio 
        try:
            print('Escuchando')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.hostname, self.port))
            self.sock.listen(1)
        except Exception as e:
            print(e)
            
    def aceptar_conexion(self):
        # Aceptar solicitudes 
        while True:
            self.connection, self.addr = self.sock.accept()
            print('conectado con %r', self.addr)
            # Manejo de procesos mediante el uso de un while y el manejo de un metodo
            proceso = multiprocessing.Process(target= self.recibir_datos, args=())
            # proceso.daemon = True
            proceso.start()
            print('Nuevo proceso inciado %r', proceso)


    def crear(self, x):
        print('Estoy en crear')

    def leer(self):
        pass

    def actualizar(self):
        pass

    def eliminar(self):
        pass

    
    def recibir_datos(self):
        datos = ''
        try:
            while self.connected:
                # Recibir datos del cliente.
                lengthbuf = self.recvall(self.connection, 4)
                length, = struct.unpack('!I', lengthbuf)
                datos = self.recvall(self.connection, length)                  
                if datos: 
                    print("Envio efectivo")
                    #self.connection.sendall(b'Se han recibido los datos')
                    self.organizar_datos(datos)
                else:
                    break
                break

        except Exception:
            self.connected = False


    def organizar_datos(self, x):
        datos = pickle.loads(x)
        datos = datos.split('/')
        print(datos)
        if(datos[0] == '1'):
            self.crear(datos)
        elif(datos[0] == '2'):
            self.leer()
        elif(datos[0] == '3'):
            self.actualizar()
        elif(datos[0] == '4'):
            self.eliminar()
        else:
            print('Operacion incorrecta')
        
    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf

    def enviar_archivo(self):
        self.conn.sendall(bytearray(self.arr))
        
    def cerrar_con(self):
        # Cerrar conexión
        self.sock.close()
    
if __name__ == "__main__":
 # Probar conexion entre cliente y socket  
    s = Server( hostname = 'localhost', port = 5050)
    s.iniciar_conexion()
    s.aceptar_conexion()
    for proceso in multiprocessing.active_children():
        print('Terminando proceso %r', proceso)
        proceso.terminate()
        proceso.join()
    print('Listo')  
