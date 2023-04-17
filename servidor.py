import threading
import socket
from dicionario import login,respostas
import socket


messages = []

clients = []
autenticados = {}

def conexao():
     #iniciando o servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
     #servidor so aceita 1 conexao por vez
    server.listen(1)

    print("Servidor iniciado")
    while True:
        cliente, address = server.accept()
        #cliente.settimeout(10)
        username = cliente.recv(1024).decode()
        password = cliente.recv(1024).decode()
        
        # Verifica se o usuário já está autenticado
        if username in autenticados:
            cliente.send("\033[1;31mVocê já fez login em outra sessão.\033[m\n".encode())
            
            continue

    #Autenticar login
        if username in login and login[username] == password:
            autenticados[username] = password
            cliente.send(f"\033[1;36m{username} sua autenticação foi bem-sucedida em {address}\033[m\n".encode())
            print(f"Conexão estabelecida com {username} em {address}")
        else:
            print(f"Tentativa de conexão falhou em {address}")
            cliente.send("\033[1;31mUnauthorized, " " Forneça credenciais válidas, ou você pode está bloqueado.\033[m\n".encode())
            
            
        # adiciona o cliente à lista de clientes conectados
        clients.append(cliente)

        # cria uma nova thread para tratar as mensagens do cliente
        thread = threading.Thread(target=messagesTreatment, args=(cliente,))
        thread.start()


    

    

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