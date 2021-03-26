import pyperclip, random,webbrowser
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import time
import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os


StupidLongVariablecounterBecauseItIsGlobal=0
def getAllLinks(url,folder):
    res=requests.get(url)
    soup=bs(res.text, 'lxml')
    khatas=soup.find_all("table",cellpadding=4)
    khatas=khatas[4:-2]
    folderWithLinks={folder:[]}
    for file in khatas:
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            global StupidLongVariablecounterBecauseItIsGlobal
            StupidLongVariablecounterBecauseItIsGlobal+=1
            title=f"{str(StupidLongVariablecounterBecauseItIsGlobal).zfill(3)} ) {file.text}"
            folderWithLinks[folder].append(title)
            folderWithLinks[folder].append(newUrl)
        else:
            newFolder=file.text[:-8] ## "Volume 15 Ang 1352-143093 files" what it looks like without the -8. The last 2 nums are the numbers of files in that folder
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            folderWithLinks.update(newFolderWithLinks)
    return folderWithLinks

def getMBs(link,path):
    khatas=getAllLinks(link,"main")
    for khata in khatas:
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        if path[-1]!="\\":
            folderPath=path+"\\"
        else:
            folderPath=path
        print(folderPath)
        if khata!="main":
            folderPath+=khata+"\\"
            os.mkdir(folderPath)
        for i in range(len(links)):
            title=titles[i][:6]+titles[i][50:-52]+".mp3"
            noNo='\/:*?"<>|' #cant name a file with any of these characters so if the title has any of these characters, the loop will replace them
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')

def main(link):
    path=simpledialog.askstring("Type","Enter the path were you want to download the files (exp: 'C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff'):")
    getMBs(link,path)    

#url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FSant_Giani_Inderjeet_Singh_%28Raqbe_wale%29%2FSri_Gurpartap_Sooraj_Parkash_Katha"
#EnterUrl(url)






#-------TKinter----------------

root=tk.Tk()
root.title("Download")
root.geometry("800x500")

instruction=tk.Label(root,fg="blue",bg="#80c1ff",font=("courier",11),text="Enter the link of the folder you want to download from GurmatVeechar.Com")
instruction.pack(side="top",pady=10)

entry=tk.Entry(root,bg="#80c1ff")
entry.pack()

forGui=[]
button=tk.Button(root,font=("courier",12),text="Search",bg="gray",command=lambda: main(entry.get()))
button.pack()

h = Scrollbar(root, orient = 'horizontal')
h.pack(side = BOTTOM, fill = X)

v = Scrollbar(root)
v.pack(side = RIGHT, fill = Y)
t = tk.Text(root, width = 50, height = 20, wrap = NONE,xscrollcommand = h.set,yscrollcommand = v.set)
t.pack(side=TOP, fill=X)
h.config(command=t.xview)
v.config(command=t.yview)

root.mainloop()
