import urllib.request
import csv
import io
import updateHelper as uh

# NEW FIELD: EUROPEAN MILLIONAIRE MAKER ON 3FEB23


url = "https://www.national-lottery.co.uk/results/euromillions/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/euromillions/draw-history/csv", "currentNums\curEuNums.csv")


def getDrawNumber(string):
    euInfo = string.split(",")
    return euInfo[-1]


def getPrizeBreakdown(string):
    prizeUrl = url + "/prize-breakdown/" + string
    prizeWeb = urllib.request.urlopen(prizeUrl)

    allWinners = []
    allUKWinners = []
    allPrizes = []

    winnerFlag = False
    winnerBreakFlag = False
    winnerFinishFlag = False
    prizeFlag = False

    for line in prizeWeb:
        if winnerFlag&(winnerBreakFlag or winnerFinishFlag):
            if winnerBreakFlag:
                allWinners.append(uh.sort(line))
            winnerBreakFlag = False
            if winnerFinishFlag:
                allUKWinners.append(uh.sort(line))
                winnerFlag = False
                winnerFinishFlag = False
        if winnerFlag & (b"prize_breakdown_inline" in line):
            winnerBreakFlag = True
        if (b"winners_count_" in line) & (b"winners_count_13" not in line):
            winnerFlag = True
        if winnerFlag & (b"UK winners" in line):
            winnerFinishFlag = True
        if prizeFlag & (""!=uh.sort(line)):
            allPrizes.append(uh.sort(line))
            prizeFlag = False
        if (b"prize_per_player_" in line) & (b"prize_per_player_13" not in line):
            prizeFlag = True

    return (allWinners, allUKWinners, allPrizes)



jackpots = uh.getJackpots(url)

try:
    lastDatabaseEntry = uh.getLastLine("databases/euroDatabase.csv")
    with open("currentNums/curEuNums.csv", "r") as curData, open("databases/euroDatabase.csv", "a") as database:
        curData.readline()
        curEuro = curData.readline().replace("\n","")
        if curEuro in lastDatabaseEntry:
            print("Euromillions database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, ukWinners, prizes = getPrizeBreakdown(getDrawNumber(curEuro))
            # WE MIGHT WANT TO REMOVE UK MILLIONAIRE MAKER HERE!
            curEuro += (","+jackpot)
            for j in range(len(winners)):
                curEuro += (","+uh.removeCommas(winners[j]))
            for k in range(len(ukWinners)):
                curEuro += (","+uh.removeCommas(ukWinners[k]))
            for l in range(len(prizes)):
                curEuro += (","+uh.removeCommas(prizes[l]))
            curEuro += "\n"
            euroResToAdd = []
            while (curEuro != (lastDatabaseEntry+"\n")):
                euroResToAdd.append(curEuro)
                i += 1
                date, jackpot = jackpots[i]
                curEuro = curData.readline()
                winners, ukWinners, prizes = getPrizeBreakdown(getDrawNumber(curEuro))
                curEuro = curEuro.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curEuro += (","+uh.removeCommas(winners[j]))
                for k in range(len(ukWinners)):
                    curEuro += (","+uh.removeCommas(ukWinners[k]))
                for l in range(len(prizes)):
                    curEuro += (","+uh.removeCommas(prizes[l]))
                curEuro += "\n"
            numToAdd = len(euroResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(euroResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Euromillions database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    with open("currentNums/curEuNums.csv", "r") as curData, open("databases/euroDatabase.csv", "w") as database:
        euroLines = curData.read().splitlines()
        euroLinesSize = len(euroLines)-1
        while (euroLinesSize > 0):
            database.write(euroLines[euroLinesSize])
            date, jackpot = jackpots[euroLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(euroLines[euroLinesSize])
            winners, ukWinners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                database.write(","+uh.removeCommas(winners[j]))
            for k in range(len(ukWinners)):
                database.write(","+uh.removeCommas(ukWinners[k]))
            for l in range(len(prizes)):
                database.write(","+uh.removeCommas(prizes[l]))
            database.write("\n")
            euroLinesSize -= 1
