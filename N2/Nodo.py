import base64
import multiprocessing
import socket, struct, pickle
from TablaValores import tabla_valores
import argparse

class nodo():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.connected = True
        self.msg = {}
        self.port_balanceador = 5050

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

        contenido = base64.b64encode(msg['parte_contenido']).decode('utf-8')

        aux = {
            msg['llave']: {
                'parte_numero': msg['parte_numero'],
                'valor': contenido
                }
            }
        
        t = tabla_valores()
        t.inicializar_tabla()
        t.crear_llave(aux)
        t.guardar_llaves()
        
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
        
    def leer(self, msg):
        t = tabla_valores()
        t.inicializar_tabla()
        llave = msg['llave']

        contenido = t.buscar_por_llave(llave)      
        contenido["valor"] = base64.b64decode(contenido["valor"].encode('utf-8'))

        self.enviar(contenido)

    def enviar(self, msg):
        # Enviar datos al balanceador utilizando la conexión existente
        print('Enviando datos al balanceador')
        msg_serializado = pickle.dumps(msg)
        length = len(msg_serializado)

        try:
            self.connection.sendall(struct.pack('!I', length))
            self.connection.sendall(msg_serializado)
        except Exception as e:
            print(f"Error al enviar datos al balanceador: {e}")
            
    
if __name__ == "__main__":
    s = nodo( hostname = 'localhost', port = 2022)
    s.iniciar_conexion()
    s.aceptar_conexion()