import socket, threading

HEADER = 64
HOST = "192.168.1.45"
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

connections = []

def handle_client(conn, addr):
    print(f"\nNew Connection {addr}")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                conn.close()
                break
            else:    
                for connection in connections:
                    connection.send(msg.encode(FORMAT))

            

while True:
    print(f"Ip: {server}")
    conn, addr = server.accept()
    thread = threading.Thread(target = handle_client, args = (conn, addr))
    thread.start()
    connections.append(conn)
    print(f"Active connections: {threading.activeCount() - 1}")