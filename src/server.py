# Server version 1.0.4
# Imports
import socketserver, socket, time, winsound, os, locale, sys
from threading import Thread as td

# Colors
PROGBAR = "\u001b[33;1m"
ERROR = "\u001b[31;1m"
LOCALMSG = "\u001b[34;1m"
SERVERMSG = "\u001b[32;1m"
RESET = "\u001b[0m"

# Constants
os.system("")
os.system('cls'); print(PROGBAR + "Loading...\n[###                           ]")
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
time.sleep(0.25)
os.system('cls'); print("Loading...\n[###############               ]")
DATAPATH = DRIVELETTER + ":/ProgramData/PDS.comSoft"
time.sleep(0.25)
os.system('cls'); print("Loading...\n[#######################       ]")
try:
    VERSION = open(DATAPATH + "/softwareVersion", "r").read()
    
    time.sleep(0.25)
    os.system('cls'); print("Loading...\n[##############################]" + RESET)
    time.sleep(1)
except:
    os.system('cls'); print(ERROR + "[STARTUP FAILED: CRITICAL FILES MISSING]" + RESET)
    time.sleep(999)


# Check to make sure the server isn't already running
serverRunFile = DATAPATH + "/server/running"
try:
    open(DATAPATH + "/server/running", "r").close() # See if the file opens

    # Don't let the server start
    os.system('cls')
    print(ERROR + "Another instance of the server is already running, or you forgot to use shutdown. If you don't have another server instance running, press ENTER\n" + RESET)
    hold = input("")

except:
    open(DATAPATH + "/server/running", "x").close()


# Print the server info
os.system('cls')
time.sleep(0.75)
print("ComSoft Server " + VERSION + "\n")

# Let the user know that the server is being started
if (os.path.isfile(DATAPATH + "/mute") == False):
    print(SERVERMSG + "Starting server (" + str(locale.getlocale()) + ")" + RESET)

else:
    print(SERVERMSG + "Starting server (" + str(locale.getlocale()) + LOCALMSG + ") in silent mode - use 'mute' to enable sound" + RESET)
time.sleep(2.5) # Gives the main thread enough time to initialize


# Server configuration variables
client_list = [] # This is the list that the clients are stored in, processed later for forwarding to all connected clients
serverIP = "" # This is where the server's IP will be stored for access by other modules that need it
name = input(LOCALMSG + "Name > " + RESET)


# The server's core functions
class Handler(socketserver.BaseRequestHandler):

    # Process the data received over the socket connection
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        # Determines if the user is a new one
        global client_list # Gets the client list

        if not (self.client_address[0] in client_list): # The user is new

            client_list.append(self.client_address[0]) # Add them to the list of known users

            try: 
                forward(self.data) # Forward it to other users - this might take a moment if there are a lot to cycle through (especially on slow network conditions)
                print(self.client_address[0] + " connected") # Print locally
                playsound(winsound.MB_ICONASTERISK) # Play notification sound
            except Exception as error:
                print(ERROR + "Something went wrong:" + str(error) + RESET)


        else: # The user is not new
            if not ("has disconnected" in self.data.decode() or "kicked for spam" in self.data.decode()): # The user isn't trying to disconnect
                print("client@" + self.client_address[0] + "~ " + self.data.decode()) # Print on the local display
                playsound(winsound.MB_ICONEXCLAMATION) # Notification sound
                forward(self.data) # Forward it to other users


            elif ("has disconnected" in self.data.decode()): # The user is trying to disconnect
                user = self.client_address[0] # The user who sent the message
                forward(self.data) # Tell other users that someone has left
                print("client@" + user + " disconnected") # Print on the local display
                playsound(winsound.MB_ICONEXCLAMATION) # Notification sound

                client_list.remove(self.client_address[0]) # Remove the person who wants to be removed 
            
            elif ("kicked for spam" in self.data.decode()): # The user was kicked for spam
                user = self.client_address[0] # The user who sent the message
                forward(self.data) # Tell other users that someone has been kicked
                print("client@" + user + " kicked for spam") # Print on the local display
                playsound(winsound.MB_ICONASTERISK) # Play the notificatin sound

                client_list.remove(self.client_address[0]) # Remove the person who got
            


