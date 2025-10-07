# IMPORTS
import json, sys
import random, curses
from curses import wrapper
from curses.textpad import Textbox


# DICE VARIABLES
diceSides      = 4
diceAmount     = 1
points         = 0
pointsMult     = 1.0
pointsMultExpo = 1.15

# SHOP VARIABLES
upgradeDice = 50
upgradeExpo = 1.05
moreDice    = 50
moreExpo    = 1.2

# BIG DICE VARIABLES
hundoDiceAmount  = 0
thundoDiceAmount = 0
mundoDiceAmount  = 0
trundoDiceAmount = 0

# LUCK VARIABLES
rollLuck    = 1
upgradeLuck = 200
luckExpo    = 1.1

# UPGRADE TREE VARIABLES
storePriceOffset = 1.0
diceAmountOffset = 1.0
luckOffset       = 1.0
multiplierOffset = 1.0

# HAS UNLOCKED
hasHundo  = False
hasThundo = False
hasMundo  = False
hasTrundo = False
hasTree   = False

# MISC
gameVersion = "1.8.0"
cards = {
    "Club":    {"0": False, "1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "7": False, "8": False, "9": False,
                "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False, 
                "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False, 
                "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False},
    "Diamond": {"0": False, "1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "7": False, "8": False, "9": False,
                "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False, 
                "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False, 
                "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False},
    "Heart":   {"0": False, "1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "7": False, "8": False, "9": False,
                "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False, 
                "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False, 
                "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False},
    "Spade":   {"0": False, "1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "7": False, "8": False, "9": False,
                "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False, 
                "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False, 
                "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False}}

def saveGame():
    
    saveData = {
        "version_info": {
            "gameVersion": gameVersion
        },
        "dice": {
            "diceSides":        diceSides,
            "diceAmount":       diceAmount,
            "hundoDiceAmount":  hundoDiceAmount,
            "thundoDiceAmount": thundoDiceAmount,
            "mundoDiceAmount":  mundoDiceAmount,
            "trundoDiceAmount": trundoDiceAmount
        },
        "points": {
            "points":           points,
            "pointsMult":       pointsMult,
            "pointsMultExpo":   pointsMultExpo
        },
        "store": {
            "upgradeDice":      upgradeDice,
            "moreDice":         moreDice,
            "rollLuck":         rollLuck,
            "upgradeLuck":      upgradeLuck
        },
        "offset": {
            "storePriceOffset": storePriceOffset,
            "diceAmountOffset": diceAmountOffset,
            "luckOffset":       luckOffset,
            "multiplierOffset": multiplierOffset
        },
        "has": {
            "hasHundo": hasHundo,
            "hasThundo": hasThundo,
            "hasMundo": hasMundo,
            "hasTrundo": hasTrundo,
            "hasTree": hasTree
        },
        "playing_cards": {
            "cards": cards
        }
    }
    
    with open("save.json", "w") as f:
        json.dump(saveData, f, indent=4)

def bigNumber(number: float):
    
    numberSuffix = ["M",   "B",   "T",   "Qa",   "Qi",   "Sx",   "Sp",   "Oc",   "No",   "D",       # e006 - e033
                    "UD",  "DD",  "TD",  "QaD",  "QiD",  "SxD",  "SpD",  "OcD",  "NoD",  "Vg",      # e036 - e063
                    "UVg", "DVg", "TVg", "QaVg", "QiVg", "SxVg", "SpVg", "OcVg", "NoVg", "Tg",      # e066 - e093
                    "UTg", "DTg", "TTg", "QaTg", "QiTg", "SxTg", "SpTg", "OcTg", "NoTg", "Qd",      # e096 - e123
                    "UQd", "DQd", "TQd", "QaQd", "QiQd", "SxQd", "SpQd", "OcQd", "NoQd", "Qt"]      # e126 - e153
    
    if number < 1_000_000:
        return str(round(number, 2))

    for i, suffix in enumerate(numberSuffix, start=2):
        if number < 990 ** (i + 1):
            return str(round(number / (1000 ** i), 2)) + suffix

    return str(round(number / (1000 ** len(numberSuffix)), 2)) + numberSuffix[-1]

def rollDice(stdscr, amount: int, sides: float, offset: float, mult: float, luck: float, cards: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda s: s.center(WIDTH - 2)
    
    totalRolls = round(amount * offset)
    total = 0
    
    for _ in range(totalRolls):
        roll = random.randint(int(luck), int(sides)) if luck < sides else sides
        total += roll
    stdscr.addstr(27, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    stdscr.addstr(28, 0, "|" + cent(f"You rolled your Dice {bigNumber(round(amount * offset))} ({round(amount)}) times!") + "|", COLOR)

    totalPoints = total * mult * cards

    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    stdscr.addstr(30, 0, "|" + cent(f"You rolled this much: {bigNumber(total)} P") + "|", COLOR)
    stdscr.addstr(31, 0, "|" + cent(f"Your current Multiplier: {round(mult, 2)} MP") + "|", COLOR)
    stdscr.addstr(32, 0, "|" + cent(f"Your card Multiplier: {round(cards, 2)} CMP") + "|", COLOR)
    stdscr.addstr(33, 0, "|" + cent(f"You now have {bigNumber(totalPoints)} more points.") + "|", COLOR)
    stdscr.addstr(34, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    stdscr.refresh()
    stdscr.getch()
    
    return totalPoints

def chooseDiceAmount(stdscr, points: float, name: str, price: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda s: s.center(WIDTH - 2)
    
    maxAmount = points // price
    
    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    stdscr.addstr(30, 0, "|" + cent(f"You have {bigNumber(points)} points.") + "|", COLOR)
    stdscr.addstr(31, 0, "|" + cent(f"With your points, you can get {bigNumber(maxAmount)} {name} sided Dice") + "|", COLOR)
    stdscr.addstr(32, 0, "|" + cent("How many Dice do you want?") + "|", COLOR)
    stdscr.addstr(33, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    stdscr.addstr(34, 0, "| >" + (WIDTH - 4) * " " + "|", COLOR)
    stdscr.addstr(35, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    
    stdscr.refresh()
    
    curses.curs_set(1)
    win = curses.newwin(1, 100, 34, 4)
    box = Textbox(win)
    
    try:
        box.edit()
        choice = int(box.gather())
    except ValueError:
        stdscr.addstr(37, 0, f"Please choose a number between 1 and {bigNumber(maxAmount)}.", COLOR)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0
    
    if not (1 <= choice <= maxAmount):
        
        if choice <= 0: msg = "You must buy at least 1 Die!"
        else:           msg = "You don't have enough points!"
            
        stdscr.addstr(37, 0, msg, COLOR)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0
    
    stdscr.addstr(36, 0, "|" + cent(f"You now have {choice} more {name} sided Dice.") + "|", COLOR)
    stdscr.addstr(37, 0, "#" + (WIDTH - 2) * "-" + "#", COLOR)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.getch()
    return choice, choice * price

def progressBar(percent: float, size: int):
    
    full = int(percent * size)
    empty = size - full
    bar = "█" * full + "░" * empty
    return f"{bar}"

def main(stdscr):
    
    # BOOLEANS
    Menu = True
    Play = False
    Store = False
    Tree = False
    Info = False
    Cards = False

    # GLOBAL VARIABLES
    global diceSides, diceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo, rollLuck, upgradeLuck, luckExpo
    global hundoDiceAmount, thundoDiceAmount, mundoDiceAmount, trundoDiceAmount
    global storePriceOffset, diceAmountOffset, luckOffset, multiplierOffset
    global hasHundo, hasThundo, hasMundo, hasTrundo, hasTree
    global gameVersion, cards
    
    # HIDE CURSOR
    curses.curs_set(0)
    
    # COLORS
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN,   curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    YELLOW  = curses.color_pair(1)
    GREEN   = curses.color_pair(2)
    RED     = curses.color_pair(3)
    BLUE    = curses.color_pair(4)
    MAGENTA = curses.color_pair(5)
    
    # MISC
    hundoPairs = {
                (1, 97),  (97, 1),                                                          # total 97
                (1, 98),  (98, 1),  (2, 49), (49, 2), (7, 14), (14, 7),                     # total 98
                (1, 99),  (99, 1),  (3, 33), (33, 3), (9, 11), (11, 9),                     # total 99
                (1, 100), (10, 10), (2, 50), (50, 2), (4, 25), (25, 4), (5, 20), (20, 5),   # total 100
                (1, 101), (101, 1),                                                         # total 101
                (1, 102), (102, 1), (2, 51), (51, 2), (3, 34), (34, 3), (6, 17), (17, 6),   # total 102
                (1, 103), (103, 1)                                                          # total 103
            }
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda s: s.center(WIDTH - 2)
    centHalf = lambda s: s.center(int(WIDTH/2 - 2))
    cardPrice = 10_000_000
    
    while True:
        
        while Menu:     # GAME MENU
            
            stdscr.clear()
            stdscr.addstr(0, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
            stdscr.addstr(1, 0, "|" + cent("0 - New  Game") + "|", RED)
            stdscr.addstr(2, 0, "|" + cent("1 - Load Game") + "|", RED)
            stdscr.addstr(3, 0, "|" + cent("2 - Exit Game") + "|", RED)
            stdscr.addstr(4, 0, "|" + cent("3 - Game info") + "|", RED)
            stdscr.addstr(5, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":           # NEW GAME
                
                stdscr.addstr(6,  0, "|" + cent("Are you sure?") + "|", RED)
                stdscr.addstr(7,  0, "#" + (WIDTH - 2) * "-" + "#", RED)
                stdscr.addstr(8,  0, "|" + cent("0 - No ") + "|", RED)
                stdscr.addstr(9,  0, "|" + cent("1 - Yes") + "|", RED)
                stdscr.addstr(10, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
                
                choice = stdscr.getkey()
                
                if choice == "0":       # NO
                    continue
                    
                elif choice == "1":     # YES
                    stdscr.clear()
                    stdscr.refresh()
                    Menu = False
                    Play = True
                
                else:                   # INVALID
                    stdscr.addstr(11, 0, "|" + cent("Invalid choice!") + "|", RED)
                    stdscr.addstr(12, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
                    stdscr.refresh()
                    stdscr.getch()
                
            elif choice == "1":         # LOAD GAME
                
                try:
                    
                    with open("save.json", "r") as f:
                        data = json.load(f)
                    
                    # DICE
                    diceSides =        data["dice"]["diceSides"]
                    diceAmount =       data["dice"]["diceAmount"]
                    hundoDiceAmount =  data["dice"]["hundoDiceAmount"]
                    thundoDiceAmount = data["dice"]["thundoDiceAmount"]
                    mundoDiceAmount =  data["dice"]["mundoDiceAmount"]
                    trundoDiceAmount = data["dice"]["trundoDiceAmount"]
                    
                    # POINTS
                    points =         data["points"]["points"]
                    pointsMult =     data["points"]["pointsMult"]
                    pointsMultExpo = data["points"]["pointsMultExpo"]
                    
                    # STORE
                    upgradeDice = data["store"]["upgradeDice"]
                    moreDice =    data["store"]["moreDice"]
                    rollLuck =    data["store"]["rollLuck"]
                    upgradeLuck = data["store"]["upgradeLuck"]
                    
                    # OFFSET
                    storePriceOffset = data["offset"]["storePriceOffset"]
                    diceAmountOffset = data["offset"]["diceAmountOffset"]
                    luckOffset =       data["offset"]["luckOffset"]
                    multiplierOffset = data["offset"]["multiplierOffset"]
                    
                    # HAS UNLOCKED
                    hasHundo  = data["has"]["hasHundo"]
                    hasThundo = data["has"]["hasThundo"]
                    hasMundo  = data["has"]["hasMundo"]
                    hasTrundo = data["has"]["hasTrundo"]
                    hasTree   = data["has"]["hasTree"]
                    
                    # CARDS
                    cards     = data["playing_cards"]["cards"]
                    
                    stdscr.addstr(6, 0, "|" + cent("Welcome back!") + "|", RED)
                    stdscr.addstr(7, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
                    stdscr.refresh()
                    stdscr.getch()
                        
                    Menu = False
                    Play = True
                        
                except OSError:
                    stdscr.addstr(6, 0, "|" + cent("Corrupt or missing file!") + "|", RED)
                    stdscr.addstr(7, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "2":         # EXIT GAME
                sys.exit()

            elif choice == "3":         # GAME INFO
                Info = True
                Menu = False

        while Play:     # GAME PLAY
            
            saveGame()
            stdscr.clear()
            
            count = sum(v for k in cards.values() for v in k.values())
            cardPoints = 1 + count/100
            
            # DICE DISPLAY
            stdscr.addstr(0, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
            stdscr.addstr(1, 0, "|" + cent(f"You have {round(diceAmount * diceAmountOffset)} ({round(diceAmount)}) {diceSides} sided Dice") + "|", BLUE)
            if hasMundo: stdscr.addstr(2, 0, "|" + cent(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} ({bigNumber(round(hundoDiceAmount))}) Hundred sided Dice") + "|", BLUE)
            else: stdscr.addstr(2, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if thundoDiceAmount > 0 or hasThundo: stdscr.addstr(3, 0, "|" + cent(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} ({bigNumber(round(thundoDiceAmount))}) Thousand sided Dice") + "|", BLUE)
            else: stdscr.addstr(3, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if mundoDiceAmount > 0 or hasMundo: stdscr.addstr(4, 0, "|" + cent(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} ({bigNumber(round(mundoDiceAmount))}) Million sided Dice") + "|", BLUE)
            else: stdscr.addstr(4, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if trundoDiceAmount > 0 or hasTrundo: stdscr.addstr(5, 0, "|" + cent(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} ({bigNumber(round(trundoDiceAmount))}) Trillion sided Dice") + "|", BLUE)
            else: stdscr.addstr(5, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            
            # POINTS AND CARDS DISPLAY
            stdscr.addstr(6, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
            stdscr.addstr(7, 0, "|" + cent(f"You have {bigNumber(points)} points and you have {count}/{len(cards["Club"]) * len(cards)} cards.") + "|", BLUE)
            
            # LUCK AND MULTIPLIER DISPLAY
            stdscr.addstr(8, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
            stdscr.addstr(9, 0, "|" + cent(f"Your lowest Dice roll: {round(rollLuck)}") + "|", BLUE)
            stdscr.addstr(10, 0, "|" + centHalf(f"Your current Multiplier: {round(pointsMult, 2)} MP"), BLUE)
            stdscr.addstr(10, int(WIDTH/2 + 1), centHalf(f"Progress to the next Multiplier upgrade: {"0" if 1000 ** pointsMult - points < 0 else bigNumber(1000 ** pointsMult - points)} points") + "|", BLUE)
            stdscr.addstr(11, 0, "|" + cent(progressBar(points / (1000 ** pointsMult), WIDTH - 2)) + "|", BLUE)
            if points >= 1000 ** pointsMult: stdscr.addstr(12, 0, "|" + cent("You have enough points to upgrade your Multiplier!") + "|", BLUE)
            else: stdscr.addstr(12, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if pointsMult >= 10: stdscr.addstr(13, 0, "|" + cent("You have enough Multiplier to upgrade it's scaling!") + "|", BLUE)
            else: stdscr.addstr(13, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            stdscr.addstr(14, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)

            # OPTIONS DISPLAY
            stdscr.addstr(15, 0, "|" + cent("1 - Dice Store") + "|", BLUE)
            stdscr.addstr(16, 0, "|" + cent("2 - Upgrade Multiplier") + "|", BLUE)
            if pointsMult >= 10: stdscr.addstr(17, 0, "|" + cent("3 - Upgrade Multiplier scaling") + "|", BLUE)
            else: stdscr.addstr(17, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            stdscr.addstr(18, 0, "|" + cent("4 - Roll Dice") + "|", BLUE)
            if hundoDiceAmount > 0: stdscr.addstr(19, 0, "|" + cent("5 - Roll the Hundred sided Dice") + "|", BLUE)
            else: stdscr.addstr(19, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if thundoDiceAmount > 0: stdscr.addstr(20, 0, "|" + cent("6 - Roll the Thousand sided Dice") + "|", BLUE)
            else: stdscr.addstr(20, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if mundoDiceAmount > 0: stdscr.addstr(21, 0, "|" + cent("7 - Roll the Million sided Dice") + "|", BLUE)
            else: stdscr.addstr(21, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if trundoDiceAmount > 0: stdscr.addstr(22, 0, "|" + cent("8 - Roll the Trillion sided Dice") + "|", BLUE)
            else: stdscr.addstr(22, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            if points >= 1e15 or hasTree: stdscr.addstr(23, 0, "|" + cent("9 - Go to the Upgrade Tree") + "|", BLUE)
            else: stdscr.addstr(23, 0, "|" + (WIDTH - 2) * " " + "|", BLUE)
            stdscr.addstr(24, 0, "|" + cent("0 - Save and Exit") + "|", BLUE)
            stdscr.addstr(25, 0, "|" + cent("M - Back to Menu") + "|", BLUE)
            stdscr.addstr(26, 0, "|" + cent("K - Look at your Cards") + "|", BLUE)
            stdscr.addstr(27, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # SAVE AND EXIT
                saveGame()
                sys.exit()
            
            elif choice == "1":     # STORE
                Store = True
                Play = False
                
            elif choice == "2":     # UPGRADE MULTIPLIER
                
                stdscr.addstr(28, 0, "|" + cent("WARNING!") + "|", BLUE)
                stdscr.addstr(29, 0, "|" + cent("UPGRADING YOUR MULTIPLIER RESETS YOUR") + "|", BLUE)
                stdscr.addstr(30, 0, "|" + cent("DICE AND POINTS BACK TO 1 AND 0") + "|", BLUE)
                stdscr.addstr(31, 0, "|" + cent("STORE PRICES ARE ALSO RESET") + "|", BLUE)
                stdscr.addstr(32, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                stdscr.addstr(33, 0, "|" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "|", BLUE)
                stdscr.addstr(34, 0, "|" + cent(f"You need {bigNumber(1000 ** pointsMult)} points to upgrade your Multiplier.") + "|", BLUE)
                stdscr.addstr(35, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                stdscr.addstr(36, 0, "|" + cent("1 - Upgrade Multiplier") + "|", BLUE)
                stdscr.addstr(37, 0, "|" + cent("0 - I don't want to") + "|", BLUE)
                stdscr.addstr(38, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                
                choice = stdscr.getkey()
                
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
                        
                        for i in cards.values():
                            for j in i:
                                i[j] = False
                        
                        stdscr.addstr(39, 0, "|" + cent("Wise choice.") + "|", BLUE)
                        stdscr.addstr(40, 0, "|" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "|", BLUE)
                        stdscr.addstr(41, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(40, 0, "You don't have enough points!", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
                
                elif choice == "0":         # NO
                    continue
                
                else:                       # INVALID
                    stdscr.addstr(40, 0, "Invalid choice!", BLUE)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "3":     # UPGRADE MULTIPLIER SCALING
                
                if pointsMult >= 10:
                
                    stdscr.addstr(28, 0, "|" + cent("WARNING!") + "|", BLUE)
                    stdscr.addstr(29, 0, "|" + cent("UPGRADING YOUR MULTIPLIER'S SCALING RESETS") + "|", BLUE)
                    stdscr.addstr(30, 0, "|" + cent("EVERYTHING BUT YOUR MULTIPLIER BACK TO 1") + "|", BLUE)
                    stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                    stdscr.addstr(32, 0, "|" + cent("0 - I don't want to") + "|", BLUE)
                    stdscr.addstr(33, 0, "|" + cent("1 - Upgrade Multiplier scaling") + "|", BLUE)
                    stdscr.addstr(34, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                    
                    choice = stdscr.getkey()
                    
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
                        trundoDiceAmount = 0
                            
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        for i in cards.values():
                            for j in i:
                                i[j] = False
                        
                        stdscr.addstr(35, 0, "|" + cent("Great choice!") + "|", BLUE)
                        stdscr.addstr(36, 0, "|" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "|", BLUE)
                        stdscr.addstr(37, 0, "#" + (WIDTH - 2) * "-" + "#", BLUE)
                        stdscr.refresh()
                        stdscr.getch()

                    elif choice == "0":     # NO
                        continue
                
                    else:                   # INVALID
                        stdscr.addstr(36, 0, "Invalid choice!", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
            
            elif choice == "4":     # ROLL DICE
                points += rollDice(stdscr, diceAmount, diceSides, diceAmountOffset, pointsMult, rollLuck, cardPoints, BLUE)
            
            elif choice == "5":     # ROLL HUNDO
                if hundoDiceAmount > 0:
                    points += rollDice(stdscr, hundoDiceAmount, 100, diceAmountOffset, pointsMult, rollLuck, cardPoints, BLUE)
                    
            elif choice == "6":     # ROLL THUNDO
                if thundoDiceAmount > 0:
                    points += rollDice(stdscr, thundoDiceAmount, 1000, diceAmountOffset, pointsMult, rollLuck, cardPoints, BLUE)
            
            elif choice == "7":     # ROLL MUNDO
                if mundoDiceAmount > 0:
                    points += rollDice(stdscr, mundoDiceAmount, 1_000_000, diceAmountOffset, pointsMult, rollLuck, cardPoints, BLUE)
                    
            elif choice == "8":     # ROLL TRUNDO
                if trundoDiceAmount > 0:
                    points += rollDice(stdscr, trundoDiceAmount, 1e12, diceAmountOffset, pointsMult, rollLuck, cardPoints, BLUE)
            
            elif choice == "9":     # UPGRADE TREE
                if points >= 1e15 or hasTree:
                    Tree = True
                    Play = False
                    hasTree = True
            
            elif choice == "m":     # MENU
                Play = False
                Menu = True
            
            elif choice == "k":     # CARDS
                Play = False
                Cards = True
            
            else:                   # INVALID
                stdscr.addstr(29, 0, "Invalid choice!", BLUE)
                stdscr.refresh()
                stdscr.getch()

        while Store:    # GAME STORE
            
            saveGame()
            stdscr.clear()
            
            # DICE DISPLAY
            stdscr.addstr(0, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
            stdscr.addstr(1, 0, "|" + cent(f"You have {round(diceAmount * diceAmountOffset)} ({round(diceAmount)}) {diceSides} sided Dice") + "|", YELLOW)
            if hasMundo: stdscr.addstr(2, 0, "|" + cent(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} ({bigNumber(round(hundoDiceAmount))}) Hundred sided Dice") + "|", YELLOW)
            else: stdscr.addstr(2, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if thundoDiceAmount > 0 or hasThundo: stdscr.addstr(3, 0, "|" + cent(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} ({bigNumber(round(thundoDiceAmount))}) Thousand sided Dice") + "|", YELLOW)
            else: stdscr.addstr(3, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if mundoDiceAmount > 0 or hasMundo: stdscr.addstr(4, 0, "|" + cent(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} ({bigNumber(round(mundoDiceAmount))}) Million sided Dice") + "|", YELLOW)
            else: stdscr.addstr(4, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if trundoDiceAmount > 0 or hasTrundo: stdscr.addstr(5, 0, "|" + cent(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} ({bigNumber(round(trundoDiceAmount))}) Trillion sided Dice") + "|", YELLOW)
            else: stdscr.addstr(5, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            
            # POINTS AND LUCK DISPLAY
            stdscr.addstr(6, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
            stdscr.addstr(7, 0, "|" + cent(f"You have {bigNumber(points)} points.") + "|", YELLOW)
            stdscr.addstr(8, 0, "|" + cent(f"Your lowest Dice roll: {round(rollLuck)}") + "|", YELLOW)
            stdscr.addstr(9, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            
            # OPTIONS DISPLAY
            stdscr.addstr(10, 0, "|" + cent(f"1 - Upgrade Dice: {bigNumber((upgradeDice * diceAmount) / storePriceOffset)} points") + "|", YELLOW)
            stdscr.addstr(11, 0, "|" + cent(f"2 - Buy more Dice: {bigNumber((moreDice * 1.5) / storePriceOffset)} points") + "|", YELLOW)
            stdscr.addstr(12, 0, "|" + cent(f"3 - Buy a Lucky Amulet: {bigNumber(upgradeLuck / storePriceOffset)} points") + "|", YELLOW)
            if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000): stdscr.addstr(13, 0, "|" + cent("4 - Get a Hundred sided Die") + "|", YELLOW)
            else: stdscr.addstr(13, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if hundoDiceAmount >= 10 or points >= 120_000: stdscr.addstr(14, 0, "|" + cent("5 - Get a Thousand sided Die") + "|", YELLOW)
            else: stdscr.addstr(14, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000: stdscr.addstr(15, 0, "|" + cent("6 - Get a Million sided Die") + "|", YELLOW)
            else: stdscr.addstr(15, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            if mundoDiceAmount >= 1_000_000 or points >= 120e12: stdscr.addstr(16, 0, "|" + cent("7 - Get a Trillion sided Die") + "|", YELLOW)
            else: stdscr.addstr(16, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
            stdscr.addstr(17, 0, "|" + cent("0 - Exit Store") + "|", YELLOW)
            stdscr.addstr(18, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":           # EXIT STORE
                Play = True
                Store = False
            
            elif choice == "1":         # UPGRADE DICE
                
                if points >= (upgradeDice * diceAmount) / storePriceOffset:
                    points -= (upgradeDice * diceAmount) / storePriceOffset
                    upgradeDice = upgradeDice ** upgradeExpo
                    diceSides += 1
                    stdscr.addstr(19, 0, "|" + cent(f"You now have {round(diceAmount * diceAmountOffset)} dice with {diceSides} sides each.") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(19, 0, "|" + cent("You don't have enough points!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "2":         # BUY MORE DICE
                
                if points >= (moreDice * 1.5) / storePriceOffset:
                    points -= (moreDice * 1.5) / storePriceOffset
                    moreDice = moreDice ** moreExpo
                    diceAmount += 1
                    stdscr.addstr(19, 0, "|" + cent(f"You now have {round(diceAmount * diceAmountOffset)} dice with {diceSides} sides each.") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(19, 0, "|" + cent("You don't have enough points!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "3":         # LUCKY AMULET
                
                if points >= upgradeLuck / storePriceOffset:
                    points -= upgradeLuck / storePriceOffset
                    upgradeLuck = upgradeLuck ** luckExpo
                    rollLuck += 1 * luckOffset
                    stdscr.addstr(19, 0, "|" + cent("You feel luckier!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(19, 0, "|" + cent("You don't have enough points!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "4":         # GET HUNDO DICE
                
                if ((diceAmount, diceSides) in hundoPairs) or (points >= 12_000):
                
                    stdscr.addstr(18, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(19, 0, "|" + cent("WARNING!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "|" + cent("YOU'RE ABOUT TO TRADE OFF ALL OF YOUR DICE FOR A Hundred SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(21, 0, "|" + cent("YOU'LL HAVE YOUR NEW Hundred SIDED DIE AND THE ORIGINAL 4 SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(22, 0, "|" + cent("YOU WON'T LOSE YOUR DICE IF YOU PAY FOR THE Hundred SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(23, 0, "|" + cent("(the Hundred sided Die doesn't persist between multiplier upgrades)") + "|", YELLOW)
                    stdscr.addstr(24, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(25, 0, "|" + cent("1 - Trade off my Dice") + "|", YELLOW)
                    stdscr.addstr(26, 0, "|" + cent("2 - Pay for the Die") + "|", YELLOW)
                    stdscr.addstr(27, 0, "|" + cent("3 - Choose how many Dice") + "|", YELLOW)
                    stdscr.addstr(28, 0, "|" + cent("0 - I don't want to") + "|", YELLOW)
                    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        if (diceAmount, diceSides) in hundoPairs:
                            
                            hundoDiceAmount += 1
                            diceSides = 4
                            diceAmount = 1
                            
                            upgradeDice = 50
                            upgradeExpo = 1.05
                            moreDice = 50
                            moreExpo = 1.2
                            
                            hasHundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Welcome your new Hundred sided Die!") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough Dice!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 12_000:
                            
                            hundoDiceAmount += 1
                            points -= 12_000
                            
                            hasHundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Welcome your new Hundred sided Die!") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough points!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "3":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Hundred", 12_000, YELLOW)
                        hundoDiceAmount += dice
                        points -= spent
                        hasHundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        stdscr.addstr(31, 0, "Invalid choice!", YELLOW)
                        stdscr.refresh()
                        stdscr.getch()

            elif choice == "5":         # GET THUNDO DICE
                
                if hundoDiceAmount >= 10 or points >= 120_000:
                
                    stdscr.addstr(18, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(19, 0, "|" + cent("WARNING!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "|" + cent("YOU'RE ABOUT TO TRADE OFF 10 OF YOUR Hundred SIDED DICE") + "|", YELLOW)
                    stdscr.addstr(21, 0, "|" + cent("OR PAY 120,000 POINTS FOR AN INCREDIBLE Thousand SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(22, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
                    stdscr.addstr(23, 0, "|" + cent("(this still doesn't persist between multiplier upgrades)") + "|", YELLOW)
                    stdscr.addstr(24, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(25, 0, "|" + cent("1 - Trade off my Dice") + "|", YELLOW)
                    stdscr.addstr(26, 0, "|" + cent("2 - Pay for the Die") + "|", YELLOW)
                    stdscr.addstr(27, 0, "|" + cent("3 - Choose how many Dice") + "|", YELLOW)
                    stdscr.addstr(28, 0, "|" + cent("0 - I don't want to") + "|", YELLOW)
                    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        if hundoDiceAmount >= 10:
                            
                            thundoDiceAmount += 1
                            hundoDiceAmount -= 10
                            
                            hasThundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Stand ready for my arrival, worm.") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough Dice!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 120_000:
                            
                            thundoDiceAmount += 1
                            points -= 120_000
                            
                            hasThundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Stand ready for my arrival, worm.") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough points!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "3":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Thousand", 120_000, YELLOW)
                        thundoDiceAmount += dice
                        points -= spent
                        hasThundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        stdscr.addstr(31, 0, "Invalid choice!", YELLOW)
                        stdscr.refresh()
                        stdscr.getch()

            elif choice == "6":         # GET MUNDO DICE
                
                if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000:
                
                    stdscr.addstr(18, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(19, 0, "|" + cent("WARNING!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "|" + cent("YOU'RE ABOUT TO TRADE OFF YOUR DICE") + "|", YELLOW)
                    stdscr.addstr(21, 0, "|" + cent("OR PAY 120 Million POINTS") + "|", YELLOW)
                    stdscr.addstr(22, 0, "|" + cent("FOR A Million SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(23, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(24, 0, "|" + cent("1 - Trade off my Hundred Sided Dice") + "|", YELLOW)
                    stdscr.addstr(25, 0, "|" + cent("2 - Trade off my Thousand Sided Dice") + "|", YELLOW)
                    stdscr.addstr(26, 0, "|" + cent("3 - Pay for the Die") + "|", YELLOW)
                    stdscr.addstr(27, 0, "|" + cent("4 - Choose how many Dice") + "|", YELLOW)
                    stdscr.addstr(28, 0, "|" + cent("0 - I don't want to") + "|", YELLOW)
                    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # HUNDO TRADE
                        
                        if hundoDiceAmount >= 10_000:
                            
                            mundoDiceAmount += 1
                            hundoDiceAmount -= 10_000
                            
                            hasMundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Are you Mr. Beast?") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough Dice!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "2":         # THUNDO TRADE
                        
                        if thundoDiceAmount >= 1000:
                            
                            mundoDiceAmount += 1
                            thundoDiceAmount -= 1000
                            
                            hasMundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Are you Mr. Beast?") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough Dice!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "3":         # ENOUGH POINTS
                        
                        if points >= 120_000_000:
                            
                            mundoDiceAmount += 1
                            points -= 120_000_000
                            
                            hasMundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("Are you Mr. Beast?") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough points!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "4":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Million", 120_000_000, YELLOW)
                        mundoDiceAmount += dice
                        points -= spent
                        hasMundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        stdscr.addstr(31, 0, "Invalid choice!", YELLOW)
                        stdscr.refresh()
                        stdscr.getch()

            elif choice == "7":         # GET TRUNDO DICE
                
                if mundoDiceAmount >= 1_000_000 or points >= 120e12:
                
                    stdscr.addstr(18, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(19, 0, "|" + cent("WARNING!") + "|", YELLOW)
                    stdscr.addstr(20, 0, "|" + cent("YOU'RE ABOUT TO TRADE OFF YOUR DICE") + "|", YELLOW)
                    stdscr.addstr(21, 0, "|" + cent("OR PAY 120 Trillion POINTS") + "|", YELLOW)
                    stdscr.addstr(22, 0, "|" + cent("FOR A Trillion SIDED DIE") + "|", YELLOW)
                    stdscr.addstr(23, 0, "|" + (WIDTH - 2) * " " + "|", YELLOW)
                    stdscr.addstr(24, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    stdscr.addstr(25, 0, "|" + cent("1 - Trade off my Dice") + "|", YELLOW)
                    stdscr.addstr(26, 0, "|" + cent("2 - Pay for the Die") + "|", YELLOW)
                    stdscr.addstr(27, 0, "|" + cent("3 - Choose how many Dice") + "|", YELLOW)
                    stdscr.addstr(28, 0, "|" + cent("0 - I don't want to") + "|", YELLOW)
                    stdscr.addstr(29, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                    
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        if mundoDiceAmount >= 1_000_000:
                            
                            trundoDiceAmount += 1
                            mundoDiceAmount -= 1_000_000
                            
                            hasTrundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("This is quite the large Die.") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough Dice!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        if points >= 120e12:
                            
                            trundoDiceAmount += 1
                            points -= 120e12
                            
                            hasTrundo = True
                            
                            stdscr.addstr(30, 0, "|" + cent("This is quite the large Die.") + "|", YELLOW)
                            stdscr.addstr(31, 0, "#" + (WIDTH - 2) * "-" + "#", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                            
                        else:
                            stdscr.addstr(31, 0, "You don't have enough points!", YELLOW)
                            stdscr.refresh()
                            stdscr.getch()
                    
                    elif choice == "3":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Trillion", 120e12, YELLOW)
                        trundoDiceAmount += dice
                        points -= spent
                        hasTrundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
                    else:                       # INVALID
                        stdscr.addstr(31, 0, "Invalid choice!", YELLOW)
                        stdscr.refresh()
                        stdscr.getch()

            else:                       # INVALID
                stdscr.addstr(20, 0, "Invalid choice!", YELLOW)
                stdscr.refresh()
                stdscr.getch()

        while Tree:     # GAME TREE
            
            saveGame()
            stdscr.clear()
            
            stdscr.addstr(0,  0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
            stdscr.addstr(1,  0, "|" + cent("Welcome to the Upgrade Tree!") + "|", GREEN)
            stdscr.addstr(2,  0, "|" + cent("If you're here, it means that you've accumulated over 1 quadrillion points") + "|", GREEN)
            stdscr.addstr(3,  0, "|" + cent("and you're wondering what this magical place could possibly be?") + "|", GREEN)
            stdscr.addstr(4,  0, "|" + cent("(also these are PERMANENT, meaning upgrading Multiplier won't reset these)") + "|", GREEN)
            stdscr.addstr(5,  0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
            stdscr.addstr(6,  0, "|" + cent("Well wait no further!") + "|", GREEN)
            stdscr.addstr(7,  0, "|" + (WIDTH - 2) * " " + "|", GREEN)
            stdscr.addstr(8,  0, "|" + cent("Here you can upgrade anything you could ever think of!") + "|", GREEN)
            stdscr.addstr(9,  0, "|" + cent("You want the Store prices to be cheaper? You got it!") + "|", GREEN)
            stdscr.addstr(10, 0, "|" + cent("You want more Dice per Dice? You can have that!") + "|", GREEN)
            stdscr.addstr(11, 0, "|" + cent("You can even have more Multiplier and better Scaling!") + "|", GREEN)
            stdscr.addstr(12, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
            stdscr.addstr(13, 0, "|" + cent("1 - View possible Upgrades") + "|", GREEN)
            stdscr.addstr(14, 0, "|" + cent("0 - Leave the Upgrade Tree") + "|", GREEN)
            stdscr.addstr(15, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # LEAVE
                Tree = False
                Play = True
            
            elif choice == "1":     # POSSIBLE UPGRADES
                
                stdscr.addstr(16, 0, "|" + cent(f"You have {bigNumber(points)} points.") + "|", GREEN)
                stdscr.addstr(17, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                stdscr.addstr(18, 0, "|" + cent(f"1 - Better store prices: {bigNumber(1e15 ** storePriceOffset)} points") + "|", GREEN)
                stdscr.addstr(19, 0, "|" + cent(f"2 - More dice per dice: {bigNumber(1e15 ** diceAmountOffset)} points") + "|", GREEN)
                stdscr.addstr(20, 0, "|" + cent(f"3 - Get even luckier: {bigNumber(1e18 ** luckOffset)} points") + "|", GREEN)
                stdscr.addstr(21, 0, "|" + cent(f"4 - More Multiplier: {bigNumber(1e21 ** multiplierOffset)} points") + "|", GREEN)
                stdscr.addstr(22, 0, "|" + cent("0 - Exit to the Upgrade Tree") + "|", GREEN)
                stdscr.addstr(23, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                
                choice = stdscr.getkey()
                
                if choice == "0":       # EXIT
                    continue
                
                elif choice == "1":     # BETTER PRICES
                    
                    if points >= 1e15 ** storePriceOffset:
                        
                        points -= 1e15 ** storePriceOffset
                        storePriceOffset += 0.2
                        
                        stdscr.addstr(24, 0, "|" + cent("Store Prices are now cheaper!") + "|", GREEN)
                        stdscr.addstr(25, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(25, 0, "You don't have enough points!", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                
                elif choice == "2":     # MORE DICE
                    
                    if points >= 1e15 ** diceAmountOffset:
                        
                        points -= 1e15 ** diceAmountOffset
                        diceAmountOffset += 0.2
                        
                        stdscr.addstr(24, 0, "|" + cent("You magically have more dice!") + "|", GREEN)
                        stdscr.addstr(25, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(25, 0, "You don't have enough points!", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                
                elif choice == "3":     # MORE LUCK
                    
                    if points >= 1e18 ** luckOffset:
                        
                        points -= 1e18 ** luckOffset
                        luckOffset += 0.2
                        
                        stdscr.addstr(24, 0, "|" + cent("You feel even luckier!") + "|", GREEN)
                        stdscr.addstr(25, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(25, 0, "You don't have enough points!", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                
                elif choice == "4":     # MORE MULTIPLIER
                    
                    if points >= 1e21 ** multiplierOffset:
                        
                        points -= 1e21 ** multiplierOffset
                        multiplierOffset += 0.2
                        
                        stdscr.addstr(24, 0, "|" + cent("The Multiplier already feels stronger!") + "|", GREEN)
                        stdscr.addstr(25, 0, "#" + (WIDTH - 2) * "-" + "#", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(25, 0, "You don't have enough points!", GREEN)
                        stdscr.refresh()
                        stdscr.getch()
                
                else:                   # INVALID
                    stdscr.addstr(25, 0, "Invalid choice!", GREEN)
                    stdscr.refresh()
                    stdscr.getch()
            
            else:                   # INVALID
                stdscr.addstr(17, 0, "Invalid choice!", GREEN)
                stdscr.refresh()
                stdscr.getch()

        while Info:     # GAME INFO
            
            saveGame()
            stdscr.clear()
            
            stdscr.addstr(0, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
            stdscr.addstr(1, 0, "|" + cent(f"Game version: {gameVersion}") + "|", RED)
            stdscr.addstr(2, 0, "|" + (WIDTH - 2) * " " + "|", RED)
            stdscr.addstr(3, 0, "|" + cent("Any - Back to Menu") + "|", RED)
            stdscr.addstr(4, 0, "#" + (WIDTH - 2) * "-" + "#", RED)
            
            stdscr.refresh()
            stdscr.getkey()
            Info = False
            Menu = True

        while Cards:    # GAME CARDS
            
            saveGame()
            stdscr.clear()
            
            countCards = sum(v for suits in cards.values() for v in suits.values())
            falseCards = [(ok, ik) for ok, suits in cards.items() for ik, v in suits.items() if not v]
            priceCard = cardPrice ** (1 + countCards/50)
            
            stdscr.addstr(0, 0, "#" + (WIDTH - 2) * "-" + "#", MAGENTA)
            x, y = 1, 0
            for suits in cards:
                for card in cards[suits]:
                    if   suits == "Club":    stdscr.addstr(x, y, f"| {card} of {suits}s |{25 * "█" if cards[suits][card] else 25 * "░"}|", MAGENTA)
                    elif suits == "Diamond": stdscr.addstr(x, y, f"| {card} of {suits}s |{22 * "█" if cards[suits][card] else 22 * "░"}|", MAGENTA)
                    elif suits == "Heart":   stdscr.addstr(x, y, f"| {card} of {suits}s |{24 * "█" if cards[suits][card] else 24 * "░"}|", MAGENTA)
                    elif suits == "Spade":   stdscr.addstr(x, y, f"| {card} of {suits}s |{23 * "█" if cards[suits][card] else 23 * "░"}|", MAGENTA)
                    x += 1
                x = 1
                y += int(WIDTH / 4)
            
            for i in range(37):
                stdscr.addstr(i + 1, WIDTH - 1, "|", MAGENTA)
            stdscr.addstr(37, 0, "#" + (WIDTH - 2) * "-" + "#", MAGENTA)
            stdscr.addstr(38, 0, "|" + cent(f"You have unlocked {countCards}/{len(cards[suits]) * len(cards)} Cards and you have {bigNumber(points)} points.") + "|", MAGENTA)
            stdscr.addstr(39, 0, "#" + (WIDTH - 2) * "-" + "#", MAGENTA)
            stdscr.addstr(40, 0, "|" + cent("0 - Stop looking at your Cards") + "|", MAGENTA)
            stdscr.addstr(41, 0, "|" + cent(f"1 - Buy a random Card: {bigNumber(priceCard)}") + "|", MAGENTA)
            stdscr.addstr(42, 0, "#" + (WIDTH - 2) * "-" + "#", MAGENTA)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # LEAVE
                Cards = False
                Play = True
                
            elif choice == "1":     # RANDOM CARD
                
                if points >= priceCard:
                    
                    points -= priceCard
                    ok, ik = random.choice(falseCards)
                    cards[ok][ik] = True
                    
                    stdscr.addstr(43, 0, "|" + cent(f"You pulled a {ik} of {ok}s for {bigNumber(priceCard)} points!") + "|", MAGENTA)
                    stdscr.addstr(44, 0, "#" + (WIDTH - 2) * "-" + "#", MAGENTA)
                    stdscr.refresh()
                    stdscr.getkey()
                
                else:
                    stdscr.addstr(44, 0, "You don't have enough points!", MAGENTA)
                    stdscr.refresh()
                    stdscr.getkey()
            
            else:                   # INVALID
                stdscr.addstr(44, 0, "Invalid choice!", MAGENTA)
                stdscr.refresh()
                stdscr.getkey()


wrapper(main)