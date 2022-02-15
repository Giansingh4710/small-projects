from selenium import webdriver
from time import sleep

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#my user agent
br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)

url='https://gurmatbibek.com/forum/list.php?3,page='
f=open("C:\\Users\\gians\\Desktop\\stuff\\gurmatbibek.txt",'w')
for i in range(185):
    f.write(f'Page {i+1}\n')
    newUrl=url+str(i+1)
    br.get(newUrl)

    fourm=br.find_element_by_css_selector('#phorum > table')
    topics=fourm.find_elements_by_tag_name("tr")
    AllTopics=[]
    num=0
    for i in topics:
        try:
            topic=i.find_elements_by_tag_name("td")
            name=topic[2].text
            about=topic[1].text
            link=topic[1].find_element_by_tag_name('a').get_attribute('href')
            num+=1
            AllTopics.append(f'{num}) {name} :  {about}, {link}')
        except:
            print("no good")
    for i in AllTopics:
        try:
            f.write(i)
            f.write('\n')
        except:
            print("no write")

br.close()
f.close()