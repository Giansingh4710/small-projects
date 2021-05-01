
#from keepAlive import KeepAlive
import smtplib
from email.message import EmailMessage
import time, requests, re
from bs4 import BeautifulSoup as bs
from threading import *
import imaplib, email, re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.headless = True



class SmsHukam():
    def sendToPhone(self, subject, body, to):
        msg = EmailMessage()

        user = 'giansingh131313@gmail.com'
        password = 'jkodhyxiypnsdifl'

        msg["From"] = user
        msg['Subject'] = subject
        msg["To"] = to
        msg.set_content(body)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg, mail_options='SMTPUTF8')
        server.quit()

    def getHukamAudio(self, theId):
        url = "https://www.sikhnet.com/gurbani/shabadid/" + theId
        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        cont = soup.find("table", class_="views-table")
        cont = cont.find("tbody")
        rows = cont.findAll("tr")
        links = []
        downloads = []
        for khata in rows:
            each = khata.find("td", class_="views-field-title")
            link = "https://www.sikhnet.com/" + each.find("a")["href"]
            downl = khata.find("td", class_="views-field-download-link")
            download = downl.find("a")["href"]
            links.append(link)
            downloads.append(download)
        return links, downloads

    def engHukam(self):
        url = "https://www.sikhitothemax.org/hukamnama"
        br = webdriver.Chrome(options=chrome_options)
        br.get(url)
        time.sleep(1)
        content = br.page_source.encode('utf-8').strip()
        soup = bs(content, "html.parser")
        shabadLink = br.current_url

        newUrl = soup.find("a", class_="hukamnama-right-link")["href"]
        Shabadid = newUrl[11:]

        newUrl = "https://www.sikhitothemax.org" + newUrl
        br = webdriver.Chrome(options=chrome_options)
        br.get(newUrl)
        time.sleep(1)
        content = br.page_source.encode('utf-8').strip()
        soup = bs(content, "html.parser")

        #shabadHeader=soup.find(class_="metadata-shabad")
        shabadHeader = soup.find(class_="meta")
        header = shabadHeader.findAll("h4")[1].text

        audios, mp3s = self.getHukamAudio(Shabadid)

        shabad = soup.find(class_="mixed-view-baani")
        lst = shabad.find_all(class_="mixed-view-baani-translation-english")
        shabadStr = ""
        for i in lst:
            shabadStr += i.text + "\n"

        final = header + "\n" + shabadStr + "\n" + shabadLink + "\n" + "Audios to listen to the Hukam: " + "\n"
        final += "     Links:\n"
        for i in audios:
            final += "          " + i + "\n"
        final += "     MP3 Files:\n"
        for i in mp3s:
            final += "          " + i + "\n"

        return final

    def engRandShabad(self):
        url = "https://www.sikhitothemax.org/shabad?random"
        br = webdriver.Chrome(options=chrome_options)
        br.get(url)
        time.sleep(1)
        content = br.page_source.encode('utf-8').strip()
        soup = bs(content, "html.parser")
        shabadLink = br.current_url

        shabadHeader = soup.find(class_="meta")
        header = shabadHeader.findAll("h4")[1].text

        shabad = soup.find(class_="mixed-view-baani")
        lst = shabad.find_all(class_="mixed-view-baani-translation-english")
        shabadStr = ""
        for i in lst:
            shabadStr += i.text + "\n"

        final = header + "\n\n" + shabadStr + "\n" + shabadLink
        try:
            Shabadid = shabadLink[11 + len("https://www.sikhitothemax.org"):]
            audios, mp3s = self.getHukamAudio(Shabadid)
            final += "\nMP3s: \n"
            for i in mp3s:
                final += i + "\n"
        except Exception as e:
            print(e)
        return final

    def gurmukhiRand(self):
        url = "https://gurbaninow.com/shabad/random"
        br = webdriver.Chrome(options=chrome_options)
        br.get(url)
        time.sleep(1)
        content = br.page_source.encode('utf-8').strip()
        shabadLink = br.current_url

        soup = bs(content, "html.parser")
        conta = soup.find("div", id="shabad")
        gurmukhi = conta.findAll("div", class_="gurmukhi unicode normal")
        english = conta.findAll("div", class_="english")
        final = ""
        for i in range(len(gurmukhi)):
            final += str(gurmukhi[i].text) + "\n"
            final += str(english[i].text) + "\n"
            final += "\n"
        final += "\n" + shabadLink + ""
        return final

    def gurmukhiHukam(self):
        url = "https://gurbaninow.com/hukamnama"
        br = webdriver.Chrome(options=chrome_options)
        br.get(url)
        time.sleep(1)
        content = br.page_source.encode('utf-8').strip()
        shabadLink = br.current_url

        soup = bs(content, "html.parser")
        conta = soup.find("div", id="shabad")
        gurmukhi = conta.findAll("div", class_="gurmukhi unicode normal")
        english = conta.findAll("div", class_="english")
        final = ""
        for i in range(len(gurmukhi)):
            final += str(gurmukhi[i].text) + "\n"
            final += str(english[i].text) + "\n"
            final += "\n"
        final += "\n" + shabadLink
        return final


