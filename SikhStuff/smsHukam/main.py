#from keepAlive import KeepAlive
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')
import timeBasedSending
import smsHukam
import reply
import time
import datetime

def preFillScrape():
    h=smsHukam.SmsHukam()
    engHukam=h.engHukam()
    gurmukhiHukam=h.gurmukhiHukam()
    engRand=[]
    gurmukhiRand=[]
    for i in range(10):
        print(f"Done with {i+1}")
        gurmukhiRand.append(h.gurmukhiRand())
        engRand.append(h.engRandShabad())
    return engHukam,gurmukhiHukam,engRand,gurmukhiRand

while True:
    #KeepAlive()

    sendToEveryOne=timeBasedSending.IfTimeSendSms()
    toMe=timeBasedSending.ShabadEveryHour()

    sendToEveryOne.start()  #thread 1
    toMe.start() #thread 2

    engHukam,gurmukhiHukam,engRand,gurmukhiRand=preFillScrape()
    audios=engHukam.split("Audios to listen to the Hukam: ")[-1]
    gurmukhiHukam+="\nAudios to listen to the Hukam:\n"+audios 

    r=reply.Reply()
    while True:
        r.run(engHukam,gurmukhiHukam,engRand,gurmukhiRand)  #main thread
        time.sleep(5)
        a=datetime.datetime.now()
        nowTime=a.strftime("%I:%M %p")
        print(nowTime)
        if nowTime=="11:00 AM": #replit sever is 4 hours ahead est, so 11am is 7am est
            break