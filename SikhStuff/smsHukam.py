import smtplib
from email.message import EmailMessage
import time,requests,re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from threading import *
import imaplib,email,re

options = webdriver.ChromeOptions()
options.headless = True

class SmsHukam():
    def sendToPhone(self,subject,body,to):
        msg=EmailMessage()
        msg.set_content(body)
        msg['subject']=subject
        msg["to"]=to
        
        user='giansingh131313@gmail.com'
        msg["from"]=user
        password='jkodhyxiypnsdifl'

        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
        server.quit()

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
        br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
        br.get(url)
        time.sleep(1)
        content=br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        shabadLink=br.current_url

        newUrl=soup.find("a",class_="hukamnama-right-link")["href"]
        Shabadid=newUrl[11:]

        newUrl="https://www.sikhitothemax.org"+newUrl
        br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
        br.get(newUrl)
        time.sleep(1)
        content=br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        
        #shabadHeader=soup.find(class_="metadata-shabad")
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
        br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
        br.get(url)
        time.sleep(1)
        content=br.page_source.encode('utf-8').strip()
        soup=bs(content,"lxml")
        shabadLink=br.current_url

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
        br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
        br.get(url)
        time.sleep(1)
        content=br.page_source.encode('utf-8').strip()
        shabadLink=br.current_url

        soup=bs(content,"lxml")
        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=gurmukhi[i].text+"\n"
            final+=english[i].text+"\n"
            final+="\n"
        return final

    def gurmukhiHukam(self):
        url="https://gurbaninow.com/hukamnama"
        br =  webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
        br.get(url)
        time.sleep(1)
        content=br.page_source.encode('utf-8').strip()
        shabadLink=br.current_url

        soup=bs(content,"lxml")
        conta=soup.find("div",id="shabad")
        gurmukhi=conta.findAll("div",class_="gurmukhi unicode normal")
        english=conta.findAll("div",class_="english")
        final=""
        for i in range(len(gurmukhi)):
            final+=gurmukhi[i].text+"\n"
            final+=english[i].text+"\n"
            final+="\n"
        return final




class Reply(Thread):
    def run(self):
        host="imap.gmail.com"
        user="giansingh131313@gmail.com"
        password='jkodhyxiypnsdifl'

        mail=imaplib.IMAP4_SSL(host)
        mail.login(user,password)
        mail.select("inbox")

        _, searchData=mail.search(None,"UNSEEN")
        for num in searchData[0].split():
            _, data=mail.fetch(num,"(RFC822)")
            _,b=data[0]
            emailMessage=email.message_from_bytes(b)
            whoSent=emailMessage["From"]
            theNumber=whoSent.split("@")[0]
            a=re.search("[0-9]{10}",theNumber)
            if a==None:
                continue
            for part in emailMessage.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    body=part.get_payload(decode=True)
                    sentFromPhone=body.decode()
                    phone=theNumber+"@pm.sprint.com"

                    h=SmsHukam()
                    if "rand" in sentFromPhone.lower() or "new" in sentFromPhone.lower():
                        newRandomShabad=h.gurmukhiRand()
                        h.sendToPhone("Random Shabad",newRandomShabad,phone)

                    elif "hukam" in sentFromPhone.lower():
                        hukamnama=h.gurmukhiHukam()
                        h.sendToPhone("Hukamnam",hukamnama,theNumber+phone)

                    elif "english hukam" in sentFromPhone.lower():
                        hukamnama=h.engHukam()
                        h.sendToPhone("English Hukam",hukamnama,phone)

                    elif "random english" in sentFromPhone.lower():
                        hukamnama=h.engRandShabad()
                        h.sendToPhone("English Hukam",hukamnama,phone)






def sendMessages():
    h=SmsHukam()
    hukamnama=h.gurmukhiRand()
    people=["6023802096@pm.sprint.com","8622827105@pm.sprint.com","2018731477@pm.sprint.com","6782670271@pm.sprint.com","6788628987@pm.sprint.com","6786430348@pm.sprint.com","6787990390@pm.sprint.com","7189155004@pm.sprint.com"]
    for i in people:
        h.sendToPhone("Hukam",hukamnama,i)
#sendMessages()
h=SmsHukam()
#hukamnama=h.gurmukhiRand()
#h.sendToPhone("Random",hukamnama,"6782670271@pm.sprint.com")
if __name__=="__main__":
    while True:
        r=Reply()
        r.start()
        h=SmsHukam()
        rand=h.engRandShabad()
        h.sendToPhone("Hukam",rand,"6782670271@pm.sprint.com ")
        #sendMessages(hukamnama)
        time.sleep(20)














'''
def getGianiSukhaJiHukamAudio():
    original="https://www.sikhnet.com/gurbani/artist/14335/audio?page="
    khataLinks=[original+str(i) for i in range(17)]
    allLinks={}
    ang=re.compile("ang-([0-9]{1,4})")
    for khataLink in khataLinks:
        res=requests.get(khataLink)
        soup=bs(res.text,"lxml")
        cont=soup.find("table",class_="views-table")
        cont=cont.find("tbody")
        rows=cont.findAll("tr")
        for khata in rows:
            each=khata.find("td",class_="views-field-title")
            link="https://www.sikhnet.com/"+each.find("a")["href"]
            try:
                theAng=ang.findall(link)[0]
                if theAng not in allLinks:
                    allLinks[theAng]=[link]
                else:
                    allLinks[theAng].append(link)
            except Exception:
                continue
    return allLinks


Carrier	      SMS gateway domain	         MMS gateway domain
AT&T	         [insert 10-digit number]@txt.att.net	[insert 10-digit number]@mms.att.net
Boost Mobile	[insert 10-digit number]@sms.myboostmobile.com	[insert 10-digit number]@myboostmobile.com
Cricket Wireless	[insert 10-digit number]@mms.cricketwireless.net	[insert 10-digit number]@mms.cricketwireless.net
Google Project Fi	[insert 10-digit number]@msg.fi.google.com	[insert 10-digit number]@msg.fi.google.com
Republic Wireless	[insert 10-digital number]@text.republicwireless.com	
Sprint	[insert 10-digit number]@messaging.sprintpcs.com	[insert 10-digit number]@pm.sprint.com
Straight Talk	[insert 10-digital number]@vtext.com	[insert 10-digit number]@mypixmessages.com
T-Mobile	[insert 10-digit number]@tmomail.net	[insert 10-digit number]@tmomail.net
Ting	[insert 10-digit number]@message.ting.com	
Tracfone	[depends on underlying carrier]	[insert 10-digit number]@mmst5.tracfone.com
U.S. Cellular	[insert 10-digit number]@email.uscc.net	[insert 10-digit number]@mms.uscc.net
Verizon	[insert 10-digit number]@vtext.com	[insert 10-digit number]@vzwpix.com
Virgin Mobile	[insert 10-digit number]@vmobl.com	[insert 10-digit number]@vmpix.com
'''