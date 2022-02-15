from selenium import webdriver
import time,os
from bs4 import BeautifulSoup as bs
import urllib.request 
import pyperclip
from threading import Thread

options = webdriver.ChromeOptions()
# options.headless = True

driverPath='C:\\Users\\gians\\Desktop\\stuff\\chromedriver_win32\\chromedriver.exe'
def linksToPlayLists(url): #gets all the links to the playlists in soundcloud
    br =  webdriver.Chrome(driverPath,options=options)
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
    f=open("./playlistLinks.txt","w",encoding="utf-8")
    
    for playlist in allPlaylists:
        atag=playlist.find("a",class_="soundTitle__title sc-link-dark sc-link-secondary sc-text-h4")
        theLinkWithTitle=(atag.text.strip(),"https://soundcloud.com"+atag["href"])
        print(theLinkWithTitle)
        playlistLinks.append(theLinkWithTitle)
        f.write(atag.text.strip()+" : "+"https://soundcloud.com"+atag["href"]+"\n")
    f.close()
    br.close()
    return playlistLinks

def linksInPlaylist(playlists): #gets all the individual katha links inside the playlists
    d={}
    for playlist in playlists:
        title=playlist[0]
        link=playlist[1]
        links=getLinksForPlaylist(link) #list of tuples where index 0 is title of link and index 1 is link
        d[title]=links
    return d

def getLinksForPlaylist(link): #gets links for katha in a playlist. This func is used for the func above
    br =  webdriver.Chrome(driverPath,options=options)
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
    pyperclip.copy(str(links))
    return links



def downloadLinksInPlaylist(directory,obj):
    for playlist in obj:
        newPlace=f"{directory}{playlist}\\"
        os.mkdir(newPlace)
        for track in obj[playlist]:
            # try:
                # downloadLink(newPlace,track)
            a=DownloadTheLink(newPlace,track)
            a.run()
            # except Exception:
                # print(f"No Download - {track}")

class DownloadTheLink(Thread):
    def __init__(self,dirr,track):
        self.track=track
        self.dir=dirr
    def run(self):
        br =  webdriver.Chrome(driverPath,options=options)
        theUrl="https://www.soundcloudmp3.org/"
        br.get(theUrl)
        # time.sleep(5)
        entry=br.find_element_by_css_selector("#conversionForm > div > input.form-control")
        entry.send_keys(self.track[1]) #track[1] is the soundcloud url link of katha
        button=br.find_element_by_css_selector("#conversionForm > div > span > button")
        button.click()

        print("After download clicked !!!!!")
        atag=br.find_element_by_css_selector("#download-btn")
        while atag.text!="Download MP3":
            atag=br.find_element_by_css_selector("#download-btn")
            time.sleep(1)

        theDownloadLink=atag.get_attribute("href")
        urllib.request.urlretrieve(theDownloadLink,f'{self.dir}{self.track[0]}.mp3')
        time.sleep(1)
        br.close()

def downloadLink(dir,track):
    br =  webdriver.Chrome(driverPath,options=options)
    theUrl="https://www.soundcloudmp3.org/"
    br.get(theUrl)
    # time.sleep(5)
    entry=br.find_element_by_css_selector("#conversionForm > div > input.form-control")
    entry.send_keys(track[1]) #track[1] is the soundcloud url link of katha
    button=br.find_element_by_css_selector("#conversionForm > div > span > button")
    button.click()

    print("After download clicked !!!!!")
    atag=br.find_element_by_css_selector("#download-btn")
    while atag.text!="Download MP3":
        atag=br.find_element_by_css_selector("#download-btn")
        time.sleep(1)

    theDownloadLink=atag.get_attribute("href")
    urllib.request.urlretrieve(theDownloadLink,f'{dir}{track[0]}.mp3')
    time.sleep(1)
    br.close()


