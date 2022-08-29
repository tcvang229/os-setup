import os
import datetime
import json
import operator

configDirectoryPath = "{}/.config/pf-calculator".format(os.getenv("HOME"))
configFilePath =  configDirectoryPath + "/pf-calculator-database.json"
paidKeyWord = "income"

def setData(data):
    """ Writes to the json file updating the data within the file. """

    if len(data) > 0:
        # Sort the list based on the due date of bills.
        data.sort(key=operator.itemgetter("dueDate"))

    with open(configFilePath, "w") as outfile:
        json.dump({"bills": data}, outfile)

def isNumber(billAmount):
    """ Checks if the incoming parameter is an integer or float. """
    try:
        int(billAmount)
        return True
    except:
        pass

    try:
         float(billAmount)
         return True
    except:
        return False
    
def isNegative(billAmount):
    """ Checks if the incoming parameter is negative. """
    try:
        if int(billAmount) < 0:
            return True
    except:
        pass

    try:
         if float(billAmount) < 0:
            return True
    except:
        return False


def validateBillRecord(billString):
    """ Method for bill validation before caching user input for bills. """

    columns = billString.split(" ")
    if len(columns) != 3:
        print("Invalid amount of columns: Columns are: Due Date (mm/dd/yy), BillName (no spaces), Bill Amount.")
        return False

    try:
        datetime.datetime.strptime(columns[0], "%m/%d/%y")
    except:
        print("Invalid date format: Date formats should be: mm/dd/yy.")
        return False

    if isNumber(columns[2]) == False:
        print("Invalid bill amount: Bill amounts may only be numeric values, e.g., 1 or 150 or 351.31.")

    if isNegative(columns[2]) == True:
        print("Invalid bill amount: Can't be a negative value.")
        return False

    return True

# Create directory and file if it doesn't exist.
if os.path.exists(configDirectoryPath) is False:
    print("Configuration directory and file was not found, currently creating the directory and file now.")
    try:
        os.mkdir(configDirectoryPath)
        print("Created: \n{}".format(configDirectoryPath))
    except:
        print("Failed to be created: \n{}".format(configDirectoryPath))

    try:
        setData([])
        print("Created: \n{}".format(configFilePath))
    except:
        print("Failed to be created: \n{}".format(configFilePath))

elif os.path.exists(configFilePath) is False:
    print("Configuration file was not found, currently creating file now.")
    try:
        setData([])
        print("Created: \n{}".format(configFilePath))
    except:
        print("Failed to be created: \n{}".format(configFilePath))

newBills = []
print("Enter in bills. When finished, enter in an empty record to finish input and show the data sheet.")
print("Valid columns: [Due Date, Bill Name, Bill Amount].\n")
print("e.g., [02/04/08, Phone Bill, 140.88].\n")
userInput = input()
while len(userInput) > 0:
    if userInput == "clear":
        setData([])
        break

    if validateBillRecord(userInput):
        columns = userInput.split(" ")
        newBills.append({"dueDate": columns[0], "billName": columns[1], "billAmount": columns[2]})

    userInput = input()

# Extending the newly added bills to the currently existing data.
currentData = json.load(open(configFilePath))
currentData["bills"].extend(newBills)
setData(currentData["bills"])

print("Displaying data table...")
print("Due Date , Bill Name , Bill Amount, Running Balance")
runningBalance = 0;
for bill in currentData["bills"]:
    if bill["billName"] == paidKeyWord:

        try:
            runningBalance = int(bill["billAmount"]) + runningBalance
        except:
            runningBalance = float(bill["billAmount"]) + runningBalance

    else:

        try:
            runningBalance = runningBalance - int(bill["billAmount"])
        except:
            runningBalance = runningBalance - float(bill["billAmount"])

    dataRow = "{0}, {1}, {2}, {3}".format(bill["dueDate"], bill["billName"], bill["billAmount"], runningBalance)
    print(dataRow)


