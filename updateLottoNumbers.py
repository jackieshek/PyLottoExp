import urllib.request
import csv
import io
import updateHelper as uh

# COULD ATTEMPT TO REWRITE WITH HMTL.PARSER CLASS OR BEAUTIFUL SOUP LIBRARY

url = "https://www.national-lottery.co.uk/results/lotto/draw-history"
urllib.request.urlretrieve("https://www.national-lottery.co.uk/results/lotto/draw-history/csv", "currentNums\curLNums.csv")

# Helper function that retrieves the draw
def getDrawNumber(string):
    lottoInfo = string.split(",")
    return lottoInfo[10]

# Function which returns a tuple of two arrays, one containing all the winners for each prize, the other containing all the prizes
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
            allWinners.append(uh.sort(line))
            winnerFlag = False
            winnerBreakFlag = False
        if winnerFlag & (b"prize_breakdown_inline" in line):
            winnerBreakFlag = True
        if b"winners_count_" in line:
            winnerFlag = True
        if prizeFlag & (""!=uh.sort(line)):
            if ("<" not in uh.sort(line)):
                allPrizes.append(uh.sort(line))
                prizeFlag = False
                rolldown = True #WE NEED THIS HIGHER UP IN SEPERATE IF CHECK FOR BASE_FUND_ROLLDOWN
        if rolldown:
            if b"Free Lotto Lucky Dip +" in line:
                allPrizes.append(uh.sort(line))
                rolldown = False
        if b"prize_per_player_" in line:
            prizeFlag = True

    return (allWinners, allPrizes)
        
            
    

jackpots = uh.getJackpots(url)

# we will check if we have a local database for the lotto numbers
try:
    lastDatabaseEntry = uh.getLastLine("databases/lottoDatabase.csv")
    # we will start updating the local file, as we found a file
    with open("currentNums/curLNums.csv", "r") as curData, open("databases/lottoDatabase.csv", "a") as database:
        # we will read the first line, which contains the headers to the columns
        curData.readline()
        curLotto = curData.readline().replace("\n","")
        if (curLotto in lastDatabaseEntry):
            # database is up to date, we do not need to do anything
            print("Lotto database is up to date :)")
            curData.close()
            database.close()
        else:
            i = 0
            date, jackpot = jackpots[i]
            winners, prizes = getPrizeBreakdown(getDrawNumber(curLotto))
            curLotto += (","+jackpot)
            for j in range(len(winners)):
                curLotto += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curLotto += (","+uh.removeCommas(prizes[k]))
            curLotto += "\n"
            lottoResToAdd = []
            while (curLotto != (lastDatabaseEntry+"\n")):
                lottoResToAdd.append(curLotto)
                i += 1
                date, jackpot = jackpots[i]
                curLotto = curData.readline()
                winners, prizes = getPrizeBreakdown(getDrawNumber(curLotto))
                #curLotto = curLotto.replace("\n",(","+jackpot+","+str(winners)+","+str(prizes)+"\n"))
                curLotto = curLotto.replace("\n",(","+jackpot))
                for j in range(len(winners)):
                    curLotto += (","+uh.removeCommas(winners[j]))
                for k in range(len(prizes)):
                    curLotto += (","+uh.removeCommas(prizes[k]))
                curLotto += "\n"
            numToAdd = len(lottoResToAdd)
            numAdded = numToAdd
            while (numToAdd > 0):
                database.write(lottoResToAdd[numToAdd-1])
                numToAdd -= 1
            print("Lotto database is now up to date: added "+str(numAdded)+" line(s)")
except FileNotFoundError:
    # we do not currently have an active database file for the lotto numbers
    # so we will make one and fill it
    with open("currentNums/curLNums.csv", "r") as curData, open("databases/lottoDatabase.csv", "w") as database:
        lottoLines = curData.read().splitlines()
        lottoLinesSize = len(lottoLines)-1
        while (lottoLinesSize > 0):
            database.write(lottoLines[lottoLinesSize])
            date, jackpot = jackpots[lottoLinesSize-1]
            database.write(","+jackpot)
            ballSet = getDrawNumber(lottoLines[lottoLinesSize])
            winners, prizes = getPrizeBreakdown(ballSet)
            for j in range(len(winners)):
                curLotto += (","+uh.removeCommas(winners[j]))
            for k in range(len(prizes)):
                curLotto += (","+uh.removeCommas(prizes[k]))
            database.write("\n")
            lottoLinesSize -= 1
