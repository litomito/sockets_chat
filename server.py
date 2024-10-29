import socket

HOST = '127.0.0.1'
PORT = 65432

# Dictionary to store clients and their status (True if they have sent a message, False otherwise)
clients = {}

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1) 
print(f'Listening on {HOST}:{PORT}')

# Function to receive data from the socket
def get_data():
    data, addr = sock.recvfrom(4096)
    return data, addr

# Function to add a client to the clients dictionary
def add_client(addr):
    if addr not in clients:
        clients[addr] = False 
        print(f"New client connected: {addr}")

# Function to send data to all clients except the sender
def send_data(data, sender_addr):
    for client in clients:
        if client != sender_addr:
            sock.sendto(data, client)

# Function to handle the client connections and messages
def handle_client():
    while True:
        try:
            data, addr = get_data()
            add_client(addr)
            if not clients[addr]:
                clients[addr] = True
                print(f"Received first message from {addr} (not broadcasting): {data.decode('utf-8')}")
            else:
                send_data(data, addr)
                print(f"Received message from {addr}: {data.decode('utf-8')}")
        except socket.timeout:
            continue

# Main function to run the server
def main():
    try:
        handle_client()
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        sock.close()

# Run only the main function if this script is executed
if __name__ == '__main__':
    main()