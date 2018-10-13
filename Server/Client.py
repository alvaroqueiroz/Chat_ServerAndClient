import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("localhost", 3333))



str_recv = s.recv(1024)
print(str_recv.decode('utf-8'))

str_send = input()
s.send(bytes(str_send, 'utf-8'))


str_recv = s.recv(1024)
print((str_recv).decode('utf-8'))

str_send = input()
s.send(bytes(str_send, 'utf-8'))

#str_send = input()
#s.send(bytes(str_send, 'utf-8'))

str_recv = s.recv(1024)
print((str_recv).decode('utf-8'))

str_recv = s.recv(1024)
print((str_recv).decode('utf-8'))

str_recv = s.recv(1024)
print((str_recv).decode('utf-8'))

s.close()