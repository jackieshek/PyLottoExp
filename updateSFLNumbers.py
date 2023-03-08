import urllib.request
import csv
import io
import updateHelper as uh

url = "https://www.national-lottery.co.uk/results/set-for-life/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/set-for-life/draw-history/csv", "currentNums\curSFLNums.csv")


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
    lastDatabaseEntry = uh.getLastLine("databases/sflDatabase.csv")
    with open("currentNums/curSFLNums.csv", "r") as curData, open("databases/sflDatabase.csv", "a") as database:
        curData.readline()
        curSFL = curData.readline().replace("\n","")
        if curSFL in lastDatabaseEntry:
            print("Set-For-Life database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getDrawNumber(curSFL))
            curSFL += (","+jackpot)
            for j in range(len(winners)):
                curSFL += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curSFL += (","+uh.removeCommas(prizes[k]))
            curSFL += "\n"
            sflResToAdd = []
            while (curSFL != (lastDatabaseEntry+"\n")):
                sflResToAdd.append(curSFL)
                i += 1
                date, jackpot = jackpots[i]
                curSFL = curData.readline()
                winners, prizes = getPrizeBreakdown(getDrawNumber(curSFL))
                curSFL = curSFL.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curSFL += (","+uh.removeCommas(winners[j]))
                for k in range(len(prizes)):
                    curSFL += (","+uh.removeCommas(prizes[k]))
                curSFL += "\n"
            numToAdd = len(sflResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(sflResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Set-For-Life database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    with open("currentNums/curSFLNums.csv", "r") as curData, open("databases/sflDatabase.csv", "w") as database:
        sflLines = curData.read().splitlines()
        sflLinesSize = len(sflLines)-1
        while (sflLinesSize > 0):
            database.write(sflLines[sflLinesSize])
            date, jackpot = jackpots[sflLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(sflLines[sflLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                database.write(","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                database.write(","+uh.removeCommas(prizes[k]))
            database.write("\n")
            sflLinesSize -= 1
