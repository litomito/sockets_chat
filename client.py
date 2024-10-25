import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

# Create a socket object and bind it to the host and port
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_sock:

    # Get the name of the user
    name = input("Enter your name: ")

    # Send the name and message to the server
    def send_data():
        while True:
            text = input("Enter your message: ")
            msg = f"{name}: {text}"
            client_sock.sendto(msg.encode('utf-8'), (HOST, PORT))

    # Receive the message from the server and print it
    def receive_data():
        while True:
            data, addr = client_sock.recvfrom(4096)
            message = data.decode('utf-8')
            # Clear the current line and print the message on the same line
            sys.stdout.write('\r' + ' ' * 100 + '\r')
            print(message)
            # Print the prompt for the user to enter a message again
            sys.stdout.write("Enter your message: ")
            sys.stdout.flush()
    
    # Start the send and receive threads
    send_thread = threading.Thread(target=send_data)
    send_thread.start()

    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

    # Wait for the threads to finish
    send_thread.join()
    receive_thread.join()