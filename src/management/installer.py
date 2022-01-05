# Installer for version 1.0.6
SOFTWARE_VERSION = "1.0.6"

# Imports
import time, os, sys, shutil
from urllib import request as urlRequest

os.system("color")

DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])

DATAPATH = DRIVELETTER + ":/ProgramData/Shoutout" # Where the data files are
CWD = os.path.dirname(__file__) # The current directory
RUNPATH = DRIVELETTER + ":/Users/" + os.getlogin() + "/Desktop/Shoutout" # Where the runnable files are

# Web-based constants
try:
    LATESTVERSION = str(urlRequest.urlopen("https://247086.github.io/communicationService/latestVersion.html").read(), "'UTF-8'")
except Exception as err:
    print("There was a problem while getting the latest version ID: " + str(err) + ". Please check your network connection, and that 247086.github.io and github.com are reachable")
    time.sleep(999)

# Check if there's a new version available
try:
        version = open(DATAPATH + "/softwareVersion").read()

        if (int(str(version).strip("1.0.")) < int(str(LATESTVERSION).strip("1.0."))): # Checks if the user's trying to update to the same version
            NotImplemented
        
        else:
            print("You already have the latest version.")
            print("If you're trying to repair a broken installation, please use repair.py instead!")
            time.sleep(10)
            os.abort()


except: # Looks like there isn't an installation
    if (os.path.isdir(DATAPATH) == True and os.path.isfile(DATAPATH + "/version") == False):
        print("There's a problem with your installation!")
        time.sleep(999)

    else:
        NotImplemented # Keep going


try:
    print("Latest version: " + LATESTVERSION + "Current version: " + version)
except:
    NotImplemented # Ignore the error and keep going


newClient = None
newServer = None

# Second, make sure the src folder on the server is reachable
try:
    newClient = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/client.py").read(), "'UTF-8'")
    newServer = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/server.py").read(), "'UTF-8'")
    flags = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/data/runFlags.json").read(), "'UTF-8'")

except Exception as err:
    print("Failed to download the latest version's code: " + str(err))
    time.sleep(999)



os.system('')
print("Communication Software - Installer || Thank you for your support!")
print("Notice: This installer is for version 1.0.5 and later. \nIf your server owner requires you to use receiver.py for compatibility, do NOT update as receiver.py is now depricated and removed\n\n")


# Get the user's consent to continue
print("Privacy notice: This installer needs to access potentially sensitive information to complete the requested action.")
print("If you choose to allow it, this installer will access your hard drive to read and write files")
allowContinue = input("Do you want to continue? [Y/N] \x10 ").capitalize()

if allowContinue:
    NotImplemented

else:
    # Exit out of the installer without modifying the system files
    os.abort()




# First, check to see if the program's data folder already exists
dataExists = os.path.isdir(DATAPATH)
runnableExists = os.path.isdir(RUNPATH)


# Now, set the installer's mode
mode = None

if dataExists: # The data already exists and the installer only needs to update it
    mode = "update"
else:
    mode = "install" # Data does not exist, so create a fresh install



print("\nKeep this window open during the installation process!")


time.sleep(2.35)


# The main function to update data
if (mode == "update"): # Only update the data - 1.0.5 and later checks to make sure that receiver.py is removed

    if (runnableExists == False):
        print("!! The runnable files database is damaged or missing and must be re-written! This might take a moment... !!")
        time.sleep(2)
        import uninstaller
        import installer

    # New runnable files
    newClientFile = newClient
    newServerFile = newServer

    # Update the runnables
    os.system('cls'); print("Updating from version " + str(version) + " to " + LATESTVERSION); print("\u001b[33m[                              ]\u001b[0m")
    time.sleep(1)
    open(RUNPATH + "/client.py", "w").write(newClientFile)
    os.system('cls'); print("Updating from version " + str(version) + " to " + LATESTVERSION); print("\u001b[33m[########                      ]\u001b[0m")
    time.sleep(1)
    open(RUNPATH + "/server.py", "w").write(newServerFile)
    os.system('cls'); print("Updating from version " + str(version) + " to " + LATESTVERSION); print("\u001b[33m[###################           ]\u001b[0m")
    time.sleep(1)

    # Try to remove the receiver file
    try:
        os.remove(RUNPATH + "/receiver.py") # Delete receiver.py
        os.system('cls'); print("Updating from version " + version + " to " + LATESTVERSION); print("\u001b[33m[##############################]\u001b[0m")
    except:
        # File was already removed
        os.system('cls'); print("Updating from version " + version + " to " + LATESTVERSION); print("\u001b[33m[##############################]\u001b[0m")
    time.sleep(1)
    print("\nUpdate complete!")
    time.sleep(5)

else: # Create entirely new data
    os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[                              ]\u001b[0m")
    
    # The new runnable files (stored on Github)
    clientFile = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/client.py").read(), "'UTF-8'")
    serverFile = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/server.py").read(), "'UTF-8'")
    
    # Data
    flags = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/data/runFlags.json").read(), "'UTF-8'")

    time.sleep(0.75)

    try:
        # Make the directories
        os.mkdir(DATAPATH) # Create the data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[#####                         ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(DATAPATH + "/client") # Create the client data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[##########                    ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(DATAPATH + "/server") # Create the server data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[###############               ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(DATAPATH + "/data") # Create the data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[#################             ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(RUNPATH) # Create the runnable file path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[####################          ]\u001b[0m")
        time.sleep(0.75)

        # Create the runnable files inside the desktop folder
        open(RUNPATH + "/client.py", "x").write(clientFile)
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[######################        ]\u001b[0m")
        time.sleep(0.75)
        open(RUNPATH + "/server.py", "x").write(serverFile)
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[#########################     ]\u001b[0m")
        time.sleep(0.75)

        # Create the required files in the data folder
        open(DATAPATH + "/softwareVersion", "x").write(SOFTWARE_VERSION) # Create the file that stores the software version
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[############################  ]\u001b[0m")
        time.sleep(0.75)
        open(DATAPATH + "/client/knownHosts", "x").close() # Create the client's known hosts file
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[############################# ]\u001b[0m")
        time.sleep(0.75)
        open(DATAPATH + "/server/bannedIP", "x").close() # Create the server's banned IPs file
        open(DATAPATH + "/data/runFlags", "x").write(flags) # Create the server's flags file, where the user can change specific flags to effect software operation
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/Shoutout\n"); print("\u001b[33m[##############################]\u001b[0m")
        time.sleep(0.75)
    
    except Exception as err:
        print("\u001b[31;1mAn unexpected problem occured while trying to install the application, preventing the install from continuing: " + str(err))
        time.sleep(2)
        print("\u001b[0mYou might have a broken installation on your device.")
        allowContinue = input("Do you want this installer to try to remove the broken installation, then re-attempt the installation? [Y/N] > ").capitalize()

        if (allowContinue == "Y"):
            import uninstaller # Runs it on import
            os.system('cls')
            import installer # Runs it on import


    time.sleep(1)
    print("\nDone - you can find the newly installed (runnable) files on your desktop, in the folder named 'Shoutout'")
    time.sleep(7)