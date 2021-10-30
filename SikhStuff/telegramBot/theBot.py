import telegram.ext
from apiKey import ACCESS_TOKEN 
import time,re

#have a repeating vaheguru
#reapeating shabad.
#hukamnama from darbar sahib
#sdoji random kirtan link
#sant giani gurbachan singh ji katha link

from telegram.ext import CommandHandler,Updater

allRepeatingMsg={}
def repeater(update: telegram.Update, context: telegram.ext.CallbackContext):
    msgAfterRpt=update.message.text.replace("/repeat","")

    def sendMsg(context: telegram.ext.CallbackContext):
        context.bot.send_message(chat_id=context.job.context, text=msgAfterRpt)
    if msgAfterRpt=="":
        context.bot.send_message(chat_id=update.message.chat_id,text="Please enter a message after '/repeat'")
        return

    if update.message.chat_id not in allRepeatingMsg:
        allRepeatingMsg[update.message.chat_id]=[msgAfterRpt]
    else:
        allRepeatingMsg[update.message.chat_id].append(msgAfterRpt)

    context.bot.send_message(chat_id=update.message.chat_id,text=f'Will repeat {msgAfterRpt}')
    a=context.job_queue.run_repeating(sendMsg, 2, context=update.message.chat_id)
    print(a)

def stop_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,text='Stoped!')
    context.job_queue.stop()

u = Updater(ACCESS_TOKEN, use_context=True)
# j = u.job_queue
repeat = CommandHandler('repeat', repeater)
stoper = CommandHandler('stop', stop_timer)
u.dispatcher.add_handler(repeat) 
u.dispatcher.add_handler(stoper) 
u.start_polling()
u.idle()














# def start(update,context):
#     update.message.reply_text("HELLLo, Using other mod")
#     print(update)
#     print(context)
#     print("inStart")

# def help(update,context):
#     print("in help")
#     update.message.reply_text("""
#     The following commands available:

#     /start -> adds you to database
#     /help -> This message
#     """
#     )


# updater=telegram.ext.Updater(ACCESS_TOKEN,use_context=True)
# dispatch=updater.dispatcher

# dispatch.add_handler(telegram.ext.CommandHandler("start",start))
# dispatch.add_handler(telegram.ext.CommandHandler("help",help))

# updater.start_polling()
# updater.idle()













































# import telebot #pyTelegramBotAPI

# bot=telebot.TeleBot(ACCESS_TOKEN)
# allUsers={} #key is chat.id value is all info needed

# @bot.message_handler(commands=["start"])
# def start(msg):
#     theId=msg.chat.id
#     if theId not in allUsers:
#         allUsers[theId]={
#             'repeatingMsg':{
#                 #the text to repeat: repeat every x seconds
#                 # "vaheguru":10
#             }
#         }
#         bot.reply_to(msg,"Welcome to Vaheguru_bot!");
#         bot.reply_to(msg,"Comands\n1) repeat x every y minutes\n2)reply to the repeating message 'stop' to stop the repeating message");
#     else:
#         bot.reply_to(msg,"Welcome again");   

# def getRepeatingTimeInSeconds(string):
#     seconds=100
#     try:
#         timeSearch=re.compile(r"(every ([0-9]{1,5})\s[m||s||h]+)")
#         theMatch=timeSearch.search(string.lower())
#         a=theMatch.group()
#         time=int(theMatch.group(2))
#         if a[-1]=="s":
#             seconds=time
#         if a[-1]=="m":
#             seconds=time*60
#         if a[-1]=="h":
#             seconds=time*60*60
#     except Exception:
#         print("no time given. Default 100 seconds")
#     return seconds

    
# def checkRepeat(msg):
#     msgTextLst=msg.text.lower().split()

#     if msgTextLst[1]=="every":
#         bot.reply_to(msg,"Nothing entered after repeat so will not repeat.\n Enter message after 'repeat' and before 'every'")
#         return False
#     if len(msgTextLst)<2:
#         bot.reply_to(msg,"Nothing entered after repeat so will not repeat")
#         return False
#     elif allUsers[msg.chat.id]['repeatingMsg']=={}:
#         endIndex=len(msgTextLst)
#         if "every" in msgTextLst:
#             endIndex=msgTextLst.index("every")

#         allUsers[msg.chat.id]['repeatingMsg']["text"]=" ".join(msg.text.split()[1:endIndex])
#         allUsers[msg.chat.id]['repeatingMsg']["repeat"]=getRepeatingTimeInSeconds(msg.text)
#         print(allUsers)
#         return True
#     else:
#         bot.reply_to(msg,"You already have a repeating message. Stop that message to start a new one")
#         return False

# def valid(msg):
#     if "repeat" ==msg.text.lower().split()[0]:
#         return checkRepeat(msg)
#     elif "stop" in msg.text.lower():
#         return True
#     elif "see repeating message" in msg.text.lower():
#         return True
#     bot.reply_to(msg,f"Invalid message!!")
#     bot.send_message(msg.chat.id,"Valid Commands\n1) Repeat (type a message you would like to repeat\nexp: repeat Vaheguru)")
#     return False

# @bot.message_handler(func=valid)
# def sendMsg(msg):
#     if msg.text.lower().split()[0]=="repeat":
#         sendRepeatingMsg(msg)
#     elif msg.text.lower().split()[0]=="stop":
#         stopRepeatingMsg(msg)
#     elif msg.text.lower()=="see repeating message":
#         showRepeationMsg(msg)

# def sendRepeatingMsg(msg):
#     theRepeatingText=allUsers[msg.chat.id]['repeatingMsg']["text"]
#     while allUsers[msg.chat.id]['repeatingMsg']!={}:
#         print(msg.text,msg.id,msg.chat.id)

#         #TODO
#         if theRepeatingText.lower().replace(" ","")=="newgurbanishabad":
#             pass
#         if theRepeatingText.lower().replace(" ","")=="randomgurbanishabad":
#             pass
#         bot.send_message(msg.chat.id,theRepeatingText);
#         time.sleep(allUsers[msg.chat.id]['repeatingMsg']["repeat"])
# def stopRepeatingMsg(msg):
#     try:
#         msgToDel=msg.reply_to_message.text
#         if msgToDel == allUsers[msg.chat.id]['repeatingMsg']["text"]:
#             allUsers[msg.chat.id]['repeatingMsg']={}
#             bot.send_message(msg.chat.id,f"Deleted Repeating Message: \n "+msgToDel);
#     except Exception as e:
#         bot.send_message(msg.chat.id,f"Nothing to delete. Please reply to the message that you would like to delete");
#         print(e)
# def showRepeationMsg(msg):
#     theMsg="You have no Repeating Message"
#     if 'text' in allUsers[msg.chat.id]['repeatingMsg']:
#         theMsg="Repeating Message: "+allUsers[msg.chat.id]['repeatingMsg']["text"]+"\nRepeats every: "+str(allUsers[msg.chat.id]['repeatingMsg']["repeat"])
#     print(theMsg)
#     bot.send_message(msg.chat.id,theMsg)
    

# bot.polling()