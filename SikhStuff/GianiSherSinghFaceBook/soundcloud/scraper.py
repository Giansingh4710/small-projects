from selenium import webdriver
import time,os
from bs4 import BeautifulSoup as bs
import urllib.request 

options = webdriver.ChromeOptions()
# options.headless = True

def linksToPlayLists(): #gets all the links to the playlists in soundcloud
    br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
    url="https://soundcloud.com/gianishersinghjiambala/sets"
    br.get(url)
    #time.sleep(4)
    scroll=0
    end=False
    while not end:
        firstScroll=br.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        if firstScroll==scroll:
            end=True
        else:
            scroll=firstScroll
    content=br.page_source.encode('utf-8').strip()
    soup=bs(content,"lxml")
    allPlaylists=soup.find("div",class_="userMain__content")
    allPlaylists=allPlaylists.find_all("li",class_="soundList__item")
    playlistLinks=[]
    f=open("./soundcloud/playlistLinks.txt","w")
    for playlist in allPlaylists:
        atag=playlist.find("a",class_="soundTitle__title sc-link-dark sc-link-secondary")
        theLinkWithTitle=(atag.text.strip(),"https://soundcloud.com"+atag["href"])
        playlistLinks.append(theLinkWithTitle)
        f.write(atag.text.strip()+" : "+"https://soundcloud.com"+atag["href"]+"\n")
    f.close()
    br.close()
    return playlistLinks

def linksInPlaylist(playlists): #gets all the individual katha links inside the playlists
    # f=open("./soundcloud/playlistLinks.txt","r")
    # playlists=f.readlines()
    # playlists=[i.split(" : ") for i in playlists]
    d={}
    for playlist in playlists:
        title=playlist[0]
        link=playlist[1]
        links=getLinksForPlaylist(link) #list of tuples where index 0 is title of link and index 1 is link
        d[title]=links
    return d

def getLinksForPlaylist(link): #gets links for katha in a playlist. This func is used for the func above
    br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
    br.get(link)
    scroll=0
    end=False
    while not end:
        firstScroll=br.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(1)
        if firstScroll==scroll:
            end=True
        else:
            scroll=firstScroll
    atags=br.find_elements_by_css_selector("div > div.trackItem__content.sc-truncate > a")
    links=[(i.text,i.get_attribute('href')) for i in atags]
    br.close()
    return links



def downloadLinksInPlaylist(directory,obj):
    for playlist in obj:
        newPlace=f"{directory}{playlist}\\"
        os.mkdir(newPlace)
        for track in obj[playlist]:
            try:
                downloadLink(newPlace,track)
            except Exception:
                print(f"No Download - {track}")

def downloadLink(dir,track):
    br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
    theUrl="https://soundcloudtomp3.app"
    br.get(theUrl)
    # time.sleep(5)
    entry=br.find_element_by_css_selector("body > div.jumbotron > div > center > form > div > input")
    entry.send_keys(track[1]) #track[1] is the soundcloud url link of katha
    button=br.find_element_by_css_selector("#fd")
    button.click()

    print("After download clicked !!!!!")
    atag=br.find_elements_by_xpath('//*[@id="dlMP3"]')
    theDownloadLink=atag[2].get_attribute("href")
    urllib.request.urlretrieve(theDownloadLink,f'{dir}{track[0]}.mp3')
    time.sleep(1)
    br.close()

dir="C:\\Users\\gians\\Desktop\\test\\"
# lst=linksToPlayLists()
# d=linksInPlaylist(lst) # d returns a dict where keys are title of playist and the items are a list of tuples(size 2) when index 0 is title of track and index 1 is link of track
# print(d)
# downloadLinksInPlaylist(dir,d)
# f=open("./soundcloud/obj.txt","w",encoding="utf-8")
# f.write(str(d))
# f.close()


