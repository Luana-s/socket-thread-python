import threading
import socket
from dicionario import login,respostas
import socket

# agora você pode utilizar o cliente para fazer a conexão e enviar/receber dados

messages = []

clients = []


def conexao():
     #iniciando o servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(1)

    print("Servidor iniciado")

    while True:

        cliente, address = server.accept()
        cliente.settimeout(10)
        username = cliente.recv(1024).decode()
        password = cliente.recv(1024).decode()
       
        #Autenticar login
        if username in login and login[username] == password:

            cliente.send(f"\033[1;36m{username} sua autenticação foi bem-sucedida  em {address}\033[m\n".encode())
            print(f"Conexão estabelecida com {username} em {address}")
            
            print("\n")
            cliente.send(f'\nDigite sua mensagem para se comunicar com outras pessoas:'.encode())

            res= respostas["200"]
            print(res)
            clients.append(cliente)
            

             #    
            thread = threading.Thread(target=messagesTreatment, args=[cliente])
            thread.start()



        else:
            cliente.send("Unauthorized, " " Forneça credenciais válidas, ou você pode está bloqueado".encode())
            print(f"Tentativa de conexão falhou em {address}")
            res= respostas["401"]
            cliente.close()



 # código para desconectar o usuário ou impedir que ele envie mensagens         
def bloquearUsuario(usuario):
    login[usuario] = True

def usuarioBloqueado(usuario): 
    res= respostas["403"]
    print(res)
    return usuario in login and login[usuario]

#recebe as mensagens do cliente e transmite 
def messagesTreatment(cliente):
    while True:
        try:
            msg = cliente.recv(2048)
            broadcast(msg, cliente)
        except:
            deleteClient(cliente)
            break
        
#envia a mesagem para todos os clientes
def broadcast(msg, cliente):
    for clientItem in clients:
        if clientItem != cliente:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(cliente):
    clients.remove(cliente)

bloquearUsuario("Jose")
conexao()