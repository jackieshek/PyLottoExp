import statistics
import csv
import re


# REWRITE ALL THIS USING CSV PACKAGE.  USE DICTREADER
# WE DO NOT NEED A GET ALL INFO METHOD, JUST SPECIFIC INFO EXTRACTOR METHODS
#   LIKE GET ALL BALLS, ALL WINNERS ETC.

# EXPANDED TO OTHER NATIONAL LOTTERY GAMES SO SOME OF THESE METHODS WOULD NEED
#   TO BE UPDATED. MAY NEED TO IMPLEMENT CASES FOR DIFFERENT GAMES
#   AS IN GAME=LOTTO;EUROMILLIONS;ETC
#   NEED TO HAVE DIFFERENT GAME FIELD NAMES AS WELL SO LOTTO_FIELD_NAMES ETC
#   CAN DESIGN A GENERAL METHOD WHICH ASKS FOR NAME OF GAME THEN FILTERS TO
#   A SUB METHOD FOR THAT SPECIFIC GAME

LOTTO_MACHINE_SET = ["Arthur","Guinevere","Lancelot","Merlin"]
# Please note sfl and thunderballs share the same machines
SFL_MACHINE_SET = ["Excalibur 1","Excalibur 2","Excalibur 3","Excalibur 4","Excalibur 5","Excalibur 6"]
GAME_SET = ["lotto","euromillions","setForLife","lottoHotPicks","euroHotPicks","thunderball"]
BALL_SET = [1,2,3,4,5,6,7,8,9,10,11]
LOTTO_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5","BALL 6",
                     "BONUS BALL","BALL SET","MACHINE","DRAW NUMBER","JACKPOT",
                     "WINNER 1","WINNER 2","WINNER 3","WINNER 4","WINNER 5","WINNER 6",
                     "PRIZE 1","PRIZE 2","PRIZE 3","PRIZE 4","PRIZE 5","PRIZE 6"]
EURO_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5",
                    "LUCKY STAR 1","LUCKY STAR 2","UK MILLIONAIRE MAKER",
                    "EUROPEAN MILLIONAIRE MAKER","DRAW NUMBER","JACKPOT",
                    "WINNER:MATCH5+2STARS","WINNER:MATCH5+1STAR","WINNER:MATCH5",
                    "WINNER:MATCH4+2STARS","WINNER:MATCH4+1STAR","WINNER:MATCH3+2STARS",
                    "WINNER:MATCH4","WINNER:MATCH2+2STARS","WINNER:MATCH3+1STAR",
                    "WINNER:MATCH3","WINNER:MATCH1+2STARS","WINNER:MATCH2+1STAR","WINNER:MATCH2",
                    "PRIZE:MATCH5+2STARS","PRIZE:MATCH5+1STAR","PRIZE:MATCH5",
                    "PRIZE:MATCH4+2STARS","PRIZE:MATCH4+1STAR","PRIZE:MATCH3+2STARS",
                    "PRIZE:MATCH4","PRIZE:MATCH2+2STARS","PRIZE:MATCH3+1STAR",
                    "PRIZE:MATCH3","PRIZE:MATCH1+2STARS","PRIZE:MATCH2+1STAR",
                    "PRIZE:MATCH2"]
SFL_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5",
                   "LIFE BALL","BALL SET","MACHINE","DRAW NUMBER","JACKPOT",
                   "WINNER:MATCH5+LIFEBALL","WINNER:MATCH5","WINNER:MATCH4+LIFEBALL",
                   "WINNER:MATCH4","WINNER:MATCH3+LIFEBALL","WINNER:MATCH3",
                   "WINNER:MATCH2+LIFEBALL","WINNER:MATCH2",
                   "PRIZE:MATCH5+LIFEBALL","PRIZE:MATCH5","PRIZE:MATCH4+LIFEBALL",
                   "PRIZE:MATCH4","PRIZE:MATCH3+LIFEBALL","PRIZE:MATCH3",
                   "PRIZE:MATCH2+LIFEBALL","PRIZE:MATCH2"]
LHP_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5","BALL 6",
                   "BALL SET","MACHINE","DRAW NUMBER","JACKPOT",
                   "WINNER 1","WINNER 2","WINNER 3","WINNER 4","WINNER 5",
                   "PRIZE 1","PRIZE 2","PRIZE 3","PRIZE 4","PRIZE 5"]
EHP_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5",
                   "BALL SET","DRAW NUMBER","JACKPOT",
                   "WINNER 1","WINNER 2","WINNER 3","WINNER 4","WINNER 5",
                   "PRIZE 1","PRIZE 2","PRIZE 3","PRIZE 4","PRIZE 5"]
THUN_FIELD_NAMES = ["DRAW DATE","BALL 1","BALL 2","BALL 3","BALL 4","BALL 5",
                    "THUNDERBALL","BALL SET","MACHINE","DRAW NUMBER","JACKPOT",
                    "WINNER:MATCH5+THUNDERBALL","WINNER:MATCH5",
                    "WINNER:MATCH4+THUNDERBALL","WINNER:MATCH4",
                    "WINNER:MATCH3+THUNDERBALL","WINNER:MATCH3",
                    "WINNER:MATCH2+THUNDERBALL","WINNER:MATCH1+THUNDERBALL",
                    "WINNER:MATCH0+THUNDERBALL",
                    "PRIZE:MATCH5+THUNDERBALL","PRIZE:MATCH5",
                    "PRIZE:MATCH4+THUNDERBALL","PRIZE:MATCH4",
                    "PRIZE:MATCH3+THUNDERBALL","PRIZE:MATCH3",
                    "PRIZE:MATCH2+THUNDERBALL","PRIZE:MATCH1+THUNDERBALL",
                    "PRIZE:MATCH0+THUNDERBALL"]


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
    return int(year+monthNum+day)


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


# Helper function that checks if it's given an array, and then furthermore
# checks if each element in the array is an integer
def listChecker(array):
    if isinstance(array, list):
        for i in range(0,len(array)):
            if not isinstance(array[i], int):
                return False
        return True
    else:
        return False


