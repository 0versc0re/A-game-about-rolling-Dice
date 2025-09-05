from random import *
import json
import os, sys


diceSides = 4
diceAmount = 1
points = 0
pointsMult = 1.0
pointsMultExpo = 1.15

upgradeDice = 50
upgradeExpo = 1.05
moreDice = 50
moreExpo = 1.2

hundoDiceAmount = 0
rollLuck = 1
upgradeLuck = 200
luckExpo = 1.1

def clear():
    os.system("cls")

def save():
    
    saveData = {
        "diceSides": diceSides,
        "diceAmount": diceAmount,
        "points": points,
        "pointsMult": pointsMult,
        "pointsMultExpo": pointsMultExpo,
        "upgradeDice": upgradeDice,
        "upgradeExpo": upgradeExpo,
        "moreDice": moreDice,
        "moreExpo": moreExpo,
        "hundoDiceAmount": hundoDiceAmount,
        "rollLuck": rollLuck,
        "upgradeLuck": upgradeLuck,
        "luckExpo": luckExpo
    }
    
    with open("save.json", "w") as f:
        json.dump(saveData, f, indent=4)

def main():
    
    Run = True
    Menu = True
    Play = False
    Store = False
    
    global diceSides, diceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo
    global hundoDiceAmount, rollLuck, upgradeLuck, luckExpo
    
    while Run:
    
        while Menu:
            
            clear()
            print("0 - New Game")
            print("1 - Load Game")
            print("2 - Exit Game")
            choice = input("> ")
            
            if choice == "0":
                Menu = False
                Play = True
                clear()
                
            elif choice == "1":
                
                try:
                    
                    with open("save.json", "r") as f:
                        data = json.load(f)
                        
                    diceSides = data["diceSides"]
                    diceAmount = data["diceAmount"]
                    points = data["points"]
                    pointsMult = data["pointsMult"]
                    pointsMultExpo = data["pointsMultExpo"]
                    upgradeDice = data["upgradeDice"]
                    upgradeExpo = data["upgradeExpo"]
                    moreDice = data["moreDice"]
                    moreExpo = data["moreExpo"]
                    hundoDiceAmount = data["hundoDiceAmount"]
                    rollLuck = data["rollLuck"]
                    upgradeLuck = data["upgradeLuck"]
                    luckExpo = data["luckExpo"]
                        
                    Menu = False
                    Play = True
                        
                except OSError:
                    print("Corrupt or missing file!")
                    input("> ")
            
            elif choice == "2":
                sys.exit()
        
        while Play:
            
            save()
            clear()
            
            print(f"Your current Dice are {diceSides} sided.")
            print(f"You have {diceAmount} Dice.")
            print(f"You have {hundoDiceAmount} 100 sided Dice.")
            print()
            print(f"Your points: {round(points, 3)}")
            print(f"Your multiplier: {round(pointsMult, 3)}")
            print(f"How lucky you are: {round(rollLuck, 3)}")
            if points >= 1000 ** pointsMult:
                print("You have enough points to upgrade your multiplier!")
            print()
            print("1 - Roll Dice")
            print("2 - Dice store")
            print("3 - Upgrade Multiplier")
            if hundoDiceAmount > 0:
                print("4 - Roll the 100 sided Dice")
            print("0 - Save and Exit")
            
            choice = input("> ")
            
            if choice == "0":
                save()
                sys.exit()
                
            elif choice == "1":
                
                print()
                rollList = []
                total = 0
                
                for roll in range(diceAmount):
                    if rollLuck < diceSides:
                        roll = randint(rollLuck, diceSides)
                    else:
                        roll = diceSides
                    points += roll * pointsMult
                    print(f"You rolled a {roll}!")
                    rollList.append(roll)
                
                print()
                print(f"Your multiplier is {round(pointsMult, 3)}.")
                
                for roll in rollList:
                    total += roll
                print(f"You now have {round(total * pointsMult, 3)} more points.")
                input("> ")
            
            elif choice == "2":
                Store = True
                Play = False
            
            elif choice == "3":
                
                print()
                print("WARNING!")
                print("UPGRADING YOUR MULTIPLIER RESETS YOUR")
                print("DICE AND POINTS BACK TO 1 AND 0")
                print("STORE PRICES ARE ALSO RESET")
                print()
                print(f"Your current multiplier: {round(pointsMult, 3)}")
                print(f"You need {round(1000 ** pointsMult, 3)} points to upgrade your Multiplier.")
                print(f"1 - Upgrade Multiplier")
                print(f"0 - I don't want to")
                
                choice = input("> ")
                
                if choice == "1":
                    
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
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        print()
                        print("Wise choice.")
                        print(f"Your new multiplier: {round(pointsMult, 3)}")
                        input("> ")
                        
                    else:
                        print("You don't have enough points!")
                        input("> ")
                
                elif choice == "0":
                    continue
            
            elif choice == "4":
                    
                    if hundoDiceAmount > 0:
                    
                        print()
                        rollList = []
                        total = 0
                        
                        for roll in range(hundoDiceAmount):
                            roll = randint(1, 100)
                            points += roll * pointsMult
                            print(f"You rolled a {roll}!")
                            rollList.append(roll)
                        
                        print()
                        print(f"Your multiplier is {round(pointsMult, 3)}.")
                        
                        for roll in rollList:
                            total += roll
                        print(f"You now have {round(total * pointsMult, 3)} more points.")
                        input("> ")
            
            else:
                print("Invalid choice!")
                input("> ")
                
        while Store:
            
            save()
            clear()
            
            hundoPairs = {
                (1, 98), (98, 1), (2, 49), (49, 2), (7, 14), (14, 7),                       # 98 total
                (100, 1), (10, 10), (2, 50), (50, 2), (4, 25), (25, 4), (5, 20), (20, 5),   # 100 total
                (1, 102), (102, 1), (2, 51), (51, 2), (3, 34), (34, 3), (6, 17), (17, 6)    # 102 total
            }
            
            print(f"Your current Dice are {diceSides} sided.")
            print(f"You have {diceAmount} Dice.")
            print(f"You have {hundoDiceAmount} a 100 sided Dice.")
            print()
            print(f"You have {round(points, 3)} points.")
            print(f"How lucky you are: {round(rollLuck, 3)}")
            if (diceAmount, diceSides) in hundoPairs:
                print()
                print("You can now get the ELUSIVE 100 sided Die (or another)")
                print("by merging your all of your Dice together!")
            print()
            print(f"1 - Upgrade Dice: {round(upgradeDice * diceAmount, 3)} points")
            print(f"2 - Buy more Dice: {round(moreDice * 1.5, 3)} points")
            if (diceAmount, diceSides) in hundoPairs:
                print("3 - Get the 100 sided Die")
            print(f"4 - Buy a Lucky Amulet: {round(upgradeLuck, 3)} points")
            print("0 - Exit Store")
            
            choice = input("> ")
            
            if choice == "1":
                
                if points >= upgradeDice * diceAmount:
                    points -= upgradeDice * diceAmount
                    upgradeDice = upgradeDice ** upgradeExpo
                    diceSides += 1
                    print(f"You now have {diceAmount} dice with {diceSides} sides each.")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "2":
                
                if points >= moreDice * 1.5:
                    points -= moreDice * 1.5
                    moreDice = moreDice ** moreExpo
                    diceAmount += 1
                    print(f"You now have {diceAmount} dice with {diceSides} sides each.")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "3":
                
                print()
                print("WARNING!")
                print("YOU'RE ABOUT TO GET RID OF ALL OF YOUR DICE FOR A 100 SIDED DIE")
                print("YOU'LL HAVE YOUR NEW 100 SIDED DIE AND THE ORIGINAL 4 SIDED DIE")
                print("(the 100 sided die doesn't persist between multiplier upgrades)")
                print()
                print("1 - I want the 100 sided die")
                print("0 - I don't want to")
                
                choice = input("> ")
                
                if choice == "1":
                    
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
                
                elif choice == "0":
                    continue
                
                else:
                    print("Invalid choice!")
                    input("> ")
            
            elif choice == "4":
                
                if points >= upgradeLuck:
                    points -= upgradeLuck
                    upgradeLuck = upgradeLuck ** luckExpo
                    rollLuck += 1
                    print("You feel luckier!")
                    input("> ")
                    
                else:
                    print("You don't have enough points!")
                    input("> ")
            
            elif choice == "0":
                Play = True
                Store = False
            
            else:
                print("Invalid choice!")
                input("> ")


if __name__ == "__main__":
    main()