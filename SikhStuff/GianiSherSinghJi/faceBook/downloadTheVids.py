from selenium import webdriver
import time
import urllib.request
import os
from datetime import datetime as dt

def download(vids):
    br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe')#,options=options)
    counter=0
    noDownload=0
    for i in vids:
        counter+=1
        time.sleep(1)
        br.get("https://www.getfvid.com/")
        time.sleep(1)
        br.find_element_by_css_selector("#form_download > div > input").send_keys(i) #sending link
        time.sleep(1)
        br.find_element_by_css_selector("#btn_submit").click() #click download button
        findaudioONLY=br.find_elements_by_tag_name("a")
        try:
            audioONLY=[i for i in findaudioONLY if i.text=="Audio Only"][0]
            url=audioONLY.get_attribute("href")
            path="D:\\GianiSherSinghJi\\"
            urllib.request.urlretrieve(url,f'{path}{str(counter)}) GianiSherSinghFacebook.mp3')
        except:
            print("Couldn't download video")
            counter-=1
            noDownload+=1
        print(f'{counter} Done out {len(vids)}!!')
    print(f"No download: {noDownload}")

def getTime(vids):
    start=str(dt.now())

    download(vids)

    end=str(dt.now())
    print(f"Start: {start}")
    print(f"End: {end}",end="\n\n")
    startSeconds=(int(start[11:13])*60*60)+(int(start[14:16])*60)+int(start[17:19])
    endSeconds=(int(end[11:13])*60*60)+(int(end[14:16])*60)+int(end[17:19])
    print(f"Seconds: {endSeconds-startSeconds}")
    print(f"Minutes: {(endSeconds-startSeconds)/60}")
    print(f"Hours: {(endSeconds-startSeconds)/(60*60)}")

filee=open("C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff\\GianiSherSinghJi\\faceBook\\theLinks.txt","r")
read=filee.readlines()
filee.close()
videos=[i[:-1] for i in read]
getTime(videos)


















'''
Old Style

def goToFacebook():
    br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe')
    br.get("https://m.facebook.com/timeline/app_section/?section_token=100053148708519%3A1560653304174514#")
    br.find_element_by_css_selector("#m_login_email").send_keys("giansingh4710@gmail.com")
    br.find_element_by_css_selector("#m_login_password").send_keys("Sjkg1212")
    br.find_element_by_class_name("_54k8").click() #Login
    time.sleep(3)
    #br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    atags=br.find_elements_by_tag_name("a")
    videos=[]
    time.sleep(1)
    for i in atags:
        href=i.get_attribute('href')
        if href==None: continue
        if "php" in href and "story" in href:
            videos.append(href)
    print(len(videos))
    br.close()
    file=open("C:\\Users\\gians\\Desktop\\CS\\pythons\\webScraping#NonGit\\selenium\\GianiSherSinghFaceBook\\theLinks.txt",'w')
    for i in videos:
        file.write(i+"\n")
        print(i)
    file.close()
    return videos
def download(vids):
    br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe')
    counter=9
    for i in vids:
        time.sleep(1)
        br.get("https://www.getfvid.com/")
        time.sleep(1)
        br.find_element_by_css_selector("#form_download > div > input").send_keys(i) #sending link
        time.sleep(1)
        audioONLY=br.find_element_by_css_selector("body > div.page-content > div > div > div.col-lg-10.col-md-10.col-centered > div > div:nth-child(3) > div > div.col-md-4.btns-download > p:nth-child(2) > a")
        url=audioONLY.get_attribute("href")
        print(url)
        #urllib.request.urlretrieve(url,f'D:\\{counter}gianiSherSinghJiFacebook.mp3')
        print(f'{counter} out of {17} Done!!')
        counter+=1

goToFacebook()
file=open("C:\\Users\\gians\\Desktop\\CS\\pythons\\notGitStuff\\GianiSherSinghFaceBook\\theLinks.txt",'r')
videolinks=file.readlines()
vids=[i for i in videolinks]
download(vids[8:])
'''