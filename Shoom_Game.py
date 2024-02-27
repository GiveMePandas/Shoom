# Shoom

# Imports
from pickle import TRUE
import random as rn
from colorama import Fore as F
import pandas as pd



roundPoints = 0
shoomPoints = 0                                 #total point storage
guessCount = 0                                  #stores number of guesses used, gC locally
currentValue = ""                               #Stores number to guess, strG locally
guess = ""                                      #user guess, U locally
guessList = []                                  #store user guesses, gL locally
possiblePoints = 0                              #store possible points, pospts locally
correctLetters = 0                              #keeps track of how many letters are correct, cL locally

#scoring system for rules
scoringTable = [("Guess","Score"), (1, 100), ("2-5","100-5*(guess-1)"),("6-9", "80-10*(guess - 5)"), ("10+", "40-2*(guess-9)")]



#table for storing data
successRate = pd.DataFrame(columns = ["Correct Positions", "Round Points", "Shoom Points", "Possible Points", "Percent Points Earned"])

# ## Create fuunction to initialize a string consisting of s,h,o,m to guess
def initializeGuess():
    x = 0
    G = 0
    strG = ""
    while x < 5: 
        G = rn.randint(0, 3)                           #generated to determine letter s = 0, h = 1, o = 2, 3 = m 
        if G == 0:
            strG = strG + "s"
        elif G == 1:
            strG = strG + "h"
        elif G == 2:
            strG = strG + "o"
        else:
            strG = strG + "m"
        x += 1
    


# ## Rules
def printRules(sL): #soringTable
    print("1. Guess 's','h','o','m' of length 5 in any order.")
    print("2. There will be repeat letters (and the same letter can appear more than twice).")
    print("3. Correct placement letters will turn green.")
    print("4. Correct letters with incorrect placement will be noted with yellow.")
    print("5. Incorrect letters will be marked with red.") 
    print("6. Unlimited guesses.")
    print("Point system:")
    for i in sL:
        print(i)


# ## Receive User input
def userGuess(gC, gL): #guessCount, guessList
    print("Need to view the rules? Type r ")
    if gC > 0:                               #if this is not the first guess, print previous guess results
        print("Previous Guesses:")
        print(gL)
    U = input("What is your guess?   ") #U stores user guess
    #check to make sure only s, h, o, m are in the answer
    for u in U:
        if (u.lower() == "s" or u.lower() == "h") or (u.lower() == "o" or u.lower() == "m"):
            continue
        elif u.lower() == "r":
            continue
        else: 
            print("Invalid Input")
            U = "ERROR"
    return U                                 #U should be stored in guess


# ## Compare User Inputs

#if r, print all rules
def ruleCheck(U, gC, gL): #Checks if prompting for rules
    if U.lower() == "r":             #examines if user is requesting rules
        printRules(scoringTable)     #call function to display rules
        U = userGuess(gC, gL)        #prompt user to guess after reading rules
    return U                         #returns new input

#check for valid U
def validityCheck(U, gC, gL): #make sure user only inputs valid answers
    if U == "ERROR":
        U = userGuess(gC, gL) #Make user guess again
    return U


# In[ ]:


def compareResults (U, gC, gL, strG): #guess, guessCount, guessList, currentValue, possiblePoints, shoomPoints
    gC += 1
    result = "" #comparison of user input and answer
    ic = 0 #keep an index that will take into account duplicates
    jc = 0 #^
    cL = 0 #track if answer is correct
    U = str(U)
    strG = str(strG)
    for i in U:
        for j in strG:
            if i == j and ic == jc:
                result = result + f"{F.GREEN}"+ i +f"{F.WHITE}" #prints correct letters & placement in green
                cL += 1
            elif i == j and ic != jc:
                result = result + f"{F.YELLOW}"+i+f"{F.WHITE}" #prints correct letters in wrong place as yellow
            else:
                result = result + f"{F.RED}"+i+f"{F.WHITE}"    #prints incorrect letters in red
            jc += 1
        ic += 1
    gL.append(result)
    print(result)
    return gL, gC, cL                


# # Calculate Points

# In[ ]:
# determine round points (drops w/ more guesses)
def roundPoints(gC):
    if gC == 1:
        points = 100
    elif gC > 1 and gC < 6:
        points = 100 - 5*(gC-1)
    elif gC > 5 and gC < 10:
        points = 80 - 10*(gC-5)
    else:
        points = 40 - 2*(gC-9)
    return points


# # Run a Round

def round(scoreList, totpts, pospts, dfi):
    strG = initializeGuess()
    cL = 0
    gC = 0
    gL = []
    while cL != 5:
        U = userGuess(gC, gL)
        while U.lower()=='r' or U.upper() == "ERROR":
            U = ruleCheck(U, gC, gL)
            U = validityCheck(U, gC, gL)
        U = U.lower()
        gL, gC, cL = compareResults(U, gC, gL, strG)
        rPoints = roundPoints(gC)
        guessScore = [cL, rPoints, totpts + int(rPoints), pospts, ((totpts+rPoints)/pospts)*100]
        scoreList.loc[len(scoreList)] = guessScore
        dfi += 1
    totpts += rPoints
    return scoreList, totpts


# # Run Full Game
dfi = 0
yorn = input("Are you ready to play? (yes or no)   ")
while yorn.lower() == "yes" or yorn.lower() == "y":
    possiblePoints += 100
    successRate, shoompoints = round(successRate, shoomPoints, possiblePoints, dfi)
    yorn = input("Would you like to try again? (yes or no)   ")
