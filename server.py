import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    """Handles a client connection, receiving calculation requests and sending responses."""
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode()  # Receive data (up to 1024 bytes) and decode
        if not data:
            break
        try:
            # Extract operands and operator from received data
            num1, operator, num2 = data.split()
            num1 = float(num1)
            num2 = float(num2)

            # Perform calculation based on operator
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2
            else:
                result = "Error: Invalid operator"

            # Send the result to the client
            conn.sendall(str(result).encode())
        except ValueError:
            conn.sendall("Error: Invalid input (expected two numbers and an operator)".encode())

    conn.close()
    print('Client connection closed:', addr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening on', (HOST, PORT))
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
