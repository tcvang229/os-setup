


# look at config-targets.conf and parse through the file
# for all entries in that config file, we'll need to
# copy the target files and create a new directory in configs
# folder.


def parseConfigFile():
    
    # List of tuples (fileURI, directoryName)
    validTuples = []
    with open("./config-targets.conf", "r") as file:
        for line in file:
            readLine(line, validTuples)
    return validTuples


def readLine(line, validTuples):
    validLine = ""
    for char in line:
        if char == "#":
            break
        validLine = validLine + char

    if (len(validLine.strip()) > 0):
        validTuple = parseLine(validLine)
        if len(validTuple) == 2:
            validTuples.append(validTuple)
    #return validLine

#def parseLine(validLine):
def parseLine(validLine):
    splittedLine = validLine.split(";")
    if len(splittedLine) > 2:
        print("BAD: Line is valid, it has more than 2 string values.")
        return ()
    return (splittedLine[0], splittedLine[1])

for line in parseConfigFile():
    print(line)

