# IMPORTS
import json, sys
import random, curses
from curses import wrapper
from curses.textpad import Textbox
from os import popen, rename
# from pprint import pprint


# POINT VARIABLES
points         = 0
pointsMult     = 1.0
pointsMultExpo = 1.15

# SHOP VARIABLES
upgradeDice = 50
upgradeExpo = 1.05
moreDice    = 50
moreExpo    = 1.2

# REGULAR DICE VARIABLES
diceSides        = 4
diceAmount       = 1
hundoDiceAmount  = 0
thundoDiceAmount = 0
mundoDiceAmount  = 0
trundoDiceAmount = 0
qindoDiceAmount  = 0

# GOLD DICE VARIABLES
goldDiceSides        = 0
goldDiceAmount       = 0
goldHundoDiceAmount  = 0
goldThundoDiceAmount = 0
goldMundoDiceAmount  = 0
goldTrundoDiceAmount = 0
goldQindoDiceAmount  = 0

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
hasQindo  = False
hasTree   = False

# MISC
gameVersion = "1.8.5"
saveName    = "defaultsave"

# CARDS
cardFour    = {
    "0": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "1": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "2": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "3": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "4": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "5": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "6": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "7": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "8": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "9": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "0": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "A": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "B": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "C": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "D": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "E": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "F": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "G": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "H": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "I": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "J": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "K": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "L": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "M": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "N": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "O": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "P": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "Q": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "R": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "S": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "T": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "U": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "V": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "W": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "X": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "Y": {"Club": False, "Diamond": False, "Heart": False, "Spade": False},
    "Z": {"Club": False, "Diamond": False, "Heart": False, "Spade": False}}
fourOfAKind = 0
cardPrice   = 10_000_000

def saveGame(name: str):
    
    saveData = {
        "game_info": {
            "gameVersion": gameVersion,
            "saveName":    saveName
        },
        "dice": {
            "regular": {
                "diceSides":            diceSides,
                "diceAmount":           diceAmount,
                "hundoDiceAmount":      hundoDiceAmount,
                "thundoDiceAmount":     thundoDiceAmount,
                "mundoDiceAmount":      mundoDiceAmount,
                "trundoDiceAmount":     trundoDiceAmount,
                "qindoDiceAmount":      qindoDiceAmount
            },
            "gold": {
                "goldDiceSides":        goldDiceSides,
                "goldDiceAmount":       goldDiceAmount,
                "goldHundoDiceAmount":  goldHundoDiceAmount,
                "goldThundoDiceAmount": goldThundoDiceAmount,
                "goldMundoDiceAmount":  goldMundoDiceAmount,
                "goldTrundoDiceAmount": goldTrundoDiceAmount,
                "goldQindoDiceAmount":  goldQindoDiceAmount
            }
        },
        "points": {
            "points":         points,
            "pointsMult":     pointsMult,
            "pointsMultExpo": pointsMultExpo
        },
        "store": {
            "upgradeDice": upgradeDice,
            "moreDice":    moreDice,
            "rollLuck":    rollLuck,
            "upgradeLuck": upgradeLuck
        },
        "offset": {
            "storePriceOffset": storePriceOffset,
            "diceAmountOffset": diceAmountOffset,
            "luckOffset":       luckOffset,
            "multiplierOffset": multiplierOffset
        },
        "has": {
            "hasHundo":  hasHundo,
            "hasThundo": hasThundo,
            "hasMundo":  hasMundo,
            "hasTrundo": hasTrundo,
            "hasQindo":  hasQindo,
            "hasTree":   hasTree
        },
        "playing_cards": {
            "cardFour":    cardFour,
            "fourOfAKind": fourOfAKind,
            "cardPrice":   cardPrice
        }
    }
    
    with open(f"{name}.json", "w") as f:
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

def progressBar(percent: float, size: int):
    
    percent = 1 if percent >= 1 else percent
    full = int(percent * size)
    empty = size - full
    bar = "█" * full + "░" * empty
    return f"{bar}"

