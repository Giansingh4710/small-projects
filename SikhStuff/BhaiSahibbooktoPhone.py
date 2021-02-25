import urllib.request
from bs4 import BeautifulSoup as bs 
import requests

#url="http://www.gurmatveechar.com/audios/Katha/02_Present_Day_Katha/Swami_Ram_Singh_Nirmala/Asa_Di_Vaar_Katha/Swami.Ram.Singh.Nirmala--Asa.Di.Vaar.Katha.01.mp3"
#urllib.request.urlretrieve(url,"D:\\testt.mp3")


url="https://www.akj.org/audio-books.php?q=MjU"
res=requests.get(url)
soup=bs(res.text, 'lxml')
chapters=soup.find("tbody")
counter=0
for chapter in chapters:
    href=chapter.find("a").get("href")
    mp3="https://www.akj.org/"+href
    counter+=1
    title=f"{counter}) {chapter.text}.mp3"
    #urllib.request.urlretrieve(mp3,f"C:\\Users\\gians\\Desktop\\GurmatKaramPhilosphy\\{title}")
    print(mp3)