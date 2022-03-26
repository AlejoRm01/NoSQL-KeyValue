import pickle, socket, multiprocessing, struct, os,shutil

class Server():

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.dicc = {}
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
            self.conn, self.addr = self.sock.accept()
            print('conectado con %r', self.addr)
            # Manejo de procesos mediante el uso de un while y el manejo de un metodo
            proceso = multiprocessing.Process(target= self.recibir_datos, args=())
            # proceso.daemon = True
            proceso.start()
            print('Nuevo proceso inciado %r', proceso)

    
    def recibir_datos(self):
        datos = ''
        while self.connected:
            try:
                # Recibir datos del cliente.
                length = self.recvall(self.conn, 4)
                print("Si recibo datos")
                datos = self.recvall(self.conn, length)              
                # self.conn.sendall(b'Se han recibido los datos')    
            except Exception:
                self.connected = False
            
    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf

    def enviar_descargable(self,datos):
        pass
    

    def enviar_archivo(self):
        message = pickle.dumps(self.dicc)
        self.conn.sendall(message)
        
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
