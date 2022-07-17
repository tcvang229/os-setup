import os
import shutil

configDirectoryPath = "{}/.config/os-setup".format(os.getenv("HOME"))
configFilePath = configDirectoryPath + "/config-targets.conf"
configBackupPath = "{}/.os-setup-configs-backup".format(os.getenv("HOME"))

def parseConfigFile():
    """Parses the config-targets.conf file to copy all targeted 
    config files and create and store them in the designated directory. 
    Returns a list of tuples that contain valid lines read from the
    config-targets.conf file."""

    # List of tuples (fileURI, directoryName)
    validTuples = []

    try:
        # Go through each line in the file and find the valid lines 
        #with open("./config-targets.conf", "r") as file:
        with open(configFilePath, "r") as file:
            for line in file:
                createAndAddValidTuple(line, validTuples)
            return validTuples
    except FileNotFoundError:
        print("Config file for Os-Setup is not found. Os-Setup will now create a new config file for you. Update the newly created config file that Os-Setup created and rerun Os-Setup.")
        createUsersActiveConfigFile()
        return []

def createAndAddValidTuple(line, validTuples):
    """Parses through the line string and creates tuples based on
    if the passed in line was correct."""

    # This string value doesn't account for the parts of the string
    # where the pound-sign/hash-tag character starts. The pound-sign/
    # hash-tag are comments in the config-targets.conf file.
    unvalidatedLine = ""
    for char in line:
        if char == "#":
            break
        unvalidatedLine = unvalidatedLine + char

    # Only find valid tuples if validLine isn't empty.
    if (len(unvalidatedLine.strip()) > 0):
        validTuple = parseLine(unvalidatedLine)
        if len(validTuple) == 2:
            validTuples.append(validTuple)

def parseLine(unvalidatedLine):
    """Splits the validLine by a semi-colon delmiter and returns a tuple. Depending on 
    if the unvalidatedLine is a valid string, an empty tuple or value-filled tuple will
    be returned."""
    splittedLine = unvalidatedLine.split(";")
    if len(splittedLine) > 2 or len(splittedLine) < 2:
        print("BAD: Line is invalid, skipping line in config file.")
        return ()
    return (splittedLine[0], splittedLine[1])

def createUsersActiveConfigFile():
    """Creates the config folder for os-setup and directory in the user's home directory."""

    configFilePathExists = os.path.exists(configFilePath)
    configBackupPathExists = os.path.exists(configBackupPath)

    if configFilePathExists and configBackupPathExists:
        return

    # Create files and folders where needed.

    if os.path.exists(configDirectoryPath) == False:
        os.mkdir(configDirectoryPath)

    if configFilePathExists == False:
        open(configFilePath, "x")

    if configBackupPathExists == False:
        os.mkdir(configBackupPath)


def copyConfigFiles():
    """Using the config-targets.conf, copies the targeted config files into
    the ~/.os-setup-configs-backup folder."""
    for line in parseConfigFile():
        uri = configBackupPath + "/{}".format(line[1])
        shutil.copyfile(line[0], uri)

createUsersActiveConfigFile()
copyConfigFiles()
