import urllib.request
from selenium import webdriver
import time,os

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--headless")
options.add_argument={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#my user agent
br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe')#,options=options)

def getKeertanis(keertanis):
    peopleUrl={}
    for keertani in keertanis:
        br.get("https://www.akj.org/keertan.php")
        dropDown=br.find_element_by_css_selector("#keert_drpdwn-selectized")
        dropDown.send_keys(keertani) #send name of keertani to input box
        optCont=br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-3.col-xs-12 > div > div.selectize-dropdown.single.selectpicker.select > div")
        opts=optCont.find_elements_by_class_name("option") #taking all the options from dropdown menu and put in list
        optLst=[i.get_attribute("data-value") for i in opts] #only the names are in this list as before there was other stuff in the list
        for i in range(len(optLst)):
            print(f'{i+1}) {optLst[i]}')
        if len(optLst)==0:
            print("invalid input. :(")  #No keertanis of that name
            continue
        elif len(optLst)==1:
            theKeertani=optLst[0]  #only 1 option so no need to chose
        else:
            ind=int(input("Type the number for the keertani you want: "))-1  #if more than 1 keertani of that name, you can pick which one you want
            theKeertani=optLst[ind]  
        print(theKeertani)
        dropDown.send_keys(theKeertani) #type the exact keetani in the "search keertani"
        while True:
            try: #selecting the keertani becomes glitchi sometimes so its in a while loop till it picks the option and in a try/except so that if somthing glitchy happens it won't break the program
                optCont.find_element_by_class_name("option").click() #select that option
                break
            except Exception:
                dropDown.clear()
                theKeertani=theKeertani[:-1] #keep deleting 1 letter off the name util there is a dropdown option. If you put the name fully correct, sometimes it doesn't show options to click'
                dropDown.send_keys(theKeertani)
        br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-12.text-center.keer-top-but > input").click() #click search button
        peopleUrl[theKeertani]=br.current_url
    print(peopleUrl)
    return peopleUrl

#this will take in the dictionary generated from the getKeertanis func
def getShabads(keertanis):
    print("Finding tracks...")
    keertanTracks={}
    for keertani in keertanis:
        br.get(keertanis[keertani]) #the key is the name and the value is the url
        pluses=br.find_elements_by_class_name("fa-plus")
        keertanTracks[keertani]=[]
        for plus in pluses:
            plus.click()
            time.sleep(0.2)  #All this code above in this func is to open all the '+' buttons on the akj website so I can scrape the shabads
        atags=br.find_elements_by_tag_name("a")
        for atag in atags:
            link=atag.get_attribute("href")
            if link!=None:
                if 'Keertan' in link and "akj" in link and "mp3" in link:  #there are alot of href links on the site so this basiclly only adds the keertani file and not the other links
                    keertanTracks[keertani].append(link)
        nextPageUl=br.find_elements_by_class_name("setPaginate") #on the buttom of the page, if the keetani has more than 1 page of keertani, this will be there
        if len(nextPageUl)>0: #if more than one page
            li=nextPageUl[0].find_elements_by_tag_name("li")
            actualPages=li[2:-2] #so basically the buttom page switcher is a ul tag. The first li tag is to let you know what page your are on like "Page 2 of 4". The last two li tags are "Next" and "Last" buttons
            theLinks=[i.find_element_by_tag_name("a").get_attribute("href") for i in actualPages] #get all the links for the differt pages of the keertani if they have more than 1
            for i in theLinks: #links to the differt pages of the same keerani
                if None not in theLinks:  #When you are on like page "2 of 5", the second li tag will have no href since you are in that link rn so it will give none. This way in the next itteration when you recurse, it wont keep recusing again becaue there will be a none in the list. This way it will only recurse once for each page
                    tracksOnOtherPage=getShabads({keertani:i})
                    for track in tracksOnOtherPage[keertani]:
                        keertanTracks[keertani].append(track)
    return keertanTracks 


def download(keertanis,thePath):
    print("Now downloading")
    for keertani in keertanis:
        counter=0
        path=thePath+keertani
        os.mkdir(path)
        for track in keertanis[keertani][::-1]: # the [::-1] means the list is reversed. I want the old tracks to be downloaded first
            counter+=1
            print(track)
            b=track.split('/')
            title=b[-1][:-1]+"3"
            print(b)
            title=f"{counter}) {title}"
            try:
                urllib.request.urlretrieve(track,f"{path}\\{title}")
                print(title)
            except Exception:
                print(f"Couldn't download: {title}")
            if counter==10: #bhai gagandeep singh ji wanted only 10 tracks of each keertani
                break

# keertanis=["Bibi Sant Kaur","bhai harsimran singh", "bibi harkiran kaur", "bhai gurbir singh","bibi baljinder kaur", "bhai jagjit singh", "bhai amolak singh","bhai harpreet singh toronto","bhai prabhjot singh delhi","bhai gurinder singh california","bhai davinderbir singh","bhai gursharan singh faridabad","bhai pritpal singh regina", "bhai dilveer singh"]
keertanis=["gian","giaan"]
a=getKeertanis(keertanis)
path="D:\\"
download(getShabads(a),path)



    
