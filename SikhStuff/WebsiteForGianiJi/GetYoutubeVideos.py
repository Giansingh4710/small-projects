from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

options = webdriver.ChromeOptions()
options.headless = True
br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=options)
url="https://www.youtube.com/c/ShriSarblohBungaNangali/videos"

def getLinksNTitles(urll):
    br.get(urll)
    content=br.page_source.encode('utf-8').strip()
    soup=bs(content,"lxml")
    vids=soup.findAll("a",id="video-title")
    span=soup.findAll("span",class_="style-scope ytd-grid-video-renderer")
    videosViews=[]
    d={}
    hrefs=["https://www.youtube.com"+i.get("href") for i in vids]
    for i in range(0,len(span),2):
        viewsNhowLongAgo=[] # a list of size 2 where index 0 in the views and index 1 is how long ago
        viewsNhowLongAgo.append(span[i].text)
        viewsNhowLongAgo.append(span[i+1].text)
        videosViews.append(viewsNhowLongAgo)
    for i in range(len(vids)):
        title=vids[i].text
        d[title]=videosViews[i]
        d[title].append(hrefs[i])
    return d

def writeInFile(dictt):
    br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=options)
    br.get("https://www.google.com/search?q=gurmukhi+to+english")
    punjabiTextBox=br.find_element_by_css_selector("#tw-source-text-ta")
    filee=open("C:\\Users\\gians\\Desktop\\stuff\\GianGurwinderSinghJi.txt","w")
    count=0
    for i in dictt:
        count+=1
        try:
            filee.write(i+" $$$ "+" # ".join(dictt[i])+"\n")
        except UnicodeEncodeError:
            print(i+" : Going to google and translating the Gurmukhi title")
            punjabiTextBox.clear()
            punjabiTextBox.send_keys(i)
            time.sleep(1)
            eng=br.find_element_by_css_selector("#tw-target-text > span").text
            try:
                filee.write(eng+" $$$ "+" # ".join(dictt[i])+"\n")
            except UnicodeEncodeError:
                filee.write(f"GianiGurwinderSingh Ji Video {count}"+" $$$ "+" # ".join(dictt[i])+"\n")
    time.sleep(20)
    filee.close()
dictt=getLinksNTitles(url)
#writeInFile(dictt)




