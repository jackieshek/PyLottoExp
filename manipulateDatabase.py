import statistics


MACHINE_SET = ["Arthur","Guinevere","Lancelot","Merlin"]
BALL_SET = [1,2,3,4,5,6,7,8,9,10,11]

# Object class for one night's result
class DrawResult:

    def __init__(self, string):
        self.date = getDate(string)
        self.balls = getBalls(string)
        self.machine = getMachine(string)
        self.ballset = getBallSet(string)
        self.drawNo = getDrawNo(string)
        self.jackpot = getJackpot(string)
        self.winners = getWinners(string)
        self.prizes = getPrizes(string)

    def isJackpotWin(self):
        return self.winners[0] >= 1

    


# Returns the date of the Lotto result
def getDate(string):
    date, comma, tail = string.partition(",")
    return date


# Converts the date to a completely numerical format
def dateConverter(string):
    monthNum = None
    day, hyphon, tail = string.partition("-")
    month, hyphon2, tail2 = tail.partition("-")
    match month:
        case "Jan":
            monthNum = "01"
        case "Feb":
            monthNum = "02"
        case "Mar":
            monthNum = "03"
        case "Apr":
            monthNum = "04"
        case "May":
            monthNum = "05"
        case "Jun":
            monthNum = "06"
        case "Jul":
            monthNum = "07"
        case "Aug":
            monthNum = "08"
        case "Sep":
            monthNum = "09"
        case "Oct":
            monthNum = "10"
        case "Nov":
            monthNum = "11"
        case "Dec":
            monthNum = "12"
    return year+hyphon+monthNum+hyphon2+day


# Returns an array of the 7 Lotto balls from a given Lotto result
def getBalls(string):
    date, com0, tail0 = string.partition(",")
    firBall, com1, tail1 = tail0.partition(",")
    secBall, com2, tail2 = tail1.partition(",")
    thiBall, com3, tail3 = tail2.partition(",")
    fouBall, com4, tail4 = tail3.partition(",")
    fifBall, com5, tail5 = tail4.partition(",")
    sixBall, com6, tail6 = tail5.partition(",")
    bonBall, com7, rest = tail6.partition(",")
    return ([int(firBall),
             int(secBall),
             int(thiBall),
             int(fouBall),
             int(fifBall),
             int(sixBall),
             int(bonBall)])


# Returns an array of arrays of all the 7 Lotto balls results from the specified file, namely our database
def getAllBalls(csvFile):
    allInfo = getAllInfo(csvFile)
    allBalls = []
    for info in allInfo:
        allBalls.append(info[1])
    return allBalls


# Returns the machine used for the set of results
def getMachine(string):
    info = string.split(",")
    return info[9]


def getBallSet(string):
    info = string.split(",")
    return info[8]


def getDrawNo(string):
    info = string.split(",")
    return info[10]


def getJackpot(string):
    info = string.split(",")
    return info[11]


def commaRemover(string):
    noComma = string.replace(",","")
    return noComma


def getWinners(string):
    winnersStart = string.find("[")+1
    winnersEnd = string.find("]")
    unsorted = string[winnersStart:winnersEnd]
    winners = []
    while unsorted != "":
        start = unsorted.find("'")
        end = unsorted[start+1:].find("'")
        winner = unsorted[start+1:start+end+1]
        winners.append(int(commaRemover(winner)))
        unsorted = unsorted[start+end+2:]
    return winners


def getPrizes(string):
    winnersEnd = string.find("]")
    unsorted = string[winnersEnd:]
    prizes = []
    while unsorted != "]":
        start = unsorted.find("'")
        end = unsorted[start+1:].find("'")
        prize = unsorted[start+1:start+end+1]
        prizes.append(prize)
        unsorted = unsorted[start+end+2:]
    return prizes


# Checks whether there is a jackpot winner for the lotto result given
def isJackpotWinner(string):
    winnerStart = string.find("[")+1
    if string[winnerStart:winnerStart+3] == "'1'":
        return True
    return False


def isJackpotWinnerList(array):
    if int(array[6][0]) >= 1:
        return True
    return False


def isRolldown(string):
    return "Rolldown" in string

''' Will likely change below method to return DrawResult class object'''
# This method puts the lotto balls into an array of numbers, appends the rest
''' RETURNS ARRAY:  array[0] = date
                    array[1] = drawn lotto balls
                    array[2] = ball set
                    array[3] = machine
                    array[4] = draw number
                    array[5] = jackpot
                    array[6] = winners array
                    array[7] = prizes array
    '''
