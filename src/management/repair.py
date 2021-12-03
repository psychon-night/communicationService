# Installer for version 1.0.5
SOFTWARE_VERSION = "1.0.5"

# Imports
import time, os, sys
from urllib import request as urlRequest

os.system("color")

DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])

DATAPATH = DRIVELETTER + ":/ProgramData/PDS.comSoft" # Where the data files are
CWD = os.path.dirname(__file__) # The current directory
RUNPATH = DRIVELETTER + ":/Users/" + os.getlogin() + "/Desktop/pds.comsoft" # Where the runnable files are

# Get the user's consent to continue
print("Privacy notice: This repairer needs to access potentially sensitive information to complete the requested action.")
print("If you choose to allow it, this repairer will access your hard drive to read and write files")
allowContinue = input("Do you want to continue? [Y/N] \x10 ").capitalize()

if allowContinue:
    # Do nothing
    allowContinue = allowContinue

else:
    # Exit out of the installer without modifying the system files
    os.abort()


import uninstaller # Runs the uninstaller program

os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[                              ]\u001b[0m")
if True: # The other code was already indented and I don't want to fix it
        
    # The new runnable files
    try:
        newClient = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/client.py").read(), "'UTF-8'")
        newServer = str(urlRequest.urlopen("https://247086.github.io/communicationService/src/server.py").read(), "'UTF-8'")

        installerFile = open(__file__, "r").read()
        uninstallerFile = open(CWD + "/uninstaller.py", "r").read()
        repairFile = open(CWD + "/repair.py", "r").read()
        
    except Exception as err:
        print("Failed to download the new files: " + str(err))
        time.sleep(999)

    time.sleep(0.75)

    try:
        # Make the directories
        os.mkdir(DATAPATH) # Create the data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[#####                         ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(DATAPATH + "/client") # Create the client data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[##########                    ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(DATAPATH + "/server") # Create the server data path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[###############               ]\u001b[0m")
        time.sleep(0.75)
        os.mkdir(RUNPATH) # Create the runnable file path
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[####################          ]\u001b[0m")
        time.sleep(0.75)

        # Create the runnable files inside the desktop folder
        open(RUNPATH + "/client.py", "x").write(newClient)
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[######################        ]\u001b[0m")
        time.sleep(0.75)
        open(RUNPATH + "/server.py", "x").write(newServer)
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[#########################     ]\u001b[0m")
        time.sleep(0.75)

        # Create the required files in the data folder
        open(DATAPATH + "/softwareVersion", "x").write(SOFTWARE_VERSION) # Create the file that stores the software version
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[############################  ]\u001b[0m")
        time.sleep(0.75)
        open(DATAPATH + "/client/knownHosts", "x").close() # Create the client's known hosts file
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[############################# ]\u001b[0m")
        time.sleep(0.75)
        open(DATAPATH + "/server/bannedIP", "x").close() # Create the server's banned IPs file
        os.system('cls'); print("Installing on drive " + DRIVELETTER + " in /ProgramData/PDS.comSoft\n"); print("\u001b[33m[##############################]\u001b[0m")
        time.sleep(0.75)

        os.mkdir(RUNPATH + "/management")
        open(RUNPATH + "/management/installer.py", "x").write(installerFile)
        open(RUNPATH + "/management/uninstaller.py", "x").write(uninstallerFile)
        open(RUNPATH + "/management/repair.py", "x").write(repairFile)
    
    except Exception as err:
        print("Failed to repair the installation: " + str(err))
        time.sleep(999)

print("\n\nDone!")
time.sleep(5)
