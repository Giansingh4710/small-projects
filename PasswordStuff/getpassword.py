import pyperclip, sys

def getpass(username):    
    file=open("C:\\Users\\gians\\Desktop\\stuff\\passwordGen.txt",'r')
    filee=file.readlines()
    file.close()
    dict={}
    for i in filee:
        try:
            lst=i.split(",")
            user=lst[0].strip().lower()
            passw=lst[1].strip()
            dict[user]=passw
        except:
            continue
    possibility=[i for i in dict if username in i ]
    if len(possibility)==0: 
        print("no password for this key")
        return "bye"
    if len(possibility)==1:
        print(f'Password "{dict[possibility[0]]}" copied for {possibility[0]}') 
        return dict[possibility[0]]
    for i in range(len(possibility)):
        print(f"{i+1}) {possibility[i]}")
    print("Select the Number: ", end=' ')
    num=int(input())-1
    print(f'Password "{dict[possibility[num]]}" copied for {possibility[num]}')
    return dict[possibility[num]]
if len(sys.argv)>1:       
    pyperclip.copy(getpass(sys.argv[1]))
else:
    print('Enter the Key: ', end=" ")
    a=input()
    pyperclip.copy(getpass(a))    






