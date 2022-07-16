import subprocess
import sys

xrandrReset = "xrandr -s 0"
xrandrPrimary = "xrandr --output eDP-1 --primary --auto"
nitrogenRestore = "nitrogen --restore"

def getConnectedMonitors():
    """ Returns a list of connected monitors. """
    output = subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()
    return [line.split()[0] for line in output if " connected " in line]


def runCommand(commandString):
    """ Run shell commands using subprocess. """
    process = subprocess.Popen(commandString.split(), stdout=subprocess.PIPE)
    process.communicate()
    processReturnCode = process.returncode
    #print("returncode: {}".format(processReturnCode))
   
    
    if processReturnCode >= 0:
        return

    # If process fails, re-run the process and 
    # give it 2 seconds before timeout exception. 
    processRerunCounter = 1
    while processReturnCode < 0 or processRerunCounter < 10:
        process = subprocess.Popen(commandString.split(), stdout=subprocess.PIPE)
        process.communicate(timeout = 2)
        processReturnCode = process.returncode

        # Break loop when return code is OK
        if processReturnCode >= 0:
            return

def setDisplays(commandString):
    try:
        # Reset xrandr to avoid display bugs
        runCommand(xrandrReset)

        # Setting the displays
        runCommand(commandString)

        # Restoring nitrogen wallpaper
        runCommand(nitrogenRestore)
    except TimeoutExpired as error: 
        print("timeoutExpired: {error}")
    except Exception as error:
        print("exception: {error}")


def start(*monitorSettings):
    """ Function for handling arguments when executing this script. """
    connectedMonitors = getConnectedMonitors()
    match monitorSettings[0].lower():
        case "auto":
            # Set all connected monitors
            command = "xrandr"
            counter = 0
            for monitor in connectedMonitors:
                if counter == 0:
                    command = command + " --output {} --primary --auto".format(monitor)
                else:
                    command = command + " --output {} --auto --left-of {}".format(monitor, connectedMonitors[counter - 1])

                counter = counter + 1

            setDisplays(command)

        case "primary":
            setDisplays(xrandrPrimary)
            


if __name__ == '__main__':
    """ When script starts, get the command arguments and start the script. """

    if (len(sys.argv) == 1):
        start("auto")
    else:
        start(sys.argv[1])



# take in user parameters for 
    # program edp
        # assuming edp is middle
    # program edp right hdmi left
    # program edp left hdmi right
    # program default
        # should be able to display all monitors,
        # odering and placing shouldn't matter
# print out all monitors
# store monitors in memory ? maybe in file later?
# set up formats:
    # edp-1 primary middle
    # hdmi-1 primary middle, edp-1 right
    # hdmi-1 primary middle, edp-1 left
    # default auto
        # should be able to connect all monitors,
        # ordering and placing shouldn't matter



