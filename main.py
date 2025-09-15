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
trundoDiceAmount = 0

# LUCK VARIABLES
rollLuck = 1
upgradeLuck = 200
luckExpo = 1.1

# UPGRADE TREE VARIABLES
storePriceOffset = 1.0
diceAmountOffset = 1.0
luckOffset = 1.0
multiplierOffset = 1.0

def clearScreen():
    os.system("cls")

def saveGame():
    
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
        "trundoDiceAmount": trundoDiceAmount,
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
    
    numberSuffix = ["M",   "B",   "T",   "Qa",   "Qi",   "Sx",   "Sp",   "Oc",   "No",   "D",       # e006 - e033
                    "UD",  "DD",  "TD",  "QaD",  "QiD",  "SxD",  "SpD",  "OcD",  "NoD",  "Vg",      # e036 - e063
                    "UVg", "DVg", "TVg", "QaVg", "QiVg", "SxVg", "SpVg", "OcVg", "NoVg", "Tg",      # e066 - e093
                    "UTg", "DTg", "TTg", "QaTg", "QiTg", "SxTg", "SpTg", "OcTg", "NoTg", "Qd",      # e096 - e123
                    "UQd", "DQd", "TQd", "QaQd", "QiQd", "SxQd", "SpQd", "OcQd", "NoQd", "Qt"]      # e126 - e153
    
    if number < 1_000_000:
        return str(round(number, 2))

    for i, suffix in enumerate(numberSuffix, start=2):
        if number < 1000 ** (i + 1):
            return str(round(number / (1000 ** i), 2)) + suffix

    return str(round(number / (1000 ** len(numberSuffix)), 2)) + numberSuffix[-1]

def rollDice(amount, sides, offset, mult, luck):
    
    print()
    totalRolls = round(amount * offset)
    total = 0

    if totalRolls < 5:
        for _ in range(totalRolls):
            roll = randint(luck, sides) if luck < sides else sides
            total += roll
            print(f"You rolled {roll}!")
    else:
        for _ in range(totalRolls):
            roll = randint(luck, sides) if luck < sides else sides
            total += roll
        print(f"You rolled your Dice {bigNumber(round(amount * offset))} times!")

    totalPoints = total * mult

    print(f"\nYour current Multiplier: {round(mult, 2)} MP")
    print(f"You now have {bigNumber(totalPoints)} more points.")
    input("> ")
    
    return totalPoints

def chooseDiceAmount(points, amount, name: str, price):
    
    maxAmount = points // price
    
    print(f"\nYou have {bigNumber(points)} points.")
    print(f"With your points, you can get {bigNumber(maxAmount)} {name} sided Dice\n")
    
    try:
        choice = int(input("How many Dice do you want? > "))
    except ValueError:
        print(f"Please choose a number between 1 and {bigNumber(maxAmount)}.")
        input("> ")
        return 0, 0
    
    if not (1 <= choice <= maxAmount):
        
        if choice <= 0:
            msg = "You must buy at least 1 Die!"
        else:
            msg = "You don't have enough points!"
            
        print(msg)
        input("> ")
        return 0, 0
    
    amount += choice
    print(f"You now have {bigNumber(amount)} {name} sided Dice.")
    input("> ")
    return choice, choice * price

