import socket, time, winsound, os
from threading import Thread as td

HOST, PORT = input("Server IP > "), 1500 # Set up the host and port values

message = "" # User's message text
name = input("Enter name > ") # User's name

# Variables used for reducing spam
messageCount = 0
allowMessaging = True

print("") # Blank space for readability

# Tell the user what's going on
print("Announcing presence to server... If the program closes, the server either refused the connection or is unreachable")
time.sleep(0.75)
print("Connecting...")
time.sleep(4)
print("")


# Send the connection message
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
    sock.connect((HOST, PORT))
    sock.sendall(bytes(name + " has established a connection", "utf-8"))
    sock.close()


# Create a message to send to the remote computer
def createMessage():
    global message
    message = input("Message > ")
    if allowMessaging == True: # Makes sure to only send if the user is allowed to based on their rate caps
        if (message == "exit" or message == "quit"):
            commandProcessor(message)
        elif (message == "changeName"):
            commandProcessor(message)
        else:
            sendMessage(message)


# Send the message the user just created
def sendMessage(data):
    global messageCount
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Sets a temporary socket connection
        
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(name + ": " + data, "utf-8"))
        sock.close()
        messageCount += 1 # Increase how many messages they have sent


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


# Make sure the user doesn't spam
def checkRate():
    global messageCount, allowMessaging

    while True:
        if (messageCount >= 7):
            print("\n[!] Woah, slow down! You're sending too many messages! --- [Only you can see this alert]")
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            while (messageCount != 0):
                allowMessaging = False
            allowMessaging = True

# Decreases the amount of messages they have sent at a 1:1 ratio
def rateTimer():
    global messageCount
    while True:
        if (messageCount > 0):
            while (messageCount != 0):
                time.sleep(1)
                messageCount -= 1


# Create a seperate thread for timed message processing. If the user tries to send too many messages, they will be rate-capped
checkerThread = td(target=checkRate, name="threaded_message_counter")
rateThread = td(target=rateTimer, name="threaded_message_counter_timing")
checkerThread.start()
rateThread.start()

# Main process that lets the user enter messages
while True:
    if allowMessaging == True:
        createMessage()