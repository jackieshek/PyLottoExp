import urllib.request
import csv
import io
import updateHelper as uh

url = "https://www.national-lottery.co.uk/results/lotto-hotpicks/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/lotto-hotpicks/draw-history/csv", "currentNums\curLHPNums.csv")


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
    lastDatabaseEntry = uh.getLastLine("databases/lHPDatabase.csv")
    with open("currentNums/curLHPNums.csv", "r") as curData, open("databases/lHPDatabase.csv", "a") as database:
        curData.readline()
        curLHP = curData.readline().replace("\n","")
        if curLHP in lastDatabaseEntry:
            print("Lotto HotPicks database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getDrawNumber(curLHP))
            curLHP += (","+jackpot)
            for j in range(len(winners)):
                curLHP += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curLHP += (","+uh.removeCommas(prizes[k]))
            curLHP += "\n"
            lHPResToAdd = []
            while (curLHP != (lastDatabaseEntry+"\n")):
                lHPResToAdd.append(curLHP)
                i += 1
                date, jackpot = jackpots[i]
                curLHP = curData.readline()
                winners, prizes = getPrizeBreakdown(getDrawNumber(curLHP))
                curLHP = curLHP.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curLHP += (","+uh.removeCommas(winners[j]))
                for k in range(len(prizes)):
                    curLHP += (","+uh.removeCommas(prizes[k]))
                curLHP += "\n"
            numToAdd = len(lHPResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(lHPResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Lotto HotPicks database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    with open("currentNums/curLHPNums.csv", "r") as curData, open("databases/lHPDatabase.csv", "w") as database:
        lHPLines = curData.read().splitlines()
        lHPLinesSize = len(lHPLines)-1
        while (lHPLinesSize > 0):
            database.write(lHPLines[lHPLinesSize])
            date, jackpot = jackpots[lHPLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(lHPLines[lHPLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                database.write(","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                database.write(","+uh.removeCommas(prizes[k]))
            database.write("\n")
            lHPLinesSize -= 1
