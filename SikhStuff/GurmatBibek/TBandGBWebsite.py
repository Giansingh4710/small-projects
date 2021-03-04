import requests
from bs4 import BeautifulSoup as bs

urls=["https://www.gurmatbibek.com/pages.php?id=3","https://www.gurmatbibek.com/pages.php?id=4"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def getLinks():
    dictt={}
    for url in urls:
        res=requests.get(url,headers=headers)
        soup=bs(res.text,"lxml")
        theArticles=soup.find("td",class_="text1",height="400",valign="top")
        theArticles=theArticles.find_all("li")
        for article in theArticles:
            title=article.text
            link=article.find('a').get("href")
            #print(f'{link}: {title}')
            dictt[link]=title
    return dictt

def getArticle(mnTp):
    dictt={}
    for topic in mnTp:  #main topic
        dictt[mnTp[topic]]=[] 
        res=requests.get(topic,headers=headers)
        soup=bs(res.text,"lxml")
        theArticles=soup.find("td",class_="text1",height="400",valign="top")
        theArticles=theArticles.find_all("li")
        for article in theArticles:
            link=article.find("a").get("href")
            res2=requests.get(link)  
            soup2=bs(res2.text,"lxml")
            theArticles2=soup2.find("td",class_="text1",height="400",valign="top")
            if theArticles2==None:
                dictt[mnTp[topic]].append(article.text);dictt[mnTp[topic]].append(link); #put the link of the subtopic article and title in the dictt whose key is the main topic
    return dictt
def onlyEnglish(topics):
    for mainTopic in topics:
        for i in range(len(topics[mainTopic])):
            if i%2==0:
                link=topics[mainTopic][i]
                title=topics[mainTopic][i+1]
                theLine=link+" : "+title
                try:
                    filee.write(theLine+"\n")
                except UnicodeEncodeError:
                    print("Can't write in gurmukhi in files! ;(")
def tapoban():
    url="http://www.tapoban.org/webforum/list.php?1,page="
    filee=open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibekArticles.txt","a")
    for i in range(23):
        print("Page"+str(i+1))
        newUrl=url+str(i+1)
        res=requests.get(newUrl)
        soup=bs(res.text,"lxml")
        container=soup.find("table",border="0",cellspacing="0",class_="PhorumStdTable")
        articles=container.find_all("tr")[1:]
        for article in articles: 
            atag=article.find("a")
            href="http://www.tapoban.org"+atag.get("href")
            title=atag.text
            fullLine=title+" : "+href
            try:
                filee.write(fullLine+"\n")
            except UnicodeEncodeError:
                print("CAN'T OPEN: ",end="")
            print(fullLine)
    filee.close()
filee=open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibekArticles.txt",'w') #I took all the links from the articles and put them into this file. To view 
mainTopics=getLinks()
allSubTopics=getArticle(mainTopics)
onlyEnglish(allSubTopics)
filee.close()
tapoban()

    



