# Imports
import socketserver, socket, time, winsound

# Let the user know that the server is being started
print("Starting global server...")
time.sleep(2.5) # Gives the main thread enough time to initialize

client_list = [] # This is the list that the clients are stored in, processed later for forwarding to all connected clients

# The server's core functions
class Handler(socketserver.BaseRequestHandler):

    # Process the data received over the socket connection
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        # Determines if the user is a new one
        global client_list # Gets the client list

        if not (self.client_address[0] in client_list): # The user is new

            client_list.append(self.client_address[0]) # Add them to the list of known users
            whoSent = self.client_address[0] # the IP of who sent the message

            forward(self.data, whoSent) # Forward it to other users - this might take a moment if there are a lot to cycle through (especially on slow network conditions)
            print(self.client_address[0] + " connected") # Print locally
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Play notification sound

        else: # The user is not new
            if not ("has disconnected" in self.data.decode()): # The user isn't trying to disconnect
                print("client@" + self.client_address[0] + "~ " + self.data.decode()) # Print on the local display
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Notification sound

                whoSent = self.client_address[0] # Who sent the message
                forward(self.data, whoSent) # Forward it to other users

            else: # The user is trying to disconnect
                user = self.client_address[0] # The user who sent the message
                forward(self.data, user) # Tell other users that someone has left
                print("client@" + user + " disconnected") # Print on the local display
                winsound.MessageBeep(winsound.MB_ICONASTERISK) # Notification sound

                client_list.remove(user) # Remove the person who wants to be removed 

# Server-side functions
def forward(data, sender): # Forward it to other users
    global client_list

    # Loop vars
    forwarded = 0
    index = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        while (forwarded != (len(client_list) - 1)):
            if not (client_list.index(index) == sender):
                sock.connect(client_list.index(index), 1500) # Connect to the desired endpoint
                sock.sendall(data) # Send the message
                sock.close() # Close the connection

                # Update the loop variables
                forwarded += 1
                index += 1
        

# Initial setup of the server
if __name__ == "__main__":
    HOST, PORT = str(socket.gethostname()), 1500 # Sets the HOST to the current IP and the port to 1500

    # Create the server, binding to localhost on port 1500
    with socketserver.TCPServer((HOST, PORT), Handler) as server:
        print("Hosting on " + server.server_address[0] + "\n") # Print the current device's LAN IP address. This IP is the one that other users need to connect to
        server.serve_forever() # Makes sure that the server runs for as long as the server terminal window is open