class Reply():
    def run(self):
        host = "imap.gmail.com"
        user = "giansingh131313@gmail.com"
        password = 'jkodhyxiypnsdifl'

        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        mail.select("inbox")

        _, searchData = mail.search(None, "UNSEEN")
        for num in searchData[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            _, b = data[0]
            emailMessage = email.message_from_bytes(b)
            whoSent = emailMessage["From"]

            theNumber = whoSent.split("@")[0]
            carrier=whoSent.split("@")[1]

            a = re.search("[0-9]{10}", theNumber)
            if a == None:
                continue
            for part in emailMessage.walk():
                if part.get_content_type(
                ) == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    sentFromPhone = body.decode()
                    sentFromPhone = sentFromPhone.lower()

                    mms=self.getCarrier(carrier)
                    phone = theNumber + mms
                    theShabad = f"Please enter valid value for a shabad.\n \"{sentFromPhone}\" is not a valid"

                    h = SmsHukam()
                    if "random english" in sentFromPhone.lower(
                    ) or "1" in sentFromPhone.lower():
                        theShabad = h.engRandShabad()
                    elif "english hukam" in sentFromPhone.lower(
                    ) or "2" in sentFromPhone.lower():
                        theShabad = h.engHukam()
                    elif "rand" in sentFromPhone.lower(
                    ) or "new" in sentFromPhone.lower(
                    ) or "3" in sentFromPhone.lower():
                        theShabad = h.gurmukhiRand()
                    elif "hukam" in sentFromPhone.lower(
                    ) or "4" in sentFromPhone.lower():
                        theShabad = h.gurmukhiHukam()
                    elif "options" in sentFromPhone.lower(
                    ) or "5" in sentFromPhone.lower():
                        theShabad = "1. random english (get a randome shabad only in english)\n2. English Hukam(get the Darbar sahib Hukamnam only in english. This also has audio attachments)\n3. random (get random shabad with Gurmukhi)\n4. Hukam(get Darbar Sahib Hukamnama with Gurmukhi)\n5. See Options again\n(Type the option you want or the corresponding number!!)"
                    h.sendToPhone("ShabadGuru", theShabad, phone)
                    print("sent")
    def getCarrier(self,car):
        opts={'txt.att.net': '@mms.att.net', 'sms.myboostmobile.com': '@myboostmobile.com', 'mms.cricketwireless.net': '@mms.cricketwireless.net', 'msg.fi.google.com': '@msg.fi.google.com', 'messaging.sprintpcs.com': '@pm.sprint.com', 'vtext.com': '@vzwpix.com', 'tmomail.net': '@tmomail.net', 'message.ting.com': '@message.ting.com', 'email.uscc.net': '@mms.uscc.net', 'vmobl.com': '@vmpix.com', 'mms.att.net': '@mms.att.net', 'myboostmobile.com': '@myboostmobile.com', 'pm.sprint.com': '@pm.sprint.com', 'vzwpix.com': '@vzwpix.com', 'mms.uscc.net': '@mms.uscc.net', 'vmpix.com': '@vmpix.com'}
        return opts[car]


class IfTimeSendSms(Thread):
    def run(self):
        h = SmsHukam()
        while True:
            a = datetime.datetime.now()
            nowTime = a.strftime("%I:%M %p")
            if nowTime == "09:00 AM" or nowTime == "07:00 PM":
                hukam = h.engHukam()
                people = [
                    "6023802096@pm.sprint.com", "8622827105@pm.sprint.com",
                    "2018731477@pm.sprint.com", "6782670271@pm.sprint.com",
                    "6788628987@pm.sprint.com", "6786430348@pm.sprint.com",
                    "6787990390@pm.sprint.com", "7189155004@pm.sprint.com"
                ]
                for i in people:
                    h.sendToPhone("Daily Hukam", hukam, i)
            time.sleep(60)


class shabadEveryHour(Thread):
    def run(self):
        h = SmsHukam()
        while True:
            shabad = h.gurmukhiRand()
            h.sendToPhone("Every Hour", shabad, "6782670271@pm.sprint.com")
            time.sleep(60 * 60)


if __name__ == "__main__":
    sendToEveryOne = IfTimeSendSms()
    toMe = shabadEveryHour()

    sendToEveryOne.start()  #thread 1
    toMe.start()  #thread 2

    r = Reply()
    while True:
        KeepAlive()
        r.run()  #main thread
        time.sleep(10)
'''



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


