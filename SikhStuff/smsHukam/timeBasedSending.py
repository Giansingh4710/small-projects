from sendMsg import sendToPhone
import smsHukam
import time
from threading import Thread
import datetime


class ShabadEveryHour(Thread):
	def run(self):
		#h=smsHukam.SmsHukam()
		#shabad=h.gurmukhiRand()
		count=0
		while True:
			count+=1
			shabad = "ਵਾਹਿਗੁਰੂ"
			sendToPhone("Remember", shabad, "6782670271@pm.sprint.com")
			a = datetime.datetime.now()
			nowTime = a.strftime("%I:%M %p")
			print(f"{count}){shabad} reminder sent: {nowTime}")
			time.sleep(3600*10)


class IfTimeSendSms(Thread):
	people = [
	    "6023802096@pm.sprint.com", "8622827105@pm.sprint.com",
	    "2018731477@pm.sprint.com", "6782670271@pm.sprint.com",
	    "6788628987@pm.sprint.com", "6786430348@pm.sprint.com",
	    "6787990390@pm.sprint.com", "7189155004@pm.sprint.com",
	    "6502915125@vzwpix.com", "2017790904@tmomail.net",
	    "2017471618@vzwpix.com"
	]

	def run(self):
		h = smsHukam.SmsHukam()
		while True:
			a = datetime.datetime.now()
			nowTime = a.strftime("%I:%M %p")
			if nowTime == "02:00 PM":
				hukam = h.gurmukhiHukam()
				for i in IfTimeSendSms.people:
					sendToPhone("Daily Hukam", hukam, i)
					print(f"Sent hukamnama to {i}")
			time.sleep(60)


def sendBegingToAll():
	hukam = "Vaheguru Ji Ka Khalsa, Vaheguru Ji Ki Fathe.\nThis is an automated Shabad sender. You all are already in the the daily hukamanama list. To remove yourself, press '4'. There may be some bugs. Will try my best to fix as we go. (Press '5' for all options)"
	for i in IfTimeSendSms.people:
		sendToPhone("Hello", hukam, i)
