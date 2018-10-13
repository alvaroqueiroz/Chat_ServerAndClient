import socket
import csv

def registrar(addr):

    str_return = "Digite o nome do usuario e senha"
    connect.sendto(bytes(str_return, 'utf-8'), addr)
    
    #receber nome e senha do usuario
    nomeusuario, temp = connect.recvfrom(1024)
    senhausuario, temp = connect.recvfrom(1024)

    #abrir arquivo csv que contem todos as credenciais

    with open('usuarios.csv','a') as usuarios:
        thewriter = csv.writer(usuarios)
        thewriter.writerow([nomeusuario.decode('utf-8'),senhausuario.decode('utf-8'),addr])

    #guardar usuario e senha em csv

def entrar(addr):

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





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 3333))
s.listen(5)


while True:
    connect, addr = s.accept()
    print("Conexão recebida :" + str(addr))

    str_return = "Bem vindo ao chat, escolha a opcao desejada:\n 1 - Registrar\n 2 - Entrar\n 3 - entrar em sala"
    connect.sendto(bytes(str_return, 'utf-8'), addr)

    str_recv, temp = connect.recvfrom(1024)
    str_recv = str_recv.decode('utf-8')

    if(str_recv == '1'):
        registrar(addr)

    if(str_recv == '2'):
        entrar(addr)


    #str_recv, temp = connect.recvfrom(1024)
    #print(str_recv)

    #str_return = "I got your command, it is " + str(str_recv)
    #connect.sendto(bytes(str_return, 'utf-8'), addr)

    connect.close()

