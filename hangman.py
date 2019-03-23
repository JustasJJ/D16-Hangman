import getpass
import random

def main():
 # w - word to guess.
  def get_w():
    while True:
      w=getpass.getpass("Enter a word to guess: ").lower()
      if w.isalpha():
       if w=="quit":
         quit=input("Do you want to quit? Y/N : ").lower()
         if quit=="y":
            return 1
            #print("See you next time.")
            #break
         else:
           print("Let's continue.")          
       else:
          return w
      else:
       print("Please, use only letters.")

 # g - your guess, a letter.
  def get_g():
    while True:
      g=input("Guess a letter: ").lower()
      if g.isalpha():
        if g=="quit":
          quit=input("Do you want to quit? Y/N : ").lower()
          if quit=="y":
            return 1
            #print("See you next time.")
            #break
          else:
            print("Let's continue.")
        elif len(g)==1:
          return g
        else:
          print("Please, use only one letters.")
      else:
        print("Please, use only one letters.")
      
 # d - difficulty, the number of wrong guesses. 
  def get_d():
    while True:
      d=input("Select a difficulty. Enter a number of wrong guesses: ")
      if d=="":
        print("Default dificulty is 7 wrong guesses.")
        return 7
      elif d.isalpha():
        if d=="quit":
          quit=input("Do you want to quit? Y/N : ").lower()
          if quit=="y":
            return 1
            #print("See you next time.")
            #break
          else:
            print("Let's continue.")
        else:
          print("Please, enter a whole number greater than 0.")
      elif d.isdigit():
        if int(d)>0:
          return int(d)
        else:
          print("Please, enter a whole number greater than 0.")
      else:
        print("Please, enter a whole number greater than 0.")
  
  def eng():
    l=[]
    for i in range(97,123):
      l.append(chr(i))
    return l

  def wtl(w):
    p=[]
    for i in range(0,len(w)):
      p.append(w[i])
    return p

  def wtp(w):
    p=[]
    for i in range(0,len(w)):
      p.append(" _ ")
    return p

  def pts(p):
    s=""
    for i in range(0,len(p)):
      s+=p[i]
    return s

  def menu():
    print('\n*********HANGMAN GAME D16**********\n')
    print('MENU:\n1. Guess a word\n2. Guess a riddle\n3. Quit game\n')
    play_mode=0
    while play_mode not in ["1","2","3"]:
     play_mode=input('Please select your option (1,2 or 3): ')
     if play_mode not in ["1","2","3"]:
       print("Incorrect! Try again.")

    if play_mode == "1":
      guess_word()
    elif play_mode == "2":
      guess_riddle()
    elif play_mode=="3":
      print("Goodbye!")
      return

  def guess_word():
    w=get_w()
    if w==1:
      print("See you next time.")
      return
  
    l=wtl(w)
    p=wtp(w)
    s=pts(p)
    d=get_d()
    if d ==1:
      print("See you next time.")
      return  
    c=0

    # print("l",l)
    # print("p",p)
    # print("s",s)

    print("\n"+s+"\n")

    while c<d:
      g=get_g()
      if g==1:
        print("See you next time.")
        break
      if g in w:
        f=w.find(g)
        while f>=0:
          p[f]=" "+g.upper()+" "
          f=w.find(g,f+1)
        print("\n\n"+g.upper(),"is in a word!\tNumber of wrong answers left:",d-c)
        s=pts(p)
        print("\n"+s+"\n")
        if "_" in s:
          pass
        else:
          print("Congratulations! You won!")
          break
      else:
        c+=1
        print("\n\n"+g.upper(),"is missing...\tNumber of wrong guesses left:",d-c)
        if d-c==0:
          print("Game over. Correct answer was:",pts(l).upper())
        else:
          print("\n"+pts(p)+"\n")
  
  def guess_riddle():
    category=""
    while category not in ["daiktai","gamta","gyvunai"]:
     category=input('Select category (daiktai, gamta, gyvunai): ').lower()
     if category not in ["daiktai","gamta","gyvunai"]:
       print("Incorrect! Try again.")
    d={}
    f=open("riddles.txt","r")
    for line in f:
      if line.strip() == '*'+category+'*':  # start reading file
          break
    for line in f:
      if "*" not in line and len(line)>3: #populates dictionary with riddles
        (key, val) = line.split("?")
        d[key+"?"] = val[1:-1]
      else:
        break   #ends reading file
    f.close()
    riddle=random.choice(list(d.keys())) #selects random riddle

    w=d[riddle]
    l=wtl(w)
    p=wtp(w)
    s=pts(p)
    d=get_d()
    if d ==1:
      print("See you next time.")
      return  
    c=0
    print(riddle[:-1]+". Kas?")
    print("\n"+s+"\n")
    while c<d:
      g=get_g()
      if g==1:
        print("See you next time.")
        break
      if g in w:
        f=w.find(g)
        while f>=0:
          p[f]=" "+g.upper()+" "
          f=w.find(g,f+1)
        print("\n\n"+g.upper(),"is in a word!\tNumber of wrong answers left:",d-c)
        s=pts(p)
        print("\n"+s+"\n")
        if "_" in s:
          pass
        else:
          print("Congratulations! You won!")
          break
      else:
        c+=1
        print("\n\n"+g.upper(),"is missing...\tNumber of wrong guesses left:",d-c)
        if d-c==0:
          print("Game over. Correct answer was:",pts(l).upper())
        else:
          print("\n"+pts(p)+"\n")
    return

  menu()
  input('(Press any key to exit.)')
main()