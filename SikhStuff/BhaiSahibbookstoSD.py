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
    print(len(audioBooks))
    return audioBooks 
getAudios()
