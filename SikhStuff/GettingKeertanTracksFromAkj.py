import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select

#options = webdriver.ChromeOptions()
#options.headless = True
#options.add_argument("--headless")
#options.add_argument={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#my user agent
br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')#,options=options)


allUrls=[]
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
    print(br.current_url)
    allUrls.append(br.current_url)
        #br.get_screenshot_as_file("screenshot.png")

allpeople=['bhai jaswant',"nirmal","gian"]
for i in allpeople:
    getKeertani(i)
print(allUrls)
'''
def getShabads():
    pass
def downloadShabads():
    pass
'''
