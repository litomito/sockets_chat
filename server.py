import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

# Create an empty list to store the clients
clients = []

# Create a socket object and bind it to the host and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1) # Set the timeout to 1 second
print(f'Listening on {HOST}:{PORT}')

# Receive data from the clients and return the data and the address
def get_data():
    data, addr = sock.recvfrom(4096)
    return data, addr
    
# Add a client to the list of clients if it is not already in the list
def add_client(addr):
    if addr not in clients:
        clients.append(addr)
        print(f"New client connected: {addr}")

# Send the data to all the clients except the sender of the data
def send_data(data, sender_addr):
    for client in clients:
        if client != sender_addr:
            sock.sendto(data, client)

# Handle the client connections and messages received from the clients
def handle_client():
    while True:
        try:
            data, addr = get_data()
            add_client(addr)
            send_data(data, addr)
            print(f"Received message from {addr}: {data.decode('utf-8')}")
        except socket.timeout:
            continue
    
# Start the thread to handle the client connections and messages
thread = threading.Thread(target=handle_client)
thread.start()

# Wait for the thread to finish
try:
    thread.join() 
except KeyboardInterrupt: 
    # Handle the KeyboardInterrupt exception when the user presses Ctrl+C to stop the server
    print("\nServer is shutting down.")
finally:
    sock.close() 