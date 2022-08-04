'Chat Room Connection - Client-To-Client'
import threading
import socket
host = '127.0.0.1'
port = 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
names = []
def broadcast(message):
    for client in clients:
        client.send(message)
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            names.remove(name)
            break
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('name?'.encode('utf-8'))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        print(f'The name of this client is {name}'.encode('utf-8'))
        broadcast(f'{name} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
