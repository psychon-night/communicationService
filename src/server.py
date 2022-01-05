# Server version 1.0.4
# Imports
import socketserver, socket, time, winsound, os, locale, sys, ctypes
from threading import Thread as td

os.system("title Shoutout Server")

# Load constants from files
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/Shoutout"
flags = open(DATAPATH + "/data/runFlags.jsonc", "r").read()

# Flag name-value pairs
FASTBOOT = "\"fastBoot\": true"
SILENTSTART = "\"silentStart\": true"
COLORBLIND = "\"disableColors\": true"
SIMPLECOMMANDS = "\"simpleCommands\": true"

# Colors
if not (COLORBLIND in flags):
    PROGBAR = "\u001b[33;1m"
    ERROR = "\u001b[31;1m"
    LOCALMSG = "\u001b[34;1m"
    SERVERMSG = "\u001b[32;1m"
    QUIET = "\u001b[38;5;240m"
    OWNERNAME = "\u001b[35;1m"
    RESET = "\u001b[0m"
else: # Switch to colorblind mode (disables colors)
    PROGBAR = "\u001b[0m";ERROR = "\u001b[0m";LOCALMSG = "\u001b[0m";SERVERMSG = "\u001b[0m";QUIET = "\u001b[0m";OWNERNAME = "\u001b[0m";RESET = "\u001b[0m"
    print("Colorblind support enabled")
    if not (FASTBOOT in flags):
        time.sleep(1)


if not (FASTBOOT in flags):
    os.system("")
    os.system('cls'); print(PROGBAR + "Loading...\n[###                           ]")
    time.sleep(0.25)
    os.system('cls'); print("Loading...\n[###############               ]")
    time.sleep(0.25)
    os.system('cls'); print("Loading...\n[#######################       ]")

    try:
        VERSION = open(DATAPATH + "/data/softwareVersion", "r").read()
        BANNEDUSERS = open(DATAPATH + "/server/bannedIP").read()
        
        time.sleep(0.25)
        os.system('cls'); print("Loading...\n[##############################]" + RESET)
        time.sleep(1)
    except:
        os.system('cls'); print(ERROR + "[STARTUP FAILED: CRITICAL FILES MISSING]" + RESET)
        time.sleep(999)

else:
    print(ERROR + "A flag has been enabled to force a faster startup. This means that the program did NOT check that critical files are present!" + RESET)
    VERSION = "FASTBOOT_1.0.6"
    try:
        BANNEDUSERS = open(DATAPATH + "/server/bannedIP", "r").read()
    except:
        BANNEDUSERS = "Failed to open the banned users file - ignored due to FASTBOOT being enabled"
        print(ERROR + BANNEDUSERS + RESET)

# Constants
if not (SIMPLECOMMANDS in flags):
    CID = "./" # The text that needs to be typed in front of commands to make them commands (instead of sending them)
else:
    CID = "" # None needed because simpleCommands is enabled


# Check to make sure the server isn't already running
serverRunFile = DATAPATH + "/server/running"

if not (SILENTSTART in flags):
    try:
        open(serverRunFile, "r").close() # See if the file opens

        # Don't let the server start
        if not (FASTBOOT in flags):
            os.system('cls')
        print(ERROR + "Another instance of the server is already running, or you forgot to use shutdown. If you don't have another server instance running, press ENTER\n" + RESET)
        hold = input("")

    except:
        open(serverRunFile, "x").close()


    # Print the server info
    if not (FASTBOOT in flags):
        os.system('cls')
    time.sleep(0.75)
    print("Shoutout Server " + VERSION + "\n")

    if not (FASTBOOT in flags):
        # Let the user know that the server is being started
        if (os.path.isfile(DATAPATH + "/mute") == False):
            print(SERVERMSG + "Starting server (" + str(locale.getlocale()) + ")" + RESET)

        else:
            print(SERVERMSG + "Starting server (" + str(locale.getlocale()) + LOCALMSG + ") in silent mode - use 'mute' to enable sound" + RESET)
        time.sleep(2.5) # Gives the main thread enough time to initialize
    else:
        print(SERVERMSG + "Fast boot is enabled. " + ERROR + "You may experience problems while using this flag!" + RESET)
else:
    os.system('cls')
    print(QUIET + "Quieter startup is enabled. Other flag messages may not be displayed during startup." + RESET)

# Server configuration variables
client_list = [] # This is the list that the clients are stored in, processed later for forwarding to all connected clients
serverIP = "" # This is where the server's IP will be stored for access by other modules that need it
name = input(LOCALMSG + "Name > " + RESET)

''' -- Actual server functionality -- '''

