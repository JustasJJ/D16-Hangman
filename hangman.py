import getpass
import random


def main():
    # w - word to guess.
    def get_input_word():
        while True:
            w = getpass.getpass("Enter a word to guess: ").lower()
            if w.isalpha():
                if w == "quit":
                    quit = input("Do you want to quit? Y/N : ").lower()
                    if quit == "y":
                        return 1
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
                        return 1
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
                        return 1
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
        p = []
        for i in range(0, len(w)):
            p.append(" _ ")
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
            print('3. Guess a riddle\n4. Quit game\n')
            play_mode = 0
            while play_mode not in ["1", "2", "3", "4"]:
                play_mode = input('Please select your option (1, 2, 3 or 4): ')
                if play_mode not in ["1", "2", "3", "4"]:
                    print("Incorrect! Try again.")
            if play_mode == "1":
                guess_word()
            elif play_mode == "2":
                guess_random_word()
            elif play_mode == "3":
                guess_riddle()
            elif play_mode == "4":
                print("Goodbye!")
                return

    def guess_word():
        w = get_input_word()
        if w == 1:
            print("See you next time.")
            return
        d = get_difficulty()
        if d == 1:
            print("See you next time.")
            return
        check_guesses(w, d)
        return

    def guess_riddle():
        d = get_difficulty()
        if d == 1:
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
        if d == 1:
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
        print("\n"+s+"\n")
        while c < d:
            draw_gallows(d-c)
            g = get_guess()
            if g == 1:
                print("See you next time.")
                break
            if g in answer:
                f = answer.find(g)
                while f >= 0:
                    p[f] = " " + g.upper() + " "
                    f = answer.find(g, f + 1)
                print("\n\n"+g.upper(), "is in a word!\t", end="")
                print("Number of wrong answers left:", d-c)
                s = puzzle_to_string(p)
                print("\n"+s+"\n")
                if "_" in s:
                    pass
                else:
                    print("Congratulations! You won!")
                    break
            else:
                c += 1
                print("\n\n"+g.upper(), "is missing...\t", end="")
                print("Number of wrong guesses left:", d-c)
                if d-c == 0:
                    draw_gallows(d-c)
                    print("Game over. Correct answer was:", end="")
                    print(puzzle_to_string(l_ans).upper())
                else:
                    print("\n" + puzzle_to_string(p) + "\n")
        input("(Press any key to continue.)")
        return

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

    menu()
    input('(Press any key to exit.)')


main()
