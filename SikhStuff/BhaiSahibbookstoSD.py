import urllib.request
from bs4 import BeautifulSoup as bs 
import requests

#url="http://www.gurmatveechar.com/audios/Katha/02_Present_Day_Katha/Swami_Ram_Singh_Nirmala/Asa_Di_Vaar_Katha/Swami.Ram.Singh.Nirmala--Asa.Di.Vaar.Katha.01.mp3"
#urllib.request.urlretrieve(url,"D:\\testt.mp3")

def getAudios():
    url="https://www.akj.org/books.php"
    res=requests.get(url)
    soup=bs(res.text, 'lxml')
    container=soup.find("div", class_="books-clms")
    ultags=container.find_all("ul")
    booksContainer=ultags[1].find_all("li")
    audioBooks=[]
    for i in booksContainer:
        spanTag=i.find("span")
        atags=spanTag.find_all('a')
        for atag in atags:
            href="https://www.akj.org/"+atag["href"]
            if "pdf" not in href:
                if "Book" in href or "book" in href:
                    audioBooks.append(href)
    return audioBooks 
def downloadBooks(linksofBooks):
    failCounter=0
    for i in linksofBooks:
        res=requests.get(i)
        soup=bs(res.text, 'lxml')
        theCointaner=soup.find("div",class_="krtn_listing")
        theCointaner=theCointaner.find("tbody")
        chapters=theCointaner.find_all("tr")
        counter=0
        for chapter in chapters:
            href=chapter.find("a").get("href")
            mp3="https://www.akj.org/"+href
            counter+=1
            title=f"{counter}) {chapter.text}.mp3"
            title=title.replace(" ","#")
            try:
                urllib.request.urlretrieve(mp3,f"D:\\Books\\{title}")
                print(f"{title} ) {mp3}")
            except:
                failCounter+=1
                print(f"Failed - {title}")
    print(f"Total chapters failed: {failCounter}")
            
        
booklinks=getAudios()
downloadBooks(booklinks)
    