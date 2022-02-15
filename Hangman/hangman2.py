


def man(thehang):
    mans={
        14:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','/','|','\\'],['|',' ',' ',' ','|'],['|',' ',' ','/',' ','\\']],
        13:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','/','|','\\'],['|',' ',' ',' ','|'],['|',' ',' ','/',' ','']],
        12:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','/','|','\\'],['|',' ',' ',' ','|'],['|',' ',' ','',' ','']],
        11:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','/','|','\\'],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        10:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ',' ','|','\\'],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        9:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','',' ','|'],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        8:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ','o'],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        7:[['______'],['|',' ',' ',' ','|'],['|',' ',' ',' ',''],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        6:[['______'],['|',' ',' ',' ',''],['|',' ',' ',' ',''],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        5:[[''],['|',' ',' ',' ',''],['|',' ',' ',' ',''],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        4:[[''],['',' ',' ',' ',''],['|',' ',' ',' ',''],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        3:[[''],['',' ',' ',' ',''],['',' ',' ',' ',''],['|',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        2:[[''],['',' ',' ',' ',''],['',' ',' ',' ',''],['',' ',' ','','',''],['|',' ',' ',' ',''],['|',' ',' ','',' ','']],
        1:[[''],['',' ',' ',' ',''],['',' ',' ',' ',''],['',' ',' ','','',''],[' ',' ',' ',' ',' '],['|',' ',' ',' ',' ',' ']],
        }
    for i in mans[thehang]:
        print(''.join(i))
def hangman(trys):
    from sys import argv
    if len(argv)>1:
        ans=' '.join(argv[1:])
        deff=None
    else:
        for i in range(3):
            typeorran=input('Would you like to type a word for your oppenent or get a random word from our dictionary?(type or ran) ')
            if typeorran.lower()=='type':
                ans=input('Type the word for your oppent: ')
                deff=None
                for i in range(90):
                    print('STOP LOOKING AT THE WORD!!!!!! vAHEGURURUUU')
                break
            elif typeorran.lower()=='ran' or typeorran.lower()=='rand':
                ans=ranword()[0]
                deff=ranword()[1]
                break
            else:
                if i==2:
                    print('Try again next time')
                    return 'BYEEEE!!!!!'
                print('Type again but properly this time please')
    wrong=[]
    dash=[]
    chacount=0
    constans=ans[:] #the answer will be changed so if the person guesses the full answer we need the full answer
    for i in ans:
        if i!=' ':
            chacount+=1
            dash.append('-')
        else:
            dash.append(' ')
    if trys<14:
        whichmans=[1]
        whichman=14//trys
        for i in range(trys-1):
    	    if i==trys-2:
    		    whichmans.append(14)
    	    elif (whichmans[-1]+ whichman)<14:
    		    whichmans.append(whichmans[-1]+ whichman)
    while True:
        print('\n\n\n')
        print(f'You have {trys} trys to guess. The word has {chacount} characters left to guess.')
        print(''.join(dash))
        if len(wrong)>0:
            print(f'Your wrong guesses: {wrong}')
        guess=input('please type your guess: ')
        if guess==constans:
            print('You WONNNNN. Tooo GOOD. Mahraj kirpa. Gurprasade')
            if deff!=None:
                print(f'{constans}: {deff}')
            return
        if guess=='fail':
            print(f'the word was {constans}.')
            if deff!=None:
                print(f'{constans}: {deff}')
            return
        if len(guess)>1:
            if guess in ans:
                print('Good guess.')
                for i in guess:
                    ind=ans.index(i)
                    ans=ans.replace(i,'-',1)
                    del dash[ind]
                    dash.insert(ind,i)
                    chacount-=1
                if ''.join(dash)==constans:
                    print('You WINNN!! Gurprasade')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return
            elif guess in constans:
                print('You have already tried this. Be careful because your losing trys')
                trys-=1
                try:
                    thehang=whichmans.pop(0)
                    man(thehang)
                except:
                    print('haha')
                if trys==0:
                    man(14)
                    print(f'You LOSE!:(. The word was {constans}')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return
            else:
                trys-=1
                wrong.append(guess)
                print('Wrong guess.')
                try:
                    thehang=whichmans.pop(0)
                    man(thehang)
                except:
                    print('Haha')
                if trys==0:
                    man(14)
                    print(f'You LOSE!:(. The word was {constans}')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return
        else:
            if guess in ans or guess.upper() in ans:
                print('Good guess.')
                anscount=ans.count(guess)
                for i in range(anscount):
                    ind=ans.index(guess)
                    ans=ans.replace(guess,'-',1)
                    del dash[ind]
                    dash.insert(ind,guess)
                    chacount-=1
                anscounts=ans.count(guess.upper())
                for i in range(anscounts):
                    ind=ans.index(guess.upper())
                    ans=ans.replace(guess.upper(),'-',1)
                    del dash[ind]
                    dash.insert(ind,guess.upper())
                    chacount-=1
                if ''.join(dash)==constans:
                    print('You WINNN!! Gurprasade')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return
            elif guess in constans:
                print('You have already tried this. Be careful because your losing trys')
                trys-=1
                try:
                    thehang=whichmans.pop(0)
                    man(thehang)
                except:
                    print('HaHa')
                if trys==0:
                    man(14)
                    print(f'You LOSE!:(. The word was {constans}')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return
            else:
                trys-=1
                wrong.append(guess)
                print('Wrong guess.')
                try:
                    thehang=whichmans.pop(0)
                    man(thehang)
                except:
                    print('haHa')
                if trys==0:
                    man(14)
                    print(f'You LOSE!:(. The word was {constans}')
                    if deff!=None:
                        print(f'{constans}: {deff}')
                    return

def ranword():
    import random
    from random import randint
    randnum=randint(0,87)     
    a=[i for i in dictt]
    randwords={}
    keysindict=[]
    for i in range(len(a)):
        if i%2==0:
            randwords[a[i][:-1]]=a[i+1][:-1]
            keysindict.append(a[i][:-1])
    return [keysindict[randnum],randwords[keysindict[randnum]]]



ditt='''grenadine
thin syrup made from pomegranate juice; used in mixed drinks
pomegranate
shrub or small tree having large red many-seeded fruit
hefty
of considerable weight and size
gladiolus
any of numerous plants of the genus Gladiolus native chiefly to tropical and South Africa having sword-shaped leaves and one-sided spikes of brightly colored funnel-shaped flowers; widely cultivated
pelter
a thrower of missiles
concretize
make something concrete
manikin
a life-size dummy used to display clothes
canvass
get opinions by asking specific questions
lubberly
clumsy and unskilled
cordial
politely warm and friendly
jocular
characterized by jokes and good humor
Utopian
of or pertaining to or resembling a utopia
tamp
press down tightly
subnormality
the state of being less than normal
obbligato
a part of the score that must be performed without change or omission
woodsy
characteristic or suggestive of woods
ha-ha
a loud laugh that sounds like a horse neighing
stevedore
a laborer who loads and unloads vessels in a port
effervescence
the process of bubbling as gas escapes
bromidic
given to uttering bromides
canoodle
fondle or pet affectionately
satrap
a governor of a province in ancient Persia
congeries
a sum total of many heterogenous things taken together
twain
two items of the same kind
kittiwake
small pearl-grey gull of northern regions
polysemy
the ambiguity of an individual word or phrase that can be used (in different contexts) to express two or more different meanings
madrigal
an unaccompanied partsong for several voices
bollard
a strong post
parvenu
a person who has suddenly risen to a higher economic status
bowdlerize
edit by omitting or modifying parts considered indelicate
mountebank
a flamboyant deceiver
hauteur
overbearing pride with a superior manner toward inferiors
asphodel
any of various chiefly Mediterranean plants of the genera Asphodeline and Asphodelus having linear leaves and racemes of white or pink or yellow flowers
annulment
an official or legal cancellation
quasi
having some resemblance
Yugoslavia
a former country of southeastern Europe bordering the Adriatic Sea; formed in 1918 and named Yugoslavia in 1929; controlled by Marshal Tito as a communist state until his death in 1980
paleobotany
the study of fossil plants
cephalopodan
relating or belonging to the class Cephalopoda
Serbian
of or relating to the people or language or culture of the region of Serbia
tribunal
an assembly to conduct judicial business
ague
chills and fever that are symptomatic of malaria
Netherlands
a constitutional monarchy in western Europe on the North Sea
Bosnian
of or relating to or characteristic of Bosnia-Herzegovina or the people of Bosnia
Albanian
of or relating to Albania or its people or language or culture
Kosovo
a republic in the Balkan Peninsula that declared independence from Serbia in 2008; populated predominantly by Albanians
Chile
a republic in southern South America on the western slopes of the Andes on the south Pacific coast
humiliating
causing embarrassment or awareness of your shortcomings
Suharto
Indonesian statesman who seized power from Sukarno in 1967
contemplate
think intently and at length, as for spiritual purposes
Peruvian
of or relating to or characteristic of Peru or its people
oust
remove from a position or office
Saddam Hussein
Iraqi leader who waged war against Iran
subsequently
happening at a time later than another time
massacre
the savage and excessive killing of many people
civilian
a nonmilitary citizen
revolt
rise up against an authority
fascist
an adherent of right-wing authoritarian views
revered
profoundly honored
regime
the governing authority of a political unit
Mandela
South African statesman who was released from prison to become the nation's first democratically elected president in 1994 (born in 1918)
triumphantly
in a triumphant manner
Pretoria
city in the Transvaal
culminate
end, especially to reach a final or climactic stage
assassinated
murdered by surprise attack for political reasons
Ferdinand I
king of Castile and Leon who achieved control of the Moorish kings of Saragossa and Seville and Toledo (1016-1065)
Suharto
Indonesian statesman who seized power from Sukarno in 1967
Burmese
of or relating to or characteristic of Myanmar or its people
Beijing
capital of the People's Republic of China in the Hebei province in northeastern China; 2nd largest Chinese city
Kyrgyzstan
a landlocked republic in west central Asia bordering on northwestern China; formerly an Asian soviet but became independent in 1991
Venezuela
a republic in northern South America on the Caribbean
charismatic
possessing an extraordinary ability to attract
daw
common black-and-grey Eurasian bird noted for thievery
upsurge
a sudden or abrupt strong increase
suffrage
a legal right to vote
minimal
the least possible
insurgency
an organized rebellion aimed at overthrowing a government
Sri Lanka
a republic on the island of Ceylon
torture
infliction of suffering to punish or obtain information
Guatemala
a republic in Central America
Bangladesh
a Muslim republic in southern Asia bordered by India to the north and west and east and the Bay of Bengal to the south; formerly part of India and then part of Pakistan; it achieved independence in 1971
manipulate
influence or control shrewdly or deviously
Bolivia
a landlocked republic in central South America
stringent
demanding strict attention to rules and procedures
vulnerable
capable of being wounded or hurt
prod
push against gently
famine
a severe shortage of food resulting in starvation and death
eradicate
destroy completely, as if down to the roots'''
dictt=ditt.splitlines()

def play():
    for i in range(3):
        try:
            x=int(input('How many trys would you like in your hangman game:'))
            break
        except:
            print('Please type a number')
    hangman(x)
counter=0
while True:
    print(f'You what played {counter} times.')
    ask=input('would you like to play(Y or N)?:'  )
    if ask.lower()=='y' or 'ye' in ask.lower():
        counter+=1
        play()
    else:
        print('Bye!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        break
