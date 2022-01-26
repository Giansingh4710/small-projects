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
            title=file.find("font",size="1",color="333333").text
        except AttributeError:
            print("No Good. But we caught it!!")#It got the ALL the text from the drop down menu and those don't have a 'color=0069c6' attribute
            continue
        newUrl="http://gurbaniupdesh.org"+file.find("a").get("href")
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
            folderPath=thePath+khata+"/"
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
            urllib.request.urlretrieve(links[i],f'{folderPath}{title}')
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


'''
Radio for Bhai Gurmail singh ji
as requested by bhai harkamal singh ji
'''

#audios will be dict where key is track name and value is track link
#exp: {"amazing track":"www.amazingtrack.com",...}

def link1Audios():
    link1='http://gurbaniupdesh.org/multimedia/listing.php?q=f&f=%2F06-Kirtan%2FBhai+Gurmail+Singh+Ji+%28Hazoori+Ragi+Sri+Darbar+Sahib+Amritsar%29'
    res=requests.get(link1)
    soup=bs(res.text, 'lxml')
    tracks=soup.find_all("table",cellpadding=4)
    tracks=tracks[4:-2]

    print(tracks)
    print(len(tracks))
    print(tracks[0])







link1='http://gurbaniupdesh.org/multimedia/listing.php?q=f&f=%2F06-Kirtan%2FBhai+Gurmail+Singh+Ji+%28Hazoori+Ragi+Sri+Darbar+Sahib+Amritsar%29'
link2='http://gurbaniupdesh.org/multimedia/listing.php?q=f&f=%2F06-Kirtan%2FBhai+Harjinder+Singh+Ji+%28Sri+Nagar+Wale%29'
link3='http://kirtansewa.net/index.php/bhai-gurmail-singh-amritsar/'
#link1Audios()
#a=getAllLinks(link1,"test")
EnterUrl(link1,'/mnt/c/Users/gians/Desktop/test','Bhai Gurmail Singh Ji 1')
EnterUrl(link2,'/mnt/c/Users/gians/Desktop/test','Bhai Harjinder Singh Ji')
