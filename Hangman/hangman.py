import sys
import random
wro=[]
def hangman(outfile,trys=9):
     if len(sys.argv)>1:
          ans=' '.join(sys.argv[1:])
     else:
          try:
               an=open('C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\Hangman\\inn.txt')
               file=an.readlines()
               rand=random.randrange(0,len(file)-1,2)
               ans=file[rand]
          except:
               ans=input('infile not working.Please Input a word: ')
               for i in range(100):
                         print('STOP LOOKING AT THE WORD')
     chacount=0
     a=0
     let=0
     chaa=[]
     dash=[]
     for cha in ans:
          chacount+=1
          chaa.append(cha)
          if cha!=' ':
               dash.append('-')
          else:
               dash.append(' ')
     print("there are"+' '+ str(chacount)+ ' characters in the answer. Guess the letters in the answer to win. {} wrong guesses and you lose'.format(trys))
     print(str(''.join(dash)))
     
     while True:
          guess=input("Guess a letter: ")
          if guess== ans:
               print("You WIN. Your answer was correct")
               break
          elif guess=='':
               print('Please put a real value')
          elif guess=='fail':
                print('The word was: {}'.format(ans))
                return
          elif len(guess)>1:
               if guess in ans:
                    let+=1
                    for i in guess:
                         ind=chaa.index(i)
                         del chaa[ind]
                         chaa.insert(ind,'-')
                         del dash[ind]
                         dash.insert(ind,i)
               else:
                    guesslen=0
                    for i in guess:
                         if i in ans:
                              guesslen+=1
                              try:
                                   ind=chaa.index(i)
                                   del chaa[ind]
                                   chaa.insert(ind,'-')
                                   del dash[ind]
                                   dash.insert(ind,i)
                              except:
                                   print(f'Guess {i} already made.')
                                   break
                         else:
                              a+=1
               if len(guess)==guesslen:
                    print(str(''.join(dash)))
                    print('good Job')
               else:
                    if wrongmove(a,guess,trys,ans)==9:
                         break
               if '-' not in dash:
                    print("YOU WINNNNNNNN!!!!!!!!!!LET's GOOOOOOOOO")
                    return
          elif (guess in ans) or (guess.upper() in ans):
               let+=1
               if (chaa.count(guess)==0) and (chaa.count(guess.upper())==0):
                    print("You already tried this. Can't you see fool")
                    continue
               for i in range(chaa.count(guess)):
                    ind=chaa.index(guess)
                    del chaa[ind]
                    chaa.insert(ind,'-')
                    del dash[ind]
                    dash.insert(ind,guess)
               for i in range(chaa.count(guess.upper())):
                    ind=chaa.index(guess.upper())
                    del chaa[ind]
                    chaa.insert(ind,'-')
                    del dash[ind]
                    dash.insert(ind,guess.upper())     
               if '-' not in dash:
                    print("YOU WINNNNNNNN!!!!!!!!!!LET's GOOOOOOOOO")
                    return
               print('Good Job, Keep going.'+' '+ str(let)+ ' correct guesses.')
               print(str(''.join(dash)))
          else:
               a+=1
               wrongmove(a,guess,trys,ans)

     try:          
          an.close()
     except:
          print('BYE!!!!')

def wrongmove(a,guess,trys,ans):
     wro.append(guess)
     print('Try Again.'+' '+ str(a)+ ' wrong guesses made. Wrong Guesses- '+ str(wro))
     if trys!=9:
          if a>=trys:
               print('YOU LOSE. Better luck next time. The word was ' + ' '+ str(ans))
               return 9
     else:
          import turtle
          t=turtle.Turtle()
          if a==1:
               t.fd(25)
          if a==2:
               t.penup()
               t.goto(25,0)
               t.pendown()
               t.lt(90)
               t.fd(100)
          if a==3:
               t.penup()
               t.goto(25,100)
               t.pendown()
               t.fd(25)
          if a==4:
               t.penup()
               t.goto(50,50)
               t.pendown()
               t.circle(25)
          if a==5:
               t.penup()
               t.goto(50,100)
               t.pendown()
               t.rt(90)
               t.penup()
               t.fd(50)
               t.pendown()
               t.fd(90)
          if a==6:
               t.penup()
               t.goto(50,10)
               t.pendown()
               t.rt(45)
               t.fd(50)
          if a==7:
               t.penup()
               t.goto(50,10)
               t.pendown()
               t.rt(135)
               t.fd(50)
          if a==8:
               t.penup()
               t.goto(50,-40)
               t.pendown()
               t.rt(45)
               t.fd(60)
          if a==9:
               t.penup()
               t.goto(50,-40)
               t.pendown()
               t.rt(135)
               t.fd(60)
               print('YOU LOSE. Better luck next time. The word was ' + ' '+ str(ans))
               return 9
hangman('inn.txt',4)
