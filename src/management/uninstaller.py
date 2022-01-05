# Uninstaller that will work for version 1.0.6 upwards

# Imports
import time, os, sys, shutil

# Constants
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/Shoutout" # Where the data is
RUNPATH = DRIVELETTER + ":/Users/" + os.getlogin() + "/Desktop/Shoutout" # Where the runable files are


os.system("")

# Ask the user if they're sure
print("\u001b[31mWARNING: Continuing with this operation will remove ALL data relating to Shoutout from your device, INCLUDING SAVED DATA!")
print("The data CANNOT be recovered after deletion!\u001b[0m")
allowContinue = input("Are you sure you want to continue? [Y/N] \x10 ").capitalize()

# Uninstalling
def run(ac):
    if (ac == "N"):
        os.abort()

    elif (ac == "Y"):
        try:
            print("\nUninstalling...")
            time.sleep(1)
            print("\u001b[31mRemoving app data...")
            shutil.rmtree(path=DATAPATH, ignore_errors=True)

            time.sleep(1)

            print("Removing executable files...")
            shutil.rmtree(path=RUNPATH, ignore_errors=True)

            time.sleep(1)
            print("\u001b[32;1mUninstalled!")
            time.sleep(3)
        
        except:
            print("Failed to remove: [unknown_err]")

    print("\u001b[0m")

run(allowContinue)