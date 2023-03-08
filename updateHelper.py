import urllib.request
import csv
import io

# Function to retrieve the last line on our csv database
def getLastLine(file):
    with open(file, "r") as test:
        lines = test.read().splitlines()
        last_line = lines[-1]
        return last_line

# Function that translate a utf8 line into string, also clears all blankspaces
def sort(utf8):
    string = utf8.decode("utf8").strip()
    return string

# Helper function to make all dates in a uniform format
def convertDate(string):
    day, space, tail = string.partition(" ")
    newDate = tail.replace(" ","-")
    return newDate

# Helper function to removes all commas in a string
def removeCommas(string):
    commaRemoved = string.replace(",","")
    return commaRemoved

# Helper function that removes xml brackets
# NOT CURRENTLY USED - MAY BE DELETED LATER
def clearXML(utf8):
    noSpace = sort(utf8)
    head, bracket1, tail = noSpace.partition(">")
    data, bracket2, rest = tail.partition("<")
    return data

# Helper function in printing the page to output terminal - DEBUGGING PURPOSES
def printPage(string):
    prizeUrl = url + "/prize-breakdown/" + string
    web = urllib.request.urlopen(prizeUrl)

    for line in web:
        print(sort(line))

# Function which returns all the jackpot amounts for each draw found on the official lotto website
def getJackpots(inputUrl):
    web = urllib.request.urlopen(inputUrl)
    tableHeaderFlag = True
    dateCellFlag = False
    tableCellBlockFlag = False
    jackpotCellFlag = False
    unsortedJackpot = []
    for line in web:
        if tableCellBlockFlag & (dateCellFlag or jackpotCellFlag):
            dateCellFlag = False
            jackpotCellFlag = False
            tableCellBlockFlag = False
            unsortedJackpot.append(sort(line))
        if (b"table_cell table_cell_1" in line) & tableHeaderFlag:
            tableHeaderFlag = False
        if (b"table_cell table_cell_1" in line) & (tableHeaderFlag==False):
            dateCellFlag = True
        if (b"table_cell table_cell_2" in line) & (tableHeaderFlag==False):
            jackpotCellFlag = True
        if (b"table_cell_block" in line) & (dateCellFlag or jackpotCellFlag):
            tableCellBlockFlag = True

    half = int(len(unsortedJackpot)/2)
    i = 0
    j = 0
    jackpot = []
    for j in range(half):
        jackpot.append((convertDate(unsortedJackpot[i]),removeCommas(unsortedJackpot[i+1])))
        i += 2
        j += 1

    return jackpot
