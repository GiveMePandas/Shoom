#!/usr/bin/env python
# coding: utf-8

# # Shoom

# In[13]:


import random as rn
from colorama import Fore as F
import pandas as pd


# In[18]:


roundPoints
shoomPoints = 0                                 #total point storage
guessCount = 0                                  #stores number of guesses
currentValue = ""                               #Stores number to guess
guess = ""                                      #user guess
guessList = []                                  #store user guesses
possiblePoints = 0                              #store possible points
#scoring system for rules
scoringTable = [("Guess","Score"), (1, 100), ("2-5","100-5*(guess-1)"),("6-9", "80-10*(guess - 5)"), ("10+", "40-2*(guess-9)")]
correctLetters = 0
#table for storing data
successRate = pd.DataFrame(columns = ["Correct Positions", "Round Points", "Shoom Points", "Possible Points", "Percent Points Earned"])


# ## Generate

# In[4]:


def initializeGuess():
    x = 0
    G = 0
    strG = ""
    while x < 4: 
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

# In[ ]:


def printRules(sL): #scoreList
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

# In[ ]:


def userGuess(gC, gL): #guessCount, guessList
    print("Need to view the rules? Type r ")
    if gC > 0:                               #if this is not the first guess, print previous guess results
        print("Previous Guesses:")
        print(gL)
    U = input("What is your 6 digit guess?") #U stores user guess
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


# # Compare User Inputs

# In[ ]:


#if r, pring all rules
def ruleCheck(U, gC, gL): #guess
    if U.lower() == "r":
        printRules()
        U = userGuess()
    return U

#check for valid U
def validityCheck(U, gC, gL):
    if U == "ERROR":
        U = userGuess()
    return U


# In[ ]:


def compareResults (U, gC, gL, strG): #guess, guessCount, guessList, currentValue, possiblePoints, shoomPoints
    gC += 1
    result = "" #comparison of user input and answer
    ic = 0 #keep an index that will take into account duplicates
    jc = 0 #^
    cL = 0 #track if answer is correct
    for i in U:
        for j in strG:
            if i == j and ic == jc:
                result = result + f"{F.GREEN}i{F.WHITE}"
                cL += 1
            elif i == j and ic != jc:
                result = result + f"{F.YELLOW}i{F.WHITE}"
            else:
                result = result + f"{F.RED}i{F.WHITE}"
            jc += 1
        ic += 1
    gL.append(result)
    return gL, gC, cL                


# # Calculate Points

# In[ ]:


def roundPoints(gC):
    if gC == 1:
        points = 100
    elif gC > 1 and gC < 6:
        points = 100 - 5*(gC-1)
    elif gC > 5 and gC < 10:
        points = 80 - 10*(gC-5)
    else:
        points = 40 - 2*(gC-9)


# # Run a Round

# In[ ]:


def round(scoreList, totpts, pospts, dfi):
    shm = totpts
    G = initializeGuess()
    while cL != 5:
        U = userGuess(gC, gL)
        while U.lower()=='r' or U.upper() == "ERROR":
            U = ruleCheck(U, gC, gL)
            U = validityCheck(U, gC, gL)
        U = U.lower()
        gL, gC, cL = compareResults(U, gC, gL, strG)
        rPoints = roundPoints(gC)
        scoreList.concat[successRate, (pd.Series([cL, rPoints, shm + rPoints, pospts, (float((shm+rPoints)/pospts)*100)], index = ["Correct Positions", "Round Points", "Shoom Points", "Possible Points", "Percent Points Earned"], name = dfi)).to_frame().T]
        dfi += 1
    return scoreList, totpts, pospts, dfi


# # Run Full Game

# In[ ]:


dfi = 0
yorn = input("Are you ready to play? (yes or no)   ")
while yorn.lower() == "yes" or yorn.lower() == "y":
    round(successRate, shoomPoints, possiblePoints, dfi)
    yorn = input("Would you like to try again?   ")

