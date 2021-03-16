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
    khatas=khatas[5:-2]
    folderWithLinks={folder:[]}
    for file in khatas:
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            global StupidLongVariablecounterBecauseItIsGlobal
            StupidLongVariablecounterBecauseItIsGlobal+=1
            title=f"{str(StupidLongVariablecounterBecauseItIsGlobal)} ) {file.text}"
            folderWithLinks[folder].append(title)
            folderWithLinks[folder].append(newUrl)
        else:
            newFolder=file.text[:-7]
            print(newFolder)
            newFolderWithLinks=getAllLinks(newUrl,newFolder)
            folderWithLinks.update(newFolderWithLinks)
    return folderWithLinks

def getMBs(link):
    import re
    mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s(MB))")
    khatas=getAllLinks(link,"main")
    print(khatas.keys())
    print(len(list(khatas.keys())))
    allMbs=""
    MBsum=0
    for i in khatas:
        allMbs+=i
    for i in mb.findall(allMbs):
        val=float(i[0][:-3])
        MBsum+=val
    for i in khatas:
        title=i[:30]+".mp3"
        finalUrl=khatas[i]
        #urllib.request.urlretrieve(finalUrl,f'C:\\Users\\gians\\Desktop\\gurmukhi\\{title}')
        #print(f'{title} - {finalUrl}')
    print(f"\nTotal MBs: {MBsum}")
    print(f"\nTotal GBs: {MBsum/1000}\n")

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

url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F02_Present_Day_Katha%2FBhai_Pinderpal_Singh_%28Ludhiane_wale%29"
EnterUrl(url)


    


        


        