# The server's core functions
class Handler(socketserver.BaseRequestHandler):     
    # Process the data received over the socket connection
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        # Determines if the user is a new one
        global client_list # Gets the client list

        try:
            if not (self.client_address[0] in BANNEDUSERS):
                if (bytes("has established a connection", "utf-8") in self.data): # The user is new
                    # if (self.client_address[0] != serverIP):

                    client_list.append(self.client_address[0]) # Add them to the list of known users
                    time.sleep(0.25)

                    forward(self.data) # Forward it to other users - this might take a moment if there are a lot to cycle through (especially on slow network conditions)
                    print(self.client_address[0] + " connected -- connected clients: " + str(client_list)) # Print locally
                    playsound(winsound.MB_ICONASTERISK) # Play notification sound
                        

                
                else: # The user is not new
                    if not ("has disconnected" in self.data.decode() or "kicked for spam" in self.data.decode()): # The user isn't trying to disconnect
                        sys.stdout.write("\n" + u"\x1b[1A" + u"\x1b[2K")
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

                        client_list.remove(self.client_address[0]) # Remove the person who got kicked

            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.client_address[0], 1500))
                    sock.sendall(bytes(ERROR + "You are banned from connecting to this server and cannot send messages to it" + RESET, "UTF-8")) # Tell the banned user of their status
                    sock.close() # Close the connection

        except Exception as err:
            print(ERROR + str(err) + RESET)

            


# Server functions
def forward(data): # Forward incoming messages to other users
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Lets the program create a temporary socket connection (outgoing)
        for client in client_list:
            print(client)
            time.sleep(0.05)
            sock.connect((client, 1500)) # Connect to the desired endpoint
            sock.sendall(data) # Send the message
            sock.close() # Close the connection
            time.sleep(0.025) # Slight pause to prevent overflow


def playsound(type): # Plays notification sounds
    if (os.path.isfile(DATAPATH + "/mute") == False):
        winsound.MessageBeep(type)


