from codecs import ignore_errors
import os
import shutil

configDirectoryPath = "{}/.config/os-setup".format(os.getenv("HOME"))
configFilePath = configDirectoryPath + "/config-targets.conf"
configBackupPath = "{}/.os-setup-configs-backup".format(os.getenv("HOME"))

cacheBasePath = "{}/.cache".format(os.getenv("HOME"))
cacheDirectoryPath = cacheBasePath + "/os-setup"

# This is a .conf file that serves as a cache to compare and contrast
# for updates in comparison to the primary .conf file. 
cacheFilePath = cacheDirectoryPath + "/config-targets-cache.conf" 

def parseConfigFile(filePath):
    """Parses the config-targets.conf file to copy all targeted 
    config files and create and store them in the designated directory. 
    Returns a list of tuples that contain valid lines read from the
    config-targets.conf file."""

    # List of tuples (fileURI, directoryName)
    validTuples = []

    try:
        # Go through each line in the file and find the valid lines 
        #with open("./config-targets.conf", "r") as file:
        with open(filePath, "r") as file:
            for line in file:
                createAndAddValidTuple(line, validTuples)
            return validTuples
    except FileNotFoundError:
        print("ERROR: Config file for Os-Setup is not found. Os-Setup will now create a new config file for you. Update the newly created config file that Os-Setup created and rerun Os-Setup.")
        createConfigFile()
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

def createConfigFile():
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

def createCacheConfigFile():
    """ Creates the cache config file for history purposes. We'll use the cache config
    file to compare and contrast to see if there are any removed target files to copy.
    If any target files are removed from the config file, the cache config file will be
    used to determine what target files are still valid or invalid. """

    if os.path.exists(cacheFilePath):
        return
    
    if os.path.exists(cacheBasePath) == False:
        os.mkdir(cacheBasePath)
    
    if os.path.exists(cacheDirectoryPath) == False:
        os.mkdir(cacheDirectoryPath)

    if os.path.exists(configFilePath) == False:
        open(cacheFilePath, "x")
    else:
        updateCacheFile()

def removeUntargetedDirectories():
    """ Removes directories that are no longer targeted in the config file. """
    currentTargets = parseConfigFile(configFilePath)
    cachedTargets = parseConfigFile(cacheFilePath)

    directoriesToRemove = []
    for targetFile in cachedTargets:
        if targetFile not in currentTargets:
            directoriesToRemove.append(targetFile[1].strip())

    for directory in directoriesToRemove:
        try:
            shutil.rmtree(configBackupPath + "/{}".format(directory), ignore_errors = True)
        except FileNotFoundError:
            print("ERROR: Unable to remove back up directory, it doesn't exist.")
    if len(directoriesToRemove) > 0:
        updateCacheFile()

def updateCacheFile():
    """ Updates cache config file. """
    shutil.copy(configFilePath, cacheFilePath)


def copyConfigFiles():
    """Using the config-targets.conf, copies the targeted config files into
    the ~/.os-setup-configs-backup folder."""
    for line in parseConfigFile(configFilePath):
        uri = configBackupPath + "/{}".format(line[1].strip())

        # Create directory if there's no directory.
        if os.path.exists(uri) == False:
            os.mkdir(uri)

        shutil.copy(line[0], uri)
        print("Copying: {}".format(line[0]))

createCacheConfigFile()
createConfigFile()
removeUntargetedDirectories()
copyConfigFiles()
updateCacheFile()
