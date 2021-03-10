import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt


StupidLongVariablecounterBecauseItIsGlobal=0
def getAllLinks(url):
    res=requests.get(url)
    soup=bs(res.text, 'lxml')
    khatas=soup.find_all("table",cellpadding=4)
    khatas=khatas[4:-2]
    linksWithTitles={}
    for file in khatas:
        newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
        if "mp3" in newUrl.lower():
            global StupidLongVariablecounterBecauseItIsGlobal
            StupidLongVariablecounterBecauseItIsGlobal+=1
            title=f"{str(StupidLongVariablecounterBecauseItIsGlobal)} ) {file.text}"
            linksWithTitles[title]=newUrl
        else:
            newLinkWithTitles=getAllLinks(newUrl)
            linksWithTitles.update(newLinkWithTitles)
    return linksWithTitles

def getMBs(link):
    import re
    mb=re.compile(r"([0-9]{1,3}(\.[0-9]*)?\s(MB))")
    khatas=getAllLinks(link)
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
        #urllib.request.urlretrieve(finalUrl,f'D:\\3)GianiSantji\\{title}')
        print(f'{title} - {finalUrl}')
    print(MBsum)

now="Start: "+str(dt.now())
print(now)

url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Dalel_Singh_Viakirt"
getMBs(url)

now="End: "+str(dt.now())
print(now)



    


        


        


