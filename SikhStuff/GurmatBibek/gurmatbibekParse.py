import pyperclip
from selenium import webdriver
with open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibek.txt",'r') as fl: #I took all the links from the fourms and put them into this file. To view 
    lines=fl.readlines()
d={}
topics=[]
for line in lines:
    try:
        line=line[3:]
        line=line.strip()
        lst=line.split(':')
        name=lst[0].strip().lower()
        title=lst[1][:-6].strip()
        link="http:"+lst[2]
        topics.append(title)
        topics.append(link)
        if name not in d:
            d[name]=[title,link]
        else:
            d[name].append(title)
            d[name].append(link)
    except IndexError:
        continue

def askTopicsorNames():
    while True:
        topicsOrNames=input("Do you want to specify by gursikh name or by topics?: ")
        if "gur" in topicsOrNames.lower() or "nam" in topicsOrNames.lower():
            gursikkh=gursikh()
            if gursikkh in d:
                titles=d[gursikkh]
            elif gursikkh.lower()=="y":
                continue
            elif gursikkh.lower()=="n":
                break
        else:
            topicc=topic()
            if len(topicc)>1:
                titles=topicc
            elif topicc.lower()=="y":
                continue
            elif topicc.lower()=="n":
                break
        chosetitle(titles)
        while True:
            sametopics=input("Would you like to see the topic list again?: ('Y' or 'N') ")
            if 'y' in sametopics.lower():
                chosetitle(titles)
            else:
                break
        again=input("Would you like to try again? ")
        if 'y' in again:
            continue
        else:
            return "Bye!! Vaheguru JIO"

def gursikh():
    theperson=input("What is the name of the Gursikh?: ")
    num=0
    options=[]
    for name in d:
        if theperson in name:
            num+=1
            print(f'{num}) {name}')
            options.append(name)
    if len(options)==0:
        print("You input was invalid.")
        again=input('Would you like to try again? ("Y" or "N"): ')
        return again
    num=int(input("Put the number corresponding to the person you are looking for: "))
    name= options[num-1]
    return name

def topic():
    topicc=input("What is the name of the topic?: ")
    allTopics=[topics[i] for i in range(len(topics)) if i%2==0]
    options=[i for i in allTopics if topicc in i] #looks at all titles and select the one that include the topicc string
    if len(options)==0:
        print("You input was invalid.")
        again=input('Would you like to try again? ("Y" or "N"): ')
        return again       
    endlistwithlinks=[]
    for i in options:
        ind=topics.index(i)+1
        endlistwithlinks.append(i) #the topic
        endlistwithlinks.append(topics[ind]) # the link  the reason I am doing this is so the return is in the same format as gursikh() func
    return endlistwithlinks

def chosetitle(titles):
    title=[titles[i] for i in range(len(titles)) if i%2==0]
    links=[titles[i] for i in range(len(titles)) if i%2==1]
    for i in range(len(links)):
        print(f'{i+1}) {title[i]}')
    num=int(input("Put the number corresponding to the topic you are looking for: "))
    whattodowithLink=input("Would you like to 'open', 'copy' or do 'nothing'? : ")
    if 'no' in whattodowithLink:
        return None
    if 'cop' in whattodowithLink:
        pyperclip.copy(links[num-1])
    else:
        br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
        br.get(links[num-1])

askTopicsorNames()