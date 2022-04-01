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
            #Se recibe el dato con la operacion del cliente, aparte en enviarlo al metodo de 
            #organizar datos para procesar y deseempaquetar la informacion
            msg = ''
            try:
                while self.connected:
                    # Recibir datos del cliente.
                    msg = self.connection.recv(1024)   
                    msg = pickle.loads(msg)         
                    msg = msg.decode() 
                    if msg: 
                        print("Envio efectivo")
                        #self.connection.sendall(b'Se han recibido los datos')
                        self.organizar_datos(msg)
                        
                        # Cerrar conexión
                        self.sock.close()
                        
                        #Borrar objetos o variables
                        self.sock = None
                        self.connection = None
                        self.addre = None
                    else:
                        break
                    break
                    
            except Exception:
                self.connected = False

    def organizar_datos(self, msg):
        #Se organiza la informacion
        
        
        if(self.msg[0] == '1'):
            self.crear()
        elif(self.msg[0] == '2'):
            self.leer()
        elif(self.msg[0] == '3'):
            self.actualizar()
        elif(self.msg[0] == '4'):
            self.eliminar()
            
    def crear(self):
        print(self.msg)
    
    def leer(self):
        pass
    
    def actualizar(self):
        pass
    
    def eliminar(self):
        pass
        
    
if __name__ == "__main__":
    # Probar conexion entre cliente y socket  
    s = nodo( hostname = 'localhost', port = 5000)
    s.iniciar_conexion()
    s.aceptar_conexion()