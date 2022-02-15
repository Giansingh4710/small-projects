import tkinter as tk
from tkinter import Scrollbar, HORIZONTAL
from tkinter.ttk import Progressbar
#from tkinter import *
from tkinter import BOTTOM, X, RIGHT, Y, NONE, TOP, END
from tkinter import simpledialog       
import time
import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os,re
mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\xa0((MB)|(KB)|(GB)))")

def getAllLinks(url,folder="main",totalFiles=0):
    res=requests.get(url)
    soup=bs(res.text, 'lxml')
    khatas=soup.find_all("table",cellpadding=4)
    khatas=khatas[4:-2]
    folderWithLinks={folder:[]}
    count=0 
    for file in khatas:
        try:
            title=file.find("font",size="2",color="0069c6").text
        except AttributeError:
            print("No Good. But we caught it!!")#It got the ALL the text from the drop down menu and those don't have a 'color=0069c6' attribute
            continue
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            totalFiles+=1
            count+=1
            length=file.find_all("td",align="right")
            for td in length:
                if "mb" in td.text.lower() or "kb" in td.text.lower():
                    theMB=td.text
            title=f"{str(count).zfill(3)} ) {title}"+"???"+theMB #the last part contians the MBs of the file.
            folderWithLinks[folder].append(title)
            folderWithLinks[folder].append(newUrl)
        else:
            newFolder=title
            newFolderWithLinks,totalFiles=getAllLinks(newUrl,newFolder,totalFiles)
            if folder=="main": # the purpose og this statement is so that when we make the folders to download the files, the folders in the folder end up in the folder lol
                folderWithLinks.update(newFolderWithLinks)
            else:
                folderWithLinks[folder].append(newFolderWithLinks) 
                #ifthere is a folder in a folder, the MAIN folder will be the key 
                # and its keys are other dictionaies. The keys to ALL dictionaries are titles of folders 
                # and the base value is a list of links
                #the program will keep recusing as long as there is folder and will stop when there are
                #mp3 files
    return folderWithLinks,totalFiles

allMbSum=0
def download(khatas,thePath,totalFiles):
    for khata in khatas:
        if khata!="main":
            folderPath=thePath+khata+"\\"
            os.mkdir(folderPath)
            print(khatas[khata])
            if ((type(khatas[khata][0])==dict)):
                listOfDict=khatas[khata]
                for dictt in listOfDict:
                    download(dictt,folderPath,totalFiles)
                continue #so the dict of dicts dosen't keep going down
        else:
            folderPath=thePath
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        FolderMbs=""
        MBsum=0
        for i in titles:
            FolderMbs+=i
        for i in mb.findall(FolderMbs):
            val=float(i[0][:-3])
            MBsum+=val
        global allMbSum
        allMbSum+=MBsum
        t.insert(END,"\n"+khata+" : "+str(MBsum)+"\n")
        for i in range(len(links)):
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|' #cant name a file with any of these characters so if the title has any of these characters, the loop will replace them
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')
            t.insert(END,f'{title} - {links[i]}\n')
            progress["value"]+= 100/totalFiles
            root.update_idletasks()
            time.sleep(0.1)

def main(link):
    t.delete(f"0.0",END)
    path=simpledialog.askstring("Type","Enter the path were you want to download the files (exp: 'C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff'):")

    label["text"]="Calculating..."
    root.update_idletasks()

    try:
        if path[-1]!="\\":
            path+="\\"

        khatas,totalFiles=getAllLinks(link)
        download(khatas,path,totalFiles)
    except Exception as e:
        t.insert(END,"ERROR: ")
        t.insert(END,e)
        print(e)

    label.config(text=f"In total, there are {totalFiles} files!!!")    

def openGV():
    import webbrowser
    webbrowser.open("http://www.gurmatveechar.com/audio.php?q")





#-------TKinter----------------

root=tk.Tk()
root.title("Download any folder from gurmatveechar.com")
root.geometry("1000x700")

instruction=tk.Label(root,fg="blue",bg="#80c1ff",font=("courier",11),text="Enter the link (in the yellow box)of the folder you want to download from Gurmatveechar.om\n(exp: 'http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29')")
instruction.pack(side="top",pady=10)

entry=tk.Entry(root,bg="yellow",width=150)
entry.pack()

forGui=[]

goToGV=tk.Button(root,font=("courier",8),text="click here to go to Gurmatveechar.com",bg="gray",command=openGV)
goToGV.pack()

button=tk.Button(root,font=("courier",12),text="click here after you have copy and pasted the link you want",bg="gray",command=lambda: main(entry.get()))
button.pack()



label=tk.Label(root,width=45,height=4,bg="#80c1ff",font=("courier",13),text="It might take some time to download the files")
label.pack()

h = Scrollbar(root, orient = 'horizontal')
h.pack(side = BOTTOM, fill = X)

progress = Progressbar(root, orient = HORIZONTAL,length = 100, mode = 'determinate',)
progress.pack(pady = 10)

v = Scrollbar(root)
v.pack(side = RIGHT, fill = Y)
t = tk.Text(root, wrap = NONE,xscrollcommand = h.set,yscrollcommand = v.set)
t.pack(side=TOP,fill="both")
h.config(command=t.xview)
v.config(command=t.yview)


root.mainloop()
