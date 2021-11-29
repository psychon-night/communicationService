import socketserver, socket, winsound, time

print("Starting DM server...")
time.sleep(2.5)

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Notification sound

        print(self.data.decode()) # Print the message on-screen

if __name__ == "__main__":
    HOST, PORT = str(socket.gethostname()), 1500 # Sets the host to the current IP and the port to 1500

    # Create the server, binding to localhost on port 1500
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:

        print("Hosting on " + server.server_address[0] + "\n") # Print the current device's IP address, used ONLY for same-network connections
        server.serve_forever() # Makes sure the server stays running as long as the server terminal is open