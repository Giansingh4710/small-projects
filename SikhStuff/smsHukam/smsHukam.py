import time,requests,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.headless = True
from bs4 import BeautifulSoup as bs
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

class SmsHukam():
    def  __init__(self):
        self.br =  webdriver.Chrome("C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe",options=chrome_options)
        self.parser="html.parser"
        self.santJiKhata=self.santJiKhataInOrder()

    def getHukamAudio(self,theId):
        url="https://www.sikhnet.com/gurbani/shabadid/"+theId
        res=requests.get(url)
        soup=bs(res.text,self.parser)
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
        soup=bs(content,self.parser)
        shabadLink=self.br.current_url

        newUrl=soup.find("a",class_="hukamnama-right-link")["href"]
        Shabadid=newUrl[11:]

        newUrl="https://www.sikhitothemax.org"+newUrl
        
        self.br.get(newUrl)
        time.sleep(1)
        content=self.br.page_source.encode('utf-8').strip()
        soup=bs(content,self.parser)
        
        shabadHeader=soup.find(class_="meta")
        header=shabadHeader.findAll("h4")[1].text


        shabad=soup.find(class_="mixed-view-baani")
        lst=shabad.find_all(class_="mixed-view-baani-translation-english")
        
        
        shabadStr=""
        for i in lst:
            shabadStr+=i.text+"\n"
        final=header+"\n"+shabadStr+"\n"+shabadLink+"\n"
        
        try:
            audios,mp3s=self.getHukamAudio(Shabadid)
            final+="Audios to listen to the Hukam: "+"\n"
            final+="     Links:\n"
            for i in audios:
                final+="          "+i+"\n"
            final+="     MP3 Files:\n"
            for i in mp3s:
                final+="          "+i+"\n"
        except Exception as e:
            print("No audio for this hukamnama")
        return final
        
    def gurmukhiRand(self):
        url="https://gurbaninow.com/shabad/random"
        
        self.br.get(url)
        time.sleep(2)
        content=self.br.page_source.encode('utf-8').strip()
        shabadLink=self.br.current_url

        soup=bs(content,self.parser)
        angNum=soup.find("div",id="shabadInfoEnglish")

        angNum=angNum.find("a").text
        angNum="Ang"+angNum.split("Ang ")[1]
        santJi=self.santJiKhata[angNum]
        santJi="\n\nKhata of Ang By Sant Giani Gurbachan Singh Ji Bhindran Vale:\n"+santJi

        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=str(gurmukhi[i].text).replace(" ", "")+"\n"
            final+=str(english[i].text)+"\n"
            final+="\n"
            
        final+="\n"+shabadLink
        if "http://sikhsoul.com/audio_files" not in santJi:
            final+=santJi
        while "https://gurbaninow.com/shabad/random" in final:
            print("Random didn't get generated")
            final=self.gurmukhiRand()
            print("Generated!!")            
        return final

    def gurmukhiHukam(self):
        url="https://gurbaninow.com/hukamnama"
        
        self.br.get(url)
        time.sleep(3)
        content=self.br.page_source.encode('utf-8').strip()
        shabadLink=self.br.current_url

        soup=bs(content,self.parser)
        angNum=soup.find("div",id="shabadInfoEnglish")
        angNum=angNum.find("a").text
        angNum="Ang"+angNum.split("Ang ")[1]
        santJi=self.santJiKhata[angNum]
        santJi="\n\nKhata of Ang By Sant Giani Gurbachan Singh Ji Bhindran Vale:\n"+santJi

        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=str(gurmukhi[i].text)+"\n"
            final+=str(english[i].text)+"\n"
            final+="\n"
        final+="\n"+shabadLink
        if "http://sikhsoul.com/audio_files" not in santJi:
            final+=santJi
        return final

    #For khata of sant Giani Gurbachan Singh ji
    def onlyLinks(self,url):
        res=requests.get(url)
        soup=bs(res.text, self.parser)
        khatas=soup.find_all("table",cellpadding=4)
        khatas=khatas[4:-2]
        folderWithLinks={}
        for file in khatas:
            try:
                title=file.find("font",size="2",color="0069c6").text
            except AttributeError:
                print("No Good. But we caught it!!")#It got the ALL the text from the drop down menu and those don't have a 'color=0069c6' attribute
                continue
            newUrl="http://www.gurmatveechar.com/"+file.find("a").get("href")
            if "mp3" in newUrl.lower():
                folderWithLinks[title]=newUrl
            else:
                newFolderWithLinks=self.onlyLinks(newUrl)
                folderWithLinks.update(newFolderWithLinks) 
        return folderWithLinks

    def santJiKhataInOrder(self):
        angs=re.compile(r"(Ang(-||\s)([0-9]{1,4})(\+[0-9]{1,4})?)")
        url="http://www.gurmatveechar.com/audio.php?q=f&f=%2FKatha%2F01_Puratan_Katha%2FSant_Gurbachan_Singh_%28Bhindran_wale%29%2FGuru_Granth_Sahib_Larivaar_Katha"
        a=self.onlyLinks(url)
        titles=list(a.keys())
        links=list(a.values())
        theAngs=[0]*1430
        for i in range(len(titles)):
            b=angs.search(titles[i])
            ang=b.group(3) #the third group gives the ang
            num=int(ang)-1
            theAngs[num]=links[i]
        default="http://sikhsoul.com/audio_files/mp3/Bani/Kirtan%20Sohila/Bhai%20Tarlochan%20Singh%20Ragi%20-%20Kirtan%20Sohaila.mp3"
        d={}
        for i in range(len(theAngs)):
            if theAngs[i]==0:
                down=default
                name=f"Ang{i+1}"
            else:
                down=theAngs[i]
                name=f"Ang{i+1}"
            d[name]=down
        return d
a=SmsHukam()

#for i in range(10): print(a.gurmukhiRand())
print(a.gurmukhiHukam())


