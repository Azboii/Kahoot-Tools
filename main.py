import random
import sys
import json
import os
import time
import requests
from colorama import Fore, Back, Style

digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
idx = 0
delst = [
"<b>", "</b>", "<i>", "</i>", "<u>", "</u>", "<sub>", "</sub>", "<sup>", "</sup>", "&#x27;", "&#x60;", "&amp;", "&quot;", "&lt;", "&gt;"
]
relst = [
"", "", "", "", "", "", "", "", "", "", "'", "`", "&", "\"", "<", ">"
]
Active = True
def is_code_valid(string):
    request = requests.get("https://kahoot.it/reserve/session/" + string, verify=True, timeout=10)
    return request

def exclude(string):
    global outstr
    outstr = string.replace(delst[0], relst[0])
    for iEx in range(1, len(delst)):
        outstr = outstr.replace(delst[iEx], relst[iEx])

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

while Active:
    clear()
    sys.stdout.write(Fore.GREEN + "\n1: Code Finder\n2: Find Answers\n3: Find Uuid\n" + Fore.RESET + "Please excuse any formating mistakes\nType ? to get help, Type QUIT to quit" + "\033[F\033[F\033[F\033[F\033[F")
    mode = input("Pick a mode: ")

    print("\n\n\n\n")   #adds space
    if mode == "?":
        clear()
        print("Mode 1: Code Finder\nThis is a tool to help find kahoot codes. This gathers kahoot codes that are somtimes " + Fore.RED + "NOT ACTIVE" + Fore.RESET + " But it stil works.\n\nMode 2: Find Answers\nThis is a tool to find answers to any kahoot. This is mostly used for live games.\nUuid: The Uuid is the code in the hosts url. Ex: https://play.kahoot.it/v2/lobby?quizId=" + Fore.BLUE + "2fd65b05-6a3b-4a3b-b8bd-45ef3a46fb0b" + Fore.RED + "\nTHIS WILL NOT WORK FOR POLLS" + Fore.RESET + "\n\nMode 3: Find Uuid\nThis is tool to find the Uuid if you cant see it / if its not a live game. All you have to do is search for the name of the Kahoot. (This is shown at the start of the kahoot)\nThe results are sorted by playcount, so if your teacher is lazy, this will help find it most of the time. " + Fore.RED + " WARNING: THIS DOES NOT WORK 100% OF THE TIME. IF THE KAHOOT IS PRIVATE, IT WILL NOT WORK (Also will not work past 100 results)")
    if mode == "1":
        clear()
        while True:
            code = ""
            for i in range(int(random.randrange(5, 7))):
                code += random.choice(digits)

            result = is_code_valid(
                code)
            if result.status_code == 200:
                idx += 1
                sys.stdout.write("\r")
                print("#" + str(idx) + "                                    ")
                print("https://kahoot.it?pin=" + code)
            else:
                sys.stdout.write("\r")
                sys.stdout.write(code + "                       ")
    if mode == "2":
        uuid = input("(WRITE THIS DOWN SOMEWHERE) Uuid: ")
        printFalseAns = input("Print wrong answers? (y/n) ")
        printInfoCards = input("Print Info Cards/Slideshows? (y/n) ")
        clear()
        print("Uuid: " + uuid + "\n")
        r = requests.get("https://create.kahoot.it/rest/kahoots/" + uuid, verify=True, timeout=10)
        r = r.content
        rjson = json.loads(r)
        questions = rjson["questions"]
        for i in range(0, len(questions)):
            if questions[i]["type"] == "quiz" or questions[i][
                    "type"] == "multiple_select_quiz":
                exclude(questions[i]["question"])

                print(Fore.RESET + "#" + str(i + 1) + " " + outstr)
                for i2 in range(0, len(questions[i]["choices"])):
                    if questions[i]["choices"][i2]["correct"] is True:
                        exclude(questions[i]["choices"][i2]["answer"])

                        print(Fore.GREEN + outstr)
                    else:
                        if printFalseAns == "y":
                            exclude(questions[i]["choices"][i2]["answer"])

                            print(Fore.RED + outstr)

            else:
                if questions[i]["type"] == "content" and printInfoCards == "y":
                    exclude("#" + str(i+1) + " " + questions[i]["title"])

                    print(Fore.BLUE + outstr)
                    exclude(questions[i]["description"])

                    print(Style.DIM + outstr + Style.NORMAL)
            print("")
    if mode == "3":
        clear()
        search = input("What is the name of the kahoot? ")
        amount = input("Amount of results? (Default: 15) ")
        print("")
        if amount == "":
            amount = "15"
        searchResult = requests.get("https://create.kahoot.it/rest/kahoots/?query=" + search + "&limit=" + amount + "&orderBy=number_of_players", verify=True, timeout=10)
        time.sleep(1)
        searchResult = searchResult.content
        searchResult = json.loads(searchResult)
        for i in range(0,len(searchResult["entities"])):

            if searchResult["entities"][i]["card"]["featured"] == "true" or searchResult["entities"][i]["card"]["young_featured"] == "true":
                sys.stdout.write(Style.NORMAL + "#" + str(i+1) + " " + searchResult["entities"][i]["card"]["title"] + " (" + str(searchResult["entities"][i]["card"]["number_of_plays"]) + " plays) " + Fore.RED + "FEATURED!" + Fore.RESET)
            else: 
                sys.stdout.write(Style.NORMAL + "#" + str(i+1) + " " + searchResult["entities"][i]["card"]["title"] + " (" + str(searchResult["entities"][i]["card"]["number_of_plays"]) + " plays)")
            print("\n" + Style.DIM + searchResult["entities"][i]["card"]["description"])
        print("")   
        chose = input(Style.NORMAL + "Number of quiz? (Press enter for " + amount + " more) ")
        if chose == "":
            loop = True
            iLoop = 2
        else:
            loop = False

        while loop is True:
            searchResult = requests.get("https://create.kahoot.it/rest/kahoots/?query=" + search + "&limit=" + str(int(amount)*int(iLoop)) + "&orderBy=number_of_players", verify=True, timeout=10)
            time.sleep(1+(iLoop/10))
            searchResult = searchResult.content
            searchResult = json.loads(searchResult)
            for i in range(int(amount)*(iLoop-1)-1,len(searchResult["entities"])):
                if searchResult["entities"][i]["card"]["featured"] == "true" or searchResult["entities"][i]["card"]["young_featured"] == "true":
                    sys.stdout.write(Style.NORMAL + "#" + str(i+1) + " " + searchResult["entities"][i]["card"]["title"] + " (" + str(searchResult["entities"][i]["card"]["number_of_plays"]) + " plays) " + Fore.RED + "FEATURED!" + Fore.RESET)
                else: 
                    sys.stdout.write(Style.NORMAL + "#" + str(i+1) + " " + searchResult["entities"][i]["card"]["title"] + " (" + str(searchResult["entities"][i]["card"]["number_of_plays"]) + " plays)")
                    print("\n" + Style.DIM + searchResult["entities"][i]["card"]["description"])
                print("")   
            chose = input(Style.NORMAL + "Number of quiz? (Press enter for " + amount + " more) ")
            if chose == "":
                iLoop = iLoop+1
            else:
                loop = False
        chose = int(chose) - 1
        print(searchResult["entities"][chose]["card"]["uuid"])

    if mode == "sus":
        clear()
        print("ඞ")
        print(
        Fore.WHITE + Back.BLACK + """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀\n
        ⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀\n
        ⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀\n
        ⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀\n
        ⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀\n
        ⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀\n
        ⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀\n
        ⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀\n
        ⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀\n
        ⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀\n
        ⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀\n
        ⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""" + Fore.RESET + Back.RESET)
    exitprogram = False
    if mode == "QUIT":
        Active = False
        exitprogram = True
    while exitprogram is False:
        sys.stdout.write(Fore.RED + "Type 'EXIT' to exit: ")
        instr = input("")
        if instr == "EXIT":
            exitprogram = True
            clear()
