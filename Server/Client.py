import socket
from threading import Thread


def main():
    while True:

        # see if the server requires input or output
        str_recv = s.recv(1024)

        # 11 for input 00 for output

        if str_recv.decode('utf-8') == '11':
            input_data()

        elif str_recv.decode('utf-8') == '00':
            output_data()

        elif str_recv.decode('utf-8') == '01':
            input_login()

        elif str_recv.decode('utf-8') == '111':
            entrar_sala()


def input_login():
    
    # in this case, client wil receive messa and display it, then will send two string, login and pass
    str_recv = s.recv(4096)
    print(str_recv.decode('utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))


def input_data():
    str_recv = s.recv(16384)
    print(str_recv.decode('utf-8'))

    str_send = input()
    s.send(bytes(str_send, 'utf-8'))


def output_data():
    str_recv = s.recv(16384)
    print(str_recv.decode('utf-8'))


def tenviafunc():
    while True:
        str_send = input()
        
        #command Exit Chat will exit chat

        if "Exit Chat" in str_send:
            break
            
        # the command Send will send archive in the addr after send command, like Send:C/stuff.pdf
        if "Send :" in str_send:
            path = str_send[6:]
            filer = open(path)
            msg = filer.read()
            s.sendall(bytes("Send :"+msg, 'utf-8'))

        else:
            s.send(bytes(str_send, 'utf-8'))
    main()

def trecebefunc():
    while True:
        str_recv = s.recv(1024).decode('utf-8')

        if "Send :" in str_recv:
            with open("Received.txt","w") as filew:
                filew.write(str_recv[6:])

        else:
            print(str_recv)

# when we enter an room, we will create two threads, one will be showing us the messages we receive, the other will be sending our messages
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

# 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this must be the ip of the machine you are using, the port can be any free
s.connect(('192.168.15.181', 3333))

str_recv = s.recv(1024)
print(str_recv.decode('utf-8'))

main()
