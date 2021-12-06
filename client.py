# Client 1.0.4
import socket, time, winsound, os, sys
from multiprocessing import Process
from threading import Thread as td

# Make the recursion limit larger to reduce crashes after recovery
sys.setrecursionlimit(10**6)


# Constants
os.system('cls'); print("Starting...\n[#########                     ]")

DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
  
time.sleep(0.25)
os.system('cls'); print("Starting...\n[###################           ]")
time.sleep(0.25)

DATAPATH = DRIVELETTER + ":/ProgramData/PDS.comSoft"

time.sleep(0.25)
os.system('cls'); print("Starting...\n[########################      ]")
time.sleep(0.25)

try:
    VERSION = open(DATAPATH + "/softwareVersion", "r").read()
    
    os.system('cls'); print("Starting...\n[##############################]")
    time.sleep(0.25)
except:
    print("[STARTUP FAILED: CRITICAL FILES MISSING]")
    time.sleep(999)

# Print the version number
os.system('cls');time.sleep(0.75); print("ComSoft Client " + VERSION + "\n")

# Sever IP and port constants
HOST, PORT = input("Server IP > "), 1500 # Set up the host and port values

message = "" # User's message text
name = input("Enter name > ") # User's name

# Variables used for reducing spam
messageCount = 0
allowMessaging = True
preventRecovery = False # if this is set to true, the recovery script is not allowed to recover from fatal errors
spamLimit = 6 # Change this value to adjust how many spam messages are needed before auto-kicking the user


# Check to see if the desired endpoint is in the knownHosts file
knownHostsFile = open(DATAPATH + "/client/knownHosts", "r")
knownHosts = knownHostsFile.read()

# Check to see that the required data exists

# Safety filter
if (HOST in knownHosts): # Checks if the host is in the known hosts file
    # Do nothing
    NotImplemented

else:
    print("Warning: The specified host (" + HOST + ") is not in the known hosts file and might pose a security risk.")
    allowConnection = input("Do you want to complete the connection? [Y/N] > ").capitalize()

    if (allowConnection == "Y"):
        print("The destination has been added to the list of known hosts\n")
        knownHostsFile.close()
        knownHostsFile = open("C:/ProgramData/PDS.comSoft/client/knownHosts", "a")
        knownHostsFile.write("\n" + str(HOST))
        knownHostsFile.close()
    else:
        print("\nThe connection will not be made")
        time.sleep(3)
        os.abort() # Kill the program


# Tell the user what's going on
print("Announcing presence to server...\n")
time.sleep(1.5)

# Send the connection message
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
        sock.connect((HOST, PORT))
        sock.sendall(bytes(name + " has established a connection", "utf-8"))
        sock.close()

except Exception as err: # Something went wrong while trying to send the message
    print("[!] - Failed to announce presence to server -- " + str(err))
    time.sleep(999)
    os.abort()


# Create a message to send to the remote computer
def createMessage():
    global message
    message = input("Message > ")
    if allowMessaging == True: # Makes sure to only send if the user is allowed to based on their rate caps
        if (message == "exit" or message == "quit" or message == "changeName" or message == "help" or message == "mute"):
            commandProcessor(message)
        else:
            sendMessage(message)


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
        print("\n[!] - Failed to send message -- " + str(err) + "\n")

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
        tempName = input("Enter new username > ") # Ask the user for a new name
        
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
        print("\n[Help]\n'help': get this message\n'exit' or 'quit': disconnect safely\n'changeName': change your name on the server\n'mute': toggle notifications")

    else:
        print("Command not found - did you type it right? [Use 'help' to get a list of safe commands]")
    
    print("") # Blank line

# Make sure the user doesn't spam - they get kicked if they do
def checkRate():
    global messageCount, allowMessaging, preventRecovery

    while True:
        if (messageCount >= spamLimit):
            print("\n[!] Anti-spam protection active [client.local.tooManyMessages()]")
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            allowMessaging = False
            preventRecovery = True
            time.sleep(4)
            sendMessage(" kicked for spam") # Forcefully disconnect the user
            os.abort()

# Decreases message count at a fixed rate
def rateTimer():
    global messageCount
    while True:
        if (messageCount > 0):
            while (messageCount != 0):
                time.sleep(1.5)
                messageCount -= 1


# Main process that lets the user enter messages
def mainLoop():
    if allowMessaging == True:
        createMessage()
        mainLoop()

# Start the messaging thread
mainThread = td(target=mainLoop, name="message processor core")
mainThread.start()

# Crash recovery
def crashRecovery():
    rec = Process(target=mainLoop, name="message processor core [recovered from crashRecovery]") # Recovery Process
    if ((td.is_alive(mainThread) == False) and (rec.is_alive() == False) and preventRecovery == False):
        if __name__ == '__main__':
            print("\n[recovery@localhost] Recovering from fatal error...")

            # Where multiprocessing comes in handy
            rec.start()
            rec.join()
    time.sleep(5) # Checks are only made every so often to save resources
    crashRecovery()


# Create all the service threads
checkerThread = td(target=checkRate, name="message counter")
rateThread = td(target=rateTimer, name="message counting timer")
checkerThread.start()
rateThread.start()

# Start the crash recovery service
crashRecovery()
