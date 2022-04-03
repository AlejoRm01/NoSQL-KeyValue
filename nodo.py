import multiprocessing
import socket, struct, pickle
from tabla_valores import *
import argparse

class nodo():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connected = True
        self.msg = {}
        self.port_balanceador_de_carga = 5050

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
        #Se organiza la informacion
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
        print('Creando')
        aux = {
            'llave':msg['llave'],
            'valor':msg['valor']
        }
        
        t = tabla_valores()
        t.inicializar_tabla()
        t.crear_llave(aux)
        t.guardar_llaves()
        
    def leer(self, msg):
        t = tabla_valores()
        t.inicializar_tabla()
        msg = t.leer_llave(msg['llave'])
         
        self.enviar(msg)
        
    def actualizar(self, msg):
        t = tabla_valores()
        t.inicializar_tabla()
        t.actualizar_llave(msg)
        t.guardar_llaves()
        
    def eliminar(self, msg):
        t = tabla_valores()
        t.inicializar_tabla()
        t.eliminar(msg['llave'])
        t.guardar_llaves()
        

    def enviar(self, msg):
        #Enviar datos al nodo  
        print('Enviando datos')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self.hostname, 4999))

        msg = pickle.dumps(msg)
        length = len(msg)
        
        connection.sendall(struct.pack('!I', length))
        connection.sendall(msg)
        connection.close()
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('port', default=5000, type=int)
    args = parser.parse_args()
    s = nodo( hostname = 'localhost', port = args.port)
    s.iniciar_conexion()
    s.aceptar_conexion()