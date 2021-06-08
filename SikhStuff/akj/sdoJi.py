from mutagen.mp3 import JOINTSTEREO
import requests
from bs4 import BeautifulSoup as bs
import urllib.request

def goldenKhajana(link):
    res=requests.get(link)
    soup=bs(res.text,"lxml")
    td=soup.find_all("td",valign="top")
    atags=[i.find("a") for i in td]
    links=[]
    names=[]
    for i in atags:
        title="http://sikhsoul.com"+i["href"]
        if title not in links:
            links.append("http://sikhsoul.com"+i["href"])
        if i.text not in names:
            names.append(i.text)
    names=names[1:]        
    return names,links

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



names,links=goldenKhajana("http://sikhsoul.com/golden_khajana/index.php?q=f&f=%2FKeertan%2FBhai+Mohinder+Singh+SDO")
import os
os.mkdir("D:\\SDOJi")
path="D:\\SDOJi"
download(links,path)




