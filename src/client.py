# Client version 1.0.6
 
import socketserver, socket, winsound, time, os, sys
from threading import Thread

os.system('cls')
os.system("title Shoutout Client")
 
# Constants, most of the time these will be used by both the client and receiver
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/Shoutout"
INCHOST, PORT = str(socket.gethostbyname(socket. gethostname())), 1500 # Sets the host to the current IP and the port to 1500
SPECIAL_MESSAGES = ['pingStat'] # List of messages that make the client file do something other than print it on-screen
flags = open(DATAPATH + "/data/runFlags.jsonc", "r").read() # The file that the flags are stored in

# Flag name-value pairs
SIMPLECOMMANDS = "\"simpleCommands\": true"
DISABLECOLORS = "\"disableColors\": true"
ALLOWHYPERLINKS = "\"allowHyperlinks\": true"

try:
    VERSION = open(DATAPATH + "/data/softwareVersion", "r").read()
except:
    print("\u001b[31;1mFailed to get current version\u001b[0m")
    time.sleep(999)

if not (SIMPLECOMMANDS in flags):
    CID = "./" # The text that needs to be typed in front of commands to make them commands (instead of sending them)
else:
    CID = "" # None needed because simpleCommands is enabled
 

# Color constants
# Various colors
if not (DISABLECOLORS in flags):
    BLUE = "\u001b[34;1m" # The color blue
    YELLOW = "\u001b[33;1m" # The color yellow
    RED = "\u001b[31;1m" # The color red
    GREEN = "\u001b[32;1m"
    NORMAL = "\u001b[0m" # Reset to default color

else:
    # All colors set to White
    BLUE = "\u001b[0m";YELLOW = "\u001b[0m";RED = "\u001b[0m";GREEN = "\u001b[0m";NORMAL = "\u001b[0m";
 
os.system("")

print(GREEN + "Shoutout Client " + VERSION + "\n" + NORMAL)
 
# Variables used by both
receiver_running = False
serverIP = "NA"
 

# Client variabes
message = "" # User's message text
name = input(BLUE + "Enter name > " + NORMAL) # User's name
failed_disconnects = 0 # How many times the client failed to disconnect correctly and safely
print("")
 
# Variables used for reducing spam
messageCount = 0
allowMessaging = True
preventRecovery = False # if this is set to true, the recovery script is not allowed to recover from fatal errors
spamLimit = 6 # Change this value to adjust how many spam messages are needed before auto-kicking the user
 

# Check to see if the desired endpoint is in the knownHosts file
knownHostsFile = open(DATAPATH + "/client/knownHosts", "r")
knownHosts = knownHostsFile.read()
 
