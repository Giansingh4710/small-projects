from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

def GoToFacebook():
    br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe')#,options=options)
    url="https://www.facebook.com/profile.php?id=100053148708519&sk=videos"
    br.get(url)
    time.sleep(4)
    html = br.find_element_by_tag_name('html')
    #scroll=html.send_keys(Keys.END) #scroll to end of page
    scroll=0
    end=False
    while not end:
        firstScroll=br.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        print(scroll)
        print(firstScroll)
        if firstScroll==scroll:
            end=True
        else:
            scroll=firstScroll
    content=br.page_source.encode('utf-8').strip()
    soup=bs(content,"lxml")
    atags=soup.findAll("a")
    videos=[]
    for i in atags:
        href=i.get("href")
        if href==None:
            continue
        if "facebook" not in href:
            videos.append("https://www.facebook.com"+href)
    videos=videos[3:] #first 3 are not relevent
    for i in videos: print(i)
    return videos

videos=GoToFacebook()
filee=open("C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff\\GianiSherSinghJi\\faceBook\\theLinks.txt","w")
for i in videos:
    filee.write(i+"\n")
filee.close()