# Server functions
def forward(data): # Forward incoming messages to other users
    global client_list

    # Loop vars
    forwarded = 0
    index = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        while (forwarded <= (len(client_list) - 1)):
            if (client_list[index] != serverIP):
                dest = client_list.pop(index)
                sock.connect((str(dest), 1500)) # Connect to the desired endpoint
                sock.sendall(data) # Send the message
                sock.close() # Close the connection
                client_list.append(dest)
                time.sleep(0.025)

            # Update the loop variables
            forwarded += 1
            index += 1

def playsound(type):
    if (os.path.isfile(DATAPATH + "/mute") == False):
        winsound.MessageBeep(type)


def serverCommandProcessor():
    global name
    command = input("")
    if (command == "help"):
        print(LOCALMSG + "\nSupported commands: 'help', 'shutdown', 'listClients', 'mute', 'clear', 'whoAmI', 'changeName'") # 'disableForwarding' for future
        print(" > 'help': get this message\n > 'shutdown': shut down the server - doesn't warn clients!\n > 'listClients': list the connected clients\n > 'mute': mute notification sounds - persists across restart. Use again to unmute\n > 'clear': clear the terminal of all messages\n > 'whoAmI': get your current username and IP\n > 'changeName': change your name on the server\n" + RESET)
    
    elif (command == "shutdown"): # This command shuts down the server
        print(SERVERMSG + "Shutting down server..." + RESET)
        time.sleep(0.75)
        os.remove(DATAPATH + "/server/running") # Allows new instances of the server to be started

        os.abort() # Forcefully close out
    
    elif (command == "listClients"):
        print(LOCALMSG); print(client_list); print(RESET)

    elif (command == "mute"):
        if (os.path.isfile(DATAPATH + "/mute") == False):
            open(DATAPATH + "/mute", "x").close() # Adds the file that mutes the notifications
            print(LOCALMSG + "\n\x10 Notifications disabled\n" + RESET)
        else:
            os.remove(DATAPATH + "/mute") # Removes the file that mutes the notifications
            print(LOCALMSG + "\n\x10 Notifications enabled\n" + RESET)

    elif (command == "clear"):
        os.system('cls')
        print("ComSoft Server " + VERSION + "\n")
        print(SERVERMSG + "Hosting on " + server.server_address[0] + "\n" + RESET)

    elif (command == "whoAmI"):
        print(ERROR + name + LOCALMSG + " on " + ERROR + socket.gethostname() + " @ " + ERROR + serverIP + RESET)

    elif (command == "changeName"):
        tempName = input(LOCALMSG + "Enter new username > " + RESET) # Ask the user for a new name
        name = tempName # Transfer the name stored in tempName to the global name variable
    
    else:
        string = u"\x1b[1A" + u"\x1b[2K" + "\u001b[35;1m" + name + u" >> " + command + "\x1b[0m \n"

        sys.stdout.write(string)
        forward(bytes(string, "utf-8"))
    serverCommandProcessor()


td(target=serverCommandProcessor, name="server command processing").start() # Start the server console


# Initial setup of the server
if __name__ == "__main__":
    HOST, PORT = str(socket.gethostname()), 1500 # Sets the HOST to the current IP and the port to 1500

    try:
        # Create the server, binding to localhost on port 1500
        with socketserver.TCPServer((HOST, PORT), Handler) as server:
            serverIP = server.server_address[0]
            os.system('cls')
            print("ComSoft Server " + VERSION + "\n")
            print(SERVERMSG + "Hosting on " + server.server_address[0] + "\n" + RESET)
            server.serve_forever() # Makes sure that the server runs for as long as the server terminal window is open
    
    except Exception as err:
        print(ERROR + "Failed to start the server: " + str(err) + RESET)