def rollDice(stdscr, regular: int, gold: int, sides: float, scale: float, offset: float, mult: float, luck: float, cards: float, four: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)

    total = 0
    totalRolls = regular * offset if regular < 1_000_000 else regular * offset / 1_000_000
    for _ in range(int(totalRolls)):
        roll = random.randint(int(luck), int(sides)) if luck < sides else sides
        total += roll
    totalPoints = total * mult * cards * four * scale if regular < 1_000_000 else total * mult * cards * four * scale * 1_000_000
    
    if gold > 0:
        goldTotal = 0
        totalRolls = gold * offset if gold < 1_000_000 else gold * offset / 1_000_000
        for _ in range(int(totalRolls)):
            roll = random.randint(int(luck), int(sides)) if luck < sides else sides
            goldTotal += roll
        totalPoints += goldTotal * mult * cards * four * scale * 2 if gold < 1_000_000 else goldTotal * mult * cards * four * scale * 2 * 1_000_000
        
    stdscr.addstr(30, 0, "▌" + cent(f"You rolled your Dice {bigNumber(round(regular * offset))} ({bigNumber(round(regular))}) times!") + "▐", COLOR)
    stdscr.addstr(31, 0, "▌" + cent(f"You rolled your Golden Dice {bigNumber(round(gold * offset))} ({bigNumber(round(gold))}) times!") + "▐", COLOR)
    stdscr.addstr(32, 0, "▛" + (WIDTH - 2) * "▀" + "▜", COLOR)
    stdscr.addstr(33, 0, "▌" + cent(f"You rolled this much: {bigNumber((total + goldTotal if gold > 0 else total) * scale)}") + "▐", COLOR)
    stdscr.addstr(34, 0, "▌" + cent(f"Your current Multiplier: {round(mult, 2)} MP") + "▐", COLOR)
    stdscr.addstr(35, 0, "▌" + cent(f"Your Card and Four of a Kind Multipliers: {round(cards, 2)}, {round(four, 2)}") + "▐", COLOR)
    stdscr.addstr(36, 0, "▌" + cent(f"You now have {bigNumber(totalPoints)} more points.") + "▐", COLOR)
    stdscr.addstr(37, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
    stdscr.refresh()
    stdscr.getch()
    
    return totalPoints

def chooseDiceAmount(stdscr, point: float, name: str, price: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)
    
    maxAmount = point // price
    
    stdscr.addstr(32, 0, "▌" + cent(f"You have {bigNumber(point)} points.") + "▐", COLOR)
    stdscr.addstr(33, 0, "▌" + cent(f"With your points, you can get {bigNumber(maxAmount)} {name} sided Dice") + "▐", COLOR)
    stdscr.addstr(34, 0, "▌" + cent("How many Dice do you want?") + "▐", COLOR)
    stdscr.addstr(35, 0, "▛" + (WIDTH - 2) * "▀" + "▜", COLOR)
    stdscr.addstr(36, 0, "▌ >" + (WIDTH - 4) * " " + "▐", COLOR)
    stdscr.addstr(37, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
    
    stdscr.refresh()
    
    curses.curs_set(1)
    win = curses.newwin(1, 100, 36, 4)
    box = Textbox(win)
    
    try:
        box.edit()
        choice = int(box.gather())
    except ValueError:
        stdscr.addstr(39, 0, f"Please choose a number between 1 and {bigNumber(maxAmount)}.", COLOR)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0
    
    if not (1 <= choice <= maxAmount):
        
        if choice <= 0: msg = "You must buy at least 1 Die!"
        else:           msg = "You don't have enough points!"
            
        stdscr.addstr(39, 0, msg, COLOR)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0
    
    stdscr.addstr(38, 0, "▌" + cent(f"You now have {choice} more {name} sided Dice.") + "▐", COLOR)
    stdscr.addstr(39, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.getch()
    
    return choice, choice * price

def diceDisplay(stdscr, name: str, price: str, tradeName: str, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)
         
    stdscr.addstr(21, 0, "▌" + cent("WARNING!") + "▐", COLOR)
    stdscr.addstr(22, 0, "▌" + cent("YOU'RE ABOUT TO TRADE OFF YOUR DICE") + "▐", COLOR)
    stdscr.addstr(23, 0, "▌" + cent(f"OR PAY {price} POINTS") + "▐", COLOR)
    stdscr.addstr(24, 0, "▌" + cent(f"FOR A {name} SIDED DIE") + "▐", COLOR)
    stdscr.addstr(25, 0, "▛" + (WIDTH - 2) * "▀" + "▜", COLOR)
    stdscr.addstr(26, 0, "▌" + cent(f"1 - Trade off my {tradeName} sided Dice") + "▐", COLOR)
    stdscr.addstr(27, 0, "▌" + cent(f"2 - Trade off my Golden {tradeName} sided Dice") + "▐", COLOR)
    stdscr.addstr(28, 0, "▌" + cent("3 - Pay for the Die") + "▐", COLOR)
    stdscr.addstr(29, 0, "▌" + cent("4 - Choose how many Dice") + "▐", COLOR)
    stdscr.addstr(30, 0, "▌" + cent("0 - I don't want to") + "▐", COLOR)
    stdscr.addstr(31, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)

def diceTrade(stdscr, tradeAmount: int, price: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)
    
    newReg  = 0
    newGold = 0
    if tradeAmount >= price:
        
        if random.randint(1, 50) != 1:
            newReg += 1
            stdscr.addstr(32, 0, "▌" + cent("Welcome your new Bigger Die!") + "▐", COLOR)
        else:
            newGold += 1
            stdscr.addstr(32, 0, "▌" + cent("Welcome your new Bigger Golden Die!") + "▐", COLOR)
            
        stdscr.addstr(33, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return price, newReg, newGold
        
    else:
        stdscr.addstr(33, 0, "You don't have enough Dice!", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0, 0

def goldDiceTrade(stdscr, tradeAmount: int, price: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)
    
    newGold = 0
    if tradeAmount >= price:
        
        newGold += 1
        
        stdscr.addstr(32, 0, "▌" + cent("Welcome your new Bigger Golden Die!") + "▐", COLOR)
        stdscr.addstr(33, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return price, newGold
        
    else:
        stdscr.addstr(33, 0, "You don't have enough Dice!", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0

def pointTrade(stdscr, point: float, price: float, COLOR):
    
    _, WIDTH = stdscr.getmaxyx() # 156
    cent = lambda c: c.center(WIDTH - 2)
    
    newReg  = 0
    newGold = 0
    if point >= price:
        
        if random.randint(1, 50) != 1:
            newReg += 1
            stdscr.addstr(32, 0, "▌" + cent("Welcome your new Die!") + "▐", COLOR)
        else:
            newGold += 1
            stdscr.addstr(32, 0, "▌" + cent("Welcome your new Golden Die!") + "▐", COLOR)
            
        stdscr.addstr(33, 0, "▙" + (WIDTH - 2) * "▄" + "▟", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return price, newReg, newGold
        
    else:
        stdscr.addstr(33, 0, "You don't have enough points!", COLOR)
        stdscr.refresh()
        stdscr.getch()
        return 0, 0, 0

def main(stdscr):
    
    # BOOLEANS
    Menu  = True
    Play  = False
    Store = False
    Tree  = False
    Info  = False
    Cards = False

    # GLOBAL VARIABLES
    global diceSides, diceAmount, goldDiceSides, goldDiceAmount, points, pointsMult, pointsMultExpo
    global upgradeDice, upgradeExpo, moreDice, moreExpo, rollLuck, upgradeLuck, luckExpo
    global hundoDiceAmount, thundoDiceAmount, mundoDiceAmount, trundoDiceAmount, qindoDiceAmount
    global goldHundoDiceAmount, goldThundoDiceAmount, goldMundoDiceAmount, goldTrundoDiceAmount, goldQindoDiceAmount
    global storePriceOffset, diceAmountOffset, luckOffset, multiplierOffset
    global hasHundo, hasThundo, hasMundo, hasTrundo, hasQindo, hasTree
    global gameVersion, saveName, cardFour, fourOfAKind, cardPrice
    
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
    _, WIDTH   = stdscr.getmaxyx()
    cent       = lambda c: c.center(WIDTH - 2)
    centHalf   = lambda h: h.center(int(WIDTH/2 - 2))
    
    # ASCII BLOCK CHARACTERS
    # BLOCK  FULL     █
    # BLOCK  HALF     ▒
    # BLOCK  SOME     ░
    # LINE   LEFT     ▐
    # LINE   RIGHT    ▌
    # BLOCK  TOP      ▀
    # BLOCK  BOTTOM   ▄
    # TOP    LEFT     ▛
    # TOP    RIGHT    ▜
    # BOTTOM LEFT     ▙
    # BOTTOM RIGHT    ▟
    
    while True:
        
        while Menu:     # GAME MENU
            
            stdscr.clear()
            stdscr.addstr(0, 0, "▛" + (WIDTH - 2) * "▀" + "▜", RED)
            stdscr.addstr(1, 0, "▌" + cent("0 - Exit   Game") + "▐", RED)
            stdscr.addstr(2, 0, "▌" + cent("1 - Load   Game") + "▐", RED)
            stdscr.addstr(3, 0, "▌" + cent("2 - New    Game") + "▐", RED)
            stdscr.addstr(4, 0, "▌" + cent("3 - Info   Game") + "▐", RED)
            stdscr.addstr(5, 0, "▌" + cent("C - Copy   Save") + "▐", RED)
            stdscr.addstr(6, 0, "▌" + cent("R - Rename Save") + "▐", RED)
            stdscr.addstr(7, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":           # EXIT   GAME
                sys.exit()
            
            elif choice == "1":         # LOAD   GAME
                
                stdscr.addstr(8,  0, "▌" + cent("Enter the Save Name") + "▐", RED)
                stdscr.addstr(9,  0, "▌ >" + (WIDTH - 4) * " " + "▐", RED)
                stdscr.addstr(10, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                stdscr.refresh()
                
                curses.curs_set(1)
                win = curses.newwin(1, 100, 9, 4)
                box = Textbox(win)
                
                box.edit()
                saveName = str(box.gather()).rstrip().lower()
                curses.curs_set(0)
                
                try:
                    
                    with open(f"{saveName}.json", "r") as f:
                        data = json.load(f)
                    
                    # REGULAR DICE
                    diceSides        = data["dice"]["regular"]["diceSides"]
                    diceAmount       = data["dice"]["regular"]["diceAmount"]
                    hundoDiceAmount  = data["dice"]["regular"]["hundoDiceAmount"]
                    thundoDiceAmount = data["dice"]["regular"]["thundoDiceAmount"]
                    mundoDiceAmount  = data["dice"]["regular"]["mundoDiceAmount"]
                    trundoDiceAmount = data["dice"]["regular"]["trundoDiceAmount"]
                    qindoDiceAmount  = data["dice"]["regular"]["qindoDiceAmount"]
                    
                    # GOLD DICE
                    goldDiceSides        = data["dice"]["gold"]["goldDiceSides"]
                    goldDiceAmount       = data["dice"]["gold"]["goldDiceAmount"]
                    goldHundoDiceAmount  = data["dice"]["gold"]["goldHundoDiceAmount"]
                    goldThundoDiceAmount = data["dice"]["gold"]["goldThundoDiceAmount"]
                    goldMundoDiceAmount  = data["dice"]["gold"]["goldMundoDiceAmount"]
                    goldTrundoDiceAmount = data["dice"]["gold"]["goldTrundoDiceAmount"]
                    goldQindoDiceAmount  = data["dice"]["gold"]["goldQindoDiceAmount"]
                    
                    # POINTS
                    points         = data["points"]["points"]
                    pointsMult     = data["points"]["pointsMult"]
                    pointsMultExpo = data["points"]["pointsMultExpo"]
                    
                    # STORE
                    upgradeDice = data["store"]["upgradeDice"]
                    moreDice    = data["store"]["moreDice"]
                    rollLuck    = data["store"]["rollLuck"]
                    upgradeLuck = data["store"]["upgradeLuck"]
                    
                    # OFFSET
                    storePriceOffset = data["offset"]["storePriceOffset"]
                    diceAmountOffset = data["offset"]["diceAmountOffset"]
                    luckOffset       = data["offset"]["luckOffset"]
                    multiplierOffset = data["offset"]["multiplierOffset"]
                    
                    # HAS UNLOCKED
                    hasHundo  = data["has"]["hasHundo"]
                    hasThundo = data["has"]["hasThundo"]
                    hasMundo  = data["has"]["hasMundo"]
                    hasTrundo = data["has"]["hasTrundo"]
                    hasQindo  = data["has"]["hasQindo"]
                    hasTree   = data["has"]["hasTree"]
                    
                    # CARDS
                    cardFour    = data["playing_cards"]["cardFour"]
                    fourOfAKind = data["playing_cards"]["fourOfAKind"]
                    cardPrice   = data["playing_cards"]["cardPrice"]
                    
                    # MISC
                    data["game_info"]["saveName"] = saveName
                    
                    stdscr.addstr(11, 0, "▌" + cent("Welcome back!") + "▐", RED)
                    stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()
                        
                    Menu = False
                    Play = True
                        
                except OSError:
                    stdscr.addstr(11, 0, "▌" + cent("Corrupt or missing file!") + "▐", RED)
                    stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "2":         # NEW    GAME
                
                stdscr.addstr(8,  0, "▌" + cent("Are you sure?") + "▐", RED)
                stdscr.addstr(9,  0, "▛" + (WIDTH - 2) * "▀" + "▜", RED)
                stdscr.addstr(10, 0, "▌" + cent("L - No ") + "▐", RED)
                stdscr.addstr(11, 0, "▌" + cent("S - Yes") + "▐", RED)
                stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                
                choice = stdscr.getkey()
                
                if choice == "l":       # NO
                    continue
                    
                elif choice == "s":     # YES
                    
                    stdscr.addstr(13, 0, "▌" + cent("Enter the Save Name") + "▐", RED)
                    stdscr.addstr(14, 0, "▌ >" + (WIDTH - 4) * " " + "▐", RED)
                    stdscr.addstr(15, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    
                    curses.curs_set(1)
                    win = curses.newwin(1, 100, 14, 4)
                    box = Textbox(win)
                    
                    box.edit()
                    saveName = str(box.gather()).rstrip().lower()
                    curses.curs_set(0)
                    
                    diceSides      = 4
                    diceAmount     = 1
                    points         = 0
                    pointsMult     = 1.0
                    pointsMultExpo = 1.15

                    upgradeDice = 50
                    upgradeExpo = 1.05
                    moreDice    = 50
                    moreExpo    = 1.2

                    hundoDiceAmount  = 0
                    thundoDiceAmount = 0
                    mundoDiceAmount  = 0
                    trundoDiceAmount = 0
                    qindoDiceAmount  = 0

                    rollLuck    = 1
                    upgradeLuck = 200
                    luckExpo    = 1.1

                    storePriceOffset = 1.0
                    diceAmountOffset = 1.0
                    luckOffset       = 1.0
                    multiplierOffset = 1.0

                    hasHundo  = False
                    hasThundo = False
                    hasMundo  = False
                    hasTrundo = False
                    hasQindo  = False
                    hasTree   = False

                    fourOfAKind = 0
                    cardPrice   = 10_000_000
                    for i in cardFour.values():
                            for j in i:
                                i[j] = False
                    
                    stdscr.clear()
                    stdscr.refresh()
                    Menu = False
                    Play = True
                
                else:                   # INVALID
                    stdscr.addstr(13, 0, "▌" + cent("Invalid choice!") + "▐", RED)
                    stdscr.addstr(14, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "3":         # INFO   GAME
                Info = True
                Menu = False

            elif choice == "c":         # COPY   SAVE
                
                stdscr.addstr(8,  0, "▌" + cent("Enter the Save Name") + "▐", RED)
                stdscr.addstr(9,  0, "▌ >" + (WIDTH - 4) * " " + "▐", RED)
                stdscr.addstr(10, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                stdscr.refresh()
                
                curses.curs_set(1)
                win = curses.newwin(1, 100, 9, 4)
                box = Textbox(win)
                
                box.edit()
                tempName = str(box.gather()).rstrip().lower()
                curses.curs_set(0)
                
                try:
                    
                    with open(f"{tempName}.json", "r") as f:
                        json.load(f)
                        
                    popen(f"copy {tempName}.json {tempName}-copy.json")
                    stdscr.addstr(11, 0, "▌" + cent(f"Copied {tempName}.json as {tempName}-copy.json.") + "▐", RED)
                    stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()
                
                except OSError:
                    
                    stdscr.addstr(11, 0, "▌" + cent("No Save with that Name!") + "▐", RED)
                    stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()

            elif choice == "r":         # RENAME SAVE
                
                stdscr.addstr(8,  0, "▌" + cent("Enter the Save Name") + "▐", RED)
                stdscr.addstr(9,  0, "▌ >" + (WIDTH - 4) * " " + "▐", RED)
                stdscr.addstr(10, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                stdscr.refresh()
                
                curses.curs_set(1)
                win = curses.newwin(1, 100, 9, 4)
                box = Textbox(win)
                box.edit()
                tempName = str(box.gather()).rstrip().lower()
                curses.curs_set(0)
                
                try:
                    
                    with open(f"{tempName}.json", "r") as f:
                        json.load(f)
                        
                    stdscr.addstr(11, 0, "▌" + cent("Enter the New Save Name") + "▐", RED)
                    stdscr.addstr(12, 0, "▌ >" + (WIDTH - 4) * " " + "▐", RED)
                    stdscr.addstr(13, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    
                    curses.curs_set(1)
                    win = curses.newwin(1, 100, 12, 4)
                    box = Textbox(win)
                    box.edit()
                    tempNewName = str(box.gather()).rstrip().lower()
                    curses.curs_set(0)
                        
                    rename(f"{tempName}.json", f"{tempNewName}.json")
                    stdscr.addstr(14, 0, "▌" + cent(f"Renamed {tempName}.json to {tempNewName}.json.") + "▐", RED)
                    stdscr.addstr(15, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()
                
                except OSError:
                    
                    stdscr.addstr(11, 0, "▌" + cent("No Save with that Name!") + "▐", RED)
                    stdscr.addstr(12, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
                    stdscr.refresh()
                    stdscr.getch()

        while Play:     # GAME PLAY
            
            saveGame(saveName)
            stdscr.clear()
            
            count = sum(v for k in cardFour.values() for v in k.values())
            cardPoints = 1 + count / 100
            fourPoints = 1 + fourOfAKind / 100
            
            # DICE DISPLAY
            stdscr.addstr(0, 0, "▛" + (WIDTH - 2) * "▀" + "▜", BLUE)
            stdscr.addstr(1, 0, "▌" + centHalf(f"You have {round(diceAmount * diceAmountOffset)} ({round(diceAmount)}) {diceSides} sided Dice"), BLUE)
            stdscr.addstr(1, int(WIDTH/2 + 1), centHalf(f"You have {round(goldDiceAmount * diceAmountOffset)} ({round(goldDiceAmount)}) {goldDiceSides} sided Golden Dice") + "▐", BLUE)
            if hasMundo: 
                    stdscr.addstr(2, 0, "▌" + centHalf(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} ({bigNumber(round(hundoDiceAmount))}) Hundred sided Dice"), BLUE)
                    stdscr.addstr(2, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldHundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldHundoDiceAmount))}) Hundred sided Golden Dice") + "▐", BLUE)
            else:   stdscr.addstr(2, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if thundoDiceAmount > 0 or hasThundo:
                    stdscr.addstr(3, 0, "▌" + centHalf(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} ({bigNumber(round(thundoDiceAmount))}) Thousand sided Dice"), BLUE)
                    stdscr.addstr(3, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldThundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldThundoDiceAmount))}) Thousand sided Golden Dice") + "▐", BLUE)
            else:   stdscr.addstr(3, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if mundoDiceAmount > 0 or hasMundo:
                    stdscr.addstr(4, 0, "▌" + centHalf(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} ({bigNumber(round(mundoDiceAmount))}) Million sided Dice"), BLUE)
                    stdscr.addstr(4, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldMundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldMundoDiceAmount))}) Million sided Golden Dice") + "▐", BLUE)
            else:   stdscr.addstr(4, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if trundoDiceAmount > 0 or hasTrundo:
                    stdscr.addstr(5, 0, "▌" + centHalf(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} ({bigNumber(round(trundoDiceAmount))}) Trillion sided Dice"), BLUE)
                    stdscr.addstr(5, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldTrundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldTrundoDiceAmount))}) Trillion sided Golden Dice") + "▐", BLUE)
            else:   stdscr.addstr(5, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if qindoDiceAmount > 0 or hasQindo:
                    stdscr.addstr(6, 0, "▌" + centHalf(f"You have {bigNumber(round(qindoDiceAmount * diceAmountOffset))} ({bigNumber(round(qindoDiceAmount))}) Quintillion sided Dice"), BLUE)
                    stdscr.addstr(6, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldQindoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldQindoDiceAmount))}) Quintillion sided Golden Dice") + "▐", BLUE)
            else:   stdscr.addstr(6, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            
            # POINTS, CARDS, LUCK AND MULTIPLIER DISPLAY
            stdscr.addstr(7,  0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
            stdscr.addstr(8,  0, "▌" + cent(f"You have {bigNumber(points)} points and you have {count}/{len(cardFour["0"]) * len(cardFour)} cards.") + "▐", BLUE)
            stdscr.addstr(9,  0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            stdscr.addstr(10, 0, "▌" + cent(f"Your lowest Dice roll: {round(rollLuck)}") + "▐", BLUE)
            stdscr.addstr(11, 0, "▌" + centHalf(f"Your current Multiplier: {round(pointsMult, 2)} MP"), BLUE)
            stdscr.addstr(11, int(WIDTH/2 + 1), centHalf(f"Progress to the next Multiplier upgrade: {"0" if 1000 ** pointsMult - points < 0 else bigNumber(1000 ** pointsMult - points)} points ") + "▐", BLUE)
            stdscr.addstr(12, 0, "▌" + cent(progressBar(points / (1000 ** pointsMult), WIDTH - 2)) + "▐", BLUE)
            if points >= 1000 ** pointsMult: stdscr.addstr(13, 0, "▌" + cent("You have enough points to upgrade your Multiplier!") + "▐", BLUE)
            else:                            stdscr.addstr(13, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if pointsMult >= 10:             stdscr.addstr(14, 0, "▌" + cent("You have enough Multiplier to upgrade it's scaling!") + "▐", BLUE)
            else:                            stdscr.addstr(14, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            stdscr.addstr(15, 0, "▛" + (WIDTH - 2) * "▀" + "▜", BLUE)

            # OPTIONS DISPLAY
            stdscr.addstr(16, 0, "▌" + cent("1 - Dice Store") + "▐", BLUE)
            stdscr.addstr(17, 0, "▌" + cent("2 - Upgrade Multiplier") + "▐", BLUE)
            if pointsMult >= 10: stdscr.addstr(18, 0, "▌" + cent("3 - Upgrade Multiplier scaling") + "▐", BLUE)
            else:                stdscr.addstr(18, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            stdscr.addstr(19, 0, "▌" + cent("4 - Roll Dice") + "▐", BLUE)
            if hundoDiceAmount > 0:       stdscr.addstr(20, 0, "▌" + cent("5 - Roll the Hundred sided Dice") + "▐", BLUE)
            else:                         stdscr.addstr(20, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if thundoDiceAmount > 0:      stdscr.addstr(21, 0, "▌" + cent("6 - Roll the Thousand sided Dice") + "▐", BLUE)
            else:                         stdscr.addstr(21, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if mundoDiceAmount > 0:       stdscr.addstr(22, 0, "▌" + cent("7 - Roll the Million sided Dice") + "▐", BLUE)
            else:                         stdscr.addstr(22, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if trundoDiceAmount > 0:      stdscr.addstr(23, 0, "▌" + cent("8 - Roll the Trillion sided Dice") + "▐", BLUE)
            else:                         stdscr.addstr(23, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if qindoDiceAmount > 0:       stdscr.addstr(24, 0, "▌" + cent("9 - Roll the Quintillion sided Dice") + "▐", BLUE)
            else:                         stdscr.addstr(24, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            if points >= 1e15 or hasTree: stdscr.addstr(25, 0, "▌" + cent("T - Go to the Upgrade Tree") + "▐", BLUE)
            else:                         stdscr.addstr(25, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
            stdscr.addstr(26, 0, "▌" + cent("0 - Save and Exit") + "▐", BLUE)
            stdscr.addstr(27, 0, "▌" + cent("M - Back to Menu") + "▐", BLUE)
            stdscr.addstr(28, 0, "▌" + cent("K - Look at your Cards") + "▐", BLUE)
            stdscr.addstr(29, 0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # SAVE AND EXIT
                saveGame(saveName)
                sys.exit()
            
            elif choice == "1":     # STORE
                Store = True
                Play = False
                
            elif choice == "2":     # UPGRADE MULTIPLIER
                
                stdscr.addstr(30, 0, "▌" + cent("WARNING!") + "▐", BLUE)
                stdscr.addstr(31, 0, "▌" + cent("UPGRADING YOUR MULTIPLIER RESETS YOUR") + "▐", BLUE)
                stdscr.addstr(32, 0, "▌" + cent("DICE AND POINTS BACK TO 1 AND 0") + "▐", BLUE)
                stdscr.addstr(33, 0, "▌" + cent("STORE PRICES ARE ALSO RESET") + "▐", BLUE)
                stdscr.addstr(34, 0, "▌" + (WIDTH - 2) * " " + "▐", BLUE)
                stdscr.addstr(35, 0, "▌" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "▐", BLUE)
                stdscr.addstr(36, 0, "▌" + cent(f"You need {bigNumber(1000 ** pointsMult)} points to upgrade your Multiplier.") + "▐", BLUE)
                stdscr.addstr(37, 0, "▛" + (WIDTH - 2) * "▀" + "▜", BLUE)
                stdscr.addstr(38, 0, "▌" + cent("1 - Upgrade Multiplier") + "▐", BLUE)
                stdscr.addstr(39, 0, "▌" + cent("0 - I don't want to") + "▐", BLUE)
                stdscr.addstr(40, 0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
                
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
                        qindoDiceAmount = 0
                        
                        goldDiceAmount = 0
                        goldDiceSides = 0
                        goldHundoDiceAmount = 0
                        goldThundoDiceAmount = 0
                        goldMundoDiceAmount = 0
                        goldTrundoDiceAmount = 0
                        goldQindoDiceAmount = 0
                        
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        cardPrice = 10_000_000
                        fourOfAKind = 0
                        for i in cardFour.values():
                            for j in i:
                                i[j] = False
                        
                        stdscr.addstr(41, 0, "▌" + cent("Wise choice.") + "▐", BLUE)
                        stdscr.addstr(42, 0, "▌" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "▐", BLUE)
                        stdscr.addstr(43, 0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
                        
                    else:
                        stdscr.addstr(42, 0, "You don't have enough points!", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
                
                elif choice == "0":         # NO
                    continue
                
                else:                       # INVALID
                    stdscr.addstr(42, 0, "Invalid choice!", BLUE)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "3":     # UPGRADE MULTIPLIER SCALING
                
                if pointsMult >= 10:
                
                    stdscr.addstr(30, 0, "▌" + cent("WARNING!") + "▐", BLUE)
                    stdscr.addstr(31, 0, "▌" + cent("UPGRADING YOUR MULTIPLIER'S SCALING RESETS") + "▐", BLUE)
                    stdscr.addstr(32, 0, "▌" + cent("EVERYTHING BUT YOUR MULTIPLIER BACK TO 1") + "▐", BLUE)
                    stdscr.addstr(33, 0, "▛" + (WIDTH - 2) * "▀" + "▜", BLUE)
                    stdscr.addstr(34, 0, "▌" + cent("0 - I don't want to") + "▐", BLUE)
                    stdscr.addstr(35, 0, "▌" + cent("1 - Upgrade Multiplier scaling") + "▐", BLUE)
                    stdscr.addstr(36, 0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
                    
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
                        qindoDiceAmount = 0
                        
                        goldDiceAmount = 0
                        goldDiceSides = 0
                        goldHundoDiceAmount = 0
                        goldThundoDiceAmount = 0
                        goldMundoDiceAmount = 0
                        goldTrundoDiceAmount = 0
                        goldQindoDiceAmount = 0
                            
                        rollLuck = 1
                        upgradeLuck = 200
                        luckExpo = 1.1
                        
                        cardPrice = 10_000_000
                        fourOfAKind = 0
                        for i in cardFour.values():
                            for j in i:
                                i[j] = False
                        
                        stdscr.addstr(37, 0, "▌" + cent("Great choice!") + "▐", BLUE)
                        stdscr.addstr(38, 0, "▌" + cent(f"Your current Multiplier: {round(pointsMult, 2)} MP") + "▐", BLUE)
                        stdscr.addstr(39, 0, "▙" + (WIDTH - 2) * "▄" + "▟", BLUE)
                        stdscr.refresh()
                        stdscr.getch()

                    elif choice == "0":     # NO
                        continue
                
                    else:                   # INVALID
                        stdscr.addstr(38, 0, "Invalid choice!", BLUE)
                        stdscr.refresh()
                        stdscr.getch()
            
            elif choice == "4":     # ROLL DICE
                points += rollDice(stdscr, diceAmount, goldDiceAmount, diceSides, 1, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
            
            elif choice == "5":     # ROLL HUNDO
                if hundoDiceAmount > 0:
                    points += rollDice(stdscr, hundoDiceAmount, goldHundoDiceAmount, 100, 1, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
                    
            elif choice == "6":     # ROLL THUNDO
                if thundoDiceAmount > 0:
                    points += rollDice(stdscr, thundoDiceAmount, goldThundoDiceAmount, 1000, 1, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
            
            elif choice == "7":     # ROLL MUNDO
                if mundoDiceAmount > 0:
                    points += rollDice(stdscr, mundoDiceAmount, goldMundoDiceAmount, 1_000_000, 1, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
                    
            elif choice == "8":     # ROLL TRUNDO
                if trundoDiceAmount > 0:
                    points += rollDice(stdscr, trundoDiceAmount, goldTrundoDiceAmount, 1_000_000, 1_000_000, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
            
            elif choice == "9":     # ROLL QINDO
                if qindoDiceAmount > 0:
                    points += rollDice(stdscr, qindoDiceAmount, goldQindoDiceAmount, 1_000_000, 1e12, diceAmountOffset, pointsMult, rollLuck, cardPoints, fourPoints, BLUE)
            
            elif choice == "t":     # UPGRADE TREE
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
                stdscr.addstr(31, 0, "Invalid choice!", BLUE)
                stdscr.refresh()
                stdscr.getch()

        while Store:    # GAME STORE
            
            saveGame(saveName)
            stdscr.clear()
            
            # DICE DISPLAY
            stdscr.addstr(0, 0, "▛" + (WIDTH - 2) * "▀" + "▜", YELLOW)
            stdscr.addstr(1, 0, "▌" + centHalf(f"You have {round(diceAmount * diceAmountOffset)} ({round(diceAmount)}) {diceSides} sided Dice"), YELLOW)
            stdscr.addstr(1, int(WIDTH/2 + 1), centHalf(f"You have {round(goldDiceAmount * diceAmountOffset)} ({round(goldDiceAmount)}) {goldDiceSides} sided Golden Dice") + "▐", YELLOW)
            if hasMundo: 
                    stdscr.addstr(2, 0, "▌" + centHalf(f"You have {bigNumber(round(hundoDiceAmount * diceAmountOffset))} ({bigNumber(round(hundoDiceAmount))}) Hundred sided Dice"), YELLOW)
                    stdscr.addstr(2, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldHundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldHundoDiceAmount))}) Hundred sided Golden Dice") + "▐", YELLOW)
            else:   stdscr.addstr(2, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if thundoDiceAmount > 0 or hasThundo:
                    stdscr.addstr(3, 0, "▌" + centHalf(f"You have {bigNumber(round(thundoDiceAmount * diceAmountOffset))} ({bigNumber(round(thundoDiceAmount))}) Thousand sided Dice"), YELLOW)
                    stdscr.addstr(3, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldThundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldThundoDiceAmount))}) Thousand sided Golden Dice") + "▐", YELLOW)
            else:   stdscr.addstr(3, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if mundoDiceAmount > 0 or hasMundo:
                    stdscr.addstr(4, 0, "▌" + centHalf(f"You have {bigNumber(round(mundoDiceAmount * diceAmountOffset))} ({bigNumber(round(mundoDiceAmount))}) Million sided Dice"), YELLOW)
                    stdscr.addstr(4, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldMundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldMundoDiceAmount))}) Million sided Golden Dice") + "▐", YELLOW)
            else:   stdscr.addstr(4, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if trundoDiceAmount > 0 or hasTrundo:
                    stdscr.addstr(5, 0, "▌" + centHalf(f"You have {bigNumber(round(trundoDiceAmount * diceAmountOffset))} ({bigNumber(round(trundoDiceAmount))}) Trillion sided Dice"), YELLOW)
                    stdscr.addstr(5, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldTrundoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldTrundoDiceAmount))}) Trillion sided Golden Dice") + "▐", YELLOW)
            else:   stdscr.addstr(5, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if qindoDiceAmount > 0 or hasQindo:
                    stdscr.addstr(6, 0, "▌" + centHalf(f"You have {bigNumber(round(qindoDiceAmount * diceAmountOffset))} ({bigNumber(round(qindoDiceAmount))}) Quintillion sided Dice"), YELLOW)
                    stdscr.addstr(6, int(WIDTH/2 + 1), centHalf(f"You have {bigNumber(round(goldQindoDiceAmount * diceAmountOffset))} ({bigNumber(round(goldQindoDiceAmount))}) Quintillion sided Golden Dice") + "▐", YELLOW)
            else:   stdscr.addstr(6, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            
            # POINTS AND LUCK DISPLAY
            stdscr.addstr(7,  0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
            stdscr.addstr(8,  0, "▌" + cent(f"You have {bigNumber(points)} points.") + "▐", YELLOW)
            stdscr.addstr(9,  0, "▌" + cent(f"Your lowest Dice roll: {round(rollLuck)}") + "▐", YELLOW)
            stdscr.addstr(10, 0, "▛" + (WIDTH - 2) * "▀" + "▜", YELLOW)
                            
            # OPTIONS DISPLAY
            stdscr.addstr(11, 0, "▌" + cent(f"1 - Upgrade Dice: {bigNumber((upgradeDice * diceAmount) / storePriceOffset)} points") + "▐", YELLOW)
            stdscr.addstr(12, 0, "▌" + cent(f"2 - Buy more Dice: {bigNumber((moreDice * 1.5) / storePriceOffset)} points") + "▐", YELLOW)
            stdscr.addstr(13, 0, "▌" + cent(f"3 - Buy a Lucky Amulet: {bigNumber(upgradeLuck / storePriceOffset)} points") + "▐", YELLOW)
            if diceAmount >= 10 or points >= 12_000:                                           stdscr.addstr(14, 0, "▌" + cent("4 - Get a Hundred sided Die") + "▐", YELLOW)
            else:                                                                              stdscr.addstr(14, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if hundoDiceAmount >= 10 or points >= 120_000:                                     stdscr.addstr(15, 0, "▌" + cent("5 - Get a Thousand sided Die") + "▐", YELLOW)
            else:                                                                              stdscr.addstr(15, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if thundoDiceAmount >= 1000 or hundoDiceAmount >= 10_000 or points >= 120_000_000: stdscr.addstr(16, 0, "▌" + cent("6 - Get a Million sided Die") + "▐", YELLOW)
            else:                                                                              stdscr.addstr(16, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if mundoDiceAmount >= 1_000_000 or points >= 120e12:                               stdscr.addstr(17, 0, "▌" + cent("7 - Get a Trillion sided Die") + "▐", YELLOW)
            else:                                                                              stdscr.addstr(17, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            if trundoDiceAmount >= 1_000_000 or points >= 120e18:                              stdscr.addstr(18, 0, "▌" + cent("8 - Get a Quintillion sided Die") + "▐", YELLOW)
            else:                                                                              stdscr.addstr(18, 0, "▌" + (WIDTH - 2) * " " + "▐", YELLOW)
            stdscr.addstr(19, 0, "▌" + cent("0 - Exit Store") + "▐", YELLOW)
            stdscr.addstr(20, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":           # EXIT STORE
                Play = True
                Store = False
            
            elif choice == "1":         # UPGRADE DICE
                
                if points >= (upgradeDice * diceAmount) / storePriceOffset:
                    
                    points -= (upgradeDice * diceAmount) / storePriceOffset
                    upgradeDice = upgradeDice ** upgradeExpo
                    
                    if random.randint(1, 50) != 1:
                        diceSides += 1
                        stdscr.addstr(21, 0, "▌" + cent(f"You now have {round(diceAmount * diceAmountOffset)} Dice with {diceSides} sides each.") + "▐", YELLOW)
                    else:
                        goldDiceSides += 1
                        stdscr.addstr(21, 0, "▌" + cent(f"You now have {round(goldDiceAmount * diceAmountOffset)} Dice with {goldDiceSides} sides each.") + "▐", YELLOW)
                        
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(21, 0, "▌" + cent("You don't have enough points!") + "▐", YELLOW)
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "2":         # BUY MORE DICE
                
                if points >= (moreDice * 1.5) / storePriceOffset:
                    
                    points -= (moreDice * 1.5) / storePriceOffset
                    moreDice = moreDice ** moreExpo
                    
                    if random.randint(1, 50) != 1:
                        diceAmount += 1
                        stdscr.addstr(21, 0, "▌" + cent(f"You now have {round(diceAmount * diceAmountOffset)} Dice with {diceSides} sides each.") + "▐", YELLOW)
                    else:
                        goldDiceAmount += 1
                        stdscr.addstr(21, 0, "▌" + cent(f"You now have {round(goldDiceAmount * diceAmountOffset)} Gold Dice with {goldDiceSides} sides each.") + "▐", YELLOW)
                    
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(21, 0, "▌" + cent("You don't have enough points!") + "▐", YELLOW)
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "3":         # LUCKY AMULET
                
                if points >= upgradeLuck / storePriceOffset:
                    points -= upgradeLuck / storePriceOffset
                    upgradeLuck = upgradeLuck ** luckExpo
                    rollLuck += 1 * luckOffset
                    stdscr.addstr(21, 0, "▌" + cent("You feel luckier!") + "▐", YELLOW)
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
                    
                else:
                    stdscr.addstr(21, 0, "▌" + cent("You don't have enough points!") + "▐", YELLOW)
                    stdscr.addstr(22, 0, "▙" + (WIDTH - 2) * "▄" + "▟", YELLOW)
                    stdscr.refresh()
                    stdscr.getch()
            
            elif choice == "4":         # GET HUNDO DICE
                
                if diceAmount >= 10 or points >= 12_000:
                    
                    diceDisplay(stdscr, "Hundred", "12000", "Regular", YELLOW)
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        trade, regular, gold = diceTrade(stdscr, diceAmount, 10, YELLOW)
                        diceAmount -= trade
                        hundoDiceAmount += regular
                        goldHundoDiceAmount += gold
                        hasHundo = True
                    
                    elif choice == "2":         # GOLDEN DICE AMOUNT
                        
                        trade, amount = goldDiceTrade(stdscr, goldDiceAmount, 10, YELLOW)
                        goldDiceAmount -= trade
                        goldHundoDiceAmount += amount
                    
                    elif choice == "3":         # ENOUGH POINTS
                        
                        spent, regular, gold = pointTrade(stdscr, points, 12_000, YELLOW)
                        points -= spent
                        hundoDiceAmount += regular
                        goldHundoDiceAmount += gold
                        hasHundo = True
                    
                    elif choice == "4":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Hundred", 12_000, YELLOW)
                        points -= spent
                        for i in range(dice):
                            if random.randint(1, 50) != 1: hundoDiceAmount += 1
                            else:                          goldHundoDiceAmount += 1
                        hasHundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
            elif choice == "5":         # GET THUNDO DICE
                
                if hundoDiceAmount >= 10 or points >= 120_000:
                    
                    diceDisplay(stdscr, "Thousand", "120000", "Hundred", YELLOW)
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        trade, regular, gold = diceTrade(stdscr, hundoDiceAmount, 10, YELLOW)
                        hundoDiceAmount -= trade
                        thundoDiceAmount += regular
                        goldThundoDiceAmount += gold
                        hasThundo = True
                    
                    elif choice == "2":         # GOLDEN DICE AMOUNT
                        
                        trade, gold = goldDiceTrade(stdscr, goldHundoDiceAmount, 10, YELLOW)
                        goldHundoDiceAmount -= trade
                        goldThundoDiceAmount += gold
                    
                    elif choice == "3":         # ENOUGH POINTS
                        
                        spent, regular, gold = pointTrade(stdscr, points, 120_000, YELLOW)
                        points -= spent
                        thundoDiceAmount += regular
                        goldThundoDiceAmount += gold
                        hasThundo = True
                    
                    elif choice == "4":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Thousand", 120_000, YELLOW)
                        points -= spent
                        for i in range(dice):
                            if random.randint(1, 50) != 1: thundoDiceAmount += 1
                            else:                          goldThundoDiceAmount += 1
                        hasThundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
            elif choice == "6":         # GET MUNDO DICE
                
                if thundoDiceAmount >= 1000 or points >= 120_000_000:
                    
                    diceDisplay(stdscr, "Million", "120 Million", "Thousand", YELLOW)
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        trade, regular, gold = diceTrade(stdscr, thundoDiceAmount, 1000, YELLOW)
                        thundoDiceAmount -= trade
                        mundoDiceAmount += regular
                        goldMundoDiceAmount += gold
                        hasMundo = True
                    
                    elif choice == "2":         # GOLDEN DICE AMOUNT
                        
                        trade, amount = goldDiceTrade(stdscr, goldThundoDiceAmount, 1000, YELLOW)
                        goldThundoDiceAmount -= trade
                        goldMundoDiceAmount += amount
                    
                    elif choice == "3":         # ENOUGH POINTS
                        
                        spent, regular, gold = pointTrade(stdscr, points, 120_000_000, YELLOW)
                        points -= spent
                        mundoDiceAmount += regular
                        goldMundoDiceAmount += gold
                        hasMundo = True
                    
                    elif choice == "4":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Million", 120_000_000, YELLOW)
                        points -= spent
                        for i in range(dice):
                            if random.randint(1, 50) != 1: mundoDiceAmount += 1
                            else:                           goldMundoDiceAmount += 1
                        hasMundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
            elif choice == "7":         # GET TRUNDO DICE
                
                if mundoDiceAmount >= 1_000_000 or points >= 120e12:
                    
                    diceDisplay(stdscr, "Trillion", "120 Trillion", "Million", YELLOW)
                    choice = stdscr.getkey()
                    
                    if choice == "1":           # DICE AMOUNT
                        
                        trade, regular, gold = diceTrade(stdscr, mundoDiceAmount, 1_000_000, YELLOW)
                        mundoDiceAmount -= trade
                        trundoDiceAmount += regular
                        goldTrundoDiceAmount += gold
                        hasTrundo = True
                    
                    elif choice == "2":         # GOLDEN DICE AMOUNT
                        
                        trade, amount = goldDiceTrade(stdscr, goldMundoDiceAmount, 1_000_000, YELLOW)
                        goldMundoDiceAmount -= trade
                        goldTrundoDiceAmount += amount
                    
                    elif choice == "2":         # ENOUGH POINTS
                        
                        spent, regular, gold = pointTrade(stdscr, points, 120e12, YELLOW)
                        points -= spent
                        trundoDiceAmount += regular
                        goldTrundoDiceAmount += gold
                        hasTrundo = True
                    
                    elif choice == "3":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Trillion", 120e12, YELLOW)
                        points -= spent
                        for i in range(dice):
                            if random.randint(1, 50) != 1: trundoDiceAmount += 1
                            else:                          goldTrundoDiceAmount += 1
                        hasTrundo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
            elif choice == "8":         # GET QINDO DICE
                
                if trundoDiceAmount >= 1_000_000 or points >= 120e18:
                    
                    diceDisplay(stdscr, "Quintillion", "120 Quintillion", "Trillion", YELLOW)
                    choice = stdscr.getkey()

                    if choice == "1":           # DICE AMOUNT
                        
                        trade, regular, gold = diceTrade(stdscr, trundoDiceAmount, 1_000_000, YELLOW)
                        trundoDiceAmount -= trade
                        qindoDiceAmount += regular
                        goldQindoDiceAmount += gold
                        hasQindo = True
                    
                    elif choice == "2":         # GOLDEN DICE AMOUNT
                        
                        trade, amount = goldDiceTrade(stdscr, goldTrundoDiceAmount, 1_000_000, YELLOW)
                        goldTrundoDiceAmount -= trade
                        goldQindoDiceAmount += amount
                    
                    elif choice == "3":         # ENOUGH POINTS
                        
                        spent, regular, gold = pointTrade(stdscr, points, 120e18, YELLOW)
                        points -= spent
                        qindoDiceAmount += regular
                        goldQindoDiceAmount += gold
                        hasQindo = True

                    elif choice == "4":         # CHOOSE HOW MANY DICE
                        
                        dice, spent = chooseDiceAmount(stdscr, points, "Quintillion", 120e18, YELLOW)
                        points -= spent
                        for i in range(dice):
                            if random.randint(1, 50) != 1: qindoDiceAmount += 1
                            else:                          goldQindoDiceAmount += 1
                        hasQindo = True

                    elif choice == "0":         # NOTHING
                        continue
                    
            else:                       # INVALID
                stdscr.addstr(22, 0, "Invalid choice!", YELLOW)
                stdscr.refresh()
                stdscr.getch()

        while Tree:     # GAME TREE
            
            saveGame(saveName)
            stdscr.clear()
            
            stdscr.addstr(0,  0, "▛" + (WIDTH - 2) * "▀" + "▜", GREEN)
            stdscr.addstr(1,  0, "▌" + cent("Welcome to the Upgrade Tree!") + "▐", GREEN)
            stdscr.addstr(2,  0, "▌" + cent("If you're here, it means that you've accumulated over 1 quadrillion points") + "▐", GREEN)
            stdscr.addstr(3,  0, "▌" + cent("and you're wondering what this magical place could possibly be?") + "▐", GREEN)
            stdscr.addstr(4,  0, "▌" + cent("(also these are PERMANENT, meaning upgrading Multiplier won't reset these)") + "▐", GREEN)
            stdscr.addstr(5,  0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
            stdscr.addstr(6,  0, "▌" + cent("Well wait no further!") + "▐", GREEN)
            stdscr.addstr(7,  0, "▌" + (WIDTH - 2) * " " + "▐", GREEN)
            stdscr.addstr(8,  0, "▌" + cent("Here you can upgrade anything you could ever think of!") + "▐", GREEN)
            stdscr.addstr(9,  0, "▌" + cent("You want the Store prices to be cheaper? You got it!") + "▐", GREEN)
            stdscr.addstr(10, 0, "▌" + cent("You want more Dice per Dice? You can have that!") + "▐", GREEN)
            stdscr.addstr(11, 0, "▌" + cent("You can even have more Multiplier and better Scaling!") + "▐", GREEN)
            stdscr.addstr(12, 0, "▛" + (WIDTH - 2) * "▀" + "▜", GREEN)
            stdscr.addstr(13, 0, "▌" + cent("1 - View possible Upgrades") + "▐", GREEN)
            stdscr.addstr(14, 0, "▌" + cent("0 - Leave the Upgrade Tree") + "▐", GREEN)
            stdscr.addstr(15, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # LEAVE
                Tree = False
                Play = True
            
            elif choice == "1":     # POSSIBLE UPGRADES
                
                stdscr.addstr(16, 0, "▌" + cent(f"You have {bigNumber(points)} points.") + "▐", GREEN)
                stdscr.addstr(17, 0, "▛" + (WIDTH - 2) * "▀" + "▜", GREEN)
                stdscr.addstr(18, 0, "▌" + cent(f"1 - Better store prices: {bigNumber(1e15 ** storePriceOffset)} points") + "▐", GREEN)
                stdscr.addstr(19, 0, "▌" + cent(f"2 - More dice per dice: {bigNumber(1e15 ** diceAmountOffset)} points") + "▐", GREEN)
                stdscr.addstr(20, 0, "▌" + cent(f"3 - Get even luckier: {bigNumber(1e18 ** luckOffset)} points") + "▐", GREEN)
                stdscr.addstr(21, 0, "▌" + cent(f"4 - More Multiplier: {bigNumber(1e21 ** multiplierOffset)} points") + "▐", GREEN)
                stdscr.addstr(22, 0, "▌" + cent("0 - Exit to the Upgrade Tree") + "▐", GREEN)
                stdscr.addstr(23, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
                
                choice = stdscr.getkey()
                
                if choice == "0":       # EXIT
                    continue
                
                elif choice == "1":     # BETTER PRICES
                    
                    if points >= 1e15 ** storePriceOffset:
                        
                        points -= 1e15 ** storePriceOffset
                        storePriceOffset += 0.2
                        
                        stdscr.addstr(24, 0, "▌" + cent("Store Prices are now cheaper!") + "▐", GREEN)
                        stdscr.addstr(25, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
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
                        
                        stdscr.addstr(24, 0, "▌" + cent("You magically have more dice!") + "▐", GREEN)
                        stdscr.addstr(25, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
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
                        
                        stdscr.addstr(24, 0, "▌" + cent("You feel even luckier!") + "▐", GREEN)
                        stdscr.addstr(25, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
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
                        
                        stdscr.addstr(24, 0, "▌" + cent("The Multiplier already feels stronger!") + "▐", GREEN)
                        stdscr.addstr(25, 0, "▙" + (WIDTH - 2) * "▄" + "▟", GREEN)
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
            
            stdscr.clear()
            stdscr.addstr(0, 0, "▛" + (WIDTH - 2) * "▀" + "▜", RED)
            stdscr.addstr(1, 0, "▌" + cent(f"Game version: {gameVersion}") + "▐", RED)
            stdscr.addstr(2, 0, "▌" + cent("Any - Back to Menu") + "▐", RED)
            stdscr.addstr(3, 0, "▙" + (WIDTH - 2) * "▄" + "▟", RED)
            stdscr.refresh()
            stdscr.getkey()
            Info = False
            Menu = True

        while Cards:    # GAME CARDS
            
            saveGame(saveName)
            stdscr.clear()
            
            countTrue = {k: sum(vv for vv in v.values()) for k, v in cardFour.items()}
            allTrueKeys = [k for k, v in cardFour.items() if all(v.values())]
            trueCards = sum(v for thing in cardFour.values() for v in thing.values())
            falseCards = [(ok, ik) for ok, thing in cardFour.items() for ik, v in thing.items() if not v]
            ableFour = False
            
            stdscr.addstr(0, 0, "▛" + (WIDTH - 2) * "▀" + "▜", MAGENTA)
            x, y = 1, 1
            for thing in cardFour:
                for suit in cardFour[thing]:
                    if countTrue[thing] == 4: ableFour = True
                    if   suit == "Club":    stdscr.addstr(x, y, f" {thing} of {suit}s  ▐{23 * "█" if countTrue[thing] == 4 else 23 * "▒" if cardFour[thing][suit] else 23 * "░"}▌ ", MAGENTA)
                    elif suit == "Heart":   stdscr.addstr(x, y, f" {thing} of {suit}s  ▐{22 * "█" if countTrue[thing] == 4 else 22 * "▒" if cardFour[thing][suit] else 22 * "░"}▌ ", MAGENTA)
                    elif suit == "Spade":   stdscr.addstr(x, y, f" {thing} of {suit}s  ▐{21 * "█" if countTrue[thing] == 4 else 21 * "▒" if cardFour[thing][suit] else 21 * "░"}▌ ", MAGENTA)
                    elif suit == "Diamond": stdscr.addstr(x, y, f" {thing} of {suit}s  ▐{20 * "█" if countTrue[thing] == 4 else 20 * "▒" if cardFour[thing][suit] else 20 * "░"}▌ ", MAGENTA)
                    y += int(WIDTH / 4)
                x += 1
                y = 1
            
            for i in range(37): stdscr.addstr(i + 1, WIDTH - 1, "▐", MAGENTA)
            for j in range(37): stdscr.addstr(j + 1, 0, "▌", MAGENTA)
            stdscr.addstr(37, 0, "▙" + (WIDTH - 2) * "▄" + "▟", MAGENTA)
            stdscr.addstr(38, 0, "▌" + cent(f"You have unlocked {trueCards}/{len(cardFour[thing]) * len(cardFour)} Cards and you have {bigNumber(points)} points.") + "▐", MAGENTA)
            stdscr.addstr(39, 0, "▛" + (WIDTH - 2) * "▀" + "▜", MAGENTA)
            stdscr.addstr(40, 0, "▌" + cent("0 - Stop looking at your Cards") + "▐", MAGENTA)
            stdscr.addstr(41, 0, "▌" + cent(f"1 - Buy a random Card: {bigNumber(cardPrice)}") + "▐", MAGENTA)
            if ableFour: stdscr.addstr(42, 0, "▌" + cent("2 - Trade away a Four of a Kind") + "▐", MAGENTA)
            else:        stdscr.addstr(42, 0, "▌" + (WIDTH - 2) * " " + "▐", MAGENTA)
            stdscr.addstr(43, 0, "▙" + (WIDTH - 2) * "▄" + "▟", MAGENTA)
            stdscr.refresh()
            
            choice = stdscr.getkey()
            
            if choice == "0":       # LEAVE
                Cards = False
                Play = True
                
            elif choice == "1":     # RANDOM CARD
                
                if not trueCards == len(cardFour[thing]) * len(cardFour):
                
                    if points >= cardPrice:
                        
                        points -= cardPrice
                        cardPrice = cardPrice * (1 + (trueCards/40))
                        ok, ik = random.choice(falseCards)
                        cardFour[ok][ik] = True
                        
                        stdscr.addstr(44, 0, "▌" + cent(f"You pulled a {ok} of {ik}s for {bigNumber(cardPrice)} points!") + "▐", MAGENTA)
                        try: stdscr.addstr(45, 0, "▙" + (WIDTH - 2) * "▄" + "▟", MAGENTA)
                        except curses.error: pass
                        stdscr.refresh()
                        stdscr.getkey()
                    
                    else:
                        stdscr.addstr(45, 0, "You don't have enough points!", MAGENTA)
                        stdscr.refresh()
                        stdscr.getkey()
                
                else:
                    stdscr.addstr(45, 0, "You have collected all the cards!", MAGENTA)
                    stdscr.refresh()
                    stdscr.getkey()
            
            elif choice == "2":     # FOUR OF A KIND
                
                if ableFour:
                    
                    randomFour = random.choice(allTrueKeys)
                    for suit in cardFour[randomFour]:
                        cardFour[randomFour][suit] = False
                    fourOfAKind += 1
                    
                    stdscr.addstr(44, 0, "▌" + cent(f"Your Four of a Kind was: {randomFour}'s!") + "▐", MAGENTA)
                    try: stdscr.addstr(45, 0, "▙" + (WIDTH - 2) * "▄" + "▟", MAGENTA)
                    except curses.error: pass
                    stdscr.refresh()
                    stdscr.getkey()
                    ableFour = False
            
            else:                   # INVALID
                stdscr.addstr(44, 0, "Invalid choice!", MAGENTA)
                stdscr.refresh()
                stdscr.getkey()


wrapper(main)