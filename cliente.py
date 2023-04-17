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

def enviarMensagens(cliente, username):
    #armazena as mensagens
    mensagens_enviadas=[]
    
    while True:
        print('\n\n\n\n')
        opcao = input('Digite "e" para enviar uma mensagem, ou "s" para sair: ')
        if opcao == 'e':
            
            print('\n')
            # enviar mensagem em formato Json
            entrada = input('Digite um id e uma mensagem em formato JSON (ex: {"id": 1, "msg": "Hello world!"}): ')
            try:
                obj = json.loads(entrada)
            except json.JSONDecodeError:
                print('A entrada deve ser um objeto JSON válido!')
                print('400 - Solicitação inválida')
                continue
            
            id = obj.get('id')
            
            #verifica se o id nao é vazio
            if id is None:
                print('A entrada deve conter o campo "id"!')
                continue
            # verrifica se o id ja foi utilizado
            if id in mensagens_enviadas:
                print('\n')
                print('O ID já foi usado em uma mensagem anterior!')
                print('400 - Solicitação inválida')
                continue
            
            msg = obj.get('msg')
            if msg is None:
                print('A entrada deve conter o campo "msg"!')
                continue
            #retorna a mensagem enviada e o usuário que enviou
            print(f'Mensagem enviada: {msg}')
            print('\n')
            print("200- Requisição bem sucedida")
            cliente.send(f'\033[1;36m<{username}> {msg}\033[m\n'.encode('utf-8'))
            
            mensagens_enviadas.append(id)
            
        
        elif opcao == 's':
            # sair
            break
        
        else:
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