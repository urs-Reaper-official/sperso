# chat_client.py
# Simple socket-based chat client (Python 3.8)
import socket
import threading
import sys

SERVER_HOST = input("Server host (default 127.0.0.1): ").strip() or "127.0.0.1"
SERVER_PORT = 5000
nickname = input("Choose a nickname: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

def receive():
    while True:
        try:
            message = client.recv(4096).decode()
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Connection closed.")
            client.close()
            break

def write():
    while True:
        try:
            text = input()
            if text.lower() == "/quit":
                client.close()
                sys.exit(0)
            client.send(f"{nickname}: {text}".encode())
        except:
            break

if __name__ == "__main__":
    threading.Thread(target=receive, daemon=True).start()
    write()

