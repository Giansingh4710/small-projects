import smtplib
from email.message import EmailMessage

def sendToPhone(subject,body,to):
    msg=EmailMessage()

    user='giansingh131313@gmail.com'
    password='jkodhyxiypnsdifl'

    msg["From"]=user
    msg['Subject']=subject
    msg["To"]=to
    msg.set_content(body)
    

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg,mail_options='SMTPUTF8')
    server.quit()