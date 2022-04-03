import multiprocessing
import random
import socket, pickle
import struct
from tabla_nodos import *
import argparse

class Balanceador_de_carga():

    def __init__(self, hostname, port, puertos):
        self.puertos = puertos
        self.nNodos = int(len(self.puertos))
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
        self.connection.close()
        msg = pickle.loads(msg)

        if(msg['operacion'] == '1'):
            self.crear(msg)
        elif(msg['operacion'] == '2'):
            self.leer(msg)
        elif(msg['operacion'] == '3'):
            self.actualizar(msg)
        elif(msg['operacion'] == '4'):
            self.eliminar(msg)                    

    def crear(self, msg):
        #Iniciar proceso de crear registro en la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        nodo = 0
        if self.nNodos-1 == 0:
            nodo = 0
        else:
            nodo = random.randrange(0, self.nNodos)
       
        aux = {
            'llave':msg['llave'],
            'nodo':nodo
        }
        
        t = tabla_nodos()
        t.inicializar_tabla()
        t.crear_llave(aux)
        t.guardar_llaves()
        
        self.enviar(msg, self.puertos[nodo])

    def leer(self, msg):
        #Iniciar proceso de leer un registro de la tabla de llaves y nodos, ademas de iniciar el proceso con el nodo
        t = tabla_nodos()
        t.inicializar_tabla()
        nodo = t.leer_llave(msg['llave'])
        self.enviar(msg, self.puertos[int(nodo)])
        
    def actualizar(self, msg):
        #Iniciar proceso de actualizar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para actualizar la llave y el valor en el servidor
        t = tabla_nodos()
        t.inicializar_tabla()
        nodo = t.leer_llave(msg['llave'])
        self.enviar(msg, self.puertos[int(nodo)])

    def eliminar(self, msg):
        #Iniciar proceso de eliminar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para eliminar la llave y el valor en el servidor
        t = tabla_nodos()
        t.inicializar_tabla()
        nodo = t.leer_llave(msg['llave'])
        t.eliminar(msg['llave'])
        t.guardar_llaves()
        self.enviar(msg, self.puertos[int(nodo)])
    
    def enviar(self, msg, port):
        #Enviar datos al nodo  
        print('Enviando datos')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', port))

        msg = pickle.dumps(msg)
        length = len(msg)
        
        connection.sendall(struct.pack('!I', length))
        connection.sendall(msg)
        connection.close()

if __name__ == "__main__":
    # Probar conexion entre cliente y socket  
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs="+", default=5000, type=int)
    args = parser.parse_args()

    s = Balanceador_de_carga( hostname = 'localhost', port = 5050, puertos = args.a)
    s.iniciar_conexion()
    s.aceptar_conexion()