def dateFormatChecker(string):
    if re.match("[0-3][0-9]-[A-Z][a-z]{2}-20[0-9]{2}", string):
        day, hyphen1, rest = string.partition("-")
        month, hyphen2, year = string.partition("-")
        if month in ["Jan","Mar","May","Jul","Aug","Oct","Dec"]:
            # 31 days
            if int(day) in range(1,32):
                return True
        elif month in ["Apr","Jun","Sep","Nov"]:
            # 30 days
            if int(day) in range(1,31):
                return True
        elif month is "Feb" and (int(year)%4==0):
            # 29 days
            if int(day) in range(1,30):
                return True
        elif month is "Feb":
            # 28 days
            if int(day) in range(1,29):
                return True
        else:
            return False
    else:
        return False


def lifeBallConverter(lifeBall):
    return int(lifeBall[:3])


# Returns an array of arrays of all the 7 Lotto balls from the specified database file
# -Note: if machine field is omitted returns all lotto ball results
#        else returns only those results from draws made by that machine
def getAllBallsLotto(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
            for result in reader:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                balls.append(int(result["BALL 6"]))
                balls.append(int(result["BONUS BALL"]))
                allBalls.append(balls)
        return allBalls
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
            for result in reader:
                if result["MACHINE"]==machine:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["BALL 6"]))
                    balls.append(int(result["BONUS BALL"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


# MIGHT WANT TO SEPERATE THE LUCKY STARS AS THEY ARE A COMPLETELY DIFFERENT
#   SET OF NUMBERS FROM THE MAIN 5 DRAWN BALLS
def getAllBallsEuro(csvFile):
    allBalls = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
        for result in reader:
            balls = []
            balls.append(int(result["BALL 1"]))
            balls.append(int(result["BALL 2"]))
            balls.append(int(result["BALL 3"]))
            balls.append(int(result["BALL 4"]))
            balls.append(int(result["BALL 5"]))
            balls.append(int(result["LUCKY STAR 1"]))
            balls.append(int(result["LUCKY STAR 2"]))
            allBalls.append(balls)
    return allBalls


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllBallsSFL(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
            for result in reader:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                balls.append(int(result["LIFE BALL"]))
                allBalls.append(balls)
        return allBalls
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
            for result in reader:
                if result["MACHINE"]==machine:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LIFE BALL"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllBallsLHP(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
            for result in reader:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                balls.append(int(result["BALL 6"]))
                allBalls.append(balls)
        return allBalls
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
            for result in reader:
                if result["MACHINE"]==machine:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LIFE BALL"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllBallsEHP(csvFile):
    allBalls = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
        for result in reader:
            balls = []
            balls.append(int(result["BALL 1"]))
            balls.append(int(result["BALL 2"]))
            balls.append(int(result["BALL 3"]))
            balls.append(int(result["BALL 4"]))
            balls.append(int(result["BALL 5"]))
            allBalls.append(balls)
    return allBalls


def getAllBallsThun(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
            for result in reader:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                balls.append(int(result["THUNDERBALL"]))
                allBalls.append(balls)
        return allBalls
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
            if result["MACHINE"]==machine:
                for result in reader:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["THUNDERBALL"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)


# Gameless version of getAllBalls, taking the game as an argument
def getAllBalls(csvFile, game, machine=None):
    match game:
        case lotto:
            return getAllBallsLotto(csvFile, machine)
        case euromillions:
            return getAllBallsEuro(csvFile)
        case setForLife:
            return getAllBallsSFL(csvFile, machine)
        case lottoHotPicks:
            return getAllBallsLHP(csvFile, machine)
        case euroHotPicks:
            return getAllBallsEHP(csvFile)
        case thunderball:
            return getAllBallsThun(csvFile, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


# Returns all ball results drawn with the ball number 'x'
#   e.g. if x = 46; then this method returns all ball results that contain 46
def getAllBallsDrawnWithXLotto(csvFile, x, machine=None):
    allBalls = []
    if x in range(1,60):
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if (x==int(result["BALL 1"]) or
                    x==int(result["BALL 2"]) or
                    x==int(result["BALL 3"]) or
                    x==int(result["BALL 4"]) or
                    x==int(result["BALL 5"]) or
                    x==int(result["BALL 6"]) or
                    x==int(result["BONUS BALL"])):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        balls.append(int(result["BONUS BALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        if (x==int(result["BALL 1"]) or
                        x==int(result["BALL 2"]) or
                        x==int(result["BALL 3"]) or
                        x==int(result["BALL 4"]) or
                        x==int(result["BALL 5"]) or
                        x==int(result["BALL 6"]) or
                        x==int(result["BONUS BALL"])):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            balls.append(int(result["BONUS BALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in lotto")


def getAllBallsDrawnWithXEuro(csvFile, x):
    allBalls = []
    if x in range(1,51):
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
            for result in reader:
                if (x==int(result["BALL 1"]) or
                    x==int(result["BALL 2"]) or
                    x==int(result["BALL 3"]) or
                    x==int(result["BALL 4"]) or
                    x==int(result["BALL 5"]) or
                    x==int(result["LUCKY STAR 1"]) or
                    x==int(result["LUCKY STAR 2"])):
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LUCKY STAR 1"]))
                    balls.append(int(result["LUCKY STAR 2"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in euromillions")


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllBallsDrawnWithXSFL(csvFile, x, machine=None):
    allBalls = []
    if x in range(1,48):
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if (x==int(result["BALL 1"]) or
                        x==int(result["BALL 2"]) or
                        x==int(result["BALL 3"]) or
                        x==int(result["BALL 4"]) or
                        x==int(result["BALL 5"]) or
                        x==int(result["LIFE BALL"])):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["LIFE BALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (x==int(result["BALL 1"]) or
                            x==int(result["BALL 2"]) or
                            x==int(result["BALL 3"]) or
                            x==int(result["BALL 4"]) or
                            x==int(result["BALL 5"]) or
                            x==int(result["LIFE BALL"])):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["LIFE BALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in set for life")


def getAllBallsDrawnWithXLHP(csvFile, x, machine=None):
    allBalls = []
    if x in range(1,60):
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if (x==int(result["BALL 1"]) or
                    x==int(result["BALL 2"]) or
                    x==int(result["BALL 3"]) or
                    x==int(result["BALL 4"]) or
                    x==int(result["BALL 5"]) or
                    x==int(result["BALL 6"])):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        if (x==int(result["BALL 1"]) or
                        x==int(result["BALL 2"]) or
                        x==int(result["BALL 3"]) or
                        x==int(result["BALL 4"]) or
                        x==int(result["BALL 5"]) or
                        x==int(result["BALL 6"])):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in lotto hot picks")


def getAllBallsDrawnWithXEHP(csvFile, x):
    allBalls = []
    if x in range(1,51):
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
            for result in reader:
                if (x==int(result["BALL 1"]) or
                    x==int(result["BALL 2"]) or
                    x==int(result["BALL 3"]) or
                    x==int(result["BALL 4"]) or
                    x==int(result["BALL 5"])):
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in euromillions hot picks")

    
def getAllBallsDrawnWithXThun(csvFile, x, machine=None):
    allBalls = []
    if x in range(1,40):
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if (x==int(result["BALL 1"]) or
                        x==int(result["BALL 2"]) or
                        x==int(result["BALL 3"]) or
                        x==int(result["BALL 4"]) or
                        x==int(result["BALL 5"]) or
                        x==int(result["THUNDERBALL"])):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["THUNDERBALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (x==int(result["BALL 1"]) or
                            x==int(result["BALL 2"]) or
                            x==int(result["BALL 3"]) or
                            x==int(result["BALL 4"]) or
                            x==int(result["BALL 5"]) or
                            x==int(result["THUNDERBALL"])):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["THUNDERBALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("Ball number given is not within the range of balls drawn in thunderball")


def getAllBallsDrawnWithX(csvFile, x, game, machine=None):
    match game:
        case lotto:
            # COULD CHECK X IN RANGE HERE INSTEAD??
            return getAllBallsDrawnWithXLotto(csvFile, x, machine)
        case euromillions:
            return getAllBallsDrawnWithXEuro(csvFile, x)
        case setForLife:
            return getAllBallsDrawnWithXSFL(csvFile, x, machine)
        case lottoHotPicks:
            return getAllBallsDrawnWithXLHP(csvFile, x, machine)
        case euroHotPicks:
            return getAllBallsDrawnWithXEHP(csvFile, x)
        case thunderball:
            return getAllBallsDrawnWithXThun(csvFile, x, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


# TO BE COMPLETED: LIST VERSION OF ABOVE - NAMELY RETURN ALL DRAWN SETS WITH BALLS IN THE LIST
def getAllBallsDrawnWithListLotto(csvFile, array, machine=None):
    allBalls = []
    # WE SHOULD CHECK IF THE ARRAY CONTAINS NUMBERS FIRST?
    if array: # USE ISINSTANCE([1,2],LIST) TO CHECK IF ARRAY IS LIST:
        if listChecker(array):
            if machine is None:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                    for result in reader:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        balls.append(int(result["BONUS BALL"]))
                        flag = True
                        for x in array:
                            if x not in balls:
                                flag = False
                                break
                        if flag:
                            allBalls.append(balls)
                return allBalls
            elif machine in LOTTO_MACHINE_SET:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                    for result in reader:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            balls.append(int(result["BONUS BALL"]))
                            flag = True
                            for x in array:
                                if x not in balls:
                                    flag = False
                                    break
                            if flag:
                                allBalls.append(balls)
                return allBalls
            else:
                raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


def getAllBallsDrawnWithListEuro(csvFile, array):
    allBalls = []
    if array:
        if listChecker(array):
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
                for result in reader:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LUCKY STAR 1"]))
                    balls.append(int(result["LUCKY STAR 2"]))
                    flag = True
                    for x in array:
                        if x not in balls:
                            flag = False
                            break
                    if flag:
                        allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllBallsDrawnWithListSFL(csvFile, array, machine=None):
    allBalls = []
    if array:
        if listChecker(array):
            if machine is None:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                    for result in reader:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["LIFE BALL"]))
                        flag = True
                        for x in array:
                            if x not in balls:
                                flag = False
                                break
                        if flag:
                            allBalls.append(balls)
                return allBalls
            elif machine in SFL_MACHINE_SET:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                    for result in reader:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["LIFE BALL"]))
                            flag = True
                            for x in array:
                                if x not in balls:
                                    flag = False
                                    break
                            if flag:
                                allBalls.append(balls)
                return allBalls
            else:
                raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


def getAllBallsDrawnWithListLHP(csvFile, array, machine=None):
    allBalls = []
    # WE SHOULD CHECK IF THE ARRAY CONTAINS NUMBERS FIRST?
    if array: # USE ISINSTANCE([1,2],LIST) TO CHECK IF ARRAY IS LIST:
        if listChecker(array):
            if machine is None:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                    for result in reader:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        flag = True
                        for x in array:
                            if x not in balls:
                                flag = False
                                break
                        if flag:
                            allBalls.append(balls)
                return allBalls
            elif machine in LOTTO_MACHINE_SET:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                    for result in reader:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            flag = True
                            for x in array:
                                if x not in balls:
                                    flag = False
                                    break
                            if flag:
                                allBalls.append(balls)
                return allBalls
            else:
                raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


def getAllBallsDrawnWithListEHP(csvFile, array):
    allBalls = []
    if array:
        if listChecker(array):
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
                for result in reader:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    flag = True
                    for x in array:
                        if x not in balls:
                            flag = False
                            break
                    if flag:
                        allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


def getAllBallsDrawnWithListThun(csvFile, array, machine=None):
    allBalls = []
    if array:
        if listChecker(array):
            if machine is None:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                    for result in reader:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["THUNDERBALL"]))
                        flag = True
                        for x in array:
                            if x not in balls:
                                flag = False
                                break
                        if flag:
                            allBalls.append(balls)
                return allBalls
            elif machine in SFL_MACHINE_SET:
                with open(csvFile, newline="") as file:
                    reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                    for result in reader:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["THUNDERBALL"]))
                            flag = True
                            for x in array:
                                if x not in balls:
                                    flag = False
                                    break
                            if flag:
                                allBalls.append(balls)
                return allBalls
            else:
                raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)
        else:
            raise ValueError("Please provide a list of numbers when using this method")
    else:
        raise ValueError("Please provide a list of numbers when using this method")


def getAllBallsDrawnWithList(csvFile, array, game, machine=None):
    match game:
        case lotto:
            return getAllBallsDrawnWithListLotto(csvFile, array, machine)
        case euromillions:
            return getAllBallsDrawnWithListEuro(csvFile, array)
        case setForLife:
            return getAllBallsDrawnWithListSFL(csvFile, array, machine)
        case lottoHotPicks:
            return getAllBallsDrawnWithListLHP(csvFile, array, machine)
        case euroHotPicks:
            return getAllBallsDrawnWithListEHP(csvFile, array)
        case thunderball:
            return getAllBallsDrawnWithListThun(csvFile, array, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


def getAllBallsOnLotto(csvFile, date, machine=None):
    if dateFormatChecker(date):
        allBalls = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        balls.append(int(result["BONUS BALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            balls.append(int(result["BONUS BALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOnEuro(csvFile, date):
    if dateFormatChecker(date):
        allBalls = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
            for result in reader:
                if result["DATE"]==date:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LUCKY STAR 1"]))
                    balls.append(int(result["LUCKY STAR 2"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOnSFL(csvFile, date, machine=None):
    if dateFormatChecker(date):
        allBalls = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["LIFE BALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["LIFE BALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOnLHP(csvFile, date, machine=None):
    if dateFormatChecker(date):
        allBalls = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOnEHP(csvFile, date):
    if dateFormatChecker(date):
        allBalls = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
            for result in reader:
                if result["DATE"]==date:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOnThun(csvFile, date, machine=None):
    if dateFormatChecker(date):
        allBalls = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["THUNDERBALL"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if result["DATE"]==date:
                        if result["MACHINE"]==machine:
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["THUNDERBALL"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("Date provided is not a valid date")


def getAllBallsOn(csvFile, date, game, machine=None):
    match game:
        case lotto:
            return getAllBallsOnLotto(csvFile, date, machine)
        case euromillions:
            return getAllBallsOnEuro(csvFile, date)
        case setForLife:
            return getAllBallsOnSFL(csvFile, date, machine)
        case lottoHotPicks:
            return getAllBallsOnLHP(csvFile, date, machine)
        case euroHotPicks:
            return getAllBallsOnEHP(csvFile, machine)
        case thunderball:
            return getAllBallsOnThun(csvFile, date, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


def getAllBallsBetweenLotto(csvFile, date1, date2, machine=None):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if (dateConverter(result["DATE"]) >= start) &
                    (dateConverter(result["DATE"]) <= end):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        balls.append(int(result["BONUS BALL"])
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (dateConverter(result["DATE"]) >= start) &
                        (dateConverter(result["DATE"]) <= end):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            balls.append(int(result["BONUS BALL"])
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetweenEuro(csvFile, date1, date2):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
            for result in reader:
                if (dateConverter(result["DATE"]) >= start) &
                (dateConverter(result["DATE"]) <= end):
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LUCKY STAR 1"]))
                    balls.append(int(result["LUCKY STAR 2"])
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetweenSFL(csvFile, date1, date2, machine=None):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if (dateConverter(result["DATE"]) >= start) &
                    (dateConverter(result["DATE"]) <= end):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["LIFE BALL"])
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (dateConverter(result["DATE"]) >= start) &
                        (dateConverter(result["DATE"]) <= end):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["LIFE BALL"])
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetweenLHP(csvFile, date1, date2, machine=None):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if (dateConverter(result["DATE"]) >= start) &
                    (dateConverter(result["DATE"]) <= end):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        allBalls.append(balls)
            return allBalls
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (dateConverter(result["DATE"]) >= start) &
                        (dateConverter(result["DATE"]) <= end):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["BALL 6"]))
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetweenEHP(csvFile, date1, date2):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
            for result in reader:
                if (dateConverter(result["DATE"]) >= start) &
                (dateConverter(result["DATE"]) <= end):
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetweenThun(csvFile, date1, date2, machine=None):
    if dateFormatChecker(date1) & dateFormatChecker(date2):
        allBalls = []
        start = dateConverter(date1)
        end = dateConverter(date2)
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if (dateConverter(result["DATE"]) >= start) &
                    (dateConverter(result["DATE"]) <= end):
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["THUNDERBALL"])
                        allBalls.append(balls)
            return allBalls
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
                for result in reader:
                    if result["MACHINE"]==machine:
                        if (dateConverter(result["DATE"]) >= start) &
                        (dateConverter(result["DATE"]) <= end):
                            balls = []
                            balls.append(int(result["BALL 1"]))
                            balls.append(int(result["BALL 2"]))
                            balls.append(int(result["BALL 3"]))
                            balls.append(int(result["BALL 4"]))
                            balls.append(int(result["BALL 5"]))
                            balls.append(int(result["THUNDERBALL"])
                            allBalls.append(balls)
            return allBalls
        else:
            raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)
    else:
        raise ValueError("A date provided is not a valid date")


def getAllBallsBetween(csvFile, date1, date2, game, machine=None):
    match game:
        case lotto:
            return getAllBallsBetweenLotto(csvFile, date1, date2, machine)
        case euromillions:
            return getAllBallsBetweenEuro(csvFile, date1, date2)
        case setForLife:
            return getAllBallsBetweenSFL(csvFile, date1, date2, machine)
        case lottoHotPicks:
            return getAllBallsBetweenLHP(csvFile, date1, date2, machine)
        case euroHotPicks:
            return getAllBallsBetweenEHP(csvFile, date1, date2)
        case thunderball:
            return getAllBallsBetweenThun(csvFile, date1, date2, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


def getAllJackpotWinnersLotto(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
            for result in reader:
                if int(reader["WINNER 1"])>0:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["BALL 6"]))
                    balls.append(int(result["BONUS BALL"]))
                    allBalls.append(balls)
        return allBalls
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LOTTO_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    if int(reader["WINNER 1"])>0:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        balls.append(int(result["BONUS BALL"]))
                        allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllJackpotWinnersEuro(csvFile):
    allBalls = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
        for result in reader:
            if int(reader["WINNER 1"])>0:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                balls.append(int(result["LUCKY STAR 1"]))
                balls.append(int(result["LUCKY STAR 2"]))
                allBalls.append(balls)
    return allBalls


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllJackpotWinnersSFL(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
            for result in reader:
                if int(reader["WINNER 1"])>0:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["LIFE BALL"]))
                    allBalls.append(balls)
        return allBalls
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=SFL_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    if int(reader["WINNER 1"])>0:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["LIFE BALL"]))
                        allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllJackpotWinnersLHP(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
            for result in reader:
                if int(reader["WINNER 1"])>0:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["BALL 6"]))
                    allBalls.append(balls)
        return allBalls
    elif machine in LHP_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=LHP_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    if int(reader["WINNER 1"])>0:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["BALL 6"]))
                        allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllJackpotWinnersEHP(csvFile):
    allBalls = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
        for result in reader:
            if int(reader["WINNER 1"])>0:
                balls = []
                balls.append(int(result["BALL 1"]))
                balls.append(int(result["BALL 2"]))
                balls.append(int(result["BALL 3"]))
                balls.append(int(result["BALL 4"]))
                balls.append(int(result["BALL 5"]))
                allBalls.append(balls)
    return allBalls


def getAllJackpotWinnersThun(csvFile, machine=None):
    allBalls = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
            for result in reader:
                if int(reader["WINNER 1"])>0:
                    balls = []
                    balls.append(int(result["BALL 1"]))
                    balls.append(int(result["BALL 2"]))
                    balls.append(int(result["BALL 3"]))
                    balls.append(int(result["BALL 4"]))
                    balls.append(int(result["BALL 5"]))
                    balls.append(int(result["THUNDERBALL"]))
                    allBalls.append(balls)
        return allBalls
    elif machine in THUN_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames=THUN_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    if int(reader["WINNER 1"])>0:
                        balls = []
                        balls.append(int(result["BALL 1"]))
                        balls.append(int(result["BALL 2"]))
                        balls.append(int(result["BALL 3"]))
                        balls.append(int(result["BALL 4"]))
                        balls.append(int(result["BALL 5"]))
                        balls.append(int(result["THUNDERBALL"]))
                        allBalls.append(balls)
        return allBalls
    else:
        raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)


def getAllJackpotWinners(csvFile, game, machine=None):
    match game:
        case lotto:
            return getAllJackpotWinnersLotto(csvFile, machine)
        case euromillions:
            return getAllJackpotWinnersEuro(csvFile)
        case setForLife:
            return getAllJackpotWinnersSFL(csvFile, machine)
        case lottoHotPicks:
            return getAllJackpotWinnersLHP(csvFile, machine)
        case euroHotPicks:
            return getAllJackpotWinnersEHP(csvFile)
        case thunderball:
            return getAllJackpotWinnersThun(csvFile, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)

'''
def getAll


def getAllJackpotsMoreThan(csvFile, game, moreThan, machine=None):
    match game:
        case lotto:
            return getAllJackpotsMoreThan(csvFile, moreThan, machine)
'''


def getAllWinnersLotto(csvFile, machine=None):
    allWinners = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                winners = []
                winners.append(result["WINNER 1"])
                winners.append(result["WINNER 2"])
                winners.append(result["WINNER 3"])
                winners.append(result["WINNER 4"])
                winners.append(result["WINNER 5"])
                winners.append(result["WINNER 6"])
                allWinners.append(winners)
        return allWinners
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    winners = []
                    winners.append(result["WINNER 1"])
                    winners.append(result["WINNER 2"])
                    winners.append(result["WINNER 3"])
                    winners.append(result["WINNER 4"])
                    winners.append(result["WINNER 5"])
                    winners.append(result["WINNER 6"])
                    allWinners.append(winners)
        return allWinners
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllWinnersEuro(csvFile):
    allWinners = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
        for result in reader:
            winners = []
            winners.append(result["WINNER:MATCH5+2STARS"])
            winners.append(result["WINNER:MATCH5+1STAR"])
            winners.append(result["WINNER:MATCH5"])
            winners.append(result["WINNER:MATCH4+2STARS"])
            winners.append(result["WINNER:MATCH4+1STAR"])
            winners.append(result["WINNER:MATCH3+2STARS"])
            winners.append(result["WINNER:MATCH4"])
            winners.append(result["WINNER:MATCH2+2STARS"])
            winners.append(result["WINNER:MATCH3+1STAR"])
            winners.append(result["WINNER:MATCH3"])
            winners.append(result["WINNER:MATCH1+2STARS"])
            winners.append(result["WINNER:MATCH2+1STAR"])
            winners.append(result["WINNER:MATCH2"])
            allWinners.append(winners)
    return allWinners


def getAllWinnersSFL(csvFile, machine=None):
    allWinners = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                winners = []
                winners.append(result["WINNER:MATCH5+LIFEBALL"])
                winners.append(result["WINNER:MATCH5"])
                winners.append(result["WINNER:MATCH4+LIFEBALL"])
                winners.append(result["WINNER:MATCH4"])
                winners.append(result["WINNER:MATCH3+LIFEBALL"])
                winners.append(result["WINNER:MATCH3"])
                winners.append(result["WINNER:MATCH2+LIFEBALL"])
                winners.append(result["WINNER:MATCH2"])
                allWinners.append(winners)
        return allWinners
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    winners = []
                    winners.append(result["WINNER:MATCH5+LIFEBALL"])
                    winners.append(result["WINNER:MATCH5"])
                    winners.append(result["WINNER:MATCH4+LIFEBALL"])
                    winners.append(result["WINNER:MATCH4"])
                    winners.append(result["WINNER:MATCH3+LIFEBALL"])
                    winners.append(result["WINNER:MATCH3"])
                    winners.append(result["WINNER:MATCH2+LIFEBALL"])
                    winners.append(result["WINNER:MATCH2"])
                    allWinners.append(winners)
        return allWinners
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllWinnersLHP(csvFile, machine=None):
    allWinners = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
            for result in reader:
                winners = []
                winners.append(result["WINNER 1"])
                winners.append(result["WINNER 2"])
                winners.append(result["WINNER 3"])
                winners.append(result["WINNER 4"])
                winners.append(result["WINNER 5"])
                allWinners.append(winners)
        return allWinners
    elif machine in LHP_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    winners = []
                    winners.append(result["WINNER 1"])
                    winners.append(result["WINNER 2"])
                    winners.append(result["WINNER 3"])
                    winners.append(result["WINNER 4"])
                    winners.append(result["WINNER 5"])
                    allWinners.append(winners)
        return allWinners
    else:
        raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllWinnersEHP(csvFile):
    allWinners = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EHP_FIELD_NAMES)
        for result in reader:
            winners = []
            winners.append(result["WINNER 1"])
            winners.append(result["WINNER 2"])
            winners.append(result["WINNER 3"])
            winners.append(result["WINNER 4"])
            winners.append(result["WINNER 5"])
            allWinners.append(winners)
    return allWinners


def getAllWinnersThun(csvFile, machine=None):
    allWinners = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
            for result in reader:
                winners = []
                winners.append(result["WINNER:MATCH5+THUNDERBALL"])
                winners.append(result["WINNER:MATCH5"])
                winners.append(result["WINNER:MATCH4+THUNDERBALL"])
                winners.append(result["WINNER:MATCH4"])
                winners.append(result["WINNER:MATCH3+THUNDERBALL"])
                winners.append(result["WINNER:MATCH3"])
                winners.append(result["WINNER:MATCH2+THUNDERBALL"])
                winners.append(result["WINNER:MATCH1+THUNDERBALL"])
                winners.append(result["WINNER:MATCH0+THUNDERBALL"])
                allWinners.append(winners)
        return allWinners
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    winners = []
                    winners.append(result["WINNER:MATCH5+THUNDERBALL"])
                    winners.append(result["WINNER:MATCH5"])
                    winners.append(result["WINNER:MATCH4+THUNDERBALL"])
                    winners.append(result["WINNER:MATCH4"])
                    winners.append(result["WINNER:MATCH3+THUNDERBALL"])
                    winners.append(result["WINNER:MATCH3"])
                    winners.append(result["WINNER:MATCH2+THUNDERBALL"])
                    winners.append(result["WINNER:MATCH1+THUNDERBALL"])
                    winners.append(result["WINNER:MATCH0+THUNDERBALL"])
                    allWinners.append(winners)
        return allWinners
    else:
        raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)


def getAllWinners(csvFile, game, machine=None):
    match game:
        case lotto:
            return getAllWinnersLotto(csvFile, machine)
        case euromillions:
            return getAllWinnersEuro(csvFile)
        case setForLife:
            return getAllWinnersSFL(csvFile, machine)
        case lottoHotPicks:
            return getAllWinnersLHP(csvFile, machine)
        case euroHotPicks:
            return getAllWinnersEHP(csvFile)
        case thunderball:
            return getAllWinnersThun(csvFile, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


#
def getAllPrizesLotto(csvFile, machine=None):
    allPrizes = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                prizes = []
                prizes.append(result["PRIZES 1"])
                prizes.append(result["PRIZES 2"])
                prizes.append(result["PRIZES 3"])
                prizes.append(result["PRIZES 4"])
                prizes.append(result["PRIZES 5"])
                prizes.append(result["PRIZES 6"])
                allPrizes.append(prizes)
        return allPrizes
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    prizes = []
                    prizes.append(result["PRIZES 1"])
                    prizes.append(result["PRIZES 2"])
                    prizes.append(result["PRIZES 3"])
                    prizes.append(result["PRIZES 4"])
                    prizes.append(result["PRIZES 5"])
                    prizes.append(result["PRIZES 6"])
                    allPrizes.append(prizes)
        return allPrizes
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllPrizesEuro(csvFile):
    allPrizes = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames=EURO_FIELD_NAMES)
        for result in reader:
            prizes = []
            prizes.append(result["PRIZE:MATCH5+2STARS"])
            prizes.append(result["PRIZE:MATCH5+1STAR"])
            prizes.append(result["PRIZE:MATCH5"])
            prizes.append(result["PRIZE:MATCH4+2STARS"])
            prizes.append(result["PRIZE:MATCH4+1STAR"])
            prizes.append(result["PRIZE:MATCH3+2STARS"])
            prizes.append(result["PRIZE:MATCH4"])
            prizes.append(result["PRIZE:MATCH2+2STARS"])
            prizes.append(result["PRIZE:MATCH3+1STAR"])
            prizes.append(result["PRIZE:MATCH3"])
            prizes.append(result["PRIZE:MATCH1+2STARS"])
            prizes.append(result["PRIZE:MATCH2+1STAR"])
            prizes.append(result["PRIZE:MATCH2"])
            allPrizes.append(prizes)
    return allPrizes


def getAllPrizesSFL(csvFile, machine=None):
    allPrizes = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                prizes = []
                prizes.append(result["PRIZE:MATCH5+LIFEBALL"])
                prizes.append(result["PRIZE:MATCH5"])
                prizes.append(result["PRIZE:MATCH4+LIFEBALL"])
                prizes.append(result["PRIZE:MATCH4"])
                prizes.append(result["PRIZE:MATCH3+LIFEBALL"])
                prizes.append(result["PRIZE:MATCH3"])
                prizes.append(result["PRIZE:MATCH2+LIFEBALL"])
                prizes.append(result["PRIZE:MATCH2"])
                allPrizes.append(prizes)
        return allPrizes
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    prizes = []
                    prizes.append(result["PRIZE:MATCH5+LIFEBALL"])
                    prizes.append(result["PRIZE:MATCH5"])
                    prizes.append(result["PRIZE:MATCH4+LIFEBALL"])
                    prizes.append(result["PRIZE:MATCH4"])
                    prizes.append(result["PRIZE:MATCH3+LIFEBALL"])
                    prizes.append(result["PRIZE:MATCH3"])
                    prizes.append(result["PRIZE:MATCH2+LIFEBALL"])
                    prizes.append(result["PRIZE:MATCH2"])
                    allPrizes.append(prizes)
        return allPrizes
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllPrizesLHP(csvFile, machine=None):
    allPrizes = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                prizes = []
                prizes.append(result["PRIZES 1"])
                prizes.append(result["PRIZES 2"])
                prizes.append(result["PRIZES 3"])
                prizes.append(result["PRIZES 4"])
                prizes.append(result["PRIZES 5"])
                allPrizes.append(prizes)
        return allPrizes
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    prizes = []
                    prizes.append(result["PRIZES 1"])
                    prizes.append(result["PRIZES 2"])
                    prizes.append(result["PRIZES 3"])
                    prizes.append(result["PRIZES 4"])
                    prizes.append(result["PRIZES 5"])
                    allPrizes.append(prizes)
        return allPrizes
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllPrizesEHP(csvFile):
    allPrizes = []
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
        for result in reader:
            prizes = []
            prizes.append(result["PRIZES 1"])
            prizes.append(result["PRIZES 2"])
            prizes.append(result["PRIZES 3"])
            prizes.append(result["PRIZES 4"])
            prizes.append(result["PRIZES 5"])
            allPrizes.append(prizes)
    return allPrizes


def getAllPrizesThun(csvFile, machine=None):
    allPrizes = []
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                prizes = []
                prizes.append(result["PRIZE:MATCH5+THUNDERBALL"])
                prizes.append(result["PRIZE:MATCH5"])
                prizes.append(result["PRIZE:MATCH4+THUNDERBALL"])
                prizes.append(result["PRIZE:MATCH4"])
                prizes.append(result["PRIZE:MATCH3+THUNDERBALL"])
                prizes.append(result["PRIZE:MATCH3"])
                prizes.append(result["PRIZE:MATCH2+THUNDERBALL"])
                prizes.append(result["PRIZE:MATCH1+THUNDERBALL"])
                prizes.append(result["PRIZE:MATCH0+THUNDERBALL"])
                allPrizes.append(prizes)
        return allPrizes
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    prizes = []
                    prizes.append(result["PRIZE:MATCH5+THUNDERBALL"])
                    prizes.append(result["PRIZE:MATCH5"])
                    prizes.append(result["PRIZE:MATCH4+THUNDERBALL"])
                    prizes.append(result["PRIZE:MATCH4"])
                    prizes.append(result["PRIZE:MATCH3+THUNDERBALL"])
                    prizes.append(result["PRIZE:MATCH3"])
                    prizes.append(result["PRIZE:MATCH2+THUNDERBALL"])
                    prizes.append(result["PRIZE:MATCH1+THUNDERBALL"])
                    prizes.append(result["PRIZE:MATCH0+THUNDERBALL"])
                    allPrizes.append(prizes)
        return allPrizes
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllPrizes(csvFile, game, machine=None):
    match game:
        case lotto:
            return getAllPrizesLotto(csvFile, machine)
        case euromillions:
            return getAllPrizesEuro(csvFile)
        case setForLife:
            return getAllPrizesSFL(csvFile, machine)
        case lottoHotPicks:
            return getAllPrizesLHP(csvFile, machine)
        case euroHotPicks:
            return getAllPrizesEHP(csvFile)
        case thunderball:
            return getAllPrizesThun(csvFile, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


def getAllBallsByPickLotto(csvFile, machine=None):
    allBallsByPick = [[],[],[],[],[],[],[]]
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                for i in range(7):
                    if i!=6:
                        allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                    else:
                        allBallsByPick[i].append(int(result["BONUS BALL"]))
        return allBallsByPick
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    for i in range(7):
                        if i!=6:
                            allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                        else:
                            allBallsByPick[i].append(int(result["BONUS BALL"]))
        return allBallsByPick
    else:
        raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)


def getAllBallsByPickEuro(csvFile):
    allBallsByPick = [[],[],[],[],[],[],[]]
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames = EURO_FIELD_NAMES)
        for result in reader:
            for i in range(7):
                if i==5:
                    allBallsByPick[i].append(int(result["LUCKY STAR 1"]))
                elif i==6:
                    allBallsByPick[i].append(int(result["LUCKY STAR 2"]))
                else:
                    allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
    return allBallsByPick


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllBallsByPickSFL(csvFile, machine=None):
    allBallsByPick = [[],[],[],[],[],[],[]]
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                for i in range(6):
                    if i!=5:
                        allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                    else:
                        allBallsByPick[i].append(int(result["LIFE BALL"]))
        return allBallsByPick
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    for i in range(6):
                        if i!=5:
                            allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                        else:
                            allBallsByPick[i].append(int(result["LIFE BALL"]))
        return allBallsByPick
    else:
        raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)


def getAllBallsByPickLHP(csvFile, machine):
    allBallsByPick = [[],[],[],[],[],[],[]]
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
            for result in reader:
                for i in range(6):
                    allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
        return allBallsByPick
    elif machine in LOTTO_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    for i in range(6):
                        allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
        return allBallsByPick
    else:
        raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LHP_MACHINE_SET)


def getAllBallsByPickEHP(csvFile):
    allBallsByPick = [[],[],[],[],[],[],[]]
    with open(csvFile, newline="") as file:
        reader = csv.DictReader(file, fieldnames = EHP_FIELD_NAMES)
        for result in reader:
            for i in range(5):
                allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
    return allBallsByPick


def getAllBallsByPickThun(csvFile, machine):
    allBallsByPick = [[],[],[],[],[],[],[]]
    if machine is None:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
            for result in reader:
                for i in range(6):
                    if i!=5:
                        allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                    else:
                        allBallsByPick[i].append(int(result["THUNDERBALL"]))
        return allBallsByPick
    elif machine in SFL_MACHINE_SET:
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
            for result in reader:
                if machine==result["MACHINE"]:
                    for i in range(6):
                        if i!=5:
                            allBallsByPick[i].append(int(result["BALL "+str(i+1)]))
                        else:
                            allBallsByPick[i].append(int(result["THUNDERBALL"]))
        return allBallsByPick
    else:
        raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % THUN_MACHINE_SET)


def getAllBallsByPick(csvFile, game, machine=None):
    match game:
        case lotto:
            return getAllBallsByPickLotto(csvFile, machine)
        case euromillions:
            return getAllBallsByPickEuro(csvFile)
        case setForLife:
            return getAllBallsByPickSFL(csvFile, machine)
        case lottoHotPicks:
            return getAllBallsByPickLHP(csvFile, machine)
        case euroHotPicks:
            return getAllBallsByPickEHP(csvFile)
        case thunderball:
            return getAllBallsByPickThun(csvFile, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


def getAllBallsByiLotto(csvFile, i, machine=None):
    validNumbers = [1,2,3,4,5,6]
    if i in validNumbers:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["BALL "+str(i)]))
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["BALL "+str(i)]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)                
    elif i==7:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["BONUS BALL"]))
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LOTTO_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["BONUS BALL"]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for lotto i.e. either: %r." % LOTTO_MACHINE_SET)                
    else:
        raise ValueError("'i' must be valid number between 1 to 7, as there are only 7 Lotto numbers picked for each draw")


