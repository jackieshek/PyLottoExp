import urllib.request
import csv
import io
import updateHelper as uh

url = "https://www.national-lottery.co.uk/results/euromillions-hotpicks/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/euromillions-hotpicks/draw-history/csv", "currentNums\curEHPNums.csv")


def getDrawNumber(string):
    sflInfo = string.split(",")
    return sflInfo[-1]


def getPrizeBreakdown(string):
    prizeUrl = url + "/prize-breakdown/" + string
    prizeWeb = urllib.request.urlopen(prizeUrl)

    allWinners = []
    allPrizes = []
    winnerFlag = False
    winnerBreakFlag = False
    prizeFlag = False
    for line in prizeWeb:
        if winnerFlag&winnerBreakFlag:
            allWinners.append(uh.sort(line))
            winnerFlag = False
            winnerBreakFlag = False
        if winnerFlag & (b"prize_breakdown_inline" in line):
            winnerBreakFlag = True
        if b"winners_count_" in line:
            winnerFlag = True
        if prizeFlag & (""!=uh.sort(line)):
            allPrizes.append(uh.sort(line))
            prizeFlag = False
        if b"prize_per_player_" in line:
            prizeFlag = True

    return (allWinners, allPrizes)


jackpots = uh.getJackpots(url)


try:
    lastDatabaseEntry = uh.getLastLine("databases/eHPDatabase.csv")
    with open("currentNums/curEHPNums.csv", "r") as curData, open("databases/eHPDatabase.csv", "a") as database:
        curData.readline()
        curEHP = curData.readline().replace("\n","")
        if curEHP in lastDatabaseEntry:
            print("Euromillions HotPicks database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getDrawNumber(curEHP))
            curEHP += (","+jackpot)
            for j in range(len(winners)):
                curEHP += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curEHP += (","+uh.removeCommas(prizes[k]))
            curEHP += "\n"
            eHPResToAdd = []
            while (curEHP != (lastDatabaseEntry+"\n")):
                eHPResToAdd.append(curEHP)
                i += 1
                date, jackpot = jackpots[i]
                curEHP = curData.readline()
                winners, prizes = getPrizeBreakdown(getDrawNumber(curEHP))
                curEHP = curEHP.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curEHP += (","+uh.removeCommas(winners[j]))
                for k in range(len(prizes)):
                    curEHP += (","+uh.removeCommas(prizes[k]))
                curEHP += "\n"
            numToAdd = len(eHPResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(eHPResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Euromillions HotPicks database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    with open("currentNums/curEHPNums.csv", "r") as curData, open("databases/eHPDatabase.csv", "w") as database:
        eHPLines = curData.read().splitlines()
        eHPLinesSize = len(eHPLines)-1
        while (eHPLinesSize > 0):
            database.write(eHPLines[eHPLinesSize])
            date, jackpot = jackpots[eHPLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(eHPLines[eHPLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                database.write(","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                database.write(","+uh.removeCommas(prizes[k]))
            database.write("\n")
            eHPLinesSize -= 1
