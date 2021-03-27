import tkinter as tk
from tkinter import Scrollbar
from tkinter.ttk import *
from tkinter import *
from tkinter import BOTTOM, X, RIGHT, Y, NONE, TOP, END
from tkinter import simpledialog       
import time
import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os,re


totalFiles=0
def getAllLinks(url,folder):
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
            global totalFiles
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
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            folderWithLinks.update(newFolderWithLinks)
    return folderWithLinks

def getMBs(link,path):
    label.config(text=f"waiting...")
    root.update_idletasks()
    khatas=getAllLinks(link,"main")
    mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\xa0((MB)|(KB)|(GB)))")
    MBsum=0
    label.config(text="Calculating the size of the files...")
    root.update_idletasks()
    t.delete(f"0.0",END)
    for folder in khatas:
        for file in khatas[folder]:
            if mb.findall(file)!=[]:
                a=mb.findall(file)[0][0]
                if "kb" in a.lower():
                    val = float(a[:-3])/1000
                elif "mb" in a.lower():
                    val=float(a[:-3])
                elif "gb" in a.lower():
                    val=float(a[:-3])*1000
                MBsum+=val
    askifContinue=tk.messagebox.askquestion("Continue?",f"In total there are {MBsum} MBs. Would you Like to download?")
    if askifContinue=="no":
        quit()
    for khata in khatas:
        t.insert(END, f"New Folder - {khata}\n")
        root.update_idletasks()
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        if path[-1]!="\\":
            folderPath=path+"\\"
        else:
            folderPath=path
        if khata!="main":
            folderPath+=khata+"\\"
            #os.mkdir(folderPath)
            print(folderPath)
        for i in range(len(links)):
            progress['value'] = 20
            root.update_idletasks()
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|' 
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            #urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            t.insert(END,f'{title} - {links[i]}\n')
            root.update_idletasks()
            print(f'{title} - {links[i]}')

def main(link):
    path=simpledialog.askstring("Type","Enter the path were you want to download the files (exp: 'C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff'):")
    getMBs(link,path)
    label.config(text=f"In total, there are {totalFiles} files!!!")    

#url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FSant_Giani_Inderjeet_Singh_%28Raqbe_wale%29%2FSri_Gurpartap_Sooraj_Parkash_Katha"
#EnterUrl(url)






#-------TKinter----------------

root=tk.Tk()
root.title("Download any folder from gurmatveechar.com")
root.geometry("1100x800")

instruction=tk.Label(root,fg="blue",bg="#80c1ff",font=("courier",11),text="Enter the link (in the yellow box)of the folder you want to download from Gurmatveechar.om\n(exp: 'http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29')")
instruction.pack(side="top",pady=10)

entry=tk.Entry(root,bg="yellow",width=150)
entry.pack()

forGui=[]
button=tk.Button(root,font=("courier",12),text="Search",bg="gray",command=lambda: main(entry.get()))
button.pack()

label=tk.Label(root,width=50,height=2,bg="#80c1ff",font=("courier",13),text="It might take some time to download the files")
label.pack(pady=10)

h = Scrollbar(root, orient = 'horizontal')
h.pack(side = BOTTOM, fill = X)

v = Scrollbar(root)
v.pack(side = RIGHT, fill = Y)
t = tk.Text(root, width = 50, height = 40, wrap = NONE,xscrollcommand = h.set,yscrollcommand = v.set)
t.pack(side=TOP, fill=X,pady=100)
h.config(command=t.xview)
v.config(command=t.yview)

progress = Progressbar(root, orient = HORIZONTAL,length = 100, mode = 'indeterminate',)
progress.pack(pady = 30)

root.mainloop()
