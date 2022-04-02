import multiprocessing
import random
import socket, pickle
import struct
from tabla_llave import *

class Balanceador_de_carga():
    
    global nServidores
    nServidores = 3
    global port_nodo
    port_nodo = [5000, 5001, 5002, 5003]
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.msg = {}
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
            #Se recibe el dato con la operacion del cliente, aparte en enviarlo al metodo de 
            #organizar datos para procesar y deseempaquetar la informacion
            proceso = multiprocessing.Process(target= self.recibir_datos, args=())
            # proceso.daemon = True
            proceso.start()
            print('Nuevo proceso inciado %r', proceso)

    def recibir_datos(self):
        #Recibir datos del cliente
        while self.connected:
            try:
                # Recibir datos del cliente.
                lengthbuf = self.recvall(self.connection, 4)
                length, = struct.unpack('!I', lengthbuf)
                msg = self.recvall(self.connection, length)              
                # self.conn.sendall(b'Se han recibido los datos')    
                self.organizar_datos(msg)

            except Exception as e:
                self.connected = False
                print(e)

    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf        
                    

    def organizar_datos(self, msg):
        #Se deseempaqueta el dato y se organiza la informacion
        msg = pickle.loads(msg)

        if(msg['operacion'] == '1'):
            self.crear(msg)
        elif(msg['operacion'] == '2'):
            self.leer(msg)
        elif(msg['operacion'] == '3'):
            self.actualizar(msg)
        elif(msg['operacion'] == '4'):
            self.eliminar(msg)         
    
    def enviar(self, msg, port):
        msg = pickle.dumps(msg)
        length = len(msg)
        self.sock.sendto(struct.pack('!I', length),('localhost', port))
        self.sock.sendto(msg, ('localhost', port))

    def crear(self, msg):
        #Iniciar proceso de crear registro en la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        servidor = random.randrange(0, nServidores)
        self.enviar(msg, 5000)


    def leer(self, msg):
        #Iniciar proceso de recuperar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para entregar la llave y el valor al cliente
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(msg[1])
        llave = None
        
    def actualizar(self, msg):
        #Iniciar proceso de actulizar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para actualizar el valor en el servidor
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(msg[1])
        llave = None
        
    def eliminar(self, msg):
        #Iniciar proceso de eliminar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para eliminar la llave y el valor en el servidor
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(msg[1])
        respuesta = llave.eliminar_llave(respuesta)
        llave.guardar_llaves()
        llave = None
        
    
if __name__ == "__main__":
 # Probar conexion entre cliente y socket  
    s = Balanceador_de_carga( hostname = 'localhost', port = 5050)
    s.iniciar_conexion()
    s.aceptar_conexion()
