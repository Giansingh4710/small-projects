import requests, time,webbrowser,random
from bs4 import BeautifulSoup
from selenium import webdriver
options = webdriver.ChromeOptions()  # will use in writeInFile function to copy gurmukhi titles and go to google translate to chage to english so that it can be written in infile
#options.headless = True

def getLinkstoEachArticle(urlLst):
    mainDict={}
    for url in urlLst:
        res=requests.get(url)
        soup=BeautifulSoup(res.text,"html.parser")
        cont=soup.find_all("article")
        for article in cont:
            title=article.find("h1").text
            link=article.find("h1").find("a").get("href")
            mainDict[title]=link
    return mainDict
def writeInFile(dictt):
    br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)
    br.get("https://www.google.com/search?q=gurmukhi+to+english")
    punjabiTextBox=br.find_element_by_css_selector("#tw-source-text-ta")
    filee=open("C:\\Users\\gians\\Desktop\\stuff\\SikhUnityWordPress.txt","w")
    for i in dictt:
        try:
            filee.write(i+" $$$ "+dictt[i]+"\n")
        except UnicodeEncodeError:
            print(i+" : Going to google and translating the Gurmukhi title")
            punjabiTextBox.clear()
            punjabiTextBox.send_keys(i)
            eng=br.find_element_by_css_selector("#tw-target-text > span").text
            filee.write(eng+" $$$ "+dictt[i]+"\n")
            time.sleep(1)
    time.sleep(20)
    filee.close()
# it would take like 30 seconds to scrape ALL the links so I am just scraping once, and writing the title and links to artilces in a text file. 
# Then I will read the file every time i run the program. The two fuctions above are to be run once. After that they should not run


def makeDict():
    filee=open("C:\\Users\\gians\\Desktop\\stuff\\SikhUnityWordPress.txt","r")
    filee=filee.readlines()
    dictt={}
    for line in filee:
        title=line.split(" $$$ ")[0]
        link=line.split(" $$$ ")[1][:-1]
        dictt[title]=link
    return dictt

def choose(dictt):
    titles=[]
    links=[]
    ask=input("Enter an article (type 'random' for random articles): ")
    if ask.lower()=="random":
        titlelst=list(dictt.keys())
        vallst=list(dictt.values())
        for i in range(10):
            randNum=random.randint(0,len(titlelst)-1)
            titles.append(titlelst[randNum])
            links.append(vallst[randNum])
    else:
        for i in dictt:
            if ask.lower() in i.lower():
                titles.append(i); links.append(dictt[i])
    while True:
        for i in range(len(links)):
            print(f"{i+1} ) {titles[i]}")
        try:
            ind=int(input("Enter a number to select the article: "))-1
            webbrowser.open(links[ind])
        except ValueError:
            print("Not a valid number!! :(")
        except IndexError:
            print("No article found corresponding to that number")

        samelist=input("Want to see the same list of articles? (Y or N): ")
        if "y" in samelist.lower():
            continue
        break
    
    again=input("Would you like to try again? (Y or N): ")
    if "n" in again.lower():
        print("BYEEEEE!!!")
        return
    else:
        choose(dictt)

allLinks=makeDict()
choose(allLinks)      
'''
This was run once to print the article into a text file. Now no need to run as text file is made.

Baseurl="https://sikhunity.wordpress.com/page/"
urls=[Baseurl+str(i+1) for i in range(57)]
links=getLinkstoEachArticle(urls)
#print(links)
writeInFile(links)
'''


