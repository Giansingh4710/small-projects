import sys

user=input("What is the username?: ")
password=input("What is the password?: ")
file=open("C:\\Users\\gians\\Desktop\\stuff\\passwordGen.txt",'a')
file.write(user+" , "+password)
file.close()