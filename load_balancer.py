import random
import socket, multiprocessing, struct, pickle
from tabla_llaves import *

class Load_Balancer():
    
    global nServidores
    nServidores = 0
    
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


    def crear(self):
        
        servidor = random.randrange(nServidores)
        aux = [self.datos[1],servidor] 
    
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.crear_llave(aux)
        llave.guardar_llaves()
        
        return respuesta

    def leer(self):
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.datos[1])
        llave = None
        
    def actualizar(self):
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.datos[1])
        llave = None
        
    def eliminar(self):
        
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.datos[1])
        respuesta = llave.eliminar_llave(respuesta)
        llave.guardar_llaves()
        llave = None
        
        return respuesta 
    
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
    s = Load_Balancer( hostname = 'localhost', port = 5050)
    s.iniciar_conexion()
    s.aceptar_conexion()
    for proceso in multiprocessing.active_children():
        print('Terminando proceso %r', proceso)
        proceso.terminate()
        proceso.join()
    print('Listo')  
