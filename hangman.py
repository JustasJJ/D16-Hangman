import getpass
import random
import datetime


class Player:
    def __init__(self, name):
        self.name = name
        self.g = 0  # games
        self.w = 0  # wins
        self.d = 0  # draws
        self.losses = 0  # losses

    def stats_change(self, wins, draws, losses):
        self.g += 1
        self.w += wins
        self.d += draws
        self.losses += losses


def main():
    # w - word to guess.
    def get_input_word():
        while True:
            w = getpass.getpass("Enter a word to guess: ").lower()
            if w.isalpha():
                if w == "quit":
                    quit = input("Do you want to quit? Y/N : ").lower()
                    if quit == "y":
                        return -1
                    else:
                        print("Let's continue.")
                else:
                    return w
            else:
                print("Please, use only letters.")

    # g - your guess, a letter.
    def get_guess():
        while True:
            g = input("Guess a letter: ").lower()
            if g.isalpha():
                if g == "quit":
                    quit = input("Do you want to quit? Y/N : ").lower()
                    if quit == "y":
                        return -1
                    else:
                        print("Let's continue.")
                elif len(g) == 1:
                    return g
                else:
                    print("Please, use only one letter.")
            else:
                print("Please, use only one letter.")

    # d - difficulty, the number of wrong guesses.
    def get_difficulty():
        while True:
            d = input("Select a difficulty. Enter a number of wrong guesses: ")
            if d == "":
                print("Default dificulty is 7 wrong guesses.")
                return 7
            elif d.isalpha():
                if d == "quit":
                    quit = input("Do you want to quit? Y/N : ").lower()
                    if quit == "y":
                        return -1
                    else:
                        print("Let's continue.")
                else:
                    print("Please, enter a whole number greater than 0.")
            elif d.isdigit():
                if int(d) > 0:
                    return int(d)
                else:
                    print("Please, enter a whole number greater than 0.")
            else:
                print("Please, enter a whole number greater than 0.")

    def word_to_list(w):  # "wheel" ---> "[w, h, e, e, l]"
        p = []
        for i in range(0, len(w)):
            p.append(w[i])
        return p

    def word_to_puzzle(w):  # "wheel" ---> "[" _ "," _ "," _ "," _ "," _ "]"
        p = [" _ "]*len(w)
        return p

    def puzzle_to_string(p):  # "[w, " _ ", " _ ", e, l]" --> " w  _  _  e  l "
        s = ""
        for i in range(0, len(p)):
            s += p[i]
        return s

    def menu():
        while True:
            print('\n*********HANGMAN GAME D16**********\n')
            print('MENU:\n1. Guess input word\n2. Guess random word')
            print('3. Guess a riddle\n4. Multiplayer: Classic Mode')
            print('5. Leaderboard\n6. Quit game\n')
            play_mode = 0
            while play_mode not in ["1", "2", "3", "4", "5", "6"]:
                play_mode = input('Please select your option (1 to 6): ')
                if play_mode not in ["1", "2", "3", "4", "5", "6"]:
                    print("Incorrect! Try again.")
            if play_mode == "1":
                guess_word()
            elif play_mode == "2":
                guess_random_word()
            elif play_mode == "3":
                guess_riddle()
            elif play_mode == "4":
                multiplayer_classic_mode()
            elif play_mode == "5":
                leaderboard()
            elif play_mode == "6":
                print("Goodbye!")
                return

    def guess_word():
        w = get_input_word()
        if w == -1:
            print("See you next time.")
            return
        d = get_difficulty()
        if d == -1:
            print("See you next time.")
            return
        check_guesses(w, d)
        return

    def guess_riddle():
        d = get_difficulty()
        if d == -1:
            print("See you next time.")
            return
        ctg = ""
        while ctg not in ["items", "nature", "animals"]:
            ctg = input('Select category (items, nature, animals): ').lower()
            if ctg not in ["items", "nature", "animals"]:
                print("Incorrect! Try again.")
        dct = {}
        f = open("riddles.txt", "r")
        for line in f:
            if line.strip() == '*' + ctg + '*':  # start reading file
                break
        for line in f:
            if "*" not in line and len(line) > 3:  # populate dict with riddles
                (key, val) = line.split("?")
                dct[key+"?"] = val[1:-1]
            else:
                break   # ends reading file
        f.close()
        riddle = random.choice(list(dct.keys()))  # select random riddle
        print(riddle[:-1] + ". Kas?")
        check_guesses(dct[riddle], d)
        return

    def guess_random_word():
        d = get_difficulty()
        if d == -1:
            print("See you next time.")
            return
        words = [line.rstrip().lower() for line in open("words.txt")]
        word = random.choice(words)
        check_guesses(word, d)
        return

    def check_guesses(answer, d):
        l_ans = word_to_list(answer)  # list containing answer split to chars
        p = word_to_puzzle(answer)
        s = puzzle_to_string(p)
        c = 0
        h = []  # histroy of guesses as a list
        hst = "none"  # history of guesses as a string
        print("\n"+s+"\n")
        while c < d:
            draw_gallows(d-c)
            g = get_guess()
            if g == -1:
                print("See you next time.")
                break
            elif g in h:
                print("\n"+g.upper(), "is already guessed. ", end="")
                print("Try other letter.")
                print("Number of wrong answers left:", d-c)
                print("Already guessed letters:", hst+".")
                print("\n"+s+"\n")
            else:
                h.append(g)
                hst = ", ".join(h).upper()
                if g in answer:
                    f = answer.find(g)
                    while f >= 0:
                        p[f] = " " + g.upper() + " "
                        f = answer.find(g, f + 1)
                    print("\n\n"+g.upper(), "is in a word!")
                    print("Number of wrong answers left:", d-c)
                    print("Already guessed letters:", hst+".")
                    s = puzzle_to_string(p)
                    print("\n"+s+"\n")
                    if "_" in s:
                        pass
                    else:
                        draw_gallows(d-c)
                        print("Congratulations! You won! ", end="")
                        break
                else:
                    c += 1
                    print("\n\n"+g.upper(), "is missing...")
                    print("Number of wrong guesses left:", d-c)
                    print("Already guessed letters:", hst+".")
                    if d-c == 0:
                        print("\n"+s+"\n")
                        draw_gallows(d-c)
                        print("Game over. Correct answer was: ", end="")
                        print(puzzle_to_string(l_ans).upper()+" ", end="")
                    else:
                        print("\n" + puzzle_to_string(p) + "\n")
        input("(Press any key to continue.)")
        return d-c

    def draw_gallows(d):
        a = "   "+"_"*8+"\n    |/   |\n    |   (_)\n"
        b = "    |   /|\\\n    |    |\n    |   / \\\n"
        c = "    |\n    |___\n"
        gallows = a+b+c
        if d > 7 or d < 0:  # max difficulty is 7.
            d = 7
        hide_list = [[21], [31, 32, 33], [44, 56], [43], [45], [66], [68]]
        for i in range(d):
            for j in hide_list[::-1][i]:
                gallows = gallows[:j]+" "+gallows[j+1:]
        print(gallows)

    def enter_player_name(player_number):
        user = ""
        while user == "":
            if player_number == 1:
                user = input("Enter first player name: ").title()
            else:
                user = input("Enter second player name: ").title()
        return user

    def multiplayer_classic_mode():
        player_1 = enter_player_name(1)
        player_2 = enter_player_name(2)
        p1 = Player(player_1)
        p2 = Player(player_2)
        d = get_difficulty()
        while True:
            rounds = input('Please select game rounds (1, 2, 3): ')
            if rounds not in ["1", "2", "3"]:
                print("Incorrect! Try again.")
            else:
                break
        tab = (int(len(player_1)) + int(len(player_2)) + 6) // 2 * "*"
        tab2 = (int(len(player_1)) + int(len(player_2))) // 2 * "*"
        while True:
            players_points = {player_1: 0, player_2: 0}
            for round in range(1, int(rounds)+1):
                for key in players_points:
                    print(tab, "ROUND:", round, tab)
                    print(tab, "RESULTS ", tab)
                    print(player_1, "   ", players_points[player_1], end="")
                    print(":", players_points[player_2], "   ", player_2)
                    print("\nPlayer", key, "Turn")
                    words = []
                    for line in open("words.txt"):
                        words.append(line.rstrip().lower())
                    word = random.choice(words)
                    answer = check_guesses(word, d)
                    if answer != 0:
                        players_points[key] = players_points[key] + 1
                    else:
                        continue
            print(tab, "ROUND:", round, tab)
            print(tab2, "FINAL RESULTS ", tab2)
            print(player_1, "   ", players_points[player_1], end="")
            print(":", players_points[player_2], "   ", player_2, "\n")

            if players_points[player_1] > players_points[player_2]:
                p1.stats_change(1, 0, 0)
                p2.stats_change(0, 0, 1)
                print("Player", player_1, "Wins!")
            elif players_points[player_1] < players_points[player_2]:
                p1.stats_change(0, 0, 1)
                p2.stats_change(1, 0, 0)
                print("Player", player_2, "Wins!")
            else:
                p1.stats_change(0, 1, 0)
                p2.stats_change(0, 1, 0)
                print("It's a draw!")
            print("\nGAMES RESULTS")
            print("Players   \tGames\tWins\tDraws\tLosses")
            print(p1.name, "\t", p1.g, "\t", p1.w, "\t", p1.d, "\t", p1.losses)
            print(p2.name, "\t", p2.g, "\t", p2.w, "\t", p2.d, "\t", p2.losses)
            repeat = input('\nPlay again? Y/N: ').lower()
            if repeat == "y":
                print("Let's play!")
            else:
                f = open('players.txt', 'a')
                print(datetime.datetime.now(), ",", p1.name, ",", p1.g,
                      ",", p1.w, ",", p1.d, ",", p1.losses, ",",
                      p2.name, file=f
                      )
                print(datetime.datetime.now(), ",", p2.name, ",", p2.g,
                      ",", p2.w, ",", p2.d, ",", p2.losses, ",",
                      p1.name, file=f
                      )
                f.close()
                break
        return

    def leaderboard():
        f = open("players.txt", "r")
        ls = []  # list of list from file
        players = []
        for line in f:
            ls.append(line.strip().split(" , "))
        f.close()
        for l in range(len(ls)):
            players.append(ls[l][1])
        players_set = set(players)
        leaderboar_list = []
        for p in players_set:
            player_list = [p, 0, 0, 0, 0]
            for l in range(len(ls)):
                if ls[l][1] == p:
                    player_list[1] += int(ls[l][2])  # games
                    player_list[2] += int(ls[l][3])  # wins
                    player_list[3] += int(ls[l][4])  # draws
                    player_list[4] += int(ls[l][5])  # losses
                else:
                    continue
            leaderboar_list.append(player_list)
        leaderboar_list.sort(key=lambda x: x[2], reverse=True)
        ll = leaderboar_list
        print("\nLEADERBOARD")
        print("\nNo\t Player    \tGames\tWins\tDraws\tLosses")
        for l in range(len(ll)):
            print(l+1, "\t", ll[l][0], "\t", ll[l][1], "\t", end="")
            print(ll[l][2], "\t", ll[l][3], "\t", ll[l][4])
        return

    menu()
    input('(Press any key to exit.)')


main()
