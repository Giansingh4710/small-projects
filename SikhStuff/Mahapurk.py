import requests
from bs4 import BeautifulSoup as bs

url="http://www.mahapurakh.com/"

res=requests.get(url)
soup=bs(res.text,"lxml")
atags=soup.find_all('a')
links=[]
for i in atags: 
    href=i.get("href")
    if href==None: continue
    if url not in href:
        href=url+href
    if "PDF" not in href:
        links.append(href)
for i in links[4:]:
    print(i)
    break