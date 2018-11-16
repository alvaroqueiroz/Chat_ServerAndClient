import socket
import csv
from threading import Thread
import datetime


def entra_sala_publica(addr, connect):
    global clientscon
    global clientsaddr

    # pede input ao cliente
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Qual o seu nome?"

    connect.sendto(bytes(str_return, 'utf-8'), addr)

    salapublica.append([addr, connect])

    nomeuser, temp = connect.recvfrom(1024)

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow(
            [now.strftime("%Y-%m-%d %H:%M") + " :Ausuário entrou na sala pública :" + nomeuser.decode('utf-8')])

    # pede input ao cliente
    str_return = '111'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    while True:

        msg, temp = connect.recvfrom(16384)
        brodcastmsg = str(nomeuser.decode('utf-8')) + ' :' + msg.decode('utf-8')

        if "Exit Chat" in brodcastmsg:
            break

        if "Send :" in brodcastmsg:
            for i in range(len(salapublica)):
                salapublica[i][1].sendto(bytes(msg.decode('utf-8'), 'utf-8'), salapublica[i][0])
        else:
            for i in range(len(salapublica)):
                salapublica[i][1].sendto(bytes(brodcastmsg, 'utf-8'), salapublica[i][0])

    mainmenu(addr, connect)


def entra_sala(addr, connect, user):
    global clientscon
    global clientsaddr

    # pede input ao cliente
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome da sala em que deseja entrar"

    connect.sendto(bytes(str_return, 'utf-8'), addr)

    nomesala, temp = connect.recvfrom(1024)

    salaindex = salas.index(nomesala.decode('utf-8'))

    salas[salaindex] = []

    salas[salaindex].append([connect, addr, user])

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow(
            [now.strftime("%Y-%m-%d %H:%M") + " :Ausuário entrou na sala " + nomesala.decode('utf-8') + " : " + user])

    # pede input ao cliente
    str_return = '111'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    while True:

        msg, temp = connect.recvfrom(16384)
        brodcastmsg = user + ' :' + msg.decode('utf-8')

        if "Exit Chat" in brodcastmsg:
            break

        if "Send :" in brodcastmsg:
            for i in range(len(salas[salaindex][0])):
                salas[salaindex][i][0].sendto(bytes(msg.decode('utf-8'), 'utf-8'), salas[salaindex][i][0])
        else:
            for i in range(len(salas[salaindex][0])):
                salas[salaindex][i][0].sendto(bytes(brodcastmsg, 'utf-8'), salas[salaindex][i][1])
    mainmenu(addr, connect)


def exclui_sala(addr, connect):
    # pede input ao cliente
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome da sala a ser excluida"

    connect.sendto(bytes(str_return, 'utf-8'), addr)

    nomesaladel, temp = connect.recvfrom(1024)

    salaindex = salas.index(nomesaladel.decode('utf-8'))
    del salas[salaindex]

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow([now.strftime("%Y-%m-%d %H:%M") + " : Sala Excluida :" + nomesaladel.decode('utf-8')])

    mainmenu(addr, connect)


def lista_salas(addr, connect):
    # avisa output ao cliente
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    # envia output ao cliente

    salasresp = ''
    for i in range(len(salas)):
        salasresp = salasresp + salas[i] + ', possui : ' + str(len(salas[i][0])) + '  usuarios \n'

    str_return = ('Salas abertas :' + salasresp + '\n programa encerrado')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    mainmenu(addr, connect)


def cria_sala(addr, connect):
    # pede input ao cliente
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome desejado para a nova sala"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    nomesala, temp = connect.recvfrom(1024)

    salas.append(nomesala.decode('utf-8'))

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow([now.strftime("%Y-%m-%d %H:%M") + " : Sala Criada :" + nomesala.decode('utf-8')])

    mainmenu(addr, connect)


def registrar_usuario(addr, connect):
    # pede input ao cliente
    str_return = '01'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome do usuario e senha"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    # receber nome e senha do usuario
    nomeusuario, temp = connect.recvfrom(1024)
    senhausuario, temp = connect.recvfrom(1024)

    # abrir arquivo csv que contem todos as credenciais

    with open('usuarios.csv', 'a') as usuarios:
        writer = csv.writer(usuarios)
        writer.writerow([nomeusuario.decode('utf-8'), senhausuario.decode('utf-8'), addr])

    UsersList.append([nomeusuario, senhausuario, addr, 'sala0'])

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow([now.strftime("%Y-%m-%d %H:%M") + " : Usuario Registrado :" + nomeusuario.decode('utf-8')])

    mainmenu(addr, connect)


