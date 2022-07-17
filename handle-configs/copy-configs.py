import os


# look at config-targets.conf and parse through the file
# for all entries in that config file, we'll need to
# copy the target files and create a new directory in configs
# folder.

configDirectoryPath = "{}/.config/os-setup".format(os.getenv("HOME"))
configFilePath = configDirectoryPath + "/config-targets.conf"

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
        print("Config file for Os-Setup is not found. Os-Setup will now create a new config file for you.")
        createConfigFiles()
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


def createConfigFiles():
    """Creates the config folder for os-setup and directory in the user's home directory."""

    # Create directory only if it doesn't exist.
    if os.path.exists(configDirectoryPath) == False:
        os.mkdir(configDirectoryPath)

    # Create file only if it doesn't exist.
    if os.path.exists(configFilePath) == False:
        open(configFilePath, "x")


createConfigFiles()
for line in parseConfigFile():
    print(line)

