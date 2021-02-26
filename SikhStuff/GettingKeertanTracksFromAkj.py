import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--headless")
options.add_argument={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#my user agent
br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=options)


peopleUrl=[] #all urls for keertan pages of people. Not in function because we loop over getKeetani Func
def getKeertani(keertani):
    akj="https://www.akj.org/keertan.php"
    br.get(akj)
    dropDown=br.find_element_by_css_selector("#keert_drpdwn-selectized")
    dropDown.send_keys(keertani)
    optCont=br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-3.col-xs-12 > div > div.selectize-dropdown.single.selectpicker.select > div")
    opts=optCont.find_elements_by_class_name("option") #taking all the ooptions from dropdown menu and put in list
    optLst=[i.text for i in opts] #only the names are in this list as before there was other stuff in the list
    print(optLst)
    for i in range(len(optLst)):
        print(f'{i+1}) {optLst[i]}')
    if len(optLst)==0:
        print("invalid input. :(")
        return None
    elif len(optLst)==1:
        theKeertani=optLst[0]
    else:
        ind=int(input("Type the number for the keertani you want: "))-1
        theKeertani=optLst[ind]
    print(theKeertani)
    dropDown.send_keys(theKeertani) #type the exact keetani in the "search keertani"
    while True:
        try:
            optCont.find_element_by_class_name("option").click() #select that option
            break
        except:
            dropDown.clear()
            theKeertani=theKeertani[:-1]
            dropDown.send_keys(theKeertani)
    br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-12.text-center.keer-top-but > input").click() #click search button
    peopleUrl.append(br.current_url)

keertanTracks=[]
def getShabads(url):
    br.get(url)
    pluses=br.find_elements_by_class_name("fa-plus")
    for plus in pluses:
        plus.click()
        time.sleep(0.1) 
    atags=br.find_elements_by_tag_name("a")
    for atag in atags:
        link=atag.get_attribute("href")
        if link!=None:
            if 'Keertan' in link and "akj" in link and "mp3" in link:
                keertanTracks.append(link)
    nextPageUl=br.find_elements_by_class_name("setPaginate")
    if len(nextPageUl)>0:
        li=nextPageUl[0].find_elements_by_tag_name("li")
        actualPages=li[2:-2]
        theLinks=[i.find_element_by_tag_name("a").get_attribute("href") for i in actualPages] #get all the links for the differt pages of the keertani if they have more than 1
        for i in theLinks:
            if None not in theLinks:
                getShabads(i)
                print(theLinks.index(i),end=" ")
                print("Done!!!!!")
    print(len(keertanTracks))

def downloadShabads(tracks):
    c=0
    for i in tracks:
        c+=1
        title=i.replace('/',"#")
        urllib.request.urlretrieve(i,f"D:\\{c}){title[31:]}")
        print(i)

'''
allpeople=['bhai jaswant',"nirmal","sant"]
for i in allpeople:
    getKeertani(i)  #the getKeertan func puts the url of the person in list-peopleUrl

for i in peopleUrl:
    getShabads(i) #the getShabads func gets all the shabds from a person and puts them in list- keertanTracks
'''

getShabads("https://www.akj.org/keertan.php?cnt=10&loc=&yr=&mn=&keert=Bhai+Jagpal+Singh+Jee+%28Kanpur%29&search_keertan=Search+Keertan")
#downloadShabads(getShabads(peopleUrl))






    
