import urllib.request
import csv
import io
import updateHelper as uh

url = "https://www.national-lottery.co.uk/results/thunderball/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/thunderball/draw-history/csv", "currentNums\curThunNums.csv")


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
    lastDatabaseEntry = uh.getLastLine("databases/thunDatabase.csv")
    with open("currentNums/curThunNums.csv", "r") as curData, open("databases/thunDatabase.csv", "a") as database:
        curData.readline()
        curThun = curData.readline().replace("\n","")
        if curThun in lastDatabaseEntry:
            print("Thunderball database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getDrawNumber(curThun))
            curThun += (","+jackpot)
            for j in range(len(winners)):
                curThun += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curThun += (","+uh.removeCommas(prizes[k]))
            curThun += "\n"
            thunResToAdd = []
            while (curThun != (lastDatabaseEntry+"\n")):
                thunResToAdd.append(curThun)
                i += 1
                date, jackpot = jackpots[i]
                curThun = curData.readline()
                winners, prizes = getPrizeBreakdown(getDrawNumber(curThun))
                curThun = curThun.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curThun += (","+uh.removeCommas(winners[j]))
                for k in range(len(prizes)):
                    curThun += (","+uh.removeCommas(prizes[k]))
                curThun += "\n"
            numToAdd = len(thunResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(thunResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Thunderball database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    with open("currentNums/curThunNums.csv", "r") as curData, open("databases/thunDatabase.csv", "w") as database:
        thunLines = curData.read().splitlines()
        thunLinesSize = len(thunLines)-1
        while (thunLinesSize > 0):
            database.write(thunLines[thunLinesSize])
            date, jackpot = jackpots[thunLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(thunLines[thunLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                database.write(","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                database.write(","+uh.removeCommas(prizes[k]))
            database.write("\n")
            thunLinesSize -= 1
