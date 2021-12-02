# This is the new combined receiver and client files - version 1.0.5
import socketserver, socket, winsound, time, os, sys
from threading import Thread

# Constants, most of the time these will be used by both the client and receiver
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/PDS.comSoft"
INCHOST, PORT = str(socket.gethostname()), 1500 # Sets the host to the current IP and the port to 1500

# Color constants
# Various colors
BLUE = "\u001b[34;1m" # The color blue
YELLOW = "\u001b[33;1m" # The color yellow
RED = "\u001b[31;1m" # The color red
GREEN = "\u001b[32;1m"
NORMAL = "\u001b[0m" # Reset to default color

# Variables used by both
receiver_running = False
serverIP = "NA"

# Client variabes
message = "" # User's message text
name = input("Enter name > ") # User's name
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
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(4096).strip() # Grab the data that was sent to the server

        playsound(winsound.MB_ICONEXCLAMATION) # Notification sound

        sys.stdout.write(self.data.decode()) # Print the message on-screen



# Functions used by both parts of the file
def playsound(type):
    if (os.path.isfile(DATAPATH + "/mute") == False):
        winsound.MessageBeep(type)



# Core functions - protected behind this if check to make sure the terminal has a chance to start up
if __name__ == "__main__":
    def incoming():
        global receiver_running, serverIP
        # Create the server, binding to localhost on port 1500
        with socketserver.TCPServer((INCHOST, PORT), MyTCPHandler) as server:
            print(GREEN + "Hosting on " + server.server_address[0] + " for incoming messages\n" + NORMAL) # Print the current device's IP address, used ONLY for same-network connections
            receiver_running == True
            serverIP = server.server_address[0]
            server.serve_forever() # Makes sure the server stays running as long as the server terminal is open
            receiver_running == True

    
    
    # Start the incoming messages thread
    Thread(target=incoming, name="receiver thread for incoming messages").start()

    time.sleep(0.5)

    HOST = input("Server IP > ")
    print(BLUE + "Attempting to connect..." + NORMAL)

    # Try to connect to the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
            sock.connect((HOST, PORT))
            sock.sendall(bytes(name + " has established a connection", "utf-8"))
            sock.close()

    except Exception as err: # Something went wrong while trying to send the message
        print(RED + "[!] - Failed to announce presence to server -- " + str(err) + NORMAL)
        time.sleep(999)
        os.abort()


    class client(): # The class that all of the client (outgoing messages) functions are stored within
        # Create a message to send to the remote computer
        def createMessage():
            time.sleep(0.25)
            global message
            message = input("\n\n")
            if allowMessaging == True: # Makes sure to only send if the user is allowed to based on their rate caps
                if (message == "exit" or message == "quit" or message == "changeName" or message == "help" or message == "mute"):
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
                print(RED + "\n[!] - Failed to send message -- " + str(err) + "\n" + NORMAL)

        # Command processor
        def commandProcessor(command):
            global name
            if (command == "exit" or command == "quit"): # The user wants to leave the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    sock.connect((HOST, PORT)) # Connect to the server
                    sock.sendall(bytes(name + " has disconnected", "utf-8")) # Send the removal message
                    sock.close()
                    
                    # Close everything by requesting the operating system kill the process, including the threads
                    os.abort()

            elif (command == "changeName"):
                tempName = input(BLUE + "Enter new username > " + NORMAL) # Ask the user for a new name
                
                # Send the name change alert
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
                    sock.connect((HOST, PORT)) # Connect to the server
                    sock.sendall(bytes(name + " changed their name to " + tempName, "utf-8")) # Send the removal message
                    sock.close()

                name = tempName # Transfer the name stored in tempName to the global name variable
            
            elif (command == "mute"): # Mute notification sounds
                if (os.path.isfile(DATAPATH + "/mute") == False):
                    open(DATAPATH + "/mute", "x").close() # Adds the file that mutes the notifications
                else:
                    os.remove(DATAPATH + "/mute") # Removes the file that mutes the notifications

            elif (command == "help"):
                print(BLUE + "\n[Help]\n'help': get this message\n'exit' or 'quit': disconnect safely\n'changeName': change your name on the server\n'mute': toggle notifications" + NORMAL)
            
            elif (command == "whoAmI"):
                print(RED + name + BLUE + " on " + RED + socket.gethostname() + BLUE + " @ " + RED + serverIP + NORMAL)
            else:
                print(RED + "Command not found - did you type it right?" + BLUE + " [Use 'help' to get a list of safe commands]" + NORMAL)
            
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