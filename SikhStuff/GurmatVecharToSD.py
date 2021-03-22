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
            newFolder=file.text[:-8] #befor when you got the text from file, it would all appear without spaces so this helps with reading
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            folderWithLinks.update(newFolderWithLinks)
    return folderWithLinks

def getMBs(link):
    import re
    mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s(MB))")
    khatas=getAllLinks(link,"main")
    allMbSum=0
    for khata in khatas:
        titles=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2==0]
        links=[khatas[khata][i] for i in range(len(khatas[khata])) if i%2!=0]
        print(khata+" : ",end="")

        folderPath="D:\\3) Khata\\SwamiJi\\VaarAsa\\"
        if khata!="main":
            folderPath+=khata+"\\"
            os.mkdir(folderPath)
        FolderMbs=""
        MBsum=0
        for i in titles:
            FolderMbs+=i
        for i in mb.findall(FolderMbs):
            val=float(i[0][:-3])
            MBsum+=val
        print(MBsum)
        allMbSum+=MBsum
        for i in range(len(links)):
            title=titles[i][6:20]+".mp3"
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
            print(f'{title} - {links[i]}')
    print(f"\nTotal MBs: {allMbSum}")
    print(f"Total GBs: {allMbSum/1000}\n")

def EnterUrl(link):
    start=str(dt.now())
    getMBs(link)
    end=str(dt.now())
    print(f"Start: {start}")
    print(f"End: {end}",end="\n\n")
    startSeconds=(int(start[11:13])*60*60)+(int(start[14:16])*60)+int(start[17:19])
    endSeconds=(int(end[11:13])*60*60)+(int(end[14:16])*60)+int(end[17:19])
    print(f"Seconds: {endSeconds-startSeconds}")
    print(f"Minutes: {(endSeconds-startSeconds)/60}")
    print(f"Hours: {(endSeconds-startSeconds)/(60*60)}")

url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FSwami_Ram_Singh_Nirmala%2FAsa_Di_Vaar_Katha"
EnterUrl(url)


    


        


        