def getInfo(string):
    substr, bracket, rest = string.partition("[")
    unsInfo = substr.split(",")
    winners = getWinners(string)
    prizes = getPrizes(string)
    nums = []
    for i in range(7):
        nums.append(int(unsInfo[i+1]))
    info = []
    info.append(unsInfo[0])
    info.append(nums)
    for j in range(4):
        info.append(unsInfo[8+j])
    info.append(winners)
    info.append(prizes)
    return info


''' Will likely change below method to return array of DrawResults instead '''
# Whole file version of getInfo. Returns all Lotto results, with the 7 Lotto balls placed into an array.
# There is an optional argument, machine, allowing filter results based on the machine specified.
''' SET OTHER OPTIONAL ARGUMENTS LIKE: if results have a jackpot winner
                                       option for specific ball set
                                       if jackpot > £2,000,000
                                       if it is a rollover
                                       '''
def getAllInfo(csvFile, machine=None):
    if machine is None:
        with open(csvFile, "r") as file:
            lottoResults = file.read().splitlines()
            allInfo = []
            for lottoRes in lottoResults:
                allInfo.append(getInfo(lottoRes))
            return allInfo
    elif machine in MACHINE_SET:
        with open(csvFile, "r") as file:
            lottoResults = file.read().splitlines()
            allInfo = []
            for lottoRes in lottoResults:
                if (getMachine(lottoRes) == machine):
                    allInfo.append(getInfo(lottoRes))
            return allInfo
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % MACHINE_SET)


def getAllWinners(csvFile, machine=None):
    if machine is None:
        with open(csvFile, "r") as file:
            lottoResults = file.read().splitlines()
            winners = []
            for lottoRes in lottoResults:
                winners.append(getWinners(lottoRes))
            return winners
    elif machine in MACHINE_SET:
        with open(csvFile, "r") as file:
            lottoResults = file.read().splitlines()
            winners = []
            for lottoRes in lottoResults:
                if (getMachine(lottoRes) == machine):
                    winners.append(getWinners(lottoRes))
            return winners
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % MACHINE_SET)


# This method returns the all Lotto numbers that were picked in the i-th position
# i.e. if i=1 then it returns an array containing all the Lotto numbers that were picked 1st on each result
def getAllBallsByi(arrayOfArrays, i):
    validNumbers = [1,2,3,4,5,6,7]
    if i in validNumbers:
        allBallsi = []
        numberOfLottos = len(arrayOfArrays)
        for j in range(numberOfLottos):
            allBallsi.append(arrayOfArrays[j][i])
        return allBallsi
    else:
        raise ValueError("'i' must be valid number between 1 to 7, as there are only 7 Lotto numbers picked for each draw")


# Returns a rearranged array of arrays sorted by their picks
# i.e. [all balls picked 1st, all balls picked 2nd, ... , all balls picked last (bonus balls)]
def getAllBallsByPick(arrayOfArrays):
    allBallsSortedByPick = []
    for i in range(7):
        allBallsSortedByPick.append(getAllBallsByi(arrayOfArrays, i))
    return allBallsSortedByPick


# Return an array of means for each array in an array of arrays
def getAllMeans(arrayOfArrays):
    meanArray = []
    for i in range(len(arrayOfArrays)):
        meanArray.append(statistics.mean(arrayOfArrays[i]))
    return meanArray


# Return an array of the standard deviation for each array in an array of arrays
def getAllStDev(arrayOfArrays):
    stDevArray = []
    for i in range(len(arrayOfArrays)):
        stDevArray.append(statistics.stdev(arrayOfArrays[i]))
    return stDevArray


    # define the get all quantiles for each number, split into perhaps 6 intervals
def getAllQuantiles(arrayOfArrays, noOfQuants=None):
    quanArray = []
    if noOfQuants == None:
        for i in range(len(arrayOfArrays)):
            quanArray.append(statistics.quantiles(arrayOfArrays[i], n=6))
        return quanArray
    elif isinstance(noOfQuants, int):
        for i in range(len(arrayOfArrays)):
            quanArray.append(statistics.quantiles(arrayOfArrays[i], n=noOfQuants))
        return quanArray
    else:
        raise ValueError("The number of quantiles specified must be an integer")
