import os
import matplotlib.pyplot as plot
import numpy as np
import math
import manipulateDatabase as md

# NEED TO UPDATE THIS METHOD; MAYBE MAKE GENERAL METHOD LIKE MD METHODS??
def barForAllNumsLotto(csvFile, bonus=None):
    n = 59
    counts = [0]*(n+1)
    bonus = [0]*(n+1)
    allBalls = md.getAllBallsLotto(csvFile)
    for i in range(len(allBalls)):
        for j in range(len(allBalls[i])):
            if bonus:
                if j == 6:
                    bonus[allBalls[i][j]] += 1
                else:
                    counts[allBalls[i][j]] += 1
            else:
                counts[allBalls[i][j]] += 1
    
    loc = np.arange(n)
    width = 0.5

    fig, ax = plot.subplots(figsize=(20.0,12.5))

    if bonus:
        cp = ax.bar(loc, counts[1:], width, label="Non-Bonus ball")
        bp = ax.bar(loc, bonus[1:], width, bottom=counts[1:], label="Bonus ball", color="red")

        labels = []
        for k in range(n):
            labels.append(k+1)

        ax.set_ylabel("Counts")
        ax.set_title("Total times each ball was drawn in Lotto")
        ax.set_xticks(loc, labels)
        ax.legend()

        ax.bar_label(cp, label_type="center")
        ax.bar_label(bp, label_type="center")

        cwd = os.getcwd()
        plot.savefig(cwd+"\\charts\\ballsBar.png", bbox_inches="tight")
    else:
        cp = ax.bar(loc, counts[1:], width)

        labels = []
        for k in range(n):
            labels.append(k+1)

        ax.set_ylabel("Counts")
        ax.set_title("Total times each ball was drawn in Lotto")
        ax.set_xticks(loc, labels)

        ax.bar_label(cp, label_type="center")

        cwd = os.getcwd()
        plot.savefig(cwd+"\\charts\\ballsBar.png", bbox_inches="tight")


def barForAllNums(csvFile, game, bonus=None):
    match game:
        case lotto:
            return barForAllNumsLotto(csvFile, bonus)


def barForJackpotWinNums(csvFile):
    n = 59
    counts = [0]*(n+1)
    allInfo = md.getAllInfo(csvFile)

    for i in range(len(allInfo)):
        if md.isJackpotWinnerList(allInfo[i]):
            for j in range(len(allInfo[i][1])):
                counts[allInfo[i][1][j]] += 1

    loc = np.arange(n)
    width = 0.5

    fig, ax = plot.subplots(figsize=(20.0,12.5))

    p = ax.bar(loc, counts[1:], width)

    labels = []
    for k in range(n):
        labels.append(k+1)

    ax.set_ylabel("Counts")
    ax.set_title("Total number of times each ball was drawn in a Winning Lotto")
    ax.set_xticks(loc, labels)

    ax.bar_label(p, label_type="center")

    cwd = os.getcwd()
    plot.savefig(cwd+"\\charts\\winningBallsBar.png", bbox_inches="tight")


def barForAllWinners(csvFile):
    n = 6
    totalWinners = [0]*6
    allWinners = md.getAllWinners(csvFile)

    for i in range(len(allWinners)):
        for j in range(6):
            totalWinners[j] += allWinners[i][j]

    loc = np.arange(6)
    width = 0.5

    fig, ax = plot.subplots(figsize=(10.0,20.0))

    p = ax.bar(loc, totalWinners, width)

    labels = ["Match 6",
              "Match 5 + Bonus",
              "Match 5",
              "Match 4",
              "Match 3",
              "Match 2"]

    ax.set_ylabel("Totals")
    ax.set_title("Total number of winners for each prize category since FILL THIS")
    ax.set_xticks(loc, labels)

    ax.bar_label(p, label_type="center")

    cwd = os.getcwd()
    plot.savefig(cwd+"\\charts\\totalWinners.png")


def barForWinners(array):
    date = array[0]
    winners = array[6]

    loc = np.arange(len(winners))
    width = 0.5

    fig, ax = plot.subplots()

    p = ax.bar(loc, winners, width)

    labels = ["Match 6",
          "Match 5 + Bonus",
          "Match 5",
          "Match 4",
          "Match 3",
          "Match 2"]

    ax.set_ylabel("Number of winners")
    ax.set_title("Number of winners for each prize category on %r." % date)
    ax.set_xticks(loc, labels)

    ax.bar_label(p, label_type="center")

    cwd = os.getcwd()
    plot.savefig(cwd+"\\charts\\winnersBar%r.png" % date)
    

''' MAKE LABELS FOR X AXIS AS DATES
    '''
def lineForWinCat(csvFile, cat):

    allWinners = md.getAllWinners(csvFile)
    n = len(allWinners)
    catStr = ""
    match cat:
        case 0:
            catStr = "Match 6"
        case 1:
            catStr = "Match 5 + Bonus"
        case 2:
            catStr = "Match 5"
        case 3:
            catStr = "Match 4"
        case 4:
            catStr = "Match 3"
        case 5:
            catStr = "Match 2"
    prizeCat = [0]*(n)
    

    for i in range(n):
        prizeCat[i] += allWinners[i][cat]

    loc = np.arange(0, n, 1)

    fig, ax = plot.subplots(figsize=(25.0,10.0))
    ax.plot(loc, prizeCat)
    ax.set(xlabel="draws", ylabel="Number of Winners",
           title="Number of winners across all draws for prize category: "+catStr)

    cwd = os.getcwd()
    plot.savefig(cwd+"\\charts\\linePrizeCat"+catStr+".png", bbox_inches="tight")


''' PLOT THIS BINOMIAL WITH THE EXPECTED BINOMIAL
    expected probability would be 1/59 * 6(or 7 if including bonus)
    '''
def binomialForNum(csvFile, num):

    count = 0
    
    allBalls = md.getAllBallsLotto(csvFile)
    n = len(allBalls)
    for i in range(n):
        for j in range(len(allBalls[i])):
            if allBalls[i][j] == num:
                count += 1

    p = count/n
    exp = 7/59 # 7/59 is including the bonus ball; 6/59 otherwise

    k = np.arange(0, n, 1)
    f = []
    e = []
    for i in range (n):
        f.append((math.comb(n,k[i]))*(p**k[i])*((1-p)**(n-k[i])))
        e.append((math.comb(n,k[i]))*(exp**k[i])*((1-exp)**(n-k[i])))

    fig, ax = plot.subplots()
    ax.plot(k,f, label="Observed distribution")
    ax.plot(k,e, "r--", label="Expected distribution")
    ax.set(xlabel="n", ylabel="probability",
           title="Binomial distribution of ball no.'"+str(num)+"'")
    ax.legend()

    cwd = os.getcwd()
    plot.savefig(cwd+"\\charts\\binomialBallNo"+str(num)+".png", bbox_inches="tight")


''' Create graphs binomial distribution graphs for tuples, such as:
    (one number in the 10s and one number in the 20s) see how often such a pair shows up,
    comparing to expected probability
    '''



barForAllNums("lottoDatabase.csv", True)
#barForJackpotWinNums("lottoDatabase.csv")
#binomialForNum("lottoDatabase.csv",11)
#barForAllWinners("lottoDatabase.csv")
#lineForWinCat("lottoDatabase.csv",5)