def usuario_entrar(addr, connect):
    global user
    # pede input ao cliente
    str_return = '01'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome do seu usuario e senha"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    # receber nome e senha do usuario
    nomeusuario, temp = connect.recvfrom(1024)
    senhausuario, temp = connect.recvfrom(1024)

    # avisa output ao cliente
    str_return = '00'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    pos = 0

    for i in range(len(UsersList)):
        if UsersList[i][0] == nomeusuario:
            pos = i
            break

    if UsersList[pos][1] == senhausuario:

        str_return = ('Bem vindo ' + (nomeusuario.decode('utf-8')))
        connect.sendto(bytes(str_return, 'utf-8'), addr)

    else:
        str_return = 'Senha incorreta, programa encerrado'
        connect.sendto(bytes(str_return, 'utf-8'), addr)

    now = datetime.datetime.now()
    with open('log.csv', 'a') as log:
        writerlog = csv.writer(log)
        writerlog.writerow([now.strftime("%Y-%m-%d %H:%M") + " : Login de usuario :" + nomeusuario.decode('utf-8')])

    user = nomeusuario.decode('utf-8')
    return user
    '''

    # verificar credenciais

    with open('usuarios.csv', 'r') as usuarios:
        reader = csv.reader(usuarios, delimiter=',', quotechar='"')
        # estruturas de dados para guardar os dados
        users = []
        usersenhas = []
        userips = []

        for row in reader:
            users.append(row[0])
            usersenhas.append(row[1])
            userips.append(row[2])

        userindex = users.index(nomeusuario.decode('utf-8'))

        if senhausuario.decode('utf-8') == usersenhas[userindex]:
            str_return = ('Bem vindo ' + (nomeusuario.decode('utf-8')))
            connect.sendto(bytes(str_return, 'utf-8'), addr)

            userips[userindex] = addr

            writer = csv.writer(open('usuarios.csv', 'w'))
            for i in range(len(users)):
                writer.writerow([users[i], usersenhas[i], userips[i]])

        else:
            str_return = 'Senha incorreta, programa encerrado'
            connect.sendto(bytes(str_return, 'utf-8'), addr)
            
            '''


def main():
    global clientscon
    global clientsaddr
    global UsersList
    global salas
    global salapublica

    trds = []
    clientscon = []
    clientsaddr = []
    UsersList = []
    salapublica = []

    for i in range(5):
        connect, addr = s.accept()
        print("Conexão recebida :" + str(addr))

        now = datetime.datetime.now()

        with open('log.csv', 'a') as log:
            writerlog = csv.writer(log)
            writerlog.writerow([now.strftime("%Y-%m-%d %H:%M") + " :Conexão recebida :" + str(addr)])

        str_return = "Bem vindo a esta porra de chat"
        connect.sendto(bytes(str_return, 'utf-8'), addr)
        clientscon.append(connect)
        clientsaddr.append(addr)
        t = Thread(target=mainmenu, args=(addr, connect))
        trds.append(t)
        t.start()

    for t in trds:
        t.join()
    connect.close()


def mainmenu(addr, connect):
    # pede input ao cliente
    global user
    str_return = '11'
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Menu de opcoes :\n 1 - Registrar\n 2 - Entrar\n 3 - Criar sala de bate papo\n 4 - Listar salas " \
                 "abertas\n 5 - Excluir sala\n 6 - Entrar em sala\n 7 - Entrar em sala publica "
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_recv, temp = connect.recvfrom(1024)
    str_recv = str_recv.decode('utf-8')

    if str_recv == '1':
        registrar_usuario(addr, connect)

    if str_recv == '2':
        user = usuario_entrar(addr, connect)
        mainmenu(addr, connect)

    if str_recv == '3':
        cria_sala(addr, connect)

    if str_recv == '4':
        lista_salas(addr, connect)

    if str_recv == '5':
        exclui_sala(addr, connect)

    if str_recv == '6':
        entra_sala(addr, connect, user)

    if str_recv == '7':
        entra_sala_publica(addr, connect)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.15.181', 3333))
s.listen(5)
salas = []
main()
