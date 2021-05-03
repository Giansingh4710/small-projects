import time,requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.headless = True
from bs4 import BeautifulSoup as bs
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

class SmsHukam():
    def  __init__(self):
        self.br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=chrome_options)
        
    def getHukamAudio(self,theId):
        url="https://www.sikhnet.com/gurbani/shabadid/"+theId
        res=requests.get(url)
        soup=bs(res.text,"lxml")
        cont=soup.find("table",class_="views-table")
        cont=cont.find("tbody")
        rows=cont.findAll("tr")
        links=[]
        downloads=[]
        for khata in rows:
            each=khata.find("td",class_="views-field-title")
            link="https://www.sikhnet.com/"+each.find("a")["href"]
            downl=khata.find("td",class_="views-field-download-link")
            download=downl.find("a")["href"]
            links.append(link)
            downloads.append(download)
        return links,downloads


    def engHukam(self):
        url="https://www.sikhitothemax.org/hukamnama"        
        self.br.get(url)
        time.sleep(1)
        content=self.br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        shabadLink=self.br.current_url

        newUrl=soup.find("a",class_="hukamnama-right-link")["href"]
        Shabadid=newUrl[11:]

        newUrl="https://www.sikhitothemax.org"+newUrl
        
        self.br.get(newUrl)
        time.sleep(1)
        content=self.br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        
        shabadHeader=soup.find(class_="meta")
        header=shabadHeader.findAll("h4")[1].text
        audios,mp3s=self.getHukamAudio(Shabadid)

        shabad=soup.find(class_="mixed-view-baani")
        lst=shabad.find_all(class_="mixed-view-baani-translation-english")
        shabadStr=""
        for i in lst:
            shabadStr+=i.text+"\n"


        final=header+"\n"+shabadStr+"\n"+shabadLink+"\n"+"Audios to listen to the Hukam: "+"\n"
        final+="     Links:\n"
        for i in audios:
            final+="          "+i+"\n"
        final+="     MP3 Files:\n"
        for i in mp3s:
            final+="          "+i+"\n"

        return final

    def engRandShabad(self):
        url="https://www.sikhitothemax.org/shabad?random"
        
        self.br.get(url)
        time.sleep(1)
        content=self.br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        shabadLink=self.br.current_url

        shabadHeader=soup.find(class_="meta")
        header=shabadHeader.findAll("h4")[1].text

        shabad=soup.find(class_="mixed-view-baani")
        lst=shabad.find_all(class_="mixed-view-baani-translation-english")
        shabadStr=""
        for i in lst:
            shabadStr+=i.text+"\n"

        final=header+"\n\n"+shabadStr+"\n"+shabadLink
        try:
            Shabadid=shabadLink[11+len("https://www.sikhitothemax.org"):]
            audios,mp3s=self.getHukamAudio(Shabadid)
            final+="\nMP3s: \n"
            for i in mp3s:
                final+=i+"\n"
        except Exception as e:
            print(e)
        return final

    def gurmukhiRand(self):
        url="https://gurbaninow.com/shabad/random"
        
        self.br.get(url)
        time.sleep(1)
        content=self.br.page_source.encode('utf-8').strip()
        shabadLink=self.br.current_url

        soup=bs(content,"lxml")
        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=str(gurmukhi[i].text)+"\n"
            final+=str(english[i].text)+"\n"
            final+="\n"
        final+="\n"+shabadLink+""
        return final

    def gurmukhiHukam(self):
        url="https://gurbaninow.com/hukamnama"
        
        self.br.get(url)
        time.sleep(3)
        content=self.br.page_source.encode('utf-8').strip()
        shabadLink=self.br.current_url

        soup=bs(content,"lxml")
        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=str(gurmukhi[i].text)+"\n"
            final+=str(english[i].text)+"\n"
            final+="\n"
        final+="\n"+shabadLink
        return final
