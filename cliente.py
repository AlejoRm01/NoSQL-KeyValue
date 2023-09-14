import socket, pickle, struct, os, base64

class Cliente():
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port 
        self.msg = {}
     
    def iniciar_conexion(self):
        # Iniciar servicio
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.hostname, self.port))
        except Exception as e:
            print(e)
    
    def leer_archivo(self, path):
        # Abrir archivo, leerlo y retornarlo
        file = open(path, 'rb')
        archivo = file.read()
        file.close()

        return archivo
    
    
    def crear(self, path):
        # Crear un registro nuevo en la base de datos usando el nombre del archivo como llave
        if os.path.exists(path):
            filename = os.path.basename(path)
            with open(path, 'rb') as file:
                image_data = file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            self.msg['operacion'] = '1'
            self.msg['llave'] = filename  # Usar el nombre del archivo como llave
            self.msg['valor'] = encoded_image

            self.enviar(self.msg)
        else:
            print("El archivo no existe.")

    def leer(self, llave):
        #Leer registro de la base de datos
        self.msg['operacion'] = '2'
        self.msg['llave'] = llave

        self.enviar(self.msg)
        msg = self.recibir_datos()
        msg = pickle.loads(msg)
        print(msg)
        
    def actualizar(self, llave, valor):
        #Actualizar registro de la base dec datos
        #valor = self.leer_archivo(path)

        self.msg['operacion'] = '3'
        self.msg['llave'] = llave
        self.msg['valor'] = valor

        self.enviar(self.msg)

    def eliminar(self, llave):
        #Eliminar registro de la base de datos<
        self.msg['operacion'] = '4'
        self.msg['llave'] = llave

        self.enviar(self.msg)

    def enviar(self, msg):   
        #Almacenar str en un contenedor dumps y enviar este al servidor
        msg = pickle.dumps(msg)
        length = len(msg)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(msg)
           
    def recibir_datos(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.hostname, 4999))
        sock.listen(1)
        conn, addr = sock.accept()
        print('Leyendo datos de: ', addr)
        while True:
            # Recibir datos del nodo.
            lengthbuf = self.recvall(conn, 4)
            length, = struct.unpack('!I', lengthbuf)
            msg = self.recvall(conn, length)                 
            return msg

    def recvall (self, sock, count): 
        buf = b'' 
        while count: 
            newbuf = sock.recv (count) 
            if not  newbuf: return None 
            buf += newbuf 
            count -= len (newbuf) 
        return buf  


if __name__ == "__main__":
    c = Cliente(hostname='localhost', port=5050)
    c.iniciar_conexion()
    
    while True:
        print("\nSeleccione una acción:")
        print("1. Crear dato desde archivo")
        print("2. Leer dato")
        print("3. Actualizar dato")
        print("4. Eliminar dato")
        print("5. Salir")
        
        opcion = input("Ingrese el número de la acción que desea realizar: ")
        
        if opcion == '1':
            path = input("Ingrese la ruta del archivo que desea almacenar: ")
            c.crear(path)
        elif opcion == '2':
            llave = input("Ingrese la llave del dato que desea leer: ")
            c.leer(llave)
        elif opcion == '3':
            llave = input("Ingrese la llave del dato que desea actualizar: ")
            valor = input("Ingrese el nuevo valor del dato: ")
            c.actualizar(llave, valor)
        elif opcion == '4':
            llave = input("Ingrese la llave del dato que desea eliminar: ")
            c.eliminar(llave)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
    
    c.sock.close()