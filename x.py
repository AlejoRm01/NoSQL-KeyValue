import os 

path = r'C:\Users\arodr\OneDrive\Escritorio\Hola.jpg'
dicc = {}

file = open(path, 'rb')
dicc['value'] = file.read()
file.read()
key = format(id(os.path.split(path)[1]))
dicc['key'] = key
file.close()

print(key)
print(dicc['key'])