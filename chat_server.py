
# chat_server.py
# Simple socket-based chat server (Python 3.8)
import socket
import threading

HOST = "0.0.0.0"   # bind to all interfaces (change to 127.0.0.1 for local-only)
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server listening on {HOST}:{PORT}")

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                break
            broadcast(msg)
        except:
            break
    if client in clients:
        idx = clients.index(client)
        nick = nicknames[idx]
        clients.remove(client)
        nicknames.remove(nick)
        client.close()
        broadcast(f"*** {nick} left the chat ***".encode())

def receive():
    while True:
        client, addr = server.accept()
        print("Connected:", addr)
        client.send("NICK".encode())
        nick = client.recv(1024).decode().strip()
        nicknames.append(nick)
        clients.append(client)
        print(f"Nickname: {nick}")
        broadcast(f"*** {nick} joined the chat ***".encode())
        thread = threading.Thread(target=handle, args=(client,), daemon=True)
        thread.start()

if __name__ == "__main__":
    receive()