def getAllBallsByiEuro(csvFile, i):
    validNumbers = [1,2,3,4,5]
    if i in validNumbers:
        allBallsi = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = EURO_FIELD_NAMES)
            for result in reader:
                allBallsi.append(int(result["BALL "+str(i)]))
        return allBallsi
    elif i==6:
        allBallsi = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = EURO_FIELD_NAMES)
            for result in reader:
                allBallsi.append(int(result["LUCKY STAR 1"]))
        return allBallsi
    elif i==7:
        allBallsi = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = EURO_FIELD_NAMES)
            for result in reader:
                allBallsi.append(int(result["LUCKY STAR 2"]))
        return allBallsi
    else:
        raise ValueError("'i' must be valid number between 1 to 7, as there are only 7 euromillions numbers picked for each draw")


# LIFE BALL IS NOT AN INTEGER; IT IS A STR IN THE FORMAT SFL_
def getAllBallsByiSFL(csvFile, i, machine=None):
    validNumbers = [1,2,3,4,5]
    if i in validNumbers:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["BALL "+str(i)]))
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["BALL "+str(i)]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)                
    elif i==6:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["LIFE BALL"]))
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = SFL_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["LIFE BALL"]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for set for life i.e. either: %r." % SFL_MACHINE_SET)                
    else:
        raise ValueError("'i' must be valid number between 1 to 6, as there are only 6 set for life numbers picked for each draw")


