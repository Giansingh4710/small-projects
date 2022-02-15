import os
from mutagen.mp3 import MP3


timeInSeconds=0
count=0
def goThroughFiles(dir):
    global timeInSeconds
    global count
    for thing in os.listdir(dir):
        if thing=="System Volume Information": continue
        path=dir+"\\"+thing
        if os.path.isdir(path):
            goThroughFiles(path)
        elif os.path.isfile(path):
            try:
                count+=1
                audio=MP3(path)
                timeInSeconds+=audio.info.length
                print(path)
            except Exception as e:
                print(f'{thing} failed : {e}')
                continue
    return timeInSeconds,count                     


def nicePrint(seconds):
    print(f"There are a total of {seconds} seconds of audio which is also:")
    minutes=seconds/60
    print(f"Minutes: {minutes}")
    hours=minutes/60
    print(f"Hours: {hours}")
    days=hours/24
    print(f"Days: {days}")

    fullDays=seconds//(60*60*24)
    timeleft=seconds-fullDays*(60*60*24)
    fullHour=timeleft//(60*60)
    timeleft=timeleft-fullHour*(60*60)
    fullminutes=timeleft//60
    timeleft=timeleft-fullminutes*60
    print("So in total:", end=" ")
    print(f"{int(fullDays)} days, {int(fullHour)} hours, {int(fullminutes)} minutes, {int(timeleft)} seconds")

directory = "C:\\Users\\gians\\Desktop\\test\\WhyGuru Course"
#directory = "D:\\"
os.chdir(directory)
a,count=goThroughFiles(directory)
nicePrint(a)
print(f"Total Files: {count}")

'''
count=0
for book in os.listdir(directory):
    if book!="System Volume Information":
        for chapter in os.listdir(book):
            thePath=f'{directory}{book}\\{chapter}'
            audio=MP3(thePath)
            timeInSeconds+=audio.info.length
            count+=1
            print(count,end=": ")
            print(timeInSeconds)
print(f"There are a total of {timeInSeconds} seconds of audio which is also:")
minutes=timeInSeconds/60
print(f"Minutes: {minutes}")
hours=minutes/60
print(f"Hours: {hours}")
days=hours/24
print(f"Days: {days}")

fullDays=timeInSeconds//(60*60*24)
timeleft=timeInSeconds-fullDays*(60*60*24)
fullHour=timeleft//(60*60)
timeleft=timeleft-fullHour*(60*60)
fullminutes=timeleft//60
timeleft=timeleft-fullminutes*60
print("So in total:", end=" ")
print(f"{int(fullDays)} days, {int(fullHour)} hours, {int(fullminutes)} minutes, {int(timeleft)} seconds")
'''