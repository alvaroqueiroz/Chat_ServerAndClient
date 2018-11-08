import socket
from threading import Thread


def main():
    while True:

        # ve se o servidor quer input ou output
        str_recv = s.recv(1024)

        # 11 para input 00 para output do servidor

        if str_recv.decode('utf-8') == '11':
            input_data()

        elif str_recv.decode('utf-8') == '00':
            output_data()

        elif str_recv.decode('utf-8') == '01':
            input_login()

        elif str_recv.decode('utf-8') == '111':
            entrar_sala()


def input_login():
    str_recv = s.recv(1024)
    print(str_recv.decode('utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))


def input_data():
    str_recv = s.recv(1024)
    print(str_recv.decode('utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))


def output_data():
    str_recv = s.recv(1024)
    print(str_recv.decode('utf-8'))


def tenviafunc():
    while True:
        str_send = input()
        s.send(bytes(str_send, 'utf-8'))


def trecebefunc():
    while True:
        str_recv = s.recv(1024)
        print(str_recv.decode('utf-8'))


def entrar_sala():
    trds = []

    tenvia = Thread(target=tenviafunc)
    trds.append(tenvia)
    tenvia.start()

    trecebe = Thread(target=trecebefunc)
    trds.append(trecebe)
    trecebe.start()

    tenvia.join()
    trecebe.join()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.25.5', 3333))

str_recv = s.recv(1024)
print(str_recv.decode('utf-8'))

main()