dir="C:\\Users\\gians\\Desktop\\test\\"
# url="https://soundcloud.com/gianishersinghjiambala/sets"
# listOfPlaylists=linksToPlayLists(url)
# obj=linksInPlaylist(listOfPlaylists)
# downloadLinksInPlaylist(dir,obj)
url="https://soundcloud.com/basicsofsikhi/sets/the-whyguru-course"
# a=getLinksForPlaylist(url)
# obj={"WhyGuru Course":a}
obj={
    "WhyGuru Course":
        [
            ('1) Introduction - Testimonials - WhyGuru Course', 'https://soundcloud.com/basicsofsikhi/introduction-testimonials-whyguru-course?in=basicsofsikhi/sets/the-whyguru-course'),
            ('2) TWGC Foundation A - Intro To The WhyGuru Course', 'https://soundcloud.com/basicsofsikhi/twgc-foundation-a-intro-to-the-whyguru-course?in=basicsofsikhi/sets/the-whyguru-course'),
            ('3) TWGC Foundation B - Guru Nanaks Youth To Guruship - The WhyGuru Course', 'https://soundcloud.com/basicsofsikhi/twgc-foundation-b-guru-nanaks-youth-to-guruship-the-whyguru-course?in=basicsofsikhi/sets/the-whyguru-course'),
            ('4) TWGC Foundation C - Q&A About Guruji And WhyGuru Course', 'https://soundcloud.com/basicsofsikhi/twgc-foundation-c-qa-about-guruji-and-whyguru-course?in=basicsofsikhi/sets/the-whyguru-course'),
            ('5) TWGC Topic #1 Part A - Guru Nanak Dev JI', 'https://soundcloud.com/basicsofsikhi/twgc-topic-1-part-a-guru-nanak-dev-ji-2?in=basicsofsikhi/sets/the-whyguru-course'),
            ('6) TWGC Topic #1 Part B - Guru Nanak Dev Ji', 'https://soundcloud.com/basicsofsikhi/twgc-topic-1-part-b-guru-nanak-dev-ji?in=basicsofsikhi/sets/the-whyguru-course'),
            ('7) TWGC Topic #1 Part C - (Q&A) Guru Nanak Dev Ji', 'https://soundcloud.com/basicsofsikhi/twgc-topic-1-part-c-qa-guru-nanak-dev-ji?in=basicsofsikhi/sets/the-whyguru-course'),
            ('8) TWGC Topic #2 Part A - Why Meditate', 'https://soundcloud.com/basicsofsikhi/twgc-topic-2-part-a-why-meditate?in=basicsofsikhi/sets/the-whyguru-course'),
            ('9) TWGC Topic #2 Part B - Why Meditate', 'https://soundcloud.com/basicsofsikhi/twgc-topic-2-part-b-why-meditate?in=basicsofsikhi/sets/the-whyguru-course'),
            ('10) TWGC Topic #3 Part A - 2nd Guru To 5th Guru', 'https://soundcloud.com/basicsofsikhi/twgc-topic-3-part-a-2nd-guru-to-5th-guru-2?in=basicsofsikhi/sets/the-whyguru-course'),
            ('11) TWGC Topic #3 Part B - 2nd Guru To 5th Guru', 'https://soundcloud.com/basicsofsikhi/twgc-topic-3-part-b-2nd-guru-to-5th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ('12) TWGC Topic #3 Part C (+Q&A) - 2nd Guru To 5th Guru', 'https://soundcloud.com/basicsofsikhi/twgc-topic-3-part-c-qa-2nd-guru-to-5th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ("13) TWGC Topic #4 Part A (+Q&A) - 5th Guru's Shaheedi And 6th Guru", 'https://soundcloud.com/basicsofsikhi/twgc-topic-4-part-a-qa-5th-gurus-shaheedi-and-6th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ('14) TWGC Topic #5 Part A - Sri Guru Granth Sahib Ji - History', 'https://soundcloud.com/basicsofsikhi/twgc-topic-5-part-a-sri-guru-granth-sahib-ji-history?in=basicsofsikhi/sets/the-whyguru-course'),
            ('15) TWGC Topic #5 Part B - Sri Guru Granth Sahib Ji - Structure', 'https://soundcloud.com/basicsofsikhi/twgc-topic-5-part-b-sri-guru-granth-sahib-ji-structure?in=basicsofsikhi/sets/the-whyguru-course'),
            ('16) TWGC Topic #6 Part A - 7th - 8th Guru', 'https://soundcloud.com/basicsofsikhi/whyguru-course-topic-6-part-a-7th-8th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ('17) TWGC Topic #6 Part B - 9th Guru', 'https://soundcloud.com/basicsofsikhi/twgc-topic-6-part-b-9th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ('18) TWGC Topic #6 Part C - 10th Guru', 'https://soundcloud.com/basicsofsikhi/twgc-topic-6-part-c-10th-guru?in=basicsofsikhi/sets/the-whyguru-course'),
            ('19) TWGC Topic #6 Part D- 7 - 10th Guru (+Q&A)', 'https://soundcloud.com/basicsofsikhi/twgc-topic-6-part-d-7-10th-guru-qa?in=basicsofsikhi/sets/the-whyguru-course'),
            ('20) TWGC Topic #7 Part A - Khalsa - What Happened In 1699?', 'https://soundcloud.com/basicsofsikhi/twgc-topic-7-part-a-khalsa-what-happened-in-1699?in=basicsofsikhi/sets/the-whyguru-course'),
            ('21) TWGC Topic #7 Part B (+Q&A) - Khalsa - Why Demand A Head?', 'https://soundcloud.com/basicsofsikhi/twgc-topic-7-part-b-qa-khalsa-why-demand-a-head?in=basicsofsikhi/sets/the-whyguru-course'),
            ('22) TWGC Topic #7 Part C - Khalsa - What Is The Concept?', 'https://soundcloud.com/basicsofsikhi/twgc-topic-7-part-c-khalsa-what-is-the-concept?in=basicsofsikhi/sets/the-whyguru-course'),
            ('23) TWGC Topic #7 Part D - Khalsa - Discussion Points', 'https://soundcloud.com/basicsofsikhi/twgc-topic-7-part-d-khalsa-discussion-points?in=basicsofsikhi/sets/the-whyguru-course'),
            ('24) TWGC Topic #8 Part A - The Misl Period - 1699 To 1708', 'https://soundcloud.com/basicsofsikhi/twgc-topic-8-part-a-the-misl-period-1699-to-1708?in=basicsofsikhi/sets/the-whyguru-course'),
            ('25) TWGC Topic #8 Part B - The Misl Period - 1708 To 1801', 'https://soundcloud.com/basicsofsikhi/twgc-topic-8-part-b-the-misl-period-1708-to-1801?in=basicsofsikhi/sets/the-whyguru-course'),
            ('26) TWGC Topic #8 Part C - The Misl Period - Discussion Points', 'https://soundcloud.com/basicsofsikhi/twgc-topic-8-part-c-the-misl-period-discussion-points?in=basicsofsikhi/sets/the-whyguru-course'),
            ('27) TWGC Topic #9 Part A - Raag Kirtan', 'https://soundcloud.com/basicsofsikhi/twgc-topic-9-part-a-raag-kirtan?in=basicsofsikhi/sets/the-whyguru-course'),
            ('28) TWGC Topic #9 Part B - Raag Kirtan', 'https://soundcloud.com/basicsofsikhi/twgc-topic-9-part-b-raag-kirtan?in=basicsofsikhi/sets/the-whyguru-course'),
            ('29) TWGC Topic #9 Part C (+Q&A) - Raag Kirtan - Discussion Points', 'https://soundcloud.com/basicsofsikhi/twgc-topic-9-part-c-qa-raag-kirtan-discussion-points?in=basicsofsikhi/sets/the-whyguru-course'),
            ('30) TWGC Topic #9 Part D - Raag Kirtan Demonstrations', 'https://soundcloud.com/basicsofsikhi/twgc-topic-9-part-d-raag-kirtan-demonstrations?in=basicsofsikhi/sets/the-whyguru-course'),
            ('31) TWGC Topic #10 Part A - Rise And Fall Of The Sikh Kingdom', 'https://soundcloud.com/basicsofsikhi/twgc-topic-10-part-a-rise-and-fall-of-the-sikh-kingdom?in=basicsofsikhi/sets/the-whyguru-course'),
            ('32) TWGC Topic #10 Part B - Sikhs Under The British Rule', 'https://soundcloud.com/basicsofsikhi/twgc-topic-10-part-b-sikhs-under-the-british-rule?in=basicsofsikhi/sets/the-whyguru-course'),
            ('33) TWGC Topic #10 Part C (+Q&A) - 1801 - 1925 Discussion Points', 'https://soundcloud.com/basicsofsikhi/twgc-topic-10-part-c-qa-1801-1925-discussion-points?in=basicsofsikhi/sets/the-whyguru-course'),
            ('34) TWGC Topic #11 Part A - 1925 To 1947 Independence From British', 'https://soundcloud.com/basicsofsikhi/twgc-topic-11-part-a-1925-to-1947-independence-from-british?in=basicsofsikhi/sets/the-whyguru-course'),
            ('35) TWGC Topic #11 Part B - 1947 To 1973 - Punjabi Suba Movement - Dharam Yudh Morcha', 'https://soundcloud.com/basicsofsikhi/twgc-topic-11-part-b-1947-to-1973-punjabi-suba-movement-dharam-yudh-morcha?in=basicsofsikhi/sets/the-whyguru-course'),
            ('36) TWGC Topic #11 Part C - 1984 June And November (plus Talking Points)', 'https://soundcloud.com/basicsofsikhi/twgc-topic-11-part-c-1984-june-and-november-plus-talking-points?in=basicsofsikhi/sets/the-whyguru-course'),
            ('37) TWGC Topic #12 Part A - 1984 To Now - Judicial Process', 'https://soundcloud.com/basicsofsikhi/twgc-topic-12-part-a-1984-to-now-judicial-process?in=basicsofsikhi/sets/the-whyguru-course'),
            ('38) TWGC Topic #12 Part B - 1984 To Now - Armed Struggle', 'https://soundcloud.com/basicsofsikhi/twgc-topic-12-part-b-1984-to-now-armed-struggle?in=basicsofsikhi/sets/the-whyguru-course'),
            ('39) TWGC Topic #12 Part C - 1984 To Now - Current State Of Punjab', 'https://soundcloud.com/basicsofsikhi/twgc-topic-12-part-c-1984-to-now-current-state-of-punjab?in=basicsofsikhi/sets/the-whyguru-course'),
            ('40) TWGC Topic #12 Part D - 1984 To Now - State Of Panth', 'https://soundcloud.com/basicsofsikhi/twgc-topic-12-part-d-1984-to-now-state-of-panth?in=basicsofsikhi/sets/the-whyguru-course'),
            ('41) TWGC Topic #12 Part E - 1984 To Now - Discussion Points', 'https://soundcloud.com/basicsofsikhi/twgc-topic-12-part-e-1984-to-now-discussion-points?in=basicsofsikhi/sets/the-whyguru-course')
        ]
}
downloadLinksInPlaylist(dir,obj)