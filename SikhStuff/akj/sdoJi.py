from mutagen.mp3 import JOINTSTEREO
import requests
from bs4 import BeautifulSoup as bs
import urllib.request

def goldenKhajana(link):
    res=requests.get(link)
    soup=bs(res.text,"lxml")
    td=soup.find_all("td",valign="top")
    atags=[i.find("a") for i in td]
    links=["http://sikhsoul.com"+i["href"] for i in atags]
    return links

def download(links,path):
    if path[-1]!="\\":
        path+="\\"
    count=0
    print(len(links))
    print(len(set(links)))
    links=sorted(set(links))
    for i in links:
        count+=1
        title=i.split("/")
        title=''.join(title[-1])
        title=title.replace("%20"," ",-1)
        title=f'{count}) {title}'
        try:
            urllib.request.urlretrieve(i,path+title)
            print(f"Downloaded: {title}")
        except Exception as e:
            print(f"No download :{e}")



links=goldenKhajana("http://sikhsoul.com/golden_khajana/index.php?q=f&f=%2FKeertan%2FBhai+Mohinder+Singh+SDO")
path="D:\\2) Keertan\\SDO ji"
download(links,path)

