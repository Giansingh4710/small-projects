import selenium
import urllib.request
from bs4 import BeautifulSoup as bs 
import requests
from datetime import datetime as dt
import os
import re

from selenium import webdriver
from time import sleep
options = webdriver.ChromeOptions()
#options.headless = True

def getKirtanSewaAudios():
    link1='http://kirtansewa.net/index.php/bhai-gurmail-singh-amritsar/'
    browser = webdriver.Chrome('C:/Users/gians/Desktop/stuff/chromedriver_win32/chromedriver.exe',options=options)
    browser.get(link1)
    cont=browser.find_element_by_class_name('entry-content')
    ptags=cont.find_elements_by_tag_name('p')

    atags=[]
    for i in ptags:
        try:
            a=i.find_element_by_tag_name('a')
            if a:
                atags.append(a)
        except Exception as e:
            #print(e)
            continue

    href=[(i.text,i.get_attribute('href')) for i in atags]
    return(href)


def download(links,folderPath):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36')]
    urllib.request.install_opener(opener)
    for i in links:
        title=i[0]+".mp3"
        link=i[1]

        urllib.request.urlretrieve(link,f'{folderPath}{title}')
        print(f'{title} - {link}')

links=getKirtanSewaAudios()
folder="C:/Users/gians/Desktop/test/kirtanSewa/"
download(links,folder)
