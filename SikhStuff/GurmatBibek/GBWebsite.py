import requests
from bs4 import BeautifulSoup as bs

urls=["https://www.gurmatbibek.com/pages.php?id=3","https://www.gurmatbibek.com/pages.php?id=4"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def getLinks():
    dict={}
    for url in urls:
        res=requests.get(url,headers=headers)
        soup=bs(res.text,"lxml")
        theArticles=soup.find("td",class_="text1",height="400",valign="top")
        theArticles=theArticles.find_all("li")
        for article in theArticles:
            title=article.text
            link=article.find('a').get("href")
            #print(f'{link}: {title}')
            dict[link]=title
    return dict

def getArticle(mnTp):
    dict={}
    for topic in mnTp:  #main topic
        dict[mnTp[topic]]=[] 
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
                dict[mnTp[topic]].append(link);dict[mnTp[topic]].append(article.text); #put the link of the subtopic article and title in the dict whose key is the main topic
    counter=0
    for i in dict:
        counter+=len(dict[i]/2)
        print(counter)
                

mainTopics=getLinks()
getArticle(mainTopics)



