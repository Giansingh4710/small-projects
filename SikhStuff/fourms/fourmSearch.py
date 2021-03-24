import pyperclip, time, random,webbrowser


#This was originally for only gurmatbibekfourm but then added gurmatbibek articles, tapoban articles and SikhUnityWordPress articles


def all_fourms_links():
    topics=[]   
    d={}
    with open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibekfourm.txt",'r') as fl: #I took all the links from the fourms and put them into this file. To view 
        lines=fl.readlines()
        for line in lines:  #for the fourm
            try:
                line=line[3:]
                line=line.strip()
                lst=line.split(':')
                name=lst[0].strip().lower()
                title=lst[1][:-6].strip().lower()
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
    with open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibekArticles.txt",'r') as filee: #This is for the articles from GB and tapoban 
        TheLines=filee.readlines()
        for line in TheLines:
            line=line.split(" : ")
            topics.append(line[0].lower()) #the title
            topics.append(line[1][:-1]) #the link

    with open("C:\\Users\\gians\\Desktop\\stuff\\SikhUnityWordPress.txt","r") as filee: #This is from articles from UnityPress
        fl=filee.readlines()
        for line in fl:
            title=line.split(" $$$ ")[0]
            link=line.split(" $$$ ")[1][:-1] #gets link and remover \n
            topics.append(title.lower())
            topics.append(link)
    return topics,d

topics,d=all_fourms_links()

def main():
    topicsNnames=input("Enter a topic or name of a GurSikh: ")
    names=gursikh(topicsNnames) # names is dict with keys as names of gursikhs and values as a list of all titles and links under that name
    topics=topic(topicsNnames)# returns a list of titles and corresponding links that have the input in it.
    allOptions=[names,topics] 
    chosetitle(allOptions)  # pick the link you want
    while True:
        sametopics=input("Would you like to see the same list again ('Y' or 'N')?: ")
        if 'y' in sametopics.lower():
            chosetitle(allOptions)
        else:
            break  
    

def gursikh(theperson):
    options={}
    if theperson=="random" or theperson=="" or theperson==" ": 
        return options
    for name in d:  #d=  is the dictionary of name of people
        if theperson in name:
            options[name]=d[name]
    return options

def topic(topicc):
    allTopics=[topics[i] for i in range(len(topics)) if i%2==0] 
    if topicc=="random" or topicc=="" or topicc==" ":
        options=[]
        for i in range(10):
            num=random.randint(0,len(allTopics)-1)
            options.append(allTopics[num])
    else:
        options=[i for i in allTopics if topicc in i] #looks at all titles and select the one that include the topicc string      
    endlistwithlinks=[]
    for i in options:
        ind=topics.index(i)+1
        endlistwithlinks.append(i) #the topic
        endlistwithlinks.append(topics[ind]) # the link - the reason I am doing this is so the return is in the same format as gursikh() func
    return endlistwithlinks

def chosetitle(lst):
    names,titles=lst

    title=[titles[i] for i in range(len(titles)) if i%2==0]
    links=[titles[i] for i in range(len(titles)) if i%2==1]
    print("\nBy Topic:\n")
    for i in range(len(links)):
        print(f'{i+1}) {title[i]}')

    print("\nBy Name:\n")
    for i in range(len(names)):
        a=len(links)+i+1
        print(f'{a}) {list(names)[i]}')
    print("\n")
    try:
        num=int(input("Put the number corresponding to the topic or gursikh you are looking for: "))
        if num<=len(links):
            theLink=links[num-1]
        else:
            theName=list(names)[num-len(links)-1]  #you can't index a dict so made into a list and then index to get the name
            print(theName)
            titles=[names[theName][i] for i in range(len(names[theName])) if i%2==0]          
            links=[names[theName][i] for i in range(len(names[theName])) if i%2==1] 
            print("\nBy Topic:\n")
            for i in range(len(links)):
                print(f'{i+1}) {titles[i]}') 
            num=int(input("Put the number corresponding to the topic you are looking for: "))
            theLink=links[num-1]
    except Exception:
        print("Your input was invalid. :(")
        theLink=""
    openLink(theLink)

def openLink(link):
    if link=="":
        print("Not valid input")
        return
    whattodowithLink=input("Would you like to 'open', 'copy' or do 'nothing'? : ")
    if 'no' in whattodowithLink:
        print("OK. No Problem !")
    if 'cop' in whattodowithLink:
        pyperclip.copy(link)
    else:
        webbrowser.open(link)

if __name__=="__main__":
    while True:
        main()
        again=input("Try again?: ")
        if "n" in again.lower():
            break