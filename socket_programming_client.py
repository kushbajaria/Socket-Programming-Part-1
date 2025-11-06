import socket

# Create a socket
s = socket.socket()

# Set which port to connect to (11123)
port = 11123

# Connect to the server
s.connect(('127.0.0.1', port))
print("Connected to the server. Please type 'quit' to exit.\n")

# While loop to take user input
while True:
    command = input("> ").strip()
    
    # Ignores empty commands
    if not command:
        continue

    # Handle ls command
    if command.lower() == 'ls':
        s.send(command.encode())
        response = s.recv(4096).decode()
        print(response)

    # Handle get command
    elif command.lower().startswith('get'):
        s.send(command.encode())

        status = s.recv(1024).decode()
        if status == "FOUND":
            filename = command.split()[1]
            with open(filename, 'wb') as f:
                s.settimeout(1)
                try:
                    while True:
                        data = s.recv(1024)
                        if not data:
                            break
                        f.write(data)
                except socket.timeout:
                    pass
                s.settimeout(None)

            print(f"File '{filename}' downloaded successfully.")
        elif status == "NOTFOUND":
            print("File not found on server.")
        else:
            print(status)

    # Handle the put command
    elif command.lower().startswith('put'):
        parts = command.split()
        if len(parts) == 2:
            filename = parts[1]
            try:
                with open(filename, 'rb') as f:
                    s.send(command.encode())
                    status = s.recv(1024).decode()

                    if status == "READY":
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            s.send(chunk)
                        s.send(b"DONE")
                        print(f"File '{filename}' uploaded successfully.")
                    else:
                        print("Server not ready for upload.")
            except FileNotFoundError:
                print("File not found locally.")
        else:
            print("Usage: put <filename>")
    
    # Exit program if user enters quit
    elif command.lower() == 'quit':
        s.send(command.encode())
        break

# Close the socket
s.close()
print("Connection closed.")