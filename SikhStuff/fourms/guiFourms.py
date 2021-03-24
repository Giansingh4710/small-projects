from tkinter.constants import CENTER, LEFT
import pyperclip, time, random,webbrowser
import tkinter as tk
from tkinter import font



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

def main(aTopicOrName):
    if aTopicOrName.strip(" ")=="":
        print("Nothing entered!!")
        label["text"]="Nothing entered!!"
        return
    else:
        topicsNnames=aTopicOrName
    names=gursikh(topicsNnames) # names is dict with keys as names of gursikhs and values as a list of all titles and links under that name
    topics=topic(topicsNnames)# returns a list of titles and corresponding links that have the input in it.
    allOptions=[names,topics] 
    if chosetitleOrPerson(allOptions)=="exit": 
        label["text"]="No articles under that input :("
        return
    label["text"]="" #to clear the
    for i in chosetitleOrPerson(allOptions):
        label["text"]+=i+'\n' 
    

def gursikh(theperson):
    options={}
    if theperson=="random" or theperson=="" or theperson==" ": 
        return options
    for name in d:  #d=  is the dictionary of name of people
        if theperson.lower() in name.lower():
            options[name]=d[name]
    return options

def topic(topicc):
    allTopics=[topics[i] for i in range(len(topics)) if i%2==0] 
    if topicc.lower()=="random" or topicc=="" or topicc==" ":
        options=[]
        for i in range(10):
            num=random.randint(0,len(allTopics)-1)
            options.append(allTopics[num])
    else:
        options=[i for i in allTopics if topicc.lower() in i.lower()] #looks at all titles and select the one that include the topicc string      
    endlistwithlinks=[]
    for i in options:
        ind=topics.index(i)+1
        endlistwithlinks.append(i) #the topic
        endlistwithlinks.append(topics[ind]) # the link - the reason I am doing this is so the return is in the same format as gursikh() func
    return endlistwithlinks

def chosetitleOrPerson(lst):
    names,titles=lst
    title=[titles[i] for i in range(len(titles)) if i%2==0]
    links=[titles[i] for i in range(len(titles)) if i%2==1]
    global forGui

    forGui=[]
    forGui.append("\nBy Topic:\n")
    for i in range(len(links)):
        forGui.append(f'{i+1}) {title[i]}')

    forGui.append("\nBy Name:\n")
    for i in range(len(names)):
        a=len(links)+i+1
        forGui.append(f'{a}) {list(names)[i]}')

    if len(forGui)==2: return "exit"
    return forGui
    try:
        for i in forGui:
            print(i)
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

#-------TKinter----------------

def test():
    print("test Passed!!")

root=tk.Tk()

height=700
width=800
canvas=tk.Canvas(root,height=height,width=width)
canvas.pack()

background=tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
#backgroundLable=tk.Label(root, image=background)
#backgroundLable.place(x=0,y=0,relheight=1,relwidth=1)

frame=tk.Frame(root,bg="#80c1ff")
frame.place(relx=0,rely=0,relwidth=1,relheight=1)

instruction=tk.Label(frame,font=("courier",11),text="Enter a name of a topic OR a name of a Gursikh.\n(When you type in the search box, the program will go through the\n Gurmat Bibek, Tapoban and Sikh Unity WordPress sites \nand search through the fourms.\n You can type the username of Gursikhs who posted Gurmat bibek and get back all \nthe fourms started by that person.")
instruction.place(relx=0.05,rely=0,relwidth=0.9,relheight=0.2)


entry=tk.Entry(frame)
entry.place(relx=0.3,rely=0.2,relwidth=0.25,relheight=0.1)

#photo = tk.PhotoImage(file = "C:\\Users\\gians\\Desktop\\pictures\\DhanGuruNanak.jpg")
#photo=photo.subsample(3,3)
forGui=[]
button=tk.Button(frame,font=("courier",12),text="Search",bg="gray",command=lambda: main(entry.get()))
button.place(relx=0.4,rely=0.3,relwidth=0.1,relheight=0.05)


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.37, rely=0.4, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame,font=("courier",8),justify=CENTER)
label.place(relwidth=1, relheight=1)

if label["text"]!="":
    numbutton=tk.Button(frame,font=("courier",12),text="num",bg="gray",command=test)
    numbutton.place(relx=0.7,rely=0.7,relwidth=0.1,relheight=0.05) 
#print(tk.font.families())
root.mainloop()
print(forGui)

