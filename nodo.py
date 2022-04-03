import multiprocessing
import socket, struct, pickle
from tabla_valor import *

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
        elif(msg['operacion'] == '5'):
            self.leer_llaves()
            
    def crear(self, msg):
        print('Creando')
        aux = {
            'llave':msg['llave'],
            'servidor':msg['valor']
        }
        
        #t = tabla_valor()
        #t.inicializar_tabla()
        #t.crear_llave(aux)
        #t.guardar_llaves()

        self.enviar(msg)
        
    
    def leer(self, msg):
        t = tabla_valor()
        t.inicializar_tabla()
        msg = t.leer_llave(msg['llave'])
                
        self.enviar(msg)
        
    def actualizar(self, msg):
        t = tabla_valor()
        t.inicializar_tabla()
        t.actualizar_llave(msg)
        t.guardar_llaves()
        
    
    def eliminar(self, msg):
        t = tabla_valor()
        t.inicializar_tabla()
        t.eliminar_llave(msg)
        t.guardar_llaves()
        
        
    def leer_llaves(self):
        t = tabla_valor()
        t.inicializar_tabla()
        msg = t.leer_lista_llaves()
        
        self.enviar(msg)

    def enviar(self, msg):
        print(msg)
        
    
if __name__ == "__main__":
    # Probar conexion entre cliente y socket  
    s = nodo( hostname = 'localhost', port = 5000)
    s.iniciar_conexion()
    s.aceptar_conexion()