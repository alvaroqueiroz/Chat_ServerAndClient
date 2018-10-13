import socket
import csv

def lista_salas(addr,connect):

    #avisa output ao cliente
    str_return = ('11')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    #envia output ao cliente
    
    salasresp = (','.join(salas)+'\n') 
    str_return = ('Salas abertas :'+salasresp)
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    mainmenu(addr,connect)


def cria_sala(addr,connect):

    #pede input ao cliente
    str_return = ('11')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome desejado para a nova sala"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    nomesala, temp = connect.recvfrom(1024)

    salas.append(nomesala.decode('utf-8'))

    mainmenu(addr,connect)



def registrar_usuario(addr,connect):

    #pede input ao cliente
    str_return = ('01')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome do usuario e senha"
    connect.sendto(bytes(str_return, 'utf-8'), addr)
    
    #receber nome e senha do usuario
    nomeusuario, temp = connect.recvfrom(1024)
    senhausuario, temp = connect.recvfrom(1024)

    #abrir arquivo csv que contem todos as credenciais


    writer = csv.writer(open('usuarios.csv', 'a'))
    writer.writerow([nomeusuario.decode('utf-8'),senhausuario.decode('utf-8'),addr])
    mainmenu(addr,connect)

def usuario_entrar(addr,connect):

    #pede input ao cliente
    str_return = ('01')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Digite o nome do seu usuario e senha"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    #receber nome e senha do usuario
    nomeusuario, temp = connect.recvfrom(1024)
    senhausuario, temp = connect.recvfrom(1024)

    #verificar credenciais

    with open('usuarios.csv') as usuarios:
        reader = csv.reader(usuarios, delimiter=',',quotechar='"')
    # estruturas de dados para guardar os dados
        users = []
        usersenhas = []
        userips = []

        for row in reader:
            user = row[0]
            usersenha = row[1]
            userip = row[2]

            users.append(user)
            usersenhas.append(usersenha)
            userips.append(userip)

        userindex = users.index(nomeusuario.decode('utf-8'))

        if senhausuario.decode('utf-8') == usersenhas[userindex]:
            str_return = ('Bem vindo '+(nomeusuario.decode('utf-8')))
            connect.sendto(bytes(str_return, 'utf-8'), addr)

            userips[userindex] = addr

            writer = csv.writer(open('usuarios.csv', 'w'))
            for i in range(len(users)):
                writer.writerow([users[i],usersenhas[i],userips[i]])
                
        else:
            str_return = ('Senha incorreta, programa encerrado')
            connect.sendto(bytes(str_return, 'utf-8'), addr)
    mainmenu(addr,connect)

def main():
    while True:

        connect, addr = s.accept()
        print("Conexão recebida :" + str(addr))

        mainmenu(addr,connect)

        connect.close()

def mainmenu(addr,connect):

    #pede input ao cliente
    str_return = ('11')
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_return = "Bem vindo ao chat, escolha a opcao desejada:\n 1 - Registrar\n 2 - Entrar\n 3 - Criar sala de bate papo\n 4 - Listar salas abertas\n"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_recv, temp = connect.recvfrom(1024)
    str_recv = str_recv.decode('utf-8')

    if(str_recv == '1'):
        registrar_usuario(addr,connect)

    if(str_recv == '2'):
        usuario_entrar(addr,connect)

    if(str_recv == '3'):
        cria_sala(addr,connect)

    if(str_recv == '4'):
        lista_salas(addr,connect)




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 3333))
s.listen(5)
salas = []
main()