def main():
    
    # BOOLEANS
    Run = True
    Menu = True
    Play = False
    Store = False
    Tree = False
    
    # GLOBAL VARIABLES
    global diceSides, diceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo, rollLuck, upgradeLuck, luckExpo
    global hundoDiceAmount, thundoDiceAmount, mundoDiceAmount, trundoDiceAmount
    global storePriceOffset, diceAmountOffset, luckOffset, multiplierOffset
    
    # GAME RUNNING
    while Run:
    
        # GAME MENU
        while Menu:
            
            clearScreen()
            print("- 0 - New Game")
            print("- 1 - Load Game")
            print("- 2 - Exit Game")
            choice = input("> ")
            
            if choice == "0":           # NEW GAME
                
                print("\nAre you sure you want to start a New Game?")
                print("- 1 - No  New Game")
                print("- 0 - Yes New Game")
                choice = input("> ")
                
                if choice == "0":       # NO
                    Menu = False
                    Play = True
                    
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
                    trundoDiceAmount = data["trundoDiceAmount"]
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
        
        # GAME PLAY
        while Play:
            
            saveGame()
            clearScreen()
            
            # DICE DISPLAY
            print(f"You have {diceAmount} {diceSides} sided Dice.")                                                                 # NOT SECRET
            print(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} Hundred sided Dice.")                               # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} Thousand sided Dice")     # SECRET
            if mundoDiceAmount > 0: print(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} Million sided Dice")    # SECRET
            if trundoDiceAmount > 0: print(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} Trillion sided Dice") # SECRET
                        
            # POINTS DISPLAY
            print(f"\nYou have {bigNumber(points)} points.")
            
            # LUCK AND MULTIPLIER DISPLAY
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            print(f"Your current Multiplier: {round(pointsMult, 2)} MP")
            if points >= 1000 ** pointsMult: print("You have enough points to upgrade your Multiplier!")
            if pointsMult >= 10: print("You have enough Multiplier to upgrade it's scaling!")

            # OPTIONS DISPLAY
            print("\n- 1 - Dice Store")
            print("- 2 - Upgrade Multiplier")
            if pointsMult >= 10: print("- 3 - Upgrade Multiplier scaling")
            print("- 4 - Roll Dice")
            if hundoDiceAmount > 0: print("- 5 - Roll the Hundred sided Dice")
            if thundoDiceAmount > 0: print("- 6 - Roll the Thousand sided Dice")
            if mundoDiceAmount > 0: print("- 7 - Roll the Million sided Dice")
            if trundoDiceAmount > 0: print("- 8 - Roll the Trillion sided Dice")
            if points >= 1e15: print("- 9 - Go to the Upgrade Tree")
            print("- 0 - Save and Exit")
            
            choice = input("> ")
            
            if choice == "0":           # SAVE AND EXIT
                saveGame()
                sys.exit()
            
            elif choice == "1":         # DICE STORE
                Store = True
                Play = False
            
            elif choice == "2":         # UPGRADE MULTIPLIER
                
                print("\nWARNING!")
                print("UPGRADING YOUR MULTIPLIER RESETS YOUR")
                print("DICE AND POINTS BACK TO 1 AND 0")
                print("STORE PRICES ARE ALSO RESET\n")
                print(f"Your current multiplier: {round(pointsMult, 2)} MP")
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
                        trundoDiceAmount = 0
                        
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        print("\nWise choice.")
                        print(f"Your new multiplier: {round(pointsMult, 2)} MP")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "0":         # NO
                    continue
                
                else:                       # INVALID
                    print("Invalid choice!")
                    input("> ")
            
            elif choice == "3":         # UPGRADE MULTIPLIER SCALING
                
                if pointsMult >= 10:
                
                    print("\nWARNING!")
                    print("UPGRADING YOUR MULTIPLIER'S SCALING RESETS")
                    print("EVERYTHING BUT YOUR MULTIPLIER BACK TO 1\n")
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
                            
                        print("\nGreat choice!")
                        print(f"Your new multiplier: {round(pointsMult, 2)} MP")
                        input("> ")

                    elif choice == "0":     # NO
                        continue
                
                    else:                   # INVALID
                        print("Invalid choice!")
                        input("> ")
            
            elif choice == "4":         # ROLL DICE
                
                points += rollDice(diceAmount, diceSides, diceAmountOffset, pointsMult, rollLuck)
            
            elif choice == "5":         # ROLL HUNDO
                    
                if hundoDiceAmount > 0:
                    points += rollDice(hundoDiceAmount, 100, diceAmountOffset, pointsMult, 1)
        
            elif choice == "6":         # ROLL THUNDO
                
                if thundoDiceAmount > 0:
                    points += rollDice(thundoDiceAmount, 1000, diceAmountOffset, pointsMult, 1)
            
            elif choice == "7":         # ROLL MUNDO
                
                if mundoDiceAmount > 0:
                    points += rollDice(mundoDiceAmount, 1_000_000, diceAmountOffset, pointsMult, 1)

            elif choice == "8":         # ROLL TRUNDO
                
                if trundoDiceAmount > 0:
                    points += rollDice(trundoDiceAmount, 1e12, diceAmountOffset, pointsMult, 1)

            elif choice == "9":         # UPGRADETREE
                if points >= 1e15:
                    Tree = True
                    Play = False
            
            else:                       # INVALID
                print("Invalid choice!")
                input("> ")
        
        # GAME STORE     
        while Store:
            
            saveGame()
            clearScreen()
            
            hundoPairs = {
                (1, 97),  (97, 1),  (1, 98), (98, 1), (2, 49), (49, 2), (7, 14), (14, 7),                     # total 97 98
                (1, 99),  (99, 1),  (3, 33), (33, 3), (9, 11), (11, 9),                                       # total 99
                (100, 1), (10, 10), (2, 50), (50, 2), (4, 25), (25, 4), (5, 20), (20, 5), (1, 101), (101, 1), # total 100 101
                (1, 102), (102, 1), (2, 51), (51, 2), (3, 34), (34, 3), (6, 17), (17, 6), (1, 103), (103, 1)  # total 102 103
            }
            
            # DICE DISPLAY
            print(f"You have {diceAmount} {diceSides} sided Dice.")                                                                 # NOT SECRET
            print(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} Hundred sided Dice.")                               # NOT SECRET
            if thundoDiceAmount > 0: print(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} Thousand sided Dice")     # SECRET
            if mundoDiceAmount > 0: print(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} Million sided Dice")    # SECRET
            if trundoDiceAmount > 0: print(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} Trillion sided Dice") # SECRET
                
            # POINTS AND LUCK DISPLAY
            print(f"\nYou have {bigNumber(points)} points.")
            print(f"How lucky you are: {round((rollLuck / diceSides) * 100, 2)}%")
            
            # BIG DICE DISPLAY
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000):
                print("\nYou can now get an ELUSIVE Hundred sided Die")
                print("by merging your all of your Dice together!")
                print("Or by paying 12000 points for it!")
            if hundoDiceAmount >= 10 or points >= 120_000:
                print("\nYou can now get an ADORED Thousand sided Die")
                print("by trading off 10 of your Hundred sided Die!")
                print("Or by paying 120000 points for it!")
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000:
                print("\nYou can now get a Million sided Die")
                print("by trading off your Dice!")
                print("Or by paying 120 Million points for it!")

            # TRILLION SIDED DICE
            if mundoDiceAmount >= 1_000_000 or points >= 120e12:
                print("\nYou can now get a Trillion sided Die")
                print("By trading off your Million sided Dice!")
                print("Or by paying 120 Trillion points for it!")
            
            # OPTIONS DISPLAY
            print(f"\n- 1 - Upgrade Dice: {bigNumber((upgradeDice * diceAmount) / storePriceOffset)} points")
            print(f"- 2 - Buy more Dice: {bigNumber((moreDice * 1.5) / storePriceOffset)} points")
            print(f"- 3 - Buy a Lucky Amulet: {bigNumber(upgradeLuck / storePriceOffset)} points")
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000): print("- 4 - Get a Hundred sided Die")
            if hundoDiceAmount >= 10 or points >= 120_000: print("- 5 - Get a Thousand sided Die")
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000: print("- 6 - Get a Million sided Die")
            if mundoDiceAmount >= 1_000_000 or points >= 120e12: print("- 7 - Get a Trillion sided Die")
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
                
                    print("\nWARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF ALL OF YOUR DICE FOR A Hundred SIDED DIE")
                    print("YOU'LL HAVE YOUR NEW Hundred SIDED DIE AND THE ORIGINAL 4 SIDED DIE")
                    print("YOU WON'T LOSE YOUR DICE IF YOU PAY FOR THE Hundred SIDED DIE")
                    print("(the Hundred sided Die doesn't persist between multiplier upgrades)\n")
                    print("- 1 - Trade off my Dice")
                    print("- 2 - Pay for the Die")
                    print("- 3 - Choose how many Dice")
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
                            
                            print("Welcome your new Hundred sided Die!")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 12_000:
                            
                            hundoDiceAmount += 1
                            points -= 12_000
                            
                            print("Welcome your new Hundred sided Die!")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "3":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(points, hundoDiceAmount, "Hundred", 12_000)
                        hundoDiceAmount += dice
                        points -= spent

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        print("Invalid choice!")
                        input("> ")

            elif choice == "5":         # GET THUNDO DICE
                
                if hundoDiceAmount >= 10 or points >= 120_000:
                    
                    print("\nWARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF 10 OF YOUR Hundred SIDED DICE")
                    print("OR PAY 120000 POINTS FOR AN INCREDIBLE Thousand SIDED DIE")
                    print("(this still doesn't persist between multiplier upgrades)\n")
                    print("- 1 - Trade off my Dice")
                    print("- 2 - Pay for the Die")
                    print("- 3 - Choose how many Dice")
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

                    elif choice == "3":         # CHOOSE HOW MANY DICE

                        dice, spent = chooseDiceAmount(points, thundoDiceAmount, "Thousand", 120_000)
                        thundoDiceAmount += dice
                        points -= spent

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        print("Invalid choice!")
                        input("> ")

            elif choice == "6":         # GET MUNDO DICE
                
                if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000:
                    
                    print("\nWARNING!")
                    print("YOU'RE ABOUT TO TRADE OFF YOUR DICE")
                    print("OR PAY 120 Million POINTS FOR A Million SIDED DIE\n")
                    print("- 1 - Trade off my Hundred sided Dice")
                    print("- 2 - Trade off my Thousand sided Dice")
                    print("- 3 - Pay for the Die")
                    print("- 4 - Choose how many Dice")
                    print("- 0 - I don't want to")
                    
                    choice = input("> ")
                    
                    if choice == "1":       # 100 SIDED TRADE
                        
                        if hundoDiceAmount >= 10_000:
                            
                            mundoDiceAmount += 1
                            hundoDiceAmount -= 10_000
                            
                            print("Are you Mr. Beast?")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "2":     # 1000 SIDED TRADE
                        
                        if thundoDiceAmount >= 1000:
                            
                            mundoDiceAmount += 1
                            thundoDiceAmount -= 1000
                            
                            print("Are you Mr. Beast?")
                            input("> ")
                            
                        else:
                            print("You don't have enough Dice!")
                            input("> ")
                    
                    elif choice == "3":     # ENOUGH POINTS
                        
                        if points >= 120_000_000:
                            
                            mundoDiceAmount += 1
                            points -= 120_000_000
                            
                            print("Are you Mr. Beast?")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                    
                    elif choice == "4":     # CHOOSE HOW MANY DICE

                        dice, spent = chooseDiceAmount(points, mundoDiceAmount, "Million", 120_000_000)
                        mundoDiceAmount += dice
                        points -= spent
                    
                    elif choice == "0":     # NOTHING
                        continue
                    
                    else:                   # INVALID
                        print("Invalid choice!")
                        input("> ")

            elif choice == "7":         # GET TRUNDO DICE
                
                if mundoDiceAmount >= 1_000_000 or points >= 120e12:
                
                    print("\nWARNING!")
                    print("YOU'RE ABOUT TO TRADE OF YOUR DICE")
                    print("OR PAY 120 Trillion POINTS FOR A Trillion SIDED DIE\n")
                    print("- 1 - Trade off my Dice")
                    print("- 2 - Pay for the Die")
                    print("- 3 - Choose how many Dice")
                    print("- 0 - I don't want to")
                    
                    choice = input("> ")
                    
                    if choice == "1":       # TRADE OFF MUNDO
                        
                        if mundoDiceAmount >= 1_000_000:
                            
                            trundoDiceAmount += 1
                            mundoDiceAmount -= 1_000_000
                            
                            print("This is quite big.")
                            input("> ")
                            
                        else:
                            print("You don't have enough dice!")
                            
                    elif choice == "2":     # PAY FOR TRUNDO
                        
                        if points >= 120e12:
                            
                            trundoDiceAmount += 1
                            points -= 120e12
                            
                            print("This is quite big.")
                            input("> ")
                            
                        else:
                            print("You don't have enough points!")
                            input("> ")
                            
                    elif choice == "3":     # CHOOSE HOW MANY DICE

                        dice, spent = chooseDiceAmount(points, trundoDiceAmount, "Trillion", 120e12)
                        trundoDiceAmount += dice
                        points -= spent
                    
                    elif choice == "0":     # NOTHING
                        continue
                    
                    else:                   # INVALID
                        print("Invalid choice!")
                        input("> ")

            else:                       # INVALID
                print("Invalid choice!")
                input("> ")

        # GAME TREE
        while Tree:
            
            saveGame()
            clearScreen()
            
            print("Welcome to the Upgrade Tree!")
            print("If you're here, it means that you've accumulated over 1 quadrillion points")
            print("and you're wondering what this magical place could possibly be?")
            print("(also these are PERMANENT, meaning upgrading Multiplier won't reset these)\n")
            print("Well wait no further!")
            print("Here you can upgrade anything you could ever think of!")
            print("You want the Store prices to be cheaper? You got it!")
            print("You want more Dice per Dice? You can have that!")
            print("You can even have more Multiplier and better Scaling!\n")
            print("- 1 - View possible Upgrades")
            print("- 0 - Leave the Upgrade Tree")
            
            choice = input("> ")
            
            if choice == "0":       # LEAVE
                Tree = False
                Play = True
            
            elif choice == "1":     # POSSIBLE UPGRADES
                
                print(f"\nYou have {bigNumber(points)} points.\n")
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