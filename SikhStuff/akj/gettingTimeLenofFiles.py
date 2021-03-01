import os
from mutagen.mp3 import MP3

directory = "D:\\"
os.chdir(directory)
timeInSeconds=0
for book in os.listdir(directory):
    if book!="System Volume Information":
        for chapter in os.listdir(book):
            thePath=f'{directory}{book}\\{chapter}'
            audio=MP3(thePath)
            timeInSeconds+=audio.info.length
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