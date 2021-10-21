import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os
import re
mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s((MB)|(KB)))")


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
            if folder=="main": # the purpose og this statement is so that when we make the folders to download the files, the folders in the folder end up in the folder lol
                folderWithLinks.update(newFolderWithLinks)
            else:
                folderWithLinks[folder].append(newFolderWithLinks) 
                #ifthere is a folder in a folder, the MAIN folder will be the key 
                # and its keys are other dictionaies. The keys to ALL dictionaries are titles of folders 
                # and the base value is a list of links
                #the program will keep recusing as long as there is folder and will stop when there are
                #mp3 files
    return folderWithLinks

allMbSum=0
def download(khatas,thePath):
    for khata in khatas:
        folderPath=thePath
        if khata!="main":
            folderPath=thePath+khata+"\\"
            os.mkdir(folderPath)
            if type(khatas[khata][0])==dict: #made this call so that it doesen't have to search through EACH file when the first is not a dict
                listOfDict=khatas[khata]
                for dictt in listOfDict:
                    try:
                        if type(dictt)==dict:  #somtimes there are folders and files in a folder so this will check for that. If not a dict, the won't recurse
                            download(dictt,folderPath)
                    except Exception as e:
                        print("error: "+e)
                continue #so the dict of dicts dosen't keep going down
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        FolderMbs=""
        MBsum=0
        for i in titles:
            FolderMbs+=i
        for i in mb.findall(FolderMbs):
            a=i[0]
            if "kb" in a.lower():
                val=float(a[:-3])/1000
            elif "gb" in a.lower():
                val=float(a[:-3])*1000
            else:
                val=float(a[:-3])
            MBsum+=val
        global allMbSum
        allMbSum+=MBsum
        print("\n"+khata+" : ",MBsum)
        for i in range(len(links)):
            title=titles[i].split("???")[0]+".mp3"
            noNo='\/:*?"<>|' #cant name a file with any of these characters so if the title has any of these characters, the loop will replace them
            for bad in noNo:
                if bad in title:
                    title=title.replace(bad,"#")
            # urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')

def EnterUrl(link,path,folderNameToPutAllFiles="main"):
    start=str(dt.now())

    if path[-1]!="/":
        path+="/"

    khatas=getAllLinks(link,folderNameToPutAllFiles)
    download(khatas,path)

    end=str(dt.now())

    print(f"\nTotal MBs: {allMbSum}")
    print(f"Total GBs: {allMbSum/1000}")
    print("In total: "+str(totalFiles)+" total files\n")
    
    print(f"Start: {start}")
    print(f"End: {end}",end="\n\n")
    startSeconds=(int(start[11:13])*60*60)+(int(start[14:16])*60)+int(start[17:19])
    endSeconds=(int(end[11:13])*60*60)+(int(end[14:16])*60)+int(end[17:19])
    print(f"Seconds: {endSeconds-startSeconds}")
    print(f"Minutes: {(endSeconds-startSeconds)/60}")
    print(f"Hours: {(endSeconds-startSeconds)/(60*60)}")


def santJiKhataInOrder(path):
    def onlyLinks(url):
        res=requests.get(url)
        soup=bs(res.text, 'lxml')
        khatas=soup.find_all("table",cellpadding=4)
        khatas=khatas[4:-2]
        folderWithLinks={}
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
                folderWithLinks[title]=newUrl
            else:
                newFolderWithLinks=onlyLinks(newUrl)
                folderWithLinks.update(newFolderWithLinks) 
        return folderWithLinks
    angs=re.compile(r"(Ang(-||\s)([0-9]{1,4})(\+[0-9]{1,4})?)")
    url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FGuru_Granth_Sahib_Larivaar_Katha"
    a=onlyLinks(url)
    titles=list(a.keys())
    links=list(a.values())
    theAngs=[0]*1430
    for i in range(len(titles)):
        b=angs.search(titles[i])
        ang=b.group(3) #the third group gives the ang
        num=int(ang)-1
        theAngs[num]=links[i]
    default="http://sikhsoul.com/audio_files/mp3/Bani/Kirtan%20Sohila/Bhai%20Tarlochan%20Singh%20Ragi%20-%20Kirtan%20Sohaila.mp3"
    for i in range(len(theAngs)):
        if theAngs[i]==0:
            down=default
            name=f"Default{i+1}.mp3"
        else:
            down=theAngs[i]
            name=f"Ang{i+1}.mp3"
        urllib.request.urlretrieve(down,f"{path}\\{name}")
        print(f"Downloaded {name}")


# url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FGuru_Granth_Sahib_Larivaar_Katha"

urls=[
    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FBaba_Mohan_Singh_%28Bhindran_wale%29","Baba_Mohan_Singh"],

    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FGiani_Kirpal_Singh_%28Boparai_wale%29%2FSri_Dasam_Granth_Katha","Giani_Kirpal_Singh Dasam Katha"],
    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FGiani_Kirpal_Singh_%28Boparai_wale%29%2FKatha_Sri_Nanak_Parkash","Giani_Kirpal_Singh Nanak Parkash"],

    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FSant_Giani_Inderjeet_Singh_%28Raqbe_wale%29%2FSahaskritee_Salok_Katha","Sant_Giani_Inderjeet_Singh Raqbe_wale Sahaskritee_Salok_Katha"],
    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FSant_Giani_Inderjeet_Singh_%28Raqbe_wale%29%2FSri_Gurpartap_Sooraj_Parkash_Katha","Sant_Giani_Inderjeet_Singh Raqbe_wale Gurpartap_Sooraj_Parkash"],

    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FBhai_Gurdas_Dian_Varan","Sant_Gurbachan_Singh Bhai_Gurdas_Dian_Vara"],
    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FGuru_Granth_Sahib_Larivaar_Katha","Sant_Gurbachan_Singh Guru_Granth_Sahib_Larivaar_Katha"],
    ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FSri_Krishan_Avtar_Katha","Sant_Gurbachan_Singh Sri_Krishan_Avtar_Katha"],
]

urls=[
   ["https://gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FBaba_Mohan_Singh_%28Bhindran_wale%29","Baba_Mohan_Singh"],
]

urls=[
   ["https://gurmatveechar.com/audio.php?","All Gurmat Vechar test"],
]

path="D:/"
path="C:/Users/gians/Desktop/test"

for url in urls:
    EnterUrl(url[0],path,url[1])
