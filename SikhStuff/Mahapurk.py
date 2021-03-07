import requests
from bs4 import BeautifulSoup as bs
import os
import urllib.request

def getMainLinks():
    url="http://www.mahapurakh.com/"
    res=requests.get(url)
    soup=bs(res.text,"lxml")
    atags=soup.find_all('a')
    links=[]
    for i in atags: 
        href=i.get("href")
        if href==None: continue
        if "http" not in href:
            href=url+href
        if "PDF" not in href and "@" not in href and "mahapur" in href: #some hrefs are emails and others not books
            if href not in links:
                links.append(href)
    return links

def getAudioFiles(links):
    dictt={}
    for i in links:
        title=i.split("http://www.mahapurakh.com//")[1]
        res=requests.get(i)
        soup=bs(res.text,"lxml")
        ultag=soup.find_all('ul')[-1]
        linksForDownload=[]
        for li in ultag:
            try:
                href=li.find('a').get("href")
                href=href.replace(" ","%20")
                linksForDownload.append(href)
            except AttributeError:
                ("NOT an A TAG WITH HREF")
        if title not in dictt:
            dictt[title]=linksForDownload
        else:
            dictt[title]+=linksForDownload
    return dictt

def selectBook(books):
    mahapuks=list(books.keys()) # names of books or mahapukrs
    chapters=list(books.values()) # a list of lists where each list has mp3 links for each chapters respectively 
    for maha in range(len(mahapuks)):
        print(f"{maha+1} ) {mahapuks[maha]}")
    whichBook=int(input("Please enter the number correspoding to the book: "))-1
    book=chapters[whichBook]
    title=mahapuks[whichBook]
    os.mkdir(f"C:\\Users\\gians\\Desktop\\Mahapurk\\{title}")
    count=0
    for cha in book:
        count+=1
        urllib.request.urlretrieve(cha,f"C:\\Users\\gians\\Desktop\\Mahapurk\\{title}\\{count}.mp3")
        print(count)
    anotherOne=input("Would you like to pick another book (Y or N): ")
    if "y" in anotherOne.lower():
        books.pop(title)
        selectBook(books)
    else:
        print("BYE!!!")
        return "Vaheguru"
    
links=getMainLinks()[3:]
dictt=getAudioFiles(links)
selectBook(dictt)

