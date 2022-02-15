import random,pyperclip,sys

all="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,<.>/?'[]}{!@#$%^&*()_=1234567890-=/*-+`~"
letsandnums="1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
def password():
    passworrd=""
    if len(sys.argv)==1:
        size=int(input("what is the lenght you want your Password to be?: "))
        allorsome=input("Do you want just nums and letters (type yes or no): ")
        restrictions=input("type any characters that you don't want the password to contain or just hit enter: ")
    else:
        size=int(sys.argv[1])
        allorsome='no'
        restrictions=""
    if 'n' in allorsome.lower():
        for i in range(size):
            ind=random.randrange(0,len(all));
            while all[ind] in restrictions:
                ind=random.randrange(0,len(all))
            passworrd+=all[ind]        
    else:
        for i in range(size):
            ind=random.randrange(0,len(letsandnums));
            while letsandnums[ind] in restrictions:
                ind=random.randrange(0,len(letsandnums));
            passworrd+=letsandnums[ind]
    return passworrd
a=password()
pyperclip.copy(a)


otherInfo=input("type the website and/or username: ")
passwords=open("C:\\Users\\gians\\Desktop\\stuff\\passwordGen.txt",'a')
passwords.write(otherInfo+ ' , '+a+'\n')
passwords.close()
print(otherInfo+ ' , '+a+'\n')







    
       
