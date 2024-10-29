import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

# Function to send a message to the server to join the chat
def join_chat(sock):
    sock.sendto("joined".encode('utf-8'), (HOST, PORT))

# Function to get the name of the user
def get_name():
    return input("Enter your name: ")

# Function to send messages to the server
def send_data(sock):
    name = get_name()
    while True:
        text = input("Enter your message: ")
        if text == "":
            print("Message cannot be empty")
            continue
        msg = f"{name}: {text}"
        sock.sendto(msg.encode('utf-8'), (HOST, PORT))

# Function to receive other clients messages from the server
def receive_data(sock):
    while True:
        data, addr = sock.recvfrom(4096)
        message = data.decode('utf-8')
        
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        print(message)
        
        sys.stdout.write("Enter your message: ")
        sys.stdout.flush()

# Main function to run the client
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_sock:
        join_chat(client_sock)

        
        send_thread = threading.Thread(target=send_data, args=(client_sock,))
        send_thread.start()

        receive_thread = threading.Thread(target=receive_data, args=(client_sock,))
        receive_thread.start()


        send_thread.join()
        receive_thread.join()

# Run only the main function if this script is executed
if __name__ == '__main__':
    main()