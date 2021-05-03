from sendMsg import sendToPhone
import imaplib,email,re,random
import timeBasedSending


class Reply():
    def run(self,engHukam,gurmukhiHukam,engRand,gurmukhiRand):
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
            emailMessage = email.message_from_bytes(b)
            whoSent = emailMessage["From"]

            theNumber = whoSent.split("@")[0]
            carrier=whoSent.split("@")[1]

            a = re.search("[0-9]{10}", theNumber)
            if a == None:
                continue
            for part in emailMessage.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    sentFromPhone = body.decode()
                    sentFromPhone = sentFromPhone.lower()

                    mms=self.getCarrier(carrier)
                    phone = theNumber + mms
                    print(phone)
                    theShabad = f"Please enter valid value for a shabad.\n \"{sentFromPhone}\" is not a valid. Press 7 for options."
                    title="Not Valid"
                    if "random english" in sentFromPhone.lower() or "1" in sentFromPhone.lower():
                        title="Random Shabad(Only English)"
                        ind=random.randint(0,9)
                        theShabad=engRand[ind]
                    elif "english hukam" in sentFromPhone.lower() or "2" in sentFromPhone.lower():
                        title="Hukamnama from Darbar Sahib(Only English)"
                        theShabad=engHukam
                    elif "rand" in sentFromPhone.lower() or "new" in sentFromPhone.lower() or "3" in sentFromPhone.lower():
                        title="Random Shabad(With Gurmukhi)"
                        ind=random.randint(0,9)
                        theShabad=gurmukhiRand[ind]
                    elif "hukam" in sentFromPhone.lower() or "4" in sentFromPhone.lower():
                        title="Hukamnama fromDarbar Sahib(With Gurmukhi)"
                        theShabad=gurmukhiHukam

                    elif "add to daily hukam" in sentFromPhone or "5" in sentFromPhone:
                        title="added to daily hukamnama"
                        if phone not in timeBasedSending.IfTimeSendSms.people:
                            theShabad="You have been added to the daily hukamnama list."
                            timeBasedSending.IfTimeSendSms.people.append(phone)
                        else:
                            theShabad="You are already in the Daily hukamnam list"

                    elif "remove from daily hukam" in sentFromPhone or "6" in sentFromPhone:
                        title="removed from daily hukamnama"
                        theShabad="You have been removed to the daily hukamnama list."
                        try:
                            timeBasedSending.IfTimeSendSms.people.remove(phone)
                        except ValueError:
                            theShabad="You are not in the list"
                        
                    elif "options" in sentFromPhone.lower() or "7" in sentFromPhone.lower():
                        title="Options"
                        theShabad = "1. random english (get a randome shabad only in english)\n2. English Hukam(get the Darbar sahib Hukamnam only in english. This also has audio attachments)\n3. random (get random shabad with Gurmukhi)\n4. Hukam(get Darbar Sahib Hukamnama with Gurmukhi)\n5. Get added to daily Hukamnama list. (you will recive the daily hukamnama at 7 am EST)\n6. Remove from daily Hukamnama list\n7. See Options again\n(Type the option you want or the corresponding number!!)"
                    elif "$alleng" in sentFromPhone:
                        title="shUUU"
                        theShabad=str(engRand)
                    elif "$allgurmukhi" in sentFromPhone:
                        title="shUUU"
                        theShabad=str(gurmukhiRand)
                    sendToPhone(title,theShabad,phone)
                    print("sent")
    def getCarrier(self,car):
        opts={'txt.att.net': '@mms.att.net', 'sms.myboostmobile.com': '@myboostmobile.com', 'mms.cricketwireless.net': '@mms.cricketwireless.net', 'msg.fi.google.com': '@msg.fi.google.com', 'messaging.sprintpcs.com': '@pm.sprint.com', 'vtext.com': '@vzwpix.com', 'tmomail.net': '@tmomail.net', 'message.ting.com': '@message.ting.com', 'email.uscc.net': '@mms.uscc.net', 'vmobl.com': '@vmpix.com', 'mms.att.net': '@mms.att.net', 'myboostmobile.com': '@myboostmobile.com', 'pm.sprint.com': '@pm.sprint.com', 'vzwpix.com': '@vzwpix.com', 'mms.uscc.net': '@mms.uscc.net', 'vmpix.com': '@vmpix.com'}
        return opts[car]