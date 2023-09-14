import multiprocessing
import random
import socket, pickle
import struct
from TablaNodos import tablaNodos
import argparse

class Balanceador():

    def __init__(self, hostname, puertos):
        self.puertos = puertos
        self.nNodos = int(len(self.puertos))
        self.hostname = hostname
        self.port = 5050
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

    def leer(self, msg):
        #Iniciar proceso de leer un registro de la tabla de llaves y nodos, ademas de iniciar el proceso con el nodo
        t = tablaNodos()
        t.inicializar_tabla()
        nodo = t.leer_llave(msg['llave'])
        self.enviar(msg, self.puertos[int(nodo)])
        
    def actualizar(self, msg):
        #Iniciar proceso de actualizar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para actualizar la llave y el valor en el servidor
        t = tablaNodos()
        t.inicializar_tabla()
        nodo = t.leer_llave(msg['llave'])
        self.enviar(msg, self.puertos[int(nodo)])

    def eliminar(self, msg):
        #Iniciar proceso de eliminar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para eliminar la llave y el valor en el servidor
        t = tablaNodos()
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

    def rearmar_archivo(self, llave):
        t = tablaNodos()
        particiones = t.obtener_partes(llave)
        archivo_rearmado = b""
        
        for parte_numero, nodo in particiones:
            parte_contenido = self.obtener_parte_archivo(llave, parte_numero, nodo)
            archivo_rearmado += parte_contenido
        
        return archivo_rearmado

    def crear(self, msg):
        # Iniciar proceso de crear registro en la tabla de llaves y servidores,
        # además de iniciar el proceso con el servidor
        nodo = 0
        if self.nNodos - 1 == 0:
            nodo = 0
        else:
            nodo = random.randrange(0, self.nNodos)

        # Particionar el archivo y guardar las particiones en la tabla de nodos
        archivo = msg['valor']
        llave = msg['llave']
        particiones = self.particionar_archivo(llave, archivo, nodo)
        
        aux = [(tupla[0], tupla[1]) for tupla in particiones]

        # Guardar las particiones en la tabla de nodos
        t = tablaNodos()
        t.inicializar_tabla()
        t.crear_llave(llave, aux)
        t.guardar_llaves()

        aux = [(tupla[-1]) for tupla in particiones]

        # Enviar mensaje a los nodos correspondientes
        self.enviar_particiones(msg, aux)

    def particionar_archivo(self, llave, archivo, nodo):
        # Particionar el archivo y guardar las particiones en la tabla de nodos
        tamano_particion = len(archivo) // self.nNodos
        particiones = []

        for i in range(self.nNodos):
            inicio = i * tamano_particion
            fin = (i + 1) * tamano_particion if i < self.nNodos - 1 else len(archivo)
            parte = archivo[inicio:fin]
            particiones.append((i, nodo, parte))  # Parte y nodo correspondiente

        return particiones

    def enviar_particiones(self, msg, particiones):
        # Enviar las particiones a los nodos correspondientes
        for i in range(len(particiones)):
            nuevo_msg = {
                'operacion': msg['operacion'],
                'llave': msg['llave'],
                'parte_numero': i,
                'parte_contenido': particiones[i]  # Enviar el contenido de la parte del archivo
            }
            self.enviar(nuevo_msg, self.puertos[i])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs="+", default=[2020], type=int)
    args = parser.parse_args()

    s = Balanceador(hostname='localhost', puertos=args.a)
    s.iniciar_conexion()
    s.aceptar_conexion()