obj={
    'Sri Pracheen Panth Prakash Katha (Audio Edited)': 
        [
            ('Sri Pracheen Panth Prakash (Part 1) - ਅੰਗਰੇਜ਼ਾਂ ਨੇ ਸਿੱਖਾਂ ਦਾ ਹਾਲ ਪੁਛਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-1?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 2) - ਸੱਚੇ ਸਿੱਖ ਇਤਿਹਾਸ ਲੱਭਣ ਦੀ ਕੋਸ਼ਿਸ਼', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-2?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 3) - ਸ੍ਰੀ ਗੁਰੂ ਨਾਨਕ ਦੇਵ ਜੀ ਅਵਤਾਰ, ਬਾਲ-ਚੋਜ ਤੇ ਵਿਆਹ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-3?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 4) - ਮੋਦੀ ਖਾਨਾ ਤੇ ਵੇਂਈ ਪ੍ਰਵੇਸ਼', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-4?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 5) - ਸਾਖੀ ਨੌਰੰਗੇ ਪਾਤਿਸ਼ਾਹ ਕੀ ਜੁਲਮੀ ਕੀ ਲਿਖਯਤੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-5?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 6) - ਸਾਖੀ ਦਸਮੇ ਪਾਤਸ਼ਾਹਿ ਕੀ ਲਿਖਯਤੇ, ਖਾਲਸਾ ਕਿਉਂ ਸਾਜਿਆ?', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-6?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 7) - ਖਾਲਸਾ ਪੰਥ ਪਰਸਨ ਕੀ ਸਾਖੀ, ਖਾਲਸੇ ਦਾ ਵਾਧਾ ਤੇ ਰਾਜ ਦਾ ਵਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-7?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 8) - ਬਾਬਾ ਬੰਦਾ ਸਿੰਘ ਬਹਾਦਰ, ਸਾਖੀ ਪਿੰਡ ਸੇਹਰ ਖੰਡੇ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-8?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 9) - ਸਾਖੀ ਪ੍ਰਸੰਗ ਮਲੇਰੀਏ, ਚਪੜ ਚਿੜੀ ਜੰਗ, ਵਜੀਦ ਖਾਂ ਮਾਰਿਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-9?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 10) - ਬੰਦਾ ਕੈਦ ਕਰਕੇ ਦਿੱਲੀ ਭੇਜਿਆ, ਬੰਦੇ ਦੀ ਮੌਤ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-10?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 11) - ਸਾਖੀ ਸ਼ਹੀਦ ਤਾਰਾ ਸਿੰਘ ਨਿਹੰਗ ਦੰਗਈ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-11?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 12) - ਤਾਰਾ ਸਿੰਘ ਨਿਹੰਗ ਸ਼ਹੀਦ ਦੀ ਤਿਆਰੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-12?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 13) - ਤੁਰਕਾਂ ਨਾਲ ਲੜ ਕੇ ਤਾਰਾ ਸਿੰਘ ਨੇ ਸ਼ਹੀਦੀ ਪਾਈ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-13?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 14) - ਸਾਖੀ ਚਮੁੰਡੇ ਤਥਾ ਕੈਰੋਂ ਨੰਗਲੀਆਂ ਰੰਧਾਵਿਆਂ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-14?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 15) - ਕਪੂਰ ਸਿੰਘ ਕੋ ਨਵਾਬੀ ਮਿਲਨ ਕਾ ਪ੍ਰਸੰਗ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-15?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 16) - ਅਕਾਲੀ ਨਿਹੰਗ ਕਪੂਰ ਸਿੰਘ ਨੂੰ ਨਵਾਬੀ ਦਿਤੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-16?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 17) - ਨਵਾਬ ਕਪੂਰ ਸਿੰਘ ਨੇ ਖਾਲਸੇ ਦੇ ਪੰਜ ਜਥੇ ਬਣਾਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-17?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 18) - ਸਾਖੀ ਨਵਾਬ ਕਪੂਰ ਸਿੰਘ ਭੁਜੰਗੀ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-18?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 19) - ਸਾਖੀ ਸ਼ਹੀਦੀ ਭਾਈ ਮਨੀ ਸਿੰਘ ਜੀ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-19?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 20) - ਸਾਖੀ ਸ਼ਹੀਦੀ ਭਾਈ ਮਨੀ ਸਿੰਘ ਜੀ ਕੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-20?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 21) - ਸਾਖੀ ਸ਼ਹੀਦੀ ਭਾਈ ਮਨੀ ਸਿੰਘ ਜੀ ਕੀ ੩', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-21?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 22) - ਸਾਖੀ ਨਾਦਰ ਸ਼ਾਹ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-22?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 23) - ਨਾਦਰ ਸ਼ਾਹ ਨੇ ਖ਼ਾਨ ਬਹਾਦਰ ਤੋਂ ਸਿੰਘਾ ਦੇ ਹਾਲ ਪੁੱਛਣੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-23?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 24) - ਮਤਾਬ ਸਿੰਘ, ਸੁੱਖਾ ਸਿੰਘ ਨੇ ਮੱਸੇ ਦਾ ਸਿਰ ਵੱਢਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-24?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 25) - ਸਾਖੀ ਬੋਤਾ ਸਿੰਘ ਸ਼ਹੀਦ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-25?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 26) - ਭਾਈ ਸੁੱਖਾ ਸਿੰਘ ਦੀ ਆਦ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-26?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 27) - ਭਾਈ ਸੁੱਖਾ ਸਿੰਘ ਦਾ ਇਕ ਗਿਲਜੇ ਨਾਲ ਦੁੰਦ ਯੁੱਧ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-27?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 28) - ਭਾਈ ਸੁੱਖਾ ਸਿੰਘ ਦਿਨ ਦਿਹਾੜੇ ਅੰਮ੍ਰਿਤਸਰ ਇਸ਼ਨਾਨ ਕਰਨਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-28?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 29) - ਖੱਡ ਵਿਚ ਸਿੰਘ ਲੁਕੇ ਤੱਕ, ਤੁਰਕਾਂ ਨੇ ਖੱਡ ਨੂੰ ਅੱਗ ਲਾਉਣੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-29?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 30) ਭਾਈ ਸੁਬੇਗ ਸਿੰਘ ਤੇ ਉਸ ਦੇ ਸਪੁਤ੍ਰ ਦੀ ਗ੍ਰਿਫ਼ਤਾਰੀ ਦੇ ਕਸ਼ਟ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-30?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 31) - ਸਾਖੀ ਭਾਈ ਤਾਰੂ ਸਿੰਘ ਭੁਜੰਗੀ ਬਿਦੇਹੀ ਸ਼ਹੀਦ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-31?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 32) - ਭਾਈ ਤਾਰੂ ਸਿੰਘ ਦੀ ਗ੍ਰਿਫ਼ਤਾਰੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-32?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 33) - ਬਾਬਰ ਦੇ ਹਿੰਦ ਵਿਚ ਆਉਣ ਦਾ ਕਾਰਨ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-33?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 34) - ਬਾਬਰ ਨੂੰ ਪਾਤਸ਼ਾਹੀ ਗੁਰੂ ਜੀ ਨੇ ਦਿੱਤੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-34?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 35) - ਬਾਬਰ ਨੂੰ ਪਾਤਸ਼ਾਹੀ ਗੁਰੂ ਜੀ ਨੇ ਦਿੱਤੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-35?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 36) - ਬਾਬਰ ਨੂੰ ਪਾਤਸ਼ਾਹੀ ਗੁਰੂ ਜੀ ਨੇ ਦਿੱਤੀ ੩', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-36?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 37) - ਬਾਬਰ ਨੂੰ ਪਾਤਸ਼ਾਹੀ ਗੁਰੂ ਜੀ ਨੇ ਦਿੱਤੀ ੪', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-37?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 38) - ਸ਼ਹੀਦੀ ਭਾਈ ਮਤਾਬ ਸਿੰਘ ਜੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-38?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 39) - ਭਾਈ ਤਾਰੂ ਸਿੰਘ ਜੀ ਦਾ ਸ਼ਹੀਦ ਹੋਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-39?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 40) - ਨਵਾਬ ਦਾ ਪਿਸ਼ਾਬ ਬੰਦ ਹੋਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-40?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 41) - ਨਵਾਬ ਦੀ ਮੌਤ ਤੇ ਸੁਬੇਗ ਸਿੰਘ ਜੰਬਰ ਦਾ ਸਿੱਕਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-panth-prakash-part-41?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 42) - ਸਾਖੀ ਜਸੂ ਬਧੇ ਕੀ ਚਲੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-42?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 43) - ਸਾਖੀ ਜਸੂ ਬਧੇ ਕੀ ਚਲੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-parkash-part-43?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 44) - ਛੋਟਾ ਘੱਲੂਘਾਰਾ ਪੜੋਲ ਕਠੂਹੇ ਵਾਲਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-44?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 45) - ਛੋਟਾ ਘੱਲੂਘਾਰਾ ਪੜੋਲ ਕਠੂਹੇ ਵਾਲਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-45?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 46) - ਛੋਟਾ ਘੱਲੂਘਾਰਾ ਪੜੋਲ ਕਠੂਹੇ ਵਾਲਾ ੩', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-46?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 47) - ਛੋਟਾ ਘੱਲੂਘਾਰਾ ਪੜੋਲ ਕਠੂਹੇ ਵਾਲਾ ੪', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-47?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 48) - ਛੋਟਾ ਘੱਲੂਘਾਰਾ ਪੜੋਲ ਕਠੂਹੇ ਵਾਲਾ ੫', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-48?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 49) - ਅਹਿਮਦ ਸ਼ਾਹ ਦਾ ਹਮਲਾ, ਲੱਖੂ ਸਿੰਘਾਂ ਦੇ ਹਵਾਲੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-49?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 50) - ਰਾਮ ਰੌਣੀ ਦਾ ਬਨਣਾ ਤੇ ਉਸ ਪਰ ਅਦੀਨਾਂ ਬੇਗ ਦਾ ਹਮਲਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-parkash-part-50?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 51) - ਰਾਮ ਰੌਣੀ ਦਾ ਬਨਣਾ ਤੇ ਉਸ ਪਰ ਅਦੀਨਾਂ ਬੇਗ ਦਾ ਹਮਲਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-parkash-part-51?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 52) - ਕੌੜਾ ਮੱਲ ਨੇ ਸਿੰਘਾਂ ਦੀ ਕੁਮਕ ਨਾਲ ਸ਼ਾਹ ਨਿਵਾਜ਼ ਨੂੰ ਮਾਰਿਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-52?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 53) - ਖਾਲਸੇ ਵਿਚ ਫੁੱਟ, ਸੁੱਖਾ ਸਿੰਘ ਸ਼ਹੀਦ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-53?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 54) - ਆਦੀਨਾ ਬੇਗ ਤੇ ਸੋਢੀ ਬਢਭਾਗ ਸਿੰਘ, ਜਲੰਧਰ ਕਤਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-54?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 55) - ਆਦੀਨਾ ਬੇਗ ਤੇ ਸੋਢੀ ਬਢਭਾਗ ਸਿੰਘ, ਜਲੰਧਰ ਕਤਲ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-55?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 56) - ਆਦੀਨਾ ਬੇਗ ਤੇ ਸੋਢੀ ਬਢਭਾਗ ਸਿੰਘ, ਜਲੰਧਰ ਕਤਲ ੩', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-56?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 57) - ਸਰਹੰਦ ਲੁੱਟਣੀ ਤੇ ਮਰਹੱਟਿਆਂ ਨਾਲ ਮੁੱਠਭੇੜ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-57?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 58) - ਸਦੀਕ ਬੇਗ ਸਰਹੰਦੀ ਨਾਲ ਮੁਕਾਬਲਾ ਤੇ ਫੇਰ ਸੁਲਹ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-58?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 59) - ਸਾਖੀ ਤੁਰਕ ਸਰਬਤ ਹਿੰਦੁਸਤਾਨੀ ਔ ਗਿਲਜੋ਼ਂ ਕੀ, ਹਾਠੂ ਸਿੰਘ ਮਝੈਲ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-59?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 60) - ਮਿੱਤ ਸਿੰਘ ਦਾ ਸ਼ਹੀਦ ਹੋਣਾ, ਜਹਾਨ ਖ਼ਾਂ ਨਾਲ ਟਾਕਰਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-60?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 61) - ਦਾਦੂ ਰਾਮ ਸਾਧ ਨੂੰ ਕਸ਼ਟ, ਮੀਰ ਮੰਨੂੰ ਦੀ ਮੌਤ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-61?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 62) - ਮਥਰਾ ਲੁੱਟੀ ਤੇ ਅਲੀਗੜ੍ਹ ਦਾ ਕਿਲ੍ਹਾ ਮਾਰਿਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-62?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 63) - ਅਥ ਸਾਖੀ ਘੱਲੂਘਾਰੇ ਮਲੇਰ ਔ ਕੁਪਰਹੀੜੇ ਕੇ ਤੁਰੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-63?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 64) - ਅਥ ਸਾਖੀ ਘੱਲੂਘਾਰੇ ਮਲੇਰ ਔ ਕੁਪਰਹੀੜੇ ਕੇ ਤੁਰੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-64?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 65) - ਅਥ ਸਾਖੀ ਘੱਲੂਘਾਰੇ ਮਲੇਰ ਔ ਕੁਪਰਹੀੜੇ ਕੇ ਤੁਰੀ ੩', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-65?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 66) - ਅਥ ਸਾਖੀ ਘੱਲੂਘਾਰੇ ਮਲੇਰ ਔ ਕੁਪਰਹੀੜੇ ਕੇ ਤੁਰੀ ੪', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-66?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 67) - ਵੈਰਾੜਾ ਤੇ ਖਾਲਸੇ ਦੀ ਅਣਬਣ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-67?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 68) - ਕਪੂਰੇ ਦਾ ਫਾਹੇ ਲੱਗਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-68?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 69) - ਮੁਰੰਡੇ ਦੇ ਰੰਘੜਾਂ ਦੀ ਸੋਧ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-69?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 70) - ਕਸੂਰ ਮਾਰ ਕੇ ਬ੍ਰਾਹਮਣ ਦੀ ਬ੍ਰਾਹਮਣੀ ਦਿਵਾਈ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-70?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 71) - ਕਸੂਰ ਮਾਰ ਕੇ ਬ੍ਰਾਹਮਣ ਦੀ ਬ੍ਰਾਹਮਣੀ ਦਿਵਾਈ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-71?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 72) - ਕਸੂਰ ਵਿਚ ਦਿਲੇ ਰਾਮ ਦਾ ਸਰਬੰਸ ਨਾਸ਼', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-72?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 73) - ਕਸੂਰ ਵਿਚ ਦਿਲੇ ਰਾਮ ਦਾ ਸਰਬੰਸ ਨਾਸ਼ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-73?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 74) - ਆਗੈ ਮੁਲਖ ਮੱਲਨ ਕੀ ਸਾਖੀ ਤੁਰੀ । ਬੁੱਢਾ ਤੇ ਤਰਨਾਂ ਦਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-74?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'),  ('Sri Pracheen Panth Prakash (Part 75) - ਸਾਖੀ ਨਵਾਬ ਸਰ ਬੁਲੰਦ ਫੜਨੇ ਕੀ ਤੁਰੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-75?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 76) - ਸਾਖੀ ਸਿਰਹੰਦ ਮੱਲਨੇ ਕੀ ਔਰ ਨਿਬਾਬ ਜੈਨੇ ਮਾਰਨ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-76?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 77) - ਸਰਹੰਦ ਵਿਖੇ ਦੇਹੁਰੇ ਬਣਵਾਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-77?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 78) - ਸਾਖੀ ਨਿਹੰਗ ਭੁਜੰਗੀ ਗੁਰਬਖ਼ਸ਼ ਸਿੰਘ ਸ਼ਹੀਦ ਜੀ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-78?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 79) - ਸਾਖੀ ਨਿਹੰਗ ਭੁਜੰਗੀ ਗੁਰਬਖ਼ਸ਼ ਸਿੰਘ ਸ਼ਹੀਦ ਜੀ ਕੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-79?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha'), 
            ('Sri Pracheen Panth Prakash (Part 80) - ਔਰ ਸਾਖੀ ਮਾਲਵੇ ਕੀ ਤੁਰੀ । ਗ੍ਰੰਥ ਸਮਾਪਤੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-pracheen-panth-prakash-part-80?in=gianishersinghjiambala/sets/sri-guru-panth-prakash-katha')
        ], 
    'Zafarnama Katha - Sri Dasam Guru Granth Sahib Ji': 
        [
            ('Sri Zafarnama Sahib Katha (Part 1)', 'https://soundcloud.com/gianishersinghjiambala/sri-dasam-guru-granth-sahib-ji-katha-4?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 2)', 'https://soundcloud.com/gianishersinghjiambala/sri-dasam-guru-granth-sahib-ji-katha-5?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 3)', 'https://soundcloud.com/gianishersinghjiambala/sri-dasam-guru-granth-sahib-ji-katha-6?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 4)', 'https://soundcloud.com/gianishersinghjiambala/sri-dasam-guru-granth-sahib-ji-katha-7?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 5)', 'https://soundcloud.com/gianishersinghjiambala/sri-dasam-guru-granth-sahib-ji-katha-8?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 6)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-06-2013-08-17?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 7)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-07?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 8)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-08?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 9)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-09?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 10)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-10?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru'), 
            ('Sri Zafarnama Sahib Katha (Part 11)', 'https://soundcloud.com/gianishersinghjiambala/zafarnama-katha-part-11?in=gianishersinghjiambala/sets/zafarnama-katha-sri-dasam-guru')
        ], 
    'Sri Japji Sahib Katha': 
        [
            ('Sri Japji Sahib Katha (Part 1) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-1?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 2) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-2?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 3) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-3?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 4) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-4?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 5) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-5?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 6) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-6?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 7) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-7?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 8) - ਸ੍ਰੀ ਮੂਲ ਮੰਤਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-8?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 9) - ਮੰਨੇ ਕੀ ਗਤਿ ਕਹੀ ਨ ਜਾਇ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-9?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'),  
            ('Sri Japji Sahib Katha (Part 10) - ਮੰਨੈ ਮਾਰਗਿ ਠਾਕ ਨ ਪਾਇ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-10?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 11) - ਮੰਨੈ ਪਾਵਹਿ ਮੋਖੁ ਦੁਆਰੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-11?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 12) - ਪੰਚ ਪਰਵਾਣ ਪੰਚ ਪਰਧਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-12?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 13) - ਪੰਚ ਪਰਵਾਣ ਪੰਚ ਪਰਧਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-13?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 14) - ਅਸੰਖ ਜਪ ਅਸੰਖ ਭਾਉ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-14?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'),  
            ('Sri Japji Sahib Katha (Part 15) - ਅਸੰਖ ਨਾਵ ਅਸੰਖ ਥਾਵ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-15?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 16) - ਤੀਰਥੁ ਤਪੁ ਦਇਆ ਦਤੁ ਦਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-16?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 17) - ਤੀਰਥੁ ਤਪੁ ਦਇਆ ਦਤੁ ਦਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-17?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 18) - ਤੀਰਥੁ ਤਪੁ ਦਇਆ ਦਤੁ ਦਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-18?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 19) - ਤੀਰਥੁ ਤਪੁ ਦਇਆ ਦਤੁ ਦਾਨੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-19?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'),  
            ('Sri Japji Sahib Katha (Part 20) - ਅੰਤੁ ਨ ਸਿਫਤੀ ਕਹਣਿ ਨ ਅੰਤੁ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-20?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 21) - ਬਹੁਤਾ ਕਰਮੁ ਲਿਖਿਆ ਨਾ ਜਾਇ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-21?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 22) - ਅਮੁਲ ਗੁਣ ਅਮੁਲ ਵਾਪਾਰ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-22?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 23) - ਅਮੁਲ ਗੁਣ ਅਮੁਲ ਵਾਪਾਰ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-23?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 24) - ਅਮੁਲ ਗੁਣ ਅਮੁਲ ਵਾਪਾਰ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-24?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 25) - ਅਮੁਲ ਗੁਣ ਅਮੁਲ ਵਾਪਾਰ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-25?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 26) - ਅਮੁਲ ਗੁਣ ਅਮੁਲ ਵਾਪਾਰ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-26?in=gianishersinghjiambala/sets/sri-japji-sahib-katha'), 
            ('Sri Japji Sahib Katha (Part 27) - ਸੋ ਦਰੁ ਕੇਹਾ ਸੋ ਘਰੁ ਕੇਹਾ ।।', 'https://soundcloud.com/gianishersinghjiambala/sri-japji-sahib-katha-part-27?in=gianishersinghjiambala/sets/sri-japji-sahib-katha')
        ], 
    'Sri Guru Tegh Bahadur Sahib Ji Katha': 
        [
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 1) - ਬਕਾਲੇ ਵਿਖੇ ਬਾਈ ਸੋਢੀ ਗੁਰੂ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-1?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 2) - ਭਾਈ ਗੜ੍ਹੀਆ ਤੇ ਦ੍ਵਾਰਕਾ ਦਾਸ ਬਕਾਲੇ ਆਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-2?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 3) - ਮੱਖਣ ਸ਼ਾਹ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-3?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 4) - ਮੱਖਣ ਸ਼ਾਹ ਬਕਾਲੇ ਪਹੁੰਚੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-4?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 5) - ਮੱਖਣ ਸ਼ਾਹ ਬਕਾਲੇ ਵਿਚ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-5?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 6) - ਮਾਤਾ ਨਾਨਕੀ ਜੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-6?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 7) - ਮੱਖਣ ਸ਼ਾਹ ਤੇ ਸ਼੍ਰੀ ਗੁਰੂ ਤੇਗ ਬਹਾਦਰ ਸਾਹਿਬ ਜੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-7?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 8) - ਗੁਰੂ ਜੀ ਦਾ ਪ੍ਰਗਟ ਹੋਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-9-part-8?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 9) - ਮੱਖਣ ਸ਼ਾਹ ਨੇ ਗੁਰੂ ਜੀ ਨੂੰ ਪ੍ਰਗਟ ਕਰ ਦਿੱਤਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-9-part-9?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 10) - ਸੋਢੀਆਂ ਦੀ ਈਰਖਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-10?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 11) - ਧੀਰਮੱਲ ਵਲੋਂ ਗੋਲੀ ਚਲਾਉਣ ਦੀ ਗੋਂਦ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-11?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 12) - ਧੀਰਮੱਲ ਵਲੋਂ ਹੋਰ ਵਿਰੋਧ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-12?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 13) - ਧੀਰਮੱਲ ਵਲੋਂ ਗੋਲੀ ਚਲੀ ਤੇ ਲੁਟ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-13?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 14) - ਧੀਰਮੱਲ ਦੀ ਕਠੋਰਤਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-15?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 15) - ਮੱਖਣ ਸ਼ਾਹ ਦਾ ਕ੍ਰੋਧ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-16?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 16) - ਮੱਖਣ ਸ਼ਾਹ ਦਾ ਸ਼ੀਹੇਂ ਮਸੰਦ ਨੂੰ ਦੰਡ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-17?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 17) - ਮੱਖਣ ਸ਼ਾਹ ਨੂੰ ਗੁਰੂ ਜੀ ਦਾ ਵਣਜਾਰਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-18?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 18) - ਮੱਖਣ ਸ਼ਾਹ ਨੂੰ ਗੁਰੂ ਜੀ ਦਾ ਵਣਜਾਰਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-19?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 19) - ਘਰ ਵਿਚ ਵਿਚਾਰ ਤੇ ਗੁਰੂ ਜੀ ਦਾ ਉਪਦੇਸ਼', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-20?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 20) - ਧੀਰਮੱਲ ਦੀਆਂ ਚੀਜ਼ਾਂ ਮੋੜੀਆਂ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-21?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 21) - ਧੀਰਮੱਲ ਦੀ ਵਾਪਸੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-22?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 22) - ਮੱਖਣ ਸ਼ਾਹ ਤੇ ਗੁਰੂ ਜੀ ਸ਼੍ਰੀ ਅਮ੍ਰਿਤਸਰ ਗਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-23?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 23) - ਸ਼੍ਰੀ ਅਮ੍ਰਿਤਸਰ ਤੋਂ ਵੱਲੇ ਗਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-24?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 24) - ਸ਼੍ਰੀ ਗੁਰੂ ਜੀ ਦਾ ਬਕਾਲੇ ਤੋਂ ਕੂਚ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-25?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 25) - ਸ਼੍ਰੀ ਗੁਰੂ ਗ੍ਰੰਥ ਜੀ ਜਲ ਵਿਚ ਰੱਖੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-26?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 26) - ਧੀਰਮੱਲ ਨੂੰ ਸੁਨੇਹਾ ਪੁੱਜਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-27?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 27) - ਧੀਰਮੱਲ ਨੂੰ ਬੀੜ ਦਾ ਮਿਲਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-28?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 28) - ਅਨੰਦਪੁਰ ਵਸਾਉਣ ਵਾਲੀ ਥਾਂ ਆਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-29?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 29) - ਮੱਖਣ ਸ਼ਾਹ ਵਿਦਾ, ਸ਼੍ਰੀ ਅਨੰਦਪੁਰ ਵਸਾਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-30?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 30) - ਮਾਖੋ ਦੈਂਤ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-31?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 31) - ਇਕ ਪੀਰ ਦਾ ਸੰਸਾ ਦੂਰ ਕੀਤਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-32?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 32) - ਗੁਰੂ ਜੀ ਦੀ ਮਹਿਮਾ, ਧੀਰਮੱਲ ਦੀ ਈਰਖਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-33?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 33) - ਧੀਰਮੱਲ ਰਾਮਰਾਇ ਮੇਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-34?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 34) - ਗੁਰੂ ਜੀ ਦਾ ਤੀਰਥਾਂ ਨੂੰ ਪਵਿਤ੍ਰ ਕਰਨ ਜਾਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-35?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 35) - ਮੂਲੋਵਾਲ ਦਾ ਮਈਆ ਤੇ ਗੋਂਦਾ, ਸ਼ੇਖੇ ਦਾ ਤਿਲੋਕਾ ਜਿਵੰਦਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-36?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 36) - ਹਡਿਆਏ ਨਗਰ ਵਿਚ ਤਾਪ ਦੇ ਰੋਗੀ ਅਰੋਗ ਕੀਤੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-37?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 37) - ਹਡਿਆਏ ਨਗਰ ਵਿਚ ਤਾਪ ਦੇ ਰੋਗੀ ਅਰੋਗ ਕੀਤੇ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-38?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 38) - ਭੰਦੇਹਰੀ, ਅਲੀਸ਼ੇਰ, ਜੋਗੇ, ਭੂਪਾਲੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 39) - ਖੀਵਾ, ਭਿੱਖੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-40?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 40) - ਦੇਸ ਰਾਜ, ਖਯਾਲਾ ਗ੍ਰਾਮ, ਦਮਦਮਾ, ਮੌੜ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-41?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 41) - ਦੇਸ ਰਾਜ ਦਾ ਅੰਤ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-42?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 42) - ਸੂਲੀਸਰ ਵਿਚ ਚੋਰ ਨੂੰ ਸੂਲੀ, ਬਰੇ ਪਿੰਡ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-43?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'),  
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 43) - ਭਰੇ, ਗੋਬਿੰਦ ਪੁਰੇ, ਗਾਗੇ, ਗੁਰਨੇ, ਮਕਰੋੜ, ਧਮਧਾਣ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-44?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 44) - ਮੇਹੇਂ ਦੀ ਘਾਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-45?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 45) - ਧਮਧਾਣ ਦਾ ਰਾਹਕ, ਤਿਖਾਣ ਸਿੱਖ, ਕੈਂਥਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-46?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 46) - ਧਮਧਾਣ ਦਾ ਰਾਹਕ, ਤਿਖਾਣ ਸਿੱਖ, ਕੈਂਥਲ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-47?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 47) - ਬਾਰਨੇ ਦੇ ਕਿਸਾਨ ਤੋਂ ਤੰਬਾਕੂ ਛੁਡਵਾਇਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-48?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 48) - ਥਾਨੇ���ਰ ਦਾ ਮੇਲਾ, ਬਣੀ ਬਦਰਪੁਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-49?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 49) - ਥਾਨੇਸਰ ਦਾ ਮੇਲਾ, ਬਣੀ ਬਦਰਪੁਰ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-50?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 50) - ਪੂਰਬ ਦੀ ਸੰਗਤ ਦੀ ਸਿੱਕ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-51?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 51) - ਕੜੇ ਪਿੰਡ ਦਾ ਮਲੂਕ ਦਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-52?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 52) - ਗੁਰੂ ਜੀ ਤ੍ਰਿਬੈਣੀ ਪੁੱਜੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-53?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 53) - ਹੇਮ ਕੁੰਟ ਦੀ ਸੋ਼ਭਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-54?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 54) - ਬ੍ਰਹਮਾ ਵਲੋਂ ਦੇਵਤਿਆਂ ਪ੍ਰਤਿ ਪੁਰਾਤਨ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-55?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 55) - ਬ੍ਰਹਮਾ ਵਲੋਂ ਦੇਵਤਿਆਂ ਪ੍ਰਤਿ ਪੁਰਾਤਨ ਕਥਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-56?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 56) - ਬ੍ਰਹਮਾ ਦਾ ਪੁਰਾਤਨ ਕਥਾ ਸੁਨਾਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-57?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 57) - ਬ੍ਰਹਮਾ ਦਾ ਪੁਰਾਤਨ ਕਥਾ ਸੁਨਾਉਣਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-58?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 58) - ਅਕਾਲ ਪੁਰਖ ਪਾਸੋਂ ਵਿਦੈਗੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-59?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 59) - ਤ੍ਰਿਬੈਣੀ ਵਿਖੇ ਨਿਵਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-60?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 60) - ਪ੍ਰਯਾਗ ਤੋਂ ਕਾਂਸ਼ੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-61?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 61) - ਪ੍ਰਯਾਗ ਤੋਂ ਕਾਂਸ਼ੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-62?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 62) - ਸਸਰਾਮ ਚਾਚੇ ਫੱਗੋ ਦੇ ਘਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-63?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 63) - ਸਸਰਾਮ ਡੇਰਾ, ਬੇਰੀ, ਬਾਗ਼ ਵਿਚ ਨਿਵਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-64?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 64) - ਗਯਾ ਤੀਰਥ, ਜੈਤਾ ਸੇਠ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-66?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji'), 
            ('Sri Guru Tegh Bahadur Sahib Ji (Part 65) - ਪਟਨੇ ਨਿਵਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-tegh-bahadur-sahib-ji-part-65?in=gianishersinghjiambala/sets/sri-guru-tegh-bahadur-sahib-ji')
        ], 
    'Sri Guru Harkrishan Sahib Ji Katha': 
        [
            ('Sri Guru Harkrishan Sahib Ji (Part 1) - ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਸਾਹਿਬ ਜੀ ਤਖ਼ਤ ਤੇ ਬੈਠੇ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-8-part-1?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 2) - ਮਸੰਦਾਂ ਨੇ ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਨੂੰ ਸਮਝਾਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-8-part-2?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 3) - ਮਸੰਦਾਂ ਨੇ ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਨੂੰ ਸਮਝਾਉਣਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-3?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 4) - ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਜੀ ਦਾ ਪ੍ਰਤਾਪ ਤੇ ਰਾਮਰਾਇ ਦੀ ਈਰਖਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-4?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 5) - ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਦਾ ਬਾਦਸ਼ਾਹ ਨੂੰ ਮਿਲਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-5?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 6) - ਨੌਰੰਗਾ ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਜੀ ਨੂੰ ਬਲਾਉਣ ਵਿਚਾਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-6?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 7) - ਨੌਰੰਗਾ ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਜੀ ਨੂੰ ਬਲਾਉਣ ਵਿਚਾਰ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-7?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'),  
            ('Sri Guru Harkrishan Sahib Ji (Part 8) - ਸਤਿਗੁਰੂ ਜੀ ਨੂੰ ਲੈਣ ਜੈ ਸਿੰਘ ਦਾ ਦੂਤ ਗਿਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-8?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 9) - ਪਰਧਾਨ ਗੁਰੂ ਜੀ ਪਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-9?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 10) - ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਜੀ ਦਾ ਦਿੱਲੀ ਨੂੰ ਜਾਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-10?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 11) - ਸੰਗਤਾਂ ਦੇ ਮੇਲੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-11?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 12) - ਝੀਵਰ ਤੋਂ ਗੀਤਾ ਦੇ ਅਰਥ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-12?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 13) - ਗੁਰੂ ਜੀ ਦਿੱਲੀ ਪੁੱਜੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-13?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 14) - ਦਿੱਲੀ ਵਿਖੇ ਨਿਵਾਸ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-14?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 15) - ਗੁਰੂ ਜੀ ਦੀ ਮਹਿਮਾ ਸੁਣਕੇ ਰਾਮਰਾਇ ਦੀ ਈਰਖਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-15?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 16) - ਗੁਰੂ ਜੀ ਦੀ ਰਾਮਰਾਇ ਬਾਰੇ ਭਵਿੱਖਬਾਣੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-16?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 17) - ਸ਼ਹਿਜ਼ਾਦਾ ਭੇਟਾ ਲੈਕੇ ਆਇਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-17?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 18) - ਜੈ ਸਿੰਘ ਦੀ ਪਟਰਾਣੀ ਪ੍ਰੀਖਿਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-18?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 19) - ਜੈ ਸਿੰਘ ਗੁਰੂ ਜੀ ਨੂੰ ਲੈਣ ਆਇਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-19?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 20) - ਪਟਰਾਣੀ ਪਛਾਣੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-20?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 21) - ਰਾਜਾ ਸਿੱਖ ਹੋਇਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-21?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 22) - ਸ਼ਹਿਰ ਤੋਂ ਬਾਹਰ ਡੇਰਾ ਲੈ ਜਾਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-22?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 23) - ਸਰੀਰ ਨੂੰ ਖੇਚਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-23?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 24) - ਸੀਤਲਾ ਨਿਕਲੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-24?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 25) - ਸੰਗਤਾਂ ਨੂੰ ਉਪਦੇਸ਼', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-25?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 26) - ਸੰਗਤਾਂ ਨੂੰ ਉਪਦੇਸ਼ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-26?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 27) - ਸੱਚਖੰਡ ਚਲੇ ਗਏ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-27?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 28) - ਸਰੀਰ ਦਾ ਸਸਕਾਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-28?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 29) - ਸੰਗਤਿ ਵਿਚ ਵਿਚਾਰ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-29?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji'), 
            ('Sri Guru Harkrishan Sahib Ji (Part 30) - ਮਸੰਦਾਂ ਦਾ ਜ਼ੋਰ, ਗੁਰੂ ਜੀ ਦੀ ਭਾਲ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-harkrishan-sahib-ji-part-30?in=gianishersinghjiambala/sets/sri-guru-harkrishan-sahib-ji')
        ], 
    'Sri Guru Har Rai Sahib Ji Katha': 
        [
            ('Sri Guru Har Rai Sahib Ji (Part 1) - ਭਾਈ ਭਗਤੂ, ਭਾਈ ਫੇਰੂ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-1?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 2) - ਭਾਈ ਭਗਤੂ, ਭਾਈ ਫੇਰੂ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-2?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 3) - ਮੰਗਲਾਚਰਣ, ਸ੍ਰੀ ਗੁਰੂ ਹਰਿਰਾਇ ਜੀ ਨਿੱਤ ਕਰਮ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-3?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 4) - ਮੰਗਲਾਚਰਣ ਸਮਾਪਤ । ਬਾਦਸ਼ਾਹੀ ਲੋੜ, ਹਰੜ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-4?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 5) - ਬਾਦਸ਼ਾਹੀ ਲੋੜ, ਹਰੜ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-5?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 6) - ਬ੍ਰਿੱਧਾ ਪ੍ਰੇਮਣ ਦਾ ਪ੍ਰਸ਼ਾਦਿ ਛਕਿਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-6?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 7) - ਬ੍ਰਿੱਧਾ ਪ੍ਰੇਮਣ ਦਾ ਪ੍ਰਸ਼ਾਦਿ ਛਕਿਆ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-7?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 8) - ਬ੍ਰਿੱਧਾ ਪ੍ਰੇਮਣ ਸਮਾਪਤ । ਅਜਗਰ ਮੁਕਤ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-8?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 9) - ਭਾਈ ਗੋਂਦੇ ਦਾ ਧਿਆਨ ਮਗਨ ਚਰਨੀਂ ਲਿਵਲੀਨ ਹੋਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-9?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 10) - ਭਾਈ ਗੋਂਦੇ ਸਮਾਪਤ । ਸਿੱਖਾ ਨੂੰ ਉਪਦੇਸ਼', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-10?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 11) - ਸਿੱਖਾ ਨੂੰ ਉਪਦੇਸ਼ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-11?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 12) - ਸਿੱਖਾ ਨੂੰ ਉਪਦੇਸ਼ ਸਮਾਪਤ । ਰਾਜੇ ਹਾਥੀ ਮੰਗਣ ਆਏ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-12?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 13) - ਭਗਤ ਭਗਵਾਨ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-13?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 14) - ਭਗਤ ਭਗਵਾਨ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-14?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 15) - ਸ਼ਾਹਜਹਾਂ ਬੀਮਾਰ ਤੇ ਸ਼ਹਿਜ਼ਾਦੇ ਆਕੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-15?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 16) - ਸ਼ਾਹਜਹਾਂ ਬੀਮਾਰ ਤੇ ਸ਼ਹਿਜ਼ਾਦੇ ਆਕੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-16?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ("Sri Guru Har Rai Sahib Ji (Part 17) - ਸ਼ੁਜਾ ਮੁਹੰਮਦ 'ਤੇ ਚੜ੍ਹਾਈ", 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-17?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 18) - ਮੁਰਾਦਬਖ਼ਸ਼ ਨਾਲ ਜੰਗ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-18?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 19) - ਦਾਰਾਸ਼ਕੋਹ ਤੇ ਔਰੰਗਜ਼ੇਬ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-19?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 20) - ਸ਼ਾਹਜਹਾਂ ਨਜ਼ਰਬੰਦ, ਦਾਰਾ ਨੱਸ ਗਿਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-20?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 21) - ਦਾਰੇ ਦਾ ਸੌ਼ਕ ਨਾਮਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-21?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 22) - ਦਾਰੇ ਦਾ ਸੌ਼ਕ ਨਾਮਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-22?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 23) - ਗੁਰੂ ਜੀ ਗੋਇੰਦਵਾਲ ਤੇ ਖੰਡੂਰ ਸਾਹਿਬ ਆਏ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-23?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 24) - ਗੁਰੂ ਜੀ ਗੋਇੰਦਵਾਲ ਤੇ ਖੰਡੂਰ ਸਾਹਿਬ ਆਏ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-24?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 25) - ਦਾਰਾ ਤੇ ਗੁਰੂ ਜੀ ਦਾ ਮੇਲ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-25?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 26) - ਦਾਰਾਸ਼ਕੋਹ ਨੂੰ ਉਪਦੇਸ਼', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-26?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 27) - ਦਾਰਾਸ਼ਕੋਹ ਨੂੰ ਉਪਦੇਸ਼ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-27?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 28) - ਦਾਰਾ ਵਿਦਾ, ਨੌਰੰਗੇ ਨਾਲ ਜੰਗ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-28?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 29) - ਦਾਰਾ ਵਿਦਾ, ਨੌਰੰਗੇ ਨਾਲ ਜੰਗ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-29?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 30) - ਦਾਰਾਸ਼ਕੋਹ ਨੂੰ ਤਕੀਏ ਵਿਚੋਂ ਫੜਨਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-30?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 31) - ਦਾਰਾਸ਼ਕੋਹ ਨੂੰ ਤਕੀਏ ਵਿਚੋਂ ਫੜਨਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-31?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 32) - ਦਾਰਾਸ਼ਕੋਹ ਨੂੰ ਕਤਲ ਕਰਨਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-32?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 33) - ਸੰਤ ਸਰਮਦ ਦੀ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-33?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 34) - ਸਰਮਦ ਦਾ ਸ਼ਰ੍ਹਾ ਨੂੰ ਨਾ ਮੰਨਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-34?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 35) - ਸਰਮਦ ਕਤਲ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-35?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 36) - ਸਰਮਦ ਕਤਲ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-36?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 37) - ਔਰੰਗਜ਼ੇਬ ਦਾ ਵੇਸ਼ਵਾ ਤੇ ਸੂਫ਼ੀ ਫ਼ਕੀਰਾਂ ਨਾਲ ਸਲੂਕ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-37?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 38) - ਔਰੰਗਜ਼ੇਬ ਦਾ ਵੇਸ਼ਵਾ ਤੇ ਸੂਫ਼ੀ ਫ਼ਕੀਰਾਂ ਨਾਲ ਸਲੂਕ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-38?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 39) - ਬੇਨਵਾ ਫ਼ਕੀਰ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-39?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 40) - ਮਥੁਰਾ ਦੀ ਤਬਾਹੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-40?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 41) - ਮਥੁਰਾ ਦੀ ਤਬਾਹੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-41?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 42) - ਮਥੁਰਾ ਦੀ ਤਬਾਹੀ ੩', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-42?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 43) - ਜੈਪੁਰ ਦੀ ਤਬਾਹੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-43?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 44) - ਪੁਸ਼ਕਰ ਦੀ ਤਬਾਹੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-44?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 45) - ਪੁਸ਼ਕਰ ਤੀਰਥ ਦਾ ਕ੍ਰੋਧ ਵਿਚ ਆਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-45?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 46) - ਅਜਮੇਰ ਦੇ ਮਜੌਰਾਂ ਦੀ ਚਲਾਕੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-46?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 47) - ਕਾਂਸ਼ੀ ਦੇ ਮੰਦਰਾਂ ਦੀ ਤਬਾਹੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-47?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 48) - ਹਿੰਦੂਆਂ ਦੀ ਗਿਰਾਵਟ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-48?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 49) - ਹਿੰਦੂਆਂ ਦੀ ਗਿਰਾਵਟ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-49?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 50) - ਮੁੱਲਾਂ, ਕਾਜ਼ੀਆਂ ਦਾ ਨੁਰੰਗੇ ਨੂੰ ਪ੍ਰੇਰਨਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-50?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 51) - ਮੁੱਲਾਂ, ਕਾਜ਼ੀਆਂ ਦਾ ਨੁਰੰਗੇ ਨੂੰ ਪ੍ਰੇਰਨਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-51?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'),  
            ('Sri Guru Har Rai Sahib Ji (Part 52) - ਔਰੰਗਜ਼ੇਬ ਦੀ ਸਤਿਗੁਰਾਂ ਨੂੰ ਚਿੱਠੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-52?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 53) - ਔਰੰਗਜ਼ੇਬ ਦਾ ਦੂਤ ਸਤਿਗੁਰੂ ਜੀ ਪਾਸ ਆਇਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-53?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 54) - ਦਿੱਲੀ ਜਾਣ ਹਿਤ ਵਿਚਾਰ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-54?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 55) - ਦਿੱਲੀ ਜਾਣ ਸਮਾਪਤ । ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਦਿੱਲੀ ਪੁੱਜੇ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-55?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 56) - ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਦਿੱਲੀ ਪੁੱਜੇ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-56?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 57) - ਸ਼੍ਰੀ ਰਾਮਰਾਇ ਨੇ ਮੋਇਆ ਬੱਕਰਾ ਜਿਵਾਇਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-57?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 58) - ਖੂਹ � ��ੇ ਬੈਠਣਾ, ਮੱਕੇ ਤੋਂ ਫਲ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-58?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 59) - ਖੂਹ ਤੇ ਬੈਠਣਾ, ਮੱਕੇ ਤੋਂ ਫਲ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-59?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 60) - ਹਿਤੂ ਬੇਗਮ, ਪਦਮਨੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-60?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 61) - ਦੋ ਚੰਦ ਦਿਖਾਏ, ਤੋਸ਼ੇਖਾਨੇ ਦੀ ਗਿਣਤੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-61?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 62) - ਤੋਸ਼ੇਖਾਨੇ ਦੀ ਗਿਣਤੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-62?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 63) - ਨਿੰਦਕ ਦੀ ਜ਼ਬਾਨ ਬੰਦ, ਦਿਨੇ ਤਾਰੇ, ਬਾਜ਼ੀ ਦਿਤੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-63?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 64) - ਨਿੰਦਕ ਦੀ ਜ਼ਬਾਨ ਬੰਦ, ਦਿਨੇ ਤਾਰੇ, ਬਾਜ਼ੀ ਦਿਤੀ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-64?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 65) - ਹੈਜੇ਼ ਦੀ ਬਿਮਾਰੀ ਹਿਟਾਈ, ਬੱਦਲਾਂ ਦੀ ਛਾਂ ਕੀਤੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-65?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 66) - ਪ੍ਰਸੂਤ ਪੀੜ ਦੂਰ ਕੀਤੀ, ਉਜ਼ਬਕ ਪਹਿਲਵਾਨ ਢੁਹਾਇਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-66?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 67) - ਅਲਾਵਦੀਨ ਦੀ ਮੌਤ, ਸੁਪਨਾ ਸੁਣਾਇਆ, ਬੇੜੀ ਜੋੜੀ, ਸੁਲੇਮਾਨੀ ਸੁਰਮਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-67?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 68) - ਗਊ ਜਿਵਾਈ, ਤਸਬੀ ਦਾ ਚੋਰ, ਮੋਤੀ ਦਿੱਤਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-68?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ("Sri Guru Har Rai Sahib Ji (Part 69) - ਖਾਧਾ ਹੋਇਆ ਦਸਿਆ, ਛੇ ਰੁੱਤਾਂ ਦੇ ਮੇਵੇ, ਅੱਗ 'ਤੇ ਬਾਗ਼", 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-69?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 70) - ਠੰਡੀ ਹਵਾ ਚਲਾਈ, ਸਮਾਧੀ, ਦਰਿਆਈ ਘੋੜਾ ਦਿੱਤਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-70?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 71) - ਭੂਮੀ ਉੱਚੀ ਕੀਤੀ, ਕੱਪੜੇ ਹੇਠੋਂ ਪੱਤਰੇ ਕੱਢੇ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-71?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 72) - ਦਰਵਾਜ਼ਿਆਂ ਦੇ ਤਾਲੇ ਖ੍ਹੋਲੇ, ਸ਼ਰਾਬ ਮਾਸ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-72?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 73) - ਕਹਾਰਾਂ ਤੋਂ ਬਿਨਾਂ ਪਾਲਕੀ ਚਲਾਈ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-73?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 74) - ਰਾਮਰਾਇ ਜੀ ਦੀ ਸਖਾਵਤ, ਬਾਦਸ਼ਾਹਾਂ ਦਾ ਬਾਦਸ਼ਾਹ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-74?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 75) - ਮਿੱਟੀ ਮੁਸਲਮਾਨ ਕੀ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-75?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 76) - ਦੋਵੇਂ ਪੁੱਤਰ ਕਿਵੇਂ ਪਰਖੇ ਸਨ?', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-76?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 77) - ਦੋਵੇਂ ਪੁੱਤਰ ਕਿਵੇਂ ਪਰਖੇ ਸਨ? ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-77?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 78) - ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਰਾਇ ਜੀ ਕਰਤਾਰਪੁਰ ਆਏ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-78?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 79) - ਕਰਤਾਰਪੁਰ ਵਸਾਉਣ ਦੀ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-79?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 80) - ਕਰਤਾਰਪੁਰ ਦੀ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-80?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 81) - ਕਰਤਾਰਪੁਰ ਦੀ ਕਥਾ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-81?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 82) - ਭਾਈ ਭਗਤੂ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-82?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 83) - ਕੋੜੇ ਤੇ ਮਰ੍ਹਾਜ ਗੋਤ ਦੇ ਕਿਸਾਨ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-83?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 84) - ਕੋੜੇ ਤੇ ਮਰ੍ਹਾਜ ਗੋਤ ਦੇ ਕਿਸਾਨ ੨', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-84?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 85) - ਕੋੜੇ ਤੇ ਮਰ੍ਹਾਜ ਗੋਤ ਦੇ ਕਿਸਾਨ ੩', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-85?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 86) - ਸ਼੍ਰੀ ਗੁਰੂ ਜੀ ਦਾ ਨਿੱਤ ਦਾ ਕਾਰਜ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-86?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 87) - ਗੁਰੂ ਜੀ ਦਾ ਡੇਰਾ ਤੁਰਕਾਂ ਦੇ ਘੇਰੇ ਵਿਚ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-87?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 88) - ਗੌਰੇ ਦਾ ਤੁਰਕਾਂ ਨਾਲ ਯੁੱਧ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-88?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 89) - ਗੌਰੇ ਦੇ ਸ੍ਰਾਪ ਬਖ਼ਸ਼ੇ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-89?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 90) - ਕਰਤਾਰਪੁਰ ਨਿਵਾਸ, ਬ੍ਰਾਹਮਣ ਪੁੱਤਰ ਮੋਇਆ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-90?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 91) - ਬ੍ਰਾਹਮਣ ਦਾ ਪੁੱਤਰ ਜਿਵਾਇਆ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-91?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 92) - ਸ਼ਕਰ ਗੰਗ ਲੱਗਣ ਦੀ ਕਥਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-92?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 93) - ਰਾਮਰਾਇ ਬਾਬਤ ਧੀਰਮਲ ਦਾ ਗੁਰੂ ਜੀ ਨੂੰ ਕਹਿਣਾ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-93?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 94) - ਗੁਰੂ ਜੀ ਦਾ ਉੱਤਰ, ਵਾਪਸ ਕੀਰਤਪੁਰ ਆਉਣਾ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-94?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 95) - ਗੁਰਬਾਣੀ ਮਹਿਮਾ, ਸਿੱਖੀ ਜਹਾਜ਼ ਪਾਠ ਗਿਆ ਹੈ', 'https://soundcloud.com/gianishersinghjiambala/patshahi-7-part-95?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 96) - ਗੁਰਬਾਣੀ ਮਹਿਮਾ, ਸਿੱਖੀ ਜਹਾਜ਼ ਪਾਠ ਗਿਆ ਹੈ ੨', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-96?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7'), 
            ('Sri Guru Har Rai Sahib Ji (Part 97) - ਸ਼੍ਰੀ ਗੁਰੂ ਹਰਿਕ੍ਰਿਸ਼ਨ ਸਾਹਿਬ ਜੀ ਨੂੰ ਗੁਰਗੱਦੀ', 'https://soundcloud.com/gianishersinghjiambala/sri-guru-har-rai-sahib-ji-part-97?in=gianishersinghjiambala/sets/sri-sooraj-prakash-patshahi-7')
        ], 
    'Raja Kharhag Singh Yudh Audio Boosted': 
        [
            ('Raja Kharhag Singh Yudh (Part 1) । ਛੰਦ ੧੩੭੦-੧੪੦੮', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-1?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 2) । ਛੰਦ ੧੪੦੮-੧੪੫੦', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-2?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 3) । ਛੰਦ ੧੪੫੦-੧੫੦੦', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-3?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 4) । ਛੰਦ ੧੫੦੦-੧੫੬੦', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-4?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 5) । ਛੰਦ ੧੫੬੦-੧੬੧੦', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-5?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 6) । ਛੰਦ ੧੬੦੮-੧੬੬੦', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-6?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 7) । ਛੰਦ ੧੬੬੦-੧੭੧੭', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-7?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio'), 
            ('Raja Kharhag Singh Yudh (Part 8) । ਛੰਦ ੧੭੧੮-੧੭੩੯', 'https://soundcloud.com/gianishersinghjiambala/raja-kharhag-singh-yudh-part-8?in=gianishersinghjiambala/sets/raja-kharhag-singh-yudh-audio')
        ], 
    'Battle of Bhangani': 
        [
            ('Battle of Bhangani (Part 1) - ਬੁੱਧੂ ਸ਼ਾਹ ਨੂੰ ਖ਼ਬਰ, ਕਾਲੇ ਖਾਂ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-1?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 2) - ਉਦਾਸੀਆਂ ਦਾ ਖਿਸਕਣਾ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-2?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 3) - ਦਲ ਦੀ ਚੜ੍ਹਾਈ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-3?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 4) - ਜੰਗ ਸ਼ੁਰੂ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-4?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 5) - ਕ੍ਰਿਪਾਲ ਮਹੰਤ ਨੇ ਹਿਆਤ ਖਾਂ ਨੂੰ ਮਾਰਨਾ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-5?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 6) - ਸਾਹਿਬ ਚੰਦ, ਦਇਆ ਰਾਮ ਤੇ ਨੰਦ ਚੰਦ ਦਾ ਯੁੱਧ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-6?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 7) - ਹਲਵਾਈ ਸਿੱਖ, ਜੀਤ ਮੱਲ ਬੱਧ, ਫ਼ਤਹਿ ਸ਼ਾਹ ਦਾ ਨੱਠ ਕੇ ਓਲ੍ਹੇ ਹੋਣਾ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-7?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 8) - ਸੰਗੋ ਸ਼ਾਹ ਤੇ ਹਰੀ ਚੰਦ ਬੱਧ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-8?in=gianishersinghjiambala/sets/battle-of-bhangani'), 
            ('Battle of Bhangani (Part 9) - ਭੰਗਾਣੀ ਯੁੱਧ ਫ਼ਤਹਿ ਕੀਤਾ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-9?in=gianishersinghjiambala/sets/battle-of-bhangani'),  
            ('Battle of Bhangani (Part 10) - ਇਨਾਮ ਵੰਡੇ, ਪਾਉਂਟੇ ਤੋਂ ਤਿਆਰੀ', 'https://soundcloud.com/gianishersinghjiambala/battle-of-bhangani-part-10?in=gianishersinghjiambala/sets/battle-of-bhangani')
        ], 
    'Raja Kharhag Singh Yudh': 
        [
            ('ਖੜਗ ਸਿੰਘ ਯੁੱਧ 1370 ਛੰਦ ਤੋਂ 1408 ਤਕ', 'https://soundcloud.com/gianishersinghjiambala/1370-1408a?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁੱਧ 1408 ਤੋਂ 1450 ਤਕ', 'https://soundcloud.com/gianishersinghjiambala/1408-1450b?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁਧ 1450 ਤੋਂ 1500', 'https://soundcloud.com/gianishersinghjiambala/1450-1500c?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁੱਧ 1500 ਤੋਂ 1560 ਤਕ', 'https://soundcloud.com/gianishersinghjiambala/1500-1560d?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁੱਧ 1560 ਤੋਂ 1610 ਤਕ', 'https://soundcloud.com/gianishersinghjiambala/1560-1610e?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁਧ 1609 ਤੋਂ 1660', 'https://soundcloud.com/gianishersinghjiambala/1609-1660f?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁਧ 1660 ਤੋਂ 1717', 'https://soundcloud.com/gianishersinghjiambala/1660-1717g?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh'), 
            ('ਖੜਗ ਸਿੰਘ ਯੁਧ 1717 ਤੋਂ 1739 ਤਕ', 'https://soundcloud.com/gianishersinghjiambala/1717-1739h?in=gianishersinghjiambala/sets/raja-kharag-singh-yudh')
        ]
}

listOfPlaylists=linksToPlayLists()
obj=linksInPlaylist(listOfPlaylists)

downloadLinksInPlaylist(dir,obj)