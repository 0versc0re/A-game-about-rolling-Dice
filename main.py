# IMPORTS
from random import *
import json
import os, sys


# DICE VARIABLES
diceSides = 4
diceAmount = 1
points = 0
pointsMult = 1.0
pointsMultExpo = 1.15

# SHOP VARIABLES
upgradeDice = 50
upgradeExpo = 1.05
moreDice = 50
moreExpo = 1.2

# BIG DICE VARIABLES
hundoDiceAmount = 0
thundoDiceAmount = 0
mundoDiceAmount = 0

# LUCK VARIABLES
rollLuck = 1
upgradeLuck = 200
luckExpo = 1.1

def clear():
    os.system("cls")

def save():
    
    saveData = {
        "diceSides":        diceSides,
        "diceAmount":       diceAmount,
        "points":           points,
        "pointsMult":       pointsMult,
        "pointsMultExpo":   pointsMultExpo,
        "upgradeDice":      upgradeDice,
        "upgradeExpo":      upgradeExpo,
        "moreDice":         moreDice,
        "moreExpo":         moreExpo,
        "hundoDiceAmount":  hundoDiceAmount,
        "thundoDiceAmount": thundoDiceAmount,
        "mundoDiceAmount":  mundoDiceAmount,
        "rollLuck":         rollLuck,
        "upgradeLuck":      upgradeLuck,
        "luckExpo":         luckExpo
    }
    
    with open("save.json", "w") as f:
        json.dump(saveData, f, indent=4)

