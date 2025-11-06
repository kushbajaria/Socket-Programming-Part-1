import socket
import os

# Create socket
s = socket.socket()
print("Socket has been successfully created!")

# Assign the socket a port number
port = 11123

""" Bind to the port, empty string will allow server 
    to listen to requests coming from other computers 
    on the network.
"""
s.bind(('', port))
print ("Socket has been binded to port %s" %(port))

# Put socked into listening mode
s.listen(5)
print("Socket is listening...")

# Establish connection with the client
c, addr = s.accept()
print(f"Got a connection from:", addr)


# Uninterrupted loop, until interrupted or error
while True:
    data = c.recv(1024).decode().strip()

    if not data:
        break
    
    print(f"Received data: {data}")

    if data.lower() == "ls":
        files = os.listdir('.')
        response = '\n'.join(files) if files else "No files found."

    elif data.lower().startswith('get'):
        parts = data.split()
        if len(parts) == 2:
            filename = parts[1]
            if os.path.exists(filename):
                c.send(b"FOUND")

                with open(filename, 'rb') as f:
                    c.sendall(f.read())
            else:
                c.send(b"NOTFOUND")
        else:
            c.send(b"ERROR: Missing filename")
        continue

    elif data.lower().startswith('put'):
        parts = data.split()
        if len(parts) == 2:
            filename = parts[1]
            c.send(b"READY")

            with open(filename, 'wb') as f:
                while True:
                    chunk = c.recv(1024)
                    if chunk == b"DONE":
                        break
                    f.write(chunk)
            response = f"File '{filename}' uploaded successfully."
        else:
            response = "ERROR: Missing filename."

    elif data.lower() == 'quit':
        response = "Goodbye!"

        c.send(response.encode())
        break

    else:
        response = "Unknown command."

    c.send(response.encode())

# Close connection
c.close()
s.close()
print("Connection closed.")