def getAllBallsByiLHP(csvFile, i, machine):
    validNumbers = [1,2,3,4,5,6]
    if i in validNumbers:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["BALL "+str(i)]))
        elif machine in LOTTO_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = LHP_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["BALL "+str(i)]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for lotto hot picks i.e. either: %r." % LOTTO_MACHINE_SET)                
    else:
        raise ValueError("'i' must be valid number between 1 to 6, as there are only 6 lotto hot picks numbers picked for each draw")


def getAllBallsByiEHP(csvFile, i):
    validNumbers = [1,2,3,4,5]
    if i in validNumbers:
        allBallsi = []
        with open(csvFile, newline="") as file:
            reader = csv.DictReader(file, fieldnames = EHP_FIELD_NAMES)
            for result in reader:
                allBallsi.append(int(result["BALL "+str(i)]))
        return allBallsi
    else:
        raise ValueError("'i' must be valid number between 1 to 5, as there are only 5 euromillions hot picks numbers picked for each draw")


def getAllBallsByiThun(csvFile, i, machine=None):
    validNumbers = [1,2,3,4,5]
    if i in validNumbers:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["BALL "+str(i)]))
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["BALL "+str(i)]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)                
    elif i==6:
        allBallsi = []
        if machine is None:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
                for result in reader:
                    allBallsi.append(int(result["THUNDERBALL"]))
        elif machine in SFL_MACHINE_SET:
            with open(csvFile, newline="") as file:
                reader = csv.DictReader(file, fieldnames = THUN_FIELD_NAMES)
                for result in reader:
                    if machine==result["MACHINE"]:
                        allBallsi.append(int(result["THUNDERBALL"]))
            return allBallsi
        else:
            raise ValueError("Machine specified must a machine that is used for thunderball i.e. either: %r." % SFL_MACHINE_SET)                
    else:
        raise ValueError("'i' must be valid number between 1 to 6, as there are only 6 thunderball numbers picked for each draw")


# This method returns the all Lotto numbers that were picked in the i-th position
# i.e. if i=1 then it returns an array containing all the Lotto numbers that were picked 1st on each result
def getAllBallsByi(csvFile, i, game, machine=None):
    match game:
        case lotto:
            return getAllBallsByiLotto(csvFile, i, machine)
        case euromillions:
            return getAllBallsByiEuro(csvFile, i)
        case setForLife:
            return getAllBallsByiSFL(csvFile, i, machine)
        case lottoHotPics:
            return getAllBallsByiLHP(csvFile, i, machine)
        case euroHotPicks:
            return getAllBallsByiEHP(csvFile, i)
        case thunderball:
            return getAllBallsByiThun(csvFile, i, machine)
        case _:
            raise ValueError("Game must be a valid national lottery game; please input either: %r." % GAME_SET)


# Returns a rearranged array of arrays sorted by their picks
# i.e. [all balls picked 1st, all balls picked 2nd, ... , all balls picked last (bonus balls)]
def getAllBallsByPickOLD(arrayOfArrays):
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
