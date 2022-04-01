import multiprocessing
import socket, struct, pickle

from django.db import connection
from tabla_valor import *

class nodo():
    
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
    
    def recibir_datos(self):
        #Se recibe el dato con la operacion del cliente, aparte en enviarlo al metodo de 
        #organizar datos para procesar y deseempaquetar la informacion
        datos = ''
        try:
            while self.connected:
                # Recibir datos del cliente.
                msg = self.connection.recv(1024)   
                msg = pickle.loads(msg)         
                msg = msg.decode('utf-8') 
                if msg: 
                    print("Envio efectivo")
                    #self.connection.sendall(b'Se han recibido los datos')
                    self.organizar_datos(msg)
                else:
                    break
                break
            
        except Exception:
            self.connected = False

    def organizar_datos(self, msg):
        #Se deseempaqueta el dato y se organiza la informacion
        self.msg = pickle.loads(msg)
        self.msg = self.msg.split('/')
        if(self.msg[0] == '1'):
            self.crear()
        elif(self.msg[0] == '2'):
            self.leer()
        elif(self.msg[0] == '3'):
            self.actualizar()
        elif(self.msg[0] == '4'):
            self.eliminar()
        else:
            print('Operacion incorrecta')
            
    def crear(self):
        pass
    
    def leer(self):
        pass
    
    def actualizar(self):
        pass
    
    def eliminar(self):
        pass
        
    def cerrar_con(self):
        # Cerrar conexión
        self.sock.close()
    
if __name__ == "__main__":
    # Probar conexion entre cliente y socket  
    s = nodo( hostname = 'localhost', port = 5050)
    s.iniciar_conexion()
    s.aceptar_conexion()

    for proceso in multiprocessing.active_children():
        print('Terminando proceso %r', proceso)
        proceso.terminate()
        proceso.join()
    print('Listo')