# Receiver server class
class ReceiverSocket(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        if not (self.data in SPECIAL_MESSAGES):
            playsound(winsound.MB_ICONEXCLAMATION) # Notification sound

            sys.stdout.write("\n" + str(self.data.decode()) + "\n") # Print the message on-screen

        else:
            if (self.data == "pingStat"):
                print(GREEN + "Connection was verified by server" + NORMAL)
 

# Functions used by both parts of the file
 
def playsound(type):
    if (os.path.isfile(DATAPATH + "/mute") == False):
        winsound.MessageBeep(type)


# Core functions - protected behind this if check to make sure the terminal has a chance to start up
if __name__ == "__main__":
    def incoming():
        global receiver_running, serverIP

        # Create the server, binding to localhost on port 1500
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((INCHOST, PORT), ReceiverSocket) as server:
            print(GREEN + "Hosting on " + server.server_address[0] + " for incoming messages\n" + NORMAL) # Print the current device's IP address, used ONLY for same-network connections
 
            receiver_running == True
            serverIP = server.server_address[0]
            server.serve_forever() # Makes sure the server stays running as long as the server terminal is open
 


    # Start the incoming messages thread
    Thread(target=incoming, name="receiver thread for incoming messages").start()
    time.sleep(0.5)
 
 
    HOST = input(BLUE + "Server IP > " + NORMAL)

    if not (HOST in knownHosts):
        print(RED + "The specified IP (" + HOST + ") isn't in the list of known hosts.")
        allow = input(BLUE + "Do you want to connect anyways and add it to the known hosts? [Y/N] > " + NORMAL).capitalize()

        if not (allow == "Y"):
            print(RED + "Aborting connection..." + NORMAL)
            time.sleep(3)
            os.abort()
            
        # Add the new host to the list
        open(DATAPATH + "/client/knownHosts", "a").write("\n" + HOST)

    print(BLUE + "Attempting to connect..." + NORMAL)

    # Try to connect to the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
            sock.connect((HOST, PORT))
            sock.sendall(bytes(name + " has established a connection", "utf-8")) # the server looks for these words to print the login message on the server terminal
            sock.close()

    except Exception as err: # Something went wrong while trying to send the message
        if not (str(err) == "[Errno 11001] getaddrinfo failed"):
            print(RED + "[!] - Failed to announce presence to server -- " + str(err) + NORMAL)
            time.sleep(30)
            os.abort()
        else:
            print(RED + "Unable to resolve destination '" + BLUE + HOST + RED + "'" + NORMAL)
 

    class client(): # The class that all of the client (outgoing messages) functions are stored within
        # Create a message to send to the remote computer
        def createMessage():
            time.sleep(0.25)
            global message

            message = input("\n")
            sys.stdout.write(u"\x1b[1A" + u"\x1b[2K")
            if allowMessaging == True: # Makes sure to only send if the user is allowed to based on their rate caps (this is currently disabled, so it's always TRUE)
                if (message == CID + "exit" or message == CID + "quit" or message == CID + "changeName" or message == CID + "help" or message == CID + "mute"):
                    client.commandProcessor(message)
                else:
                    client.sendMessage(message)
 
        # Send the message the user just created
        def sendMessage(data):
            try:
                global messageCount
 
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    # Connect to server and send data
                    sock.connect((HOST, PORT))
                    sock.sendall(bytes(name + ": " + data, "utf-8"))
                    sock.close()
 
                    messageCount += 1 # Increase how many messages they have sent

            except Exception as err: # Something went wrong trying to send the message to the server
                if (str(err) != "[Errno 11001] getaddrinfo failed"):
                    print(RED + "\n[!] - Failed to send message -- " + str(err) + "\n" + NORMAL)
                else:
                    print(RED + "Unable to resolve destination '" + BLUE + HOST + RED + "'." + NORMAL )

        # Command processor
 
        def commandProcessor(command):
            global name, failed_disconnects
 
            if (command == CID + "exit" or command == CID + "quit"): # The user wants to leave the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    try:
                        sock.connect((HOST, PORT)) # Connect to the server
                        sock.sendall(bytes(name + " has disconnected", "utf-8")) # Send the removal message
                        sock.close()
    
                        # Close everything by requesting the operating system kill the process, including the threads
                        os.abort()
                    except:
                        if (failed_disconnects <= 6):
                            print(RED + "Failed to disconnect. Trying again in 5 seconds..." + NORMAL)
                            failed_disconnects += 1
                            time.sleep(5)
                            client.commandProcessor(CID + "exit")
                        else:
                            print(RED + "Failed to disconnect too many times. The program will now self-terminate, but " + BLUE + " this may cause serious server-side errors!")
                            time.sleep(5)
                            os.abort()
 
 
 
            elif (command == CID + "changeName"):
                tempName = input(BLUE + "Enter new username > " + NORMAL) # Ask the user for a new name

                # Send the name change alert
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    sock.connect((HOST, PORT)) # Connect to the server
                    sock.sendall(bytes(name + " changed their name to " + tempName, "utf-8")) # Send the removal message
                    sock.close()

                name = tempName # Transfer the name stored in tempName to the global name variable
 

            elif (command == CID + "mute"): # Mute notification sounds
                if (os.path.isfile(DATAPATH + "/mute") == False):
                    open(DATAPATH + "/mute", "x").close() # Adds the file that mutes the notifications
                else:
                    os.remove(DATAPATH + "/mute") # Removes the file that mutes the notifications

            elif (command == CID + "help"):
                print(BLUE + "\n[Help]\n'help': get this message\n'exit' or 'quit': disconnect safely\n'changeName': change your name on the server\n'mute': toggle notifications" + NORMAL)

            elif (command == CID + "whoAmI"):
                print(RED + name + BLUE + " on " + RED + socket.gethostname() + BLUE + " @ " + RED + serverIP + NORMAL)

            print("") # Blank
 
   
 
        # Main process that lets the user enter messages
    def mainLoop():
        print("\n")
        while True:
            if allowMessaging == True:
                client.createMessage()
 
 
    # Start up the outgoing message thread
    mainThread = Thread(target=mainLoop, name="sender thread for outgoing messages")
    mainThread.start()