opts={"txt.att.net":"@mms.att.net","sms.myboostmobile.com":"@myboostmobile.com","mms.cricketwireless.net":"@mms.cricketwireless.net","msg.fi.google.com":"@msg.fi.google.com","messaging.sprintpcs.com":"@pm.sprint.com",
"vtext.com":"@mypixmessages.com","tmomail.net":"@tmomail.net","message.ting.com":"@message.ting.com","email.uscc.net":"@mms.uscc.net","vtext.com":"@vzwpix.com","vmobl.com":"@vmpix.com"}

new={}
print(len(opts))
for i in opts:
    new[opts[i][1:]]=opts[i]
for i in new:
    opts[i]=new[i]

print(len(opts))
print(opts)