def main():
    
    # BOOLEANS
    Run = True
    Menu = True
    Play = False
    Store = False
    
    # GLOBAL VARIABLES
    global diceSides, diceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo
    global hundoDiceAmount, thundoDiceAmount, mundoDiceAmount
    global rollLuck, upgradeLuck, luckExpo
    
    while Run:
    
        while Menu:
            
            clear()
            print("- 0 - New Game")
            print("- 1 - Load Game")
            print("- 2 - Exit Game")
            choice = input("> ")
            
            if choice == "0":           # NEW GAME
                
                print()
                print("Are you sure you want to start a New Game?")
                print("- 1 - No  New Game")
                print("- 0 - Yes New Game")
                choice = input("> ")
                
                if choice == "0":       # NO
                    Menu = False
                    Play = True
                    clear()
                    
                elif choice == "1":     # YES
                    continue
                
                else:                   # INVALID
                    print("Invalid choice!")
                    input("> ")
                
            elif choice == "1":         # LOAD GAME
                
                try:
                    
                    with open("save.json", "r") as f:
                        data = json.load(f)
                        
                    diceSides =        data["diceSides"]
                    diceAmount =       data["diceAmount"]
                    points =           data["points"]
                    pointsMult =       data["pointsMult"]
                    pointsMultExpo =   data["pointsMultExpo"]
                    upgradeDice =      data["upgradeDice"]
                    upgradeExpo =      data["upgradeExpo"]
                    moreDice =         data["moreDice"]
                    moreExpo =         data["moreExpo"]
                    hundoDiceAmount =  data["hundoDiceAmount"]
                    thundoDiceAmount = data["thundoDiceAmount"]
                    mundoDiceAmount =  data["mundoDiceAmount"]
                    rollLuck =         data["rollLuck"]
                    upgradeLuck =      data["upgradeLuck"]
                    luckExpo =         data["luckExpo"]
                        
                    Menu = False
                    Play = True
                        
                except OSError:
                    print("Corrupt or missing file!")
                    input("> ")
            
            elif choice == "2":         # EXIT GAME
                sys.exit()
        
        while Play:
            
            save()
            clear()
            
            # DICE DISPLAY
            print(f"You have {diceAmount} {diceSides} sided Dice.")                             # NOT SECRET
            print(f"You have {hundoDiceAmount} 100 sided Dice.")                                # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {thundoDiceAmount} 1000 sided Dice")      # SECRET
            if mundoDiceAmount > 0: print(f"You have {mundoDiceAmount} Million sided Dice")     # BIG SECRET
                        
            # POINTS DISPLAY
            print()
            if points < 900_000: print(f"You have {round(points, 2)} points.")                            # LESS THAN MILLION
            elif points < 900_000_000: print(f"You have {round(points / 1_000_000, 2)}M points.")         # LESS THAN BILLION
            elif points < 900_000_000_000: print(f"You have {round(points / 1_000_000_000, 2)}B points.") # LESS THAN TRILLION
            else: print(f"You have {round(points / 1_000_000_000_000, 2)}T points.")                      # MORE THAN TRILLION
            
            # LUCK AND MULTIPLIER DISPLAY
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            print(f"Your current multiplier: {round(pointsMult, 2)}")
            if points >= 1000 ** pointsMult: print("You have enough points to upgrade your multiplier!")

            # OPTIONS DISPLAY
            print()
            print("- 1 - Roll Dice")
            print("- 2 - Dice store")
            print("- 3 - Upgrade Multiplier")
            if hundoDiceAmount > 0: print("- 4 - Roll the 100 sided Dice")
            if thundoDiceAmount > 0: print("- 5 - Roll the 1000 sided Dice")
            if mundoDiceAmount > 0: print("- 6 - Roll the Million sided Dice")
            print("- 0 - Save and Exit")
            
            choice = input("> ")
            
            if choice == "0":           # SAVE AND EXIT
                save()
                sys.exit()
                
            elif choice == "1":         # ROLL DICE
                
                print()
                rollList = []
                total = 0
                
                if diceAmount < 5:
                    for roll in range(diceAmount):
                        if rollLuck < diceSides:
                            roll = randint(rollLuck, diceSides)
                        else:
                            roll = diceSides
                        points += roll * pointsMult
                        rollList.append(roll)
                        print(f"You rolled a {roll}!")
                else:
                    for roll in range(diceAmount):
                        if rollLuck < diceSides:
                            roll = randint(rollLuck, diceSides)
                        else:
                            roll = diceSides
                        points += roll * pointsMult
                        rollList.append(roll)
                    print(f"You rolled your Dice {diceAmount} times!")
                
                print()
                print(f"Your current multiplier: {round(pointsMult, 2)}")
                for roll in rollList:
                    total += roll
                print(f"You now have {round(total * pointsMult, 2)} more points.")
                input("> ")
            
            elif choice == "2":         # DICE STORE
                Store = True
                Play = False
            
            elif choice == "3":         # UPGRADE MULTIPLIER
                
                print()
                print("WARNING!")
                print("UPGRADING YOUR MULTIPLIER RESETS YOUR")
                print("DICE AND POINTS BACK TO 1 AND 0")
                print("STORE PRICES ARE ALSO RESET")
                print()
                print(f"Your current multiplier: {round(pointsMult, 2)}")
                
                if 1000 ** pointsMult < 900_000: print(f"You need {round(1000 ** pointsMult, 2)} points to upgrade your Multiplier.")                               # LESS THAN MILLION
                elif 1000 ** pointsMult < 900_000_000: print(f"You need {round(1000 ** pointsMult / 1_000_000, 2)}M points to upgrade your Multiplier.")            # LESS THAN BILLION
                elif 1000 ** pointsMult < 900_000_000_000: print(f"You need {round(1000 ** pointsMult / 1_000_000_000, 2)}B points to upgrade your Multiplier.")    # LESS THAN TRILLION
                else: print(f"You need {round(1000 ** pointsMult / 1_000_000_000_000, 2)}T points to upgrade your Multiplier.")                                     # MORE THAN TRILLION
                
                print(f"- 1 - Upgrade Multiplier")
                print(f"- 0 - I don't want to")
                
                choice = input("> ")
                
                if choice == "1":           # YES
                    
                    if points >= 1000 ** pointsMult:
                        points -= 1000 ** pointsMult
                        pointsMult = pointsMult * pointsMultExpo
                        
                        diceSides = 4
                        diceAmount = 1
                        points = 0

                        upgradeDice = 50
                        upgradeExpo = 1.05
                        moreDice = 50
                        moreExpo = 1.2
                        
                        hundoDiceAmount = 0
                        thundoDiceAmount = 0
                        mundoDiceAmount = 0
                        
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        print()
                        print("Wise choice.")
                        print(f"Your new multiplier: {round(pointsMult, 2)}")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "0":         # NO
                    continue
            
            elif choice == "4":         # ROLL HUNDO
                    
                if hundoDiceAmount > 0:
                    
                    print()
                    rollList = []
                    total = 0
                    
                    if hundoDiceAmount < 5:
                        for roll in range(hundoDiceAmount):
                            roll = randint(1, 100)
                            points += roll * pointsMult
                            rollList.append(roll)
                            print(f"You rolled a {roll}!")
                    else:
                        for roll in range(hundoDiceAmount):
                            roll = randint(1, 100)
                            points += roll * pointsMult
                            rollList.append(roll)
                        print(f"You rolled your Dice {hundoDiceAmount} times!")
                    
                    print()
                    print(f"Your current multiplier: {round(pointsMult, 2)}")
                    for roll in rollList:
                        total += roll
                    print(f"You now have {round(total * pointsMult, 2)} more points.")
                    input("> ")
            
            elif choice == "5":         # ROLL THUNDO
                
                if thundoDiceAmount > 0:
                    
                    print()
                    rollList = []
                    total = 0
                    
                    if thundoDiceAmount < 5:
                        for roll in range(thundoDiceAmount):
                            roll = randint(1, 1000)
                            points += roll * pointsMult
                            rollList.append(roll)
                            print(f"You rolled a {roll}!")
                    else:
                        for roll in range(thundoDiceAmount):
                            roll = randint(1, 1000)
                            points += roll * pointsMult
                            rollList.append(roll)
                        print(f"You rolled your Dice {thundoDiceAmount} times!")
                    
                    print()
                    print(f"Your current multiplier: {round(pointsMult, 2)}")
                    for roll in rollList:
                        total += roll
                    if total * pointsMult < 900_000: print(f"You now have {round(total * pointsMult, 2)} more points.")
                    elif total * pointsMult < 900_000_000: print(f"You now have {round(total * pointsMult / 1_000_000, 2)}M more points.")
                    else: print(f"You now have {round(total * pointsMult / 1_000_000_000, 2)}B more points.")
                    input("> ")
            
            elif choice == "6":         # ROLL MUNDO
                
                if mundoDiceAmount > 0:
                    
                    print()
                    rollList = []
                    total = 0
                    
                    if mundoDiceAmount < 5:
                        for roll in range(mundoDiceAmount):
                            roll = randint(1, 1_000_000)
                            points += roll * pointsMult
                            rollList.append(roll)
                            print(f"You rolled a {roll}!")
                    else:
                        for roll in range(mundoDiceAmount):
                            roll = randint(1, 1_000_000)
                            points += roll * pointsMult
                            rollList.append(roll)
                        print(f"You rolled your Dice {mundoDiceAmount} times!")
                    
                    print()
                    print(f"Your current multiplier: {round(pointsMult, 2)}")
                    for roll in rollList:
                        total += roll
                    if total * pointsMult < 900_000: print(f"You now have {round(total * pointsMult, 2)} more points.")
                    elif total * pointsMult < 900_000_000: print(f"You now have {round(total * pointsMult / 1_000_000, 2)}M more points.")
                    else: print(f"You now have {round(total * pointsMult / 1_000_000_000, 2)}B more points.")
                    input("> ")
            
            else:                       # INVALID
                print("Invalid choice!")
                input("> ")
                
        while Store:
            
            save()
            clear()
            
            hundoPairs = {
                (1, 96),  (2, 48),  (3, 32), (32, 3), (4, 24), (24, 4), (6, 16), (16, 6), (12, 8),  (8, 12),    # total 96
                (1, 97),  (97, 1),  (1, 98), (98, 1), (2, 49), (49, 2), (7, 14), (14, 7),                       # total 97 98
                (1, 99),  (99, 1),  (3, 33), (33, 3), (9, 11), (11, 9),                                         # total 99
                (100, 1), (10, 10), (2, 50), (50, 2), (4, 25), (25, 4), (5, 20), (20, 5), (1, 101), (101, 1),   # total 100 101
                (1, 102), (102, 1), (2, 51), (51, 2), (3, 34), (34, 3), (6, 17), (17, 6), (1, 103), (103, 1),   # total 102 103
                (1 ,104), (104, 1), (2, 52), (52, 2), (26, 4), (4, 26), (13, 8), (8, 13)                        # total 104
            }
            
            # DICE DISPLAY
            print(f"You have {diceAmount} {diceSides} sided Dice.")                             # NOT SECRET
            print(f"You have {hundoDiceAmount} 100 sided Dice.")                                # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {thundoDiceAmount} 1000 sided Dice")      # SECRET
            if mundoDiceAmount > 0: print(f"You have {mundoDiceAmount} Million sided Dice")     # BIG SECRET
                
            # POINTS AND LUCK DISPLAY
            print()
            if points < 900_000: print(f"You have {round(points, 2)} points.")                            # LESS THAN MILLION
            elif points < 900_000_000: print(f"You have {round(points / 1_000_000, 2)}M points.")         # LESS THAN BILLION
            elif points < 900_000_000_000: print(f"You have {round(points / 1_000_000_000, 2)}B points.") # LESS THAN TRILLION
            else: print(f"You have {round(points / 1_000_000_000_000, 2)}T points.")                      # MORE THAN TRILLION
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            
            # BIG DICE DISPLAY
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000):
                print()
                print("You can now get an ELUSIVE 100 sided Die")
                print("by merging your all of your Dice together!")
                print("Or by paying 12000 points for it!")
            if hundoDiceAmount >= 10 or points >= 120_000:
                print()
                print("You can now get an ADORED 1000 sided Die")
                print("by trading off 10 of your 100 sided Die!")
                print("Or by paying 120000 points for it!")
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000:
                print()
                print("You can now get the Million sided Die")
                print("by trading off your Dice!")
                print("Or by paying 120 Million points for it!")
            
            # OPTIONS DISPLAY
            print()
            if upgradeDice * diceAmount < 900_000: print(f"- 1 - Upgrade Dice: {round(upgradeDice * diceAmount, 2)} points")                      # LESS THAN MILLION
            elif upgradeDice * diceAmount < 900_000_000: print(f"- 1 - Upgrade Dice: {round(upgradeDice * diceAmount / 1_000_000, 2)}M points")   # LESS THAN BILLION
            else: print(f"- 1 - Upgrade Dice: {round(upgradeDice * diceAmount / 1_000_000_000, 2)}B points")                                      # MORE THAN BILLION
                
            if moreDice * 1.5 < 900_000: print(f"- 2 - Buy more Dice: {round(moreDice * 1.5, 2)} points")                                         # LESS THAN MILLION
            elif moreDice * 1.5 < 900_000_000: print(f"- 2 - Buy more Dice: {round(moreDice * 1.5 / 1_000_000, 2)}M points")                      # LESS THAN BILLION
            else: print(f"- 2 - Buy more Dice: {round(moreDice * 1.5 / 1_000_000_000, 2)}B points")                                               # MORE THAN BILLION
                
            if upgradeLuck < 900_000: print(f"- 3 - Buy a Lucky Amulet: {round(upgradeLuck, 2)} points")                                          # LESS THAN MILLION
            elif upgradeLuck < 900_000_000: print(f"- 3 - Buy a Lucky Amulet: {round(upgradeLuck / 1_000_000, 2)}M points")                       # LESS THAN BILLION
            else: print(f"- 3 - Buy a Lucky Amulet: {round(upgradeLuck / 1_000_000_000, 2)}B points")                                             # MORE THAN BILLION
                
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000): print("- 4 - Get a 100 sided Die")                          # GET YOURSELF A 100  SIDED DIE
            if hundoDiceAmount >= 10 or points >= 120_000: print("- 5 - Get a 1000 sided Die")                                            # GET YOURSELF A 1000 SIDED DIE
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000: print("- 6 - Get a Million sided Die")     # GET YOURSELF A Million SIDED DIE
            print("- 0 - Exit Store")
            
            choice = input("> ")
            
            if choice == "0":           # EXIT STORE
                Play = True
                Store = False
            
            elif choice == "1":         # UPGRADE DICE
                
                if points >= upgradeDice * diceAmount:
                    points -= upgradeDice * diceAmount
                    upgradeDice = upgradeDice ** upgradeExpo
                    diceSides += 1
                    print(f"You now have {diceAmount} dice with {diceSides} sides each.")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "2":         # BUY MORE DICE
                
                if points >= moreDice * 1.5:
                    points -= moreDice * 1.5
                    moreDice = moreDice ** moreExpo
                    diceAmount += 1
                    print(f"You now have {diceAmount} dice with {diceSides} sides each.")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "3":         # LUCKY AMULET
                
                if points >= upgradeLuck:
                    points -= upgradeLuck
                    upgradeLuck = upgradeLuck ** luckExpo
                    rollLuck += 1
                    print("You feel luckier!")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "4":         # GET HUNDO DICE
                
                if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000):
                
                    print()
                    print("WARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF ALL OF YOUR DICE FOR A 100 SIDED DIE")
                    print("YOU'LL HAVE YOUR NEW 100 SIDED DIE AND THE ORIGINAL 4 SIDED DIE")
                    print("YOU WON'T LOSE YOUR DICE IF YOU PAY FOR THE 100 SIDED DIE")
                    print("(the 100 sided Die doesn't persist between multiplier upgrades)")
                    print()
                    print("- 1 - Trade off my Dice")
                    print("- 2 - Pay for the Die")
                    print("- 3 - I want 10 of those")
                    print("- 4 - I want 100 of those")
                    print("- 0 - I don't want to")
                    
                    choice = input("> ")
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        if (diceAmount, diceSides) in hundoPairs:
                            
                            hundoDiceAmount += 1
                            diceSides = 4
                            diceAmount = 1
                            
                            upgradeDice = 50
                            upgradeExpo = 1.05
                            moreDice = 50
                            moreExpo = 1.2
                            
                            print("Welcome your new 100 sided Die!")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 12_000:
                            
                            hundoDiceAmount += 1
                            points -= 12_000
                            
                            print("Welcome your new 100 sided Die!")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "3":         # 10 WITH POINTS
                        
                        if points >= 120_000:
                            
                            hundoDiceAmount += 10
                            points -= 120_000
                            
                            print("Just get a 1000 sided Die.")
                            input("> ")
                        
                        else:
                            print("You don't have enough points!")
                            input("> ")
                            
                    elif choice == "4":         # 100 WITH POINTS
                        
                        if points >= 1_200_000:
                            
                            hundoDiceAmount += 100
                            points -= 1_200_000
                            
                            print("I don't get why you would buy this.")
                            input("> ")
                        
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        print("Invalid choice!")
                        input("> ")
            
            elif choice == "41":        # GET HUNDO DICE WITH DICE
                
                if ((diceAmount, diceSides) in hundoPairs):
                    
                    hundoDiceAmount += 1
                    diceSides = 4
                    diceAmount = 1
                            
                    upgradeDice = 50
                    upgradeExpo = 1.05
                    moreDice = 50
                    moreExpo = 1.2
                    
            elif choice == "42":        # GET HUNDO DICE WITH POINTS
                
                if points >= 12_000:
                    hundoDiceAmount += 1
                    points -= 12_000

            elif choice == "43":        # GET HUNDO DICE WITH POINTS x10
                
                if points >= 120_000:
                    hundoDiceAmount += 10
                    points -= 120_000
            
            elif choice == "44":        # GET HUNDO DICE WITH POINTS x100
                
                if points >= 1_200_000:
                    hundoDiceAmount += 100
                    points -= 1_200_000
            
            elif choice == "5":         # GET THUNDO DICE
                
                if hundoDiceAmount >= 10 or points >= 120_000:
                    
                    print()
                    print("WARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF 10 OF YOUR 100 SIDED DICE")
                    print("OR PAY 120000 POINTS FOR AN INCREDIBLE 1000 SIDED DIE")
                    print("(this still doesn't persist between multiplier upgrades)")
                    print()
                    print("- 1 - Trade off my Dice")
                    print("- 2 - Pay for the Die")
                    print("- 3 - I want 10 of those")
                    print("- 4 - I want 100 of those")
                    print("- 0 - I don't want to")
                    
                    choice = input("> ")
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        if hundoDiceAmount >= 10:
                            
                            thundoDiceAmount += 1
                            hundoDiceAmount -= 10
                            
                            print("Stand ready for my arrival, worm.")
                            input("> ")
                        
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 120_000:
                            
                            thundoDiceAmount += 1
                            points -= 120_000
                            
                            print("Stand ready for my arrival, worm.")
                            input("> ")
                        
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "3":         # 10 WITH POINTS
                        
                        if points >= 1_200_000:
                            
                            thundoDiceAmount += 10
                            points -= 1_200_000
                            
                            print("Detected motion at front door.")
                            input("> ")
                        
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "4":         # 100 WITH POINTS
                        
                        if points >= 12_000_000:
                            
                            thundoDiceAmount += 100
                            points -= 12_000_000
                            
                            print("Detected motion at front door.")
                            input("> ")
                        
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        print("Invalid choice!")
                        input("> ")
            
            elif choice == "51":        # GET THUNDO DICE WITH DICE
                
                if hundoDiceAmount >= 10:
                    thundoDiceAmount += 1
                    hundoDiceAmount -= 10

            elif choice == "52":        # GET THUNDO DICE WITH POINTS
                
                if points >= 120_000:
                    thundoDiceAmount += 1
                    points -= 120_000
            
            elif choice == "53":        # GET THUNDO DICE WITH POINTS x10
                        
                if points >= 1_200_000:
                    thundoDiceAmount += 10
                    points -= 1_200_000
            
            elif choice == "54":        # GET THUNDO DICE WITH POINTS x100
                
                if points >= 12_000_000:
                    thundoDiceAmount += 100
                    points -= 12_000_000
            
            elif choice == "6":         # GET MUNDO DICE
                
                if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000:
                    
                    print()
                    print("WARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF YOUR DICE")
                    print("OR PAY 120 Million POINTS FOR A Million SIDED DIE")
                    print()
                    print("- 1 - Trade off my 100 sided Dice")
                    print("- 2 - Trade off my 1000 sided Dice")
                    print("- 3 - Pay for the Die")
                    print("- 4 - I want 10 of those")
                    print("- 5 - I want 100 of those")
                    print("- 0 - I don't want to")
                    
                    choice = input("> ")
                    
                    if choice == "1":       # 100 SIDED TRADE
                        
                        if hundoDiceAmount >= 10_000:
                            
                            mundoDiceAmount += 1
                            hundoDiceAmount -= 10_000
                            
                            print("Scrooge McDuck over here.")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "2":     # 1000 SIDED TRADE
                        
                        if thundoDiceAmount >= 1000:
                            
                            mundoDiceAmount += 1
                            thundoDiceAmount -= 1000
                            
                            print("Scrooge McDuck over here.")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "3":     # ENOUGH POINTS
                        
                        if points >= 120_000_000:
                            
                            mundoDiceAmount += 1
                            points -= 120_000_000
                            
                            print("Scrooge McDuck over here.")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "4":     # ENOUGH POINTS x10
                        
                        if points >= 1_200_000_000:
                            
                            mundoDiceAmount += 10
                            points -= 1_200_000_000
                            
                            print("Do a moneyspread.")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "5":     # ENOUGH POINTS x100
                        
                        if points >= 12_000_000_000:
                            
                            mundoDiceAmount += 100
                            points -= 12_000_000_000
                            
                            print("You are the richest person ever!")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "0":     # NOTHING
                        continue
                    
                    else:                   # INVALID
                        print("Invalid choice!")
                        input("> ")
            
            elif choice == "61":        # GET MUNDO DICE WITH 100 DICE
                
                if hundoDiceAmount >= 10_000:
                    mundoDiceAmount += 1
                    hundoDiceAmount -= 10_000
            
            elif choice == "62":        # GET MUNDO DICE WITH 1000 DICE
                
                if thundoDiceAmount >= 1000:
                    mundoDiceAmount += 1
                    thundoDiceAmount -= 1000
            
            elif choice == "63":        # GET MUNDO DICE WITH POINTS
                
                if points >= 120_000_000:
                    mundoDiceAmount += 1
                    points -= 120_000_000
            
            elif choice == "64":        # GET MUNDO DICE WITH POINTS x10
                
                if points >= 1_200_000_000:
                    mundoDiceAmount += 10
                    points -= 1_200_000_000
            
            elif choice == "65":        # GET MUNDO DICE WITH POINTS x100
                
                if points >= 12_000_000_000:
                    mundoDiceAmount += 100
                    points -= 12_000_000_000
            
            else:                       # INVALID
                print("Invalid choice!")
                input("> ")

if __name__ == "__main__":
    main()