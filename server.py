# Server version 1.0.3
# Imports
import socketserver, socket, time, winsound, os, locale
from threading import Thread as td

# Constants
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/PDS.comSoft"
try:
    VERSION = open(DATAPATH + "/softwareVersion", "r").read()
except:
    os.system('cls'); print("[STARTUP FAILED: CRITICAL FILES MISSING]")
    time.sleep(999)

# Print the version info
print("ComSoft Server " + VERSION + "\n")


# Let the user know that the server is being started
print("Starting server (" + str(locale.getlocale()) + ")")
time.sleep(2.5) # Gives the main thread enough time to initialize


# Server configuration variables
client_list = [] # This is the list that the clients are stored in, processed later for forwarding to all connected clients
serverIP = "" # This is where the server's IP will be stored for access by other modules that need it


# The server's core functions
class Handler(socketserver.BaseRequestHandler):

    # Process the data received over the socket connection
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        # Determines if the user is a new one
        global client_list # Gets the client list

        if not (self.client_address[0] in client_list): # The user is new

            client_list.append(self.client_address[0]) # Add them to the list of known users


            forward(self.data) # Forward it to other users - this might take a moment if there are a lot to cycle through (especially on slow network conditions)
            print(self.client_address[0] + " connected") # Print locally
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Play notification sound


        else: # The user is not new
            if not ("has disconnected" in self.data.decode() or "kicked for spam" in self.data.decode()): # The user isn't trying to disconnect
                print("client@" + self.client_address[0] + "~ " + self.data.decode()) # Print on the local display
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) # Notification sound
                forward(self.data) # Forward it to other users


            elif ("has disconnected" in self.data.decode()): # The user is trying to disconnect
                user = self.client_address[0] # The user who sent the message
                forward(self.data) # Tell other users that someone has left
                print("client@" + user + " disconnected") # Print on the local display
                winsound.MessageBeep(winsound.MB_ICONASTERISK) # Notification sound

                client_list.remove(self.client_address[0]) # Remove the person who wants to be removed 
            
            elif ("kicked for spam" in self.data.decode()): # The user was kicked for spam
                user = self.client_address[0] # The user who sent the message
                forward(self.data) # Tell other users that someone has been kicked
                print("client@" + user + " kicked for spam") # Print on the local display
                winsound.MessageBeep(winsound.MB_ICONASTERISK) # Notification sound

                client_list.remove(self.client_address[0]) # Remove the person who got
            


# Server functions
def forward(data): # Forward incoming messages to other users
    global client_list

    # Loop vars
    forwarded = 0
    index = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        while (forwarded != (len(client_list) - 1)):
            if (client_list[index] != socket.gethostname()):
                sock.connect((client_list[index], 1500)) # Connect to the desired endpoint
                sock.sendall(data) # Send the message
                sock.close() # Close the connection

            # Update the loop variables
            forwarded += 1
            index += 1


def serverCommandProcessor():
    time.sleep(0.75)
    command = input("")
    if (command == "help"):
        print("Supported commands: 'help', 'shutdown', 'disableForwarding'")
    
    elif (command == "shutdown"): # This command shuts down the server
        print("Shutting down server...")
        time.sleep(0.75)

        forward("[Server] Shutdown in progress") # Tell the other users that the server is in shutdown
        time.sleep(0.75)

        with socketserver.TCPServer((serverIP, 1500), Handler) as server: # Connect to itself
            server.shutdown() # Shut down the server softly

        time.sleep(0.75)
        exit()
    serverCommandProcessor()


td(target=serverCommandProcessor, name="server command processing").start() # Start the server console


# Initial setup of the server
if __name__ == "__main__":
    HOST, PORT = str(socket.gethostname()), 1500 # Sets the HOST to the current IP and the port to 1500

    # Create the server, binding to localhost on port 1500
    with socketserver.TCPServer((HOST, PORT), Handler) as server:
        serverIP = server.server_address[0]
        print("Hosting on " + server.server_address[0] + "\n") # Print the current device's LAN IP address. This IP is the one that other users need to connect to
        server.serve_forever() # Makes sure that the server runs for as long as the server terminal window is open