def serverCommandProcessor(): # Lets the operator use commands or send messages to connected clients
    global name, client_list
    command = input("")
    SUPPORTED_COMMANDS = CID + 'help', CID + 'shutdown', CID + 'listClients', CID + 'mute', CID + 'clear', CID + 'whoAmI', CID + 'changeName', CID + 'ban', CID + 'clientStatus'


    if (command == CID + "help"): # This command lets the user view supported commands
        print(LOCALMSG + "\nSupported commands: " + str(str(SUPPORTED_COMMANDS).strip(")")).strip("("))
        print(ERROR + "Do not forget to include the " + CID + " before your command or " + SERVERMSG + "it will be sent to clients" + LOCALMSG)
        print(" > 'help': get this message\n > 'shutdown': shut down the server - doesn't warn clients!\n > 'listClients': list the connected clients\n > 'mute': mute notification sounds - persists across restart. Use again to unmute\n > 'clear': clear the terminal of all messages\n > 'whoAmI': get your current username and IP\n > 'changeName': change your name on the server\n > 'banIP': ban any IP. Messages from that IP will be ignored\n > 'clientStatus': get the connection status of clients (detect problems like unexpected disconnects)\n" + RESET)

        if (SILENTSTART in flags):
            print(QUIET + "Some commands, such as mute, will have their outputs silenced since you are in quieter mode\n" + RESET)
    

    elif (command == CID + "shutdown"): # This command shuts down the server
        print(SERVERMSG + "Shutting down server..." + RESET) # Print the alert
        time.sleep(1.3) # Sleep
        if not (SILENTSTART in flags):
            os.remove(DATAPATH + "/server/running") # Allows new instances of the server to be started without the warning
        else:
            print("Ignoring lack of runtime files, quiet mode preventing optimal shutdown. Forcing...")

        os.abort() # Forcefully close out
    

    elif (command == CID + "listClients"): # lists the connected clients
        print(LOCALMSG); print(client_list); print(RESET)


    elif (command == CID + "mute"): # mutes ALL Shoutout notifications, even those from other files
        if (os.path.isfile(DATAPATH + "/mute") == False):
            open(DATAPATH + "/mute", "x").close() # Adds the file that mutes the notifications
            if not (SILENTSTART in flags):
                print(LOCALMSG + "\n\x10 Notifications disabled\n" + RESET)

        else:
            os.remove(DATAPATH + "/mute") # Removes the file that mutes the notifications
            if not (SILENTSTART in flags):
                print(LOCALMSG + "\n\x10 Notifications enabled\n" + RESET)


    elif (command == CID + "clear"): # clear the screen
        os.system('cls')
        if not (SILENTSTART in flags):
            print("Shoutout Server " + VERSION + "\n")
            print(SERVERMSG + "Hosting on " + server.server_address[0] + "\n" + RESET)
        else:
            print(QUIET + "IP: " + serverIP + "\n" + RESET)


    elif (command == CID + "whoAmI"): # get local device information
        print(ERROR + name + LOCALMSG + " on " + ERROR + socket.gethostname() + " @ " + ERROR + serverIP + RESET)


    elif (command == CID + "changeName"): # let the user change their display name
        tempName = input(LOCALMSG + "Enter new username > " + RESET) # Ask the user for a new name
        name = tempName # Transfer the name stored in tempName to the global name variable


    elif (command == CID + "ban"): # let the user an a specific client
        target = input(LOCALMSG + "Enter IP [type 'list' to list connected clients] > " + RESET)

        if (target == "list"):
            print(LOCALMSG + str(client_list))
            
            target = input("Enter IP > " + RESET)

        
        if (target in client_list):
            print(SERVERMSG + target + " is being banned..." + RESET)
            forward(ERROR + "The user at " + target + " was banned by the server owner" + RESET)

            client_list.remove(target)

            # Add them to the banned IP file
            banfile = open(DATAPATH + "/server/bannedIP", "a")
            banfile.write("\n" + target)
            banfile.close()

        else:
            print(LOCALMSG + "That IP (" + target + ") isn't actively connected or is otherwise incorrect.")
            ac = input("Do you want to try to ban by IP anyways? [Y/N] > " + RESET).capitalize()

            if (ac == "Y"):
                try: # Tries to ban the target 
                    print(SERVERMSG + target + " is being banned..." + RESET)
                    forward(ERROR + "The user at " + target + " was banned by the server owner" + RESET)

                    try:
                        client_list.remove(target)
                    except:
                        NotImplemented # Ignore the error and keep going, the user isn't currently connected

                    # Add them to the banned IP file
                    banfile = open(DATAPATH + "/server/bannedIP", "a")
                    banfile.write("\n" + target)
                    banfile.close()

                except Exception as err: # Something went wring
                    print(ERROR + "Failed to ban the target: " + str(err) + RESET)
            else:
                print(LOCALMSG + "Action aborted" + RESET)
        
        print("\n") # Print blank line to improve readability

    elif (command == serverIP):
        print(SERVERMSG + serverIP + LOCALMSG + " is your IP device's network address. Sending this may pose a security risk!" + RESET)

        send = input(LOCALMSG + "Did you want to send that to connected clients? [Y/N] > ").capitalize()

        if (send == "Y"):
            string = u"\x1b[1A" + u"\x1b[2K" + u"\x1b[1A" + u"\x1b[2K" + u"\x1b[1A" + u"\x1b[2K" + OWNERNAME + name + u" >> " + command + "\x1b[0m \n"
            sys.stdout.write(string)
            string = u"\x1b[1A" + u"\x1b[2K" + OWNERNAME + name + u" >> " + command + "\x1b[0m \n"
            forward(bytes(string, "utf-8"))


    elif (command == CID + "clientStatus"): # Shows the connection status of all clients in client_list by sending forced response data
        index = 0
        for clients in client_list:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    dest = client_list.pop(index) # Get the next user to forward to
                    sock.connect((str(dest), 1500)) # Connect to the desired endpoint
                    sock.sendall("pingStat") # Send the message
                    sock.close() # Close the connection
                    client_list.insert(index, dest) # Re-add the user to the list
                    time.sleep(0.025) # Slight pause to prevent overflow

                    print(LOCALMSG + "Client at " + ERROR + dest + LOCALMSG + "is " + SERVERMSG + "connected")
                
                except:
                    print(LOCALMSG + "Client at " + ERROR + dest + LOCALMSG + "is " + ERROR + "unresponsive and is being removed from client list...")
                    client_list.remove(dest)

                finally:
                    index += 1
    
    else: # the host isn't trying to execute a command and is trying to send a message
        string = u"\x1b[1A" + u"\x1b[2K" + OWNERNAME + name + u" >> " + command + "\x1b[0m \n"

        sys.stdout.write(string)
        forward(bytes(string, "utf-8"))
    serverCommandProcessor()


td(target=serverCommandProcessor, name="server command processing").start() # Start the server console


# Initial setup of the server
if __name__ == "__main__":
    HOST, PORT = str(socket.gethostname()), 1500 # Sets the HOST to the current IP and the port to 1500

    try:
        # Create the server, binding to localhost on port 1500
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((HOST, PORT), Handler) as server:
            serverIP = server.server_address[0]
            if not (FASTBOOT in flags):
                os.system('cls')
            if not (SILENTSTART in flags):
                print("Shoutout Server " + VERSION + "\n")
                print(SERVERMSG + "Hosting on " + server.server_address[0] + "\n" + RESET)
            else:
                print(QUIET + "IP: " + serverIP + "\n" + RESET)
            server.serve_forever() # Makes sure that the server runs for as long as the server terminal window is open
    
    except Exception as err:
        print(ERROR + "Failed to start the server: " + str(err) + RESET)