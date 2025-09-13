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

# UPGRADE TREE VARIABLES
storePriceOffset = 1.0
diceAmountOffset = 1.0
luckOffset = 1.0
multiplierOffset = 1.0

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
        "luckExpo":         luckExpo,
        "storePriceOffset": storePriceOffset,
        "diceAmountOffset": diceAmountOffset,
        "luckOffset":       luckOffset,
        "multiplierOffset": multiplierOffset
    }
    
    with open("save.json", "w") as f:
        json.dump(saveData, f, indent=4)

def bigNumber(number):
    
    numberSuffix = ["M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "D",
                    "Ud", "Dd", "Td", "Qad", "Qid", "Sxd", "Spd", "Ocd", "Nod"]
    
    if number < 1_000_000:
        return str(round(number, 2))

    for i, suffix in enumerate(numberSuffix, start=2):
        if number < 1000 ** (i + 1):
            return str(round(number / (1000 ** i), 2)) + suffix

    return str(round(number / (1000 ** len(numberSuffix)), 2)) + numberSuffix[-1]

def main():
    
    # BOOLEANS
    Run = True
    Menu = True
    Play = False
    Store = False
    Tree = False
    
    # GLOBAL VARIABLES
    global diceSides, diceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo
    global hundoDiceAmount, thundoDiceAmount, mundoDiceAmount
    global rollLuck, upgradeLuck, luckExpo
    global storePriceOffset, diceAmountOffset, luckOffset, multiplierOffset
    
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
                    storePriceOffset = data["storePriceOffset"]
                    diceAmountOffset = data["diceAmountOffset"]
                    luckOffset =       data["luckOffset"]
                    multiplierOffset = data["multiplierOffset"]
                        
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
            print(f"You have {diceAmount} {diceSides} sided Dice.")                                                              # NOT SECRET
            print(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} 100 sided Dice.")                            # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} 1000 sided Dice")  # SECRET
            if mundoDiceAmount > 0: print(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} Million sided Dice") # SECRET
                        
            # POINTS DISPLAY
            print()
            print(f"You have {bigNumber(points)} points.")
            
            # LUCK AND MULTIPLIER DISPLAY
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            print(f"Your current multiplier: {round(pointsMult, 2)}")
            if points >= 1000 ** pointsMult: print("You have enough points to upgrade your multiplier!")
            if pointsMult >= 10: print("You have enough Multiplier to upgrade it's scaling!")

            # OPTIONS DISPLAY
            print()
            print("- 1 - Roll Dice")
            print("- 2 - Dice store")
            print("- 3 - Upgrade Multiplier")
            if hundoDiceAmount > 0: print("- 4 - Roll the 100 sided Dice")
            if thundoDiceAmount > 0: print("- 5 - Roll the 1000 sided Dice")
            if mundoDiceAmount > 0: print("- 6 - Roll the Million sided Dice")
            if pointsMult >= 10: print("- 7 - Upgrade Multiplier scaling")
            if points >= 1e15: print("- 8 - Go to the Upgrade Tree")
            print("- 0 - Save and Exit")
            
            choice = input("> ")
            
            if choice == "0":           # SAVE AND EXIT
                save()
                sys.exit()
                
            elif choice == "1":         # ROLL DICE

                print()
                totalRolls = round(diceAmount * diceAmountOffset)
                total = 0
                
                if totalRolls < 5:
                    for _ in range(totalRolls):
                        roll = randint(rollLuck, diceSides) if rollLuck < diceSides else diceSides
                        total += roll
                        print(f"You rolled a {roll}!")
                else:
                    for _ in range(totalRolls):
                        roll = randint(rollLuck, diceSides) if rollLuck < diceSides else diceSides
                        total += roll
                    print(f"You rolled your Dice {bigNumber(round(diceAmount * diceAmountOffset))} times!")
                    
                totalPoints = total * pointsMult
                points += totalPoints
                
                print()
                print(f"Your current Multiplier: {round(pointsMult, 2)}")
                print(f"You now have {bigNumber(totalPoints)} more points.")
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
                print(f"You need {bigNumber(1000 ** pointsMult)} points to upgrade your Multiplier.")
                
                print("- 1 - Upgrade Multiplier")
                print("- 0 - I don't want to")
                
                choice = input("> ")
                
                if choice == "1":           # YES
                    
                    if points >= 1000 ** pointsMult:
                        points -= 1000 ** pointsMult
                        pointsMult *= pointsMultExpo * multiplierOffset
                        
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
                
                else:                       # INVALID
                    print("Invalid choice!")
                    input("> ")
                
            elif choice == "4":         # ROLL HUNDO
                    
                if hundoDiceAmount > 0:
                    
                    print()
                    totalRolls = round(hundoDiceAmount * diceAmountOffset)
                    total = 0
                    
                    if totalRolls < 5:
                        for _ in range(totalRolls):
                            roll = randint(1, 100)
                            total += roll
                            print(f"You rolled a {roll}!")
                    else:
                        for _ in range(totalRolls):
                            roll = randint(1, 100)
                            total += roll
                        print(f"You rolled your Dice {bigNumber(round(hundoDiceAmount * diceAmountOffset))} times!")
                        
                    totalPoints = total * pointsMult
                    points += totalPoints
                    
                    print()
                    print(f"Your current Multiplier: {round(pointsMult, 2)}")
                    print(f"You now have {bigNumber(totalPoints)} more points.")
                    input("> ")
            
            elif choice == "5":         # ROLL THUNDO
                
                if thundoDiceAmount > 0:
                    
                    print()
                    totalRolls = round(thundoDiceAmount * diceAmountOffset)
                    total = 0
                    
                    if totalRolls < 5:
                        for _ in range(totalRolls):
                            roll = randint(1, 1_000)
                            total += roll
                            print(f"You rolled a {roll}!")
                    else:
                        for _ in range(totalRolls):
                            roll = randint(1, 1_000)
                            total += roll
                        print(f"You rolled your Dice {bigNumber(round(thundoDiceAmount * diceAmountOffset))} times!")
                        
                    totalPoints = total * pointsMult
                    points += totalPoints
                    
                    print()
                    print(f"Your current Multiplier: {round(pointsMult, 2)}")
                    print(f"You now have {bigNumber(totalPoints)} more points.")
                    input("> ")
            
            elif choice == "6":         # ROLL MUNDO
                
                if mundoDiceAmount > 0:
                    
                    print()
                    totalRolls = round(mundoDiceAmount * diceAmountOffset)
                    total = 0
                    
                    if totalRolls < 5:
                        for _ in range(totalRolls):
                            roll = randint(1, 1_000_000)
                            total += roll
                            print(f"You rolled a {roll}!")
                    else:
                        for _ in range(totalRolls):
                            roll = randint(1, 1_000_000)
                            total += roll
                        print(f"You rolled your Dice {bigNumber(round(mundoDiceAmount * diceAmountOffset))} times!")
                        
                    totalPoints = total * pointsMult
                    points += totalPoints
                    
                    print()
                    print(f"Your current Multiplier: {round(pointsMult, 2)}")
                    print(f"You now have {bigNumber(totalPoints)} more points.")
                    input("> ")
            
            elif choice == "7":         # UPGRADE MULTIPLIER SCALING
                
                if pointsMult >= 10:
                
                    print()
                    print("WARNING!")
                    print("UPGRADING YOUR MULTIPLIER'S SCALING RESETS")
                    print("EVERYTHING BUT YOUR MULTIPLIER BACK TO 1")
                    print()
                    print("- 1 - Upgrade Multiplier scaling")
                    print("- 0 - I don't want to")
                    
                    choice == input("> ")
                    
                    if choice == "1":       # YES
                        
                        pointsMult -= 10
                        pointsMultExpo += 0.15 * multiplierOffset
                            
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
                        print("Great choice!")
                        print(f"Your new multiplier: {round(pointsMult, 2)}")
                        input("> ")

                    elif choice == "0":     # NO
                        continue
                
                    else:                   # INVALID
                        print("Invalid choice!")
                        input("> ")
            
            elif choice == "8":         # UPGRADETREE
                
                if points >= 1e15:
                    Tree = True
                    Play = False
            
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
            print(f"You have {diceAmount} {diceSides} sided Dice.")                                    # NOT SECRET
            print(f"You have {bigNumber(hundoDiceAmount)} 100 sided Dice.")                            # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {bigNumber(thundoDiceAmount)} 1000 sided Dice")  # SECRET
            if mundoDiceAmount > 0: print(f"You have {bigNumber(mundoDiceAmount)} Million sided Dice") # BIG SECRET
                
            # POINTS AND LUCK DISPLAY
            print()
            print(f"You have {bigNumber(points)} points.")
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            
            # BIG DICE DISPLAY ONLY IF NO MUNDO
            if mundoDiceAmount < 0:
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
            print(f"- 1 - Upgrade Dice: {bigNumber((upgradeDice * diceAmount) / storePriceOffset)} points")
            print(f"- 2 - Buy more Dice: {bigNumber((moreDice * 1.5) / storePriceOffset)} points")
            print(f"- 3 - Buy a Lucky Amulet: {bigNumber(upgradeLuck / storePriceOffset)} points")
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000): print("- 4 - Get a 100 sided Die")
            if hundoDiceAmount >= 10 or points >= 120_000: print("- 5 - Get a 1000 sided Die")
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000: print("- 6 - Get a Million sided Die")
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
                    rollLuck += 1 * luckOffset
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
                    if points >= 120_000: print("- 3 - I want 10 of those")
                    if points >= 1_200_000: print("- 4 - I want 100 of those")
                    if points >= 12_000_000: print("- 5 - I want 1000 of those")
                    if points >= 120_000_000: print("- 6 - I want 10000 of those")
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
                            
                    elif choice == "4":         # 100 WITH POINTS
                        
                        if points >= 1_200_000:
                            
                            hundoDiceAmount += 100
                            points -= 1_200_000
                            
                            print("I don't get why you would buy this.")
                            input("> ")
                    
                    elif choice == "5":         # 1000 WITH POINTS
                        
                        if points >= 12_000_000:
                            
                            hundoDiceAmount += 1000
                            points -= 12_000_000
                                
                            print("You do you I guess.")
                            input("> ")

                    elif choice == "6":         # 10000 WITH POINTS
                        
                        if points >= 120_000_000:
                            
                            hundoDiceAmount += 10_000
                            points -= 120_000_000
                                
                            print("This is just dumb.")
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
            
            elif choice == "45":        # GET HUNDO DICE WITH POINTS x1000
                
                if points >= 12_000_000:
                    hundoDiceAmount += 1000
                    points -= 120_000_000
                    
            elif choice == "46":        # GET HUNDO DICE WITH POINTS x10000
                
                if points >= 120_000_000:
                    hundoDiceAmount += 10_000
                    points -= 120_000_000
            
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
                    if points >= 1_200_000: print("- 3 - I want 10 of those")
                    if points >= 12_000_000: print("- 4 - I want 100 of those")
                    if points >= 120_000_000: print("- 5 - I want 1000 of those")
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
                    
                    elif choice == "4":         # 100 WITH POINTS
                        
                        if points >= 12_000_000:
                            
                            thundoDiceAmount += 100
                            points -= 12_000_000
                            
                            print("Detected motion at front door.")
                            input("> ")

                    elif choice == "5":         # 1000 WITH POINTS
                        
                        if points >= 120_000_000:
                            
                            thundoDiceAmount += 1000
                            points -= 120_000_000
                            
                            print("JUST GET A MILLION SIDED DIE!")
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
            
            elif choice == "55":        # GET THUNDO DICE WITH POINTS x1000
                
                if points >= 120_000_000:
                    thundoDiceAmount += 1000
                    points -= 120_000_000
            
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
                    if points >= 1_200_000_000: print("- 4 - I want 10 of those")
                    if points >= 12_000_000_000: print("- 5 - I want 100 of those")
                    if points >= 120_000_000_000: print("- 6 - I want 1000 of those")
                    if points >= 1_200_000_000_000: print("- 7 - I want 10000 of those")
                    if points >= 12_000_000_000_000: print("- 8 - I want 100000 of those")
                    if points >= 120_000_000_000_000: print("- 9 - I want a Million of those")
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
                    
                    elif choice == "5":     # ENOUGH POINTS x100
                        
                        if points >= 12_000_000_000:
                            
                            mundoDiceAmount += 100
                            points -= 12_000_000_000
                            
                            print("You are the richest person ever!")
                            input("> ")
                            
                    elif choice == "6":     # ENOUGH POINTS x1000
                        
                        if points >= 120_000_000_000:
                            
                            mundoDiceAmount += 1000
                            points -= 120_000_000_000
                            
                            print("Who's could be calling me at this hour?")
                            print("Money's calling.")
                            input("> ")
                    
                    elif choice == "7":     # ENOUGH POINTS x10000
                        
                        if points >= 1_200_000_000_000:
                            
                            mundoDiceAmount += 10_000
                            points -= 1_200_000_000_000
                            
                            print("Mr. Beast")
                            input("> ")
                            
                    elif choice == "8":     # ENOUGH POINTS x100000
                        
                        if points >= 12_000_000_000_000:
                            
                            mundoDiceAmount += 100_000
                            points -= 12_000_000_000_000
                            
                            print("Elon Musk")
                            input("> ")
                    
                    elif choice == "9":     # ENOUGH POINTS xMILLION
                        
                        if points >= 120_000_000_000_000:
                            
                            mundoDiceAmount += 1_000_000
                            points -= 120_000_000_000_000
                            
                            print("Ho Lee Sheet")
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
            
            elif choice == "66":        # GET MUNDO DICE WITH POINTS x1000
                
                if points >= 120_000_000_000:
                    mundoDiceAmount += 1000
                    points -= 120_000_000_000
            
            elif choice == "67":        # GET MUNDO DICE WITH POINTS x10000
                
                if points >= 1_200_000_000_000:
                    mundoDiceAmount += 10_000
                    points -= 1_200_000_000_000
                    
            elif choice == "68":        # GET MUNDO DICE WITH POINTS x100000
                
                if points >= 12_000_000_000_000:
                    mundoDiceAmount += 100_000
                    points -= 12_000_000_000_000
            
            elif choice == "69":        # GET MUNDO DICE WITH POINTS xMILLION
                
                if points >= 120_000_000_000_000:
                    mundoDiceAmount += 1_000_000
                    points -= 120_000_000_000_000
            
            else:                       # INVALID
                print("Invalid choice!")
                input("> ")

        while Tree:
            
            save()
            clear()
            
            print("Welcome to the Upgrade Tree!")
            print("If you're here, it means that you've accumulated over 1 quadrillion points")
            print("and you're wondering what this magical place could possibly be?")
            print("(also these are PERMANENT, meaning upgrading Multiplier won't reset these)")
            print()
            print("Well wait no further!")
            print("Here you can upgrade anything you could ever think of!")
            print("You want the Store prices to be cheaper? You got it!")
            print("You want more Dice per Dice? You can have that!")
            print("You can even have more Multiplier and better Scaling!")
            print()
            print("- 1 - View possible Upgrades")
            print("- 0 - Leave the Upgrade Tree")
            
            choice = input("> ")
            
            if choice == "0":       # LEAVE
                Tree = False
                Play = True
            
            elif choice == "1":     # POSSIBLE UPGRADES
                
                print()
                print(f"You have {bigNumber(points)} points.")
                print()
                print(f"- 1 - Better store prices: {bigNumber(1e15 * storePriceOffset)} points")
                print(f"- 2 - More dice per dice: {bigNumber(1e15 * diceAmountOffset)} points")
                print(f"- 3 - Get even luckier: {bigNumber(1e18 * luckOffset)} points")
                print(f"- 4 - More Multiplier: {bigNumber(1e21 * multiplierOffset)} points")
                print("- 0 - Exit to the Upgrade Tree")
                
                choice = input("> ")
                
                if choice == "0":       # EXIT
                    continue
                
                elif choice == "1":     # BETTER PRICES
                    
                    if points >= 1e15:
                        
                        storePriceOffset += 0.2
                        points -= 1e15
                        
                        print("Store Prices are now cheaper!")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "2":     # MORE DICE
                    
                    if points >= 1e15:
                        
                        points -= 1e15
                        diceAmountOffset += 0.2
                        
                        print("You magically have more dice!")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "3":     # MORE LUCK
                    
                    if points >= 1e18:
                        
                        points -= 1e18
                        luckOffset += 0.2
                        
                        print("You feel even luckier!")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "4":     # MORE MULTIPLIER
                    
                    if points >= 1e21:
                        
                        points -= 1e21
                        multiplierOffset += 0.2
                        
                        print("The Multiplier already feels stronger!")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                else:                   # INVALID
                    print("Invalid choice!")
                    input("> ")
            
            else:                   # INVALID
                print("Invalid choice!")
                input("> ")

if __name__ == "__main__":
    main()