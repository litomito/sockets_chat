import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

# Global variable to stop the threads
stop_threads = False

# Function to send a message to the server to join the chat
def join_chat(sock):
    sock.sendto("joined".encode('utf-8'), (HOST, PORT))

# Function to get the name of the user
def get_name():
    return input("Enter your name: ")

# Function to send messages to the server from the client and if the user presses Ctrl+C the client will exit the chat
def send_data(sock):
    global stop_threads
    name = get_name()
    # Check if the name is empty and ask for it again
    while name == "":
        print("Name cannot be empty")
        name = get_name()
    while not stop_threads:
        try:
            text = input("Enter your message: ")
            if text == "":
                print("Message cannot be empty")
                continue
            msg = f"{name}: {text}"
            sock.sendto(msg.encode('utf-8'), (HOST, PORT))
        except (OSError, KeyboardInterrupt):
            break

# Function to receive other clients messages from the server
def receive_data(sock):
    global stop_threads
    while not stop_threads:
        try:
            data, addr = sock.recvfrom(4096)
            message = data.decode('utf-8')
            
            sys.stdout.write('\r' + ' ' * 100 + '\r')
            print(message)
            
            sys.stdout.write("Enter your message: ")
            sys.stdout.flush()
        except (OSError, KeyboardInterrupt):
            break

# Main function to run the client and start the threads
def main():
    global stop_threads
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_sock:
            join_chat(client_sock)

            send_thread = threading.Thread(target = send_data, args = (client_sock,))
            receive_thread = threading.Thread(target = receive_data, args = (client_sock,))

            send_thread.daemon = True
            receive_thread.daemon = True

            send_thread.start()
            receive_thread.start()

            send_thread.join()
            receive_thread.join()
    except KeyboardInterrupt:
        print("\nClient is shutting down.")
    finally:
        stop_threads = True
        client_sock.close()

# Run only the main function if this script is executed
if __name__ == '__main__':
    main()