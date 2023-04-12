import threading
import socket
import json
from dicionario import login, respostas

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 8000))

    # Envia o nome de usuário e senha para autenticação
    username = input("Nome de usuário: ")
    password = input("Senha: ")
    cliente.send(username.encode())
    cliente.send(password.encode())

    #utilizando a biblioteca de thereads
    thread1 = threading.Thread(target=receberMensagens, args=[cliente])
    thread2 = threading.Thread(target=enviarMensagens, args=[cliente, username])
    #inicia a thread
    thread1.start()
    thread2.start()



#envia mensagens 
def enviarMensagens(cliente, username):
    mensagens = []
    while True:
        opcao = input('Digite "e" para enviar uma mensagem, ou "s" para sair: ')
        if opcao == 'e':
            # enviar mensagem
            entrada = input('Digite um id e uma mensagem em formato JSON (ex: {"id": 1, "msg": "Hello world!"}): ')
            try:
                obj = json.loads(entrada)
            except json.JSONDecodeError:
                print('A entrada deve ser um objeto JSON válido!')
                print('400 - solicitacao invalida')
 
                continue
            nome = obj.get('id')
            msg = obj.get('msg')
            if nome is None or msg is None:
                print('A entrada deve conter os campos "id" e "msg"!')
                continue
            print(f'Mensagem enviada: {msg}')
            print('\n')
            print("200- Requisição bem sucedida")
            cliente.send(f'<{username}> {msg}'.encode('utf-8'))
            
            mensagens.append(msg)
        
        elif opcao == 's':
            # sair
            break
        
        else:
            # opção inválida
            print('Opção inválida!')

            
#recebe as mensagens enviadas dos clientes
def receberMensagens(cliente):
    while True:
        try:
            msg = cliente.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            cliente.close()
            break




main()