import random
import socket, multiprocessing, struct, pickle
from tabla_llave import *

class Balanceador_de_carga():
    
    global nServidores
    nServidores = 0
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.arr = []
        self.msg = ''
        self.connected = True
        
    def iniciar_escucha(self):
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
            
    def iniciar_conexion_nodo(self):
        # Iniciar servicio
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.hostname, self.port))
        except Exception as e:
            print(e)
    
    def recibir_datos(self):
        #Se recibe el dato con la operacion del cliente, aparte en enviarlo al metodo de 
        #organizar datos para procesar y deseempaquetar la informacion
        datos = ''
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
                else:
                    break
                break

        except Exception:
            self.connected = False


    def organizar_datos(self, msg):
        #Se deseempaqueta el dato y se organiza la informacion
        self.msg = msg.split('/')
        print(self.msg)
        if(self.msg[0] == '1'):
            self.crear()
        elif(self.msg[0] == '2'):
            self.leer()
        elif(self.msg[0] == '3'):
            self.actualizar()
        elif(self.msg[0] == '4'):
            self.eliminar()
    
    def enviar(self, msg):
        msg = pickle.dumps(msg)
        self.sock.send(msg)

    def crear(self):
        #Iniciar proceso de crear registro en la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        print(self.msg)
        servidor = random.randrange(nServidores)
        aux = [self.msg[1],servidor] 
    
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.crear_llave(aux)
        llave.guardar_llaves()
        
        return respuesta

    def leer(self):
        #Iniciar proceso de recuperar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para entregar la llave y el valor al cliente
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.msg[1])
        llave = None
        
    def actualizar(self):
        #Iniciar proceso de actulizar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para actualizar el valor en el servidor
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.msg[1])
        llave = None
        
    def eliminar(self):
        #Iniciar proceso de eliminar un registro de la tabla de llaves y servidores, ademas de iniciar el proceso con el servidor
        #para eliminar la llave y el valor en el servidor
        llave = Tabla_llaves()
        llave.inicializar_tabla()
        respuesta = llave.ver_llave(self.msg[1])
        respuesta = llave.eliminar_llave(respuesta)
        llave.guardar_llaves()
        llave = None
        
        return respuesta 
        
    def cerrar_con(self):
        # Cerrar conexión
        self.sock.close()
    
if __name__ == "__main__":
 # Probar conexion entre cliente y socket  
    s = Balanceador_de_carga( hostname = 'localhost', port = 5050)
    s.iniciar_conexion_nodo()
    s.enviar(b'1/2/odio la vida')
    #s.iniciar_escucha()
'''
    s.aceptar_conexion()
    for proceso in multiprocessing.active_children():
        print('Terminando proceso %r', proceso)
        proceso.terminate()
        proceso.join()
    print('Listo')
'''     
