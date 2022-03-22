import urllib.request
import csv
import io

url = "https://www.national-lottery.co.uk/results/lotto/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/lotto/draw-history/csv", "curLNums.csv")

def getLastLine(file):
    with open(file, "r") as test:
        lines = test.read().splitlines()
        last_line = lines[-1]
        return last_line

def sort(utf8):
    string = utf8.decode("utf8").strip()
    return string

def convertDate(string):
    day, space, tail = string.partition(" ")
    newDate = tail.replace(" ","-")
    return newDate

def removeCommas(string):
    commaRemoved = string.replace(",","")
    return commaRemoved

def getJackpots():
    web = urllib.request.urlopen(url)
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

def clearXML(utf8):
    noSpace = sort(utf8)
    head, bracket1, tail = noSpace.partition(">")
    data, bracket2, rest = tail.partition("<")
    return data

def getBallSet(string):
    lottoInfo = string.split(",")
    return lottoInfo[10]

def getPrizeBreakdown(string):
    prizeUrl = url + "/prize-breakdown/" + string
    prizeWeb = urllib.request.urlopen(prizeUrl)

    allWinners = []
    allPrizes = []
    winnerFlag = False
    winnerBreakFlag = False
    prizeFlag = False
    rolldown = False
    for line in prizeWeb:
        if winnerFlag&winnerBreakFlag:
            allWinners.append(sort(line))
            winnerFlag = False
            winnerBreakFlag = False
        if winnerFlag & (b"prize_breakdown_inline" in line):
            winnerBreakFlag = True
        if b"winners_count_" in line:
            winnerFlag = True
        if prizeFlag & (""!=sort(line)):
            if ("<" not in sort(line)):
                allPrizes.append(sort(line))
                prizeFlag = False
                rolldown = True
        if rolldown:
            if b"Free Lotto Lucky Dip +" in line:
                allPrizes.append(sort(line))
                rolldown = False
        if b"prize_per_player_" in line:
            prizeFlag = True

    return (allWinners, allPrizes)
        
            
    

jackpots = getJackpots()

# we will check if we have a local database for the lotto numbers
try:
    lastDatabaseEntry = getLastLine("lottoDatabase.csv")
    # we will start updating the local file, as we found a file
    with open("curLNums.csv", "r") as curData, open("lottoDatabase.csv", "a") as database:
        # we will read the first line, which contains the headers to the columns
        curData.readline()
        curLotto = curData.readline().replace("\n","")
        if (curLotto in lastDatabaseEntry):
            # database is up to date, we do not need to do anything
            print("Database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getBallSet(curLotto))
            curLotto += (","+jackpot+","+str(winners)+","+str(prizes)+"\n")
            lottoResToAdd = []
            while (curLotto != (lastDatabaseEntry+"\n")):
                lottoResToAdd.append(curLotto)
                i += 1
                date, jackpot = jackpots[i]
                curLotto = curData.readline()
                winners, prizes = getPrizeBreakdown(getBallSet(curLotto))
                curLotto = curLotto.replace("\n",(","+jackpot+","+str(winners)+","+str(prizes)+"\n"))
            numToAdd = len(lottoResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(lottoResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    # we do not currently have an active database file for the lotto numbers
    # so we will make one and fill it
    with open("curLNums.csv", "r") as curData, open("lottoDatabase.csv", "w") as database:
        lottoLines = curData.read().splitlines()
        lottoLinesSize = len(lottoLines)-1
        while (lottoLinesSize > 0):
            database.write(lottoLines[lottoLinesSize])
            date, jackpot = jackpots[lottoLinesSize-1]
            database.write(","+jackpot)
            ballSet = getBallSet(lottoLines[lottoLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            database.write(","+str(winners)+","+str(prizes))
            database.write("\n")
            lottoLinesSize -= 1
