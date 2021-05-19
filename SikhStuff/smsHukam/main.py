from keepAlive import KeepAlive

import timeBasedSending
import smsHukam
import reply
import time
import datetime


def preFillScrape():
	h = smsHukam.SmsHukam()
	engHukam = h.engHukam()
	gurmukhiHukam = h.gurmukhiHukam()
	gurmukhiRand = []
	for i in range(10):
		print(f"Done with {i+1}")
		gurmukhiRand.append(h.gurmukhiRand())
	return engHukam, gurmukhiHukam, gurmukhiRand


while True:
	KeepAlive()

	sendToEveryOne = timeBasedSending.IfTimeSendSms()
	toMe = timeBasedSending.ShabadEveryHour()

	sendToEveryOne.start()  #thread 1
	toMe.start()  #thread 2

	engHukam, gurmukhiHukam, gurmukhiRand = preFillScrape()
	r = reply.Reply()
	while True:
		r.run(gurmukhiHukam, gurmukhiRand)  #main thread
		time.sleep(5)
		a = datetime.datetime.now()
		nowTime = a.strftime("%I:%M %p")
		if nowTime == "04:00 AM":  #replit sever is 4 hours ahead est,
			break
