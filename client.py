import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        # Get user input for calculation (ensure valid format)
        expression = input("Enter expression (number1 operator number2): ")
        if not expression.strip():
            break

        # Send expression to the server
        s.sendall(expression.encode())

        # Receive response from the server and display it
        data = s.recv(1024).decode()
        print(data)

print('Connection closed')
