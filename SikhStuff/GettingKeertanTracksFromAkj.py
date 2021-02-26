import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--headless")
options.add_argument={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#my user agent
br = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')#,options=options)


allUrls=[]
def getKeertani(keertani):
    akj="https://www.akj.org/keertan.php"
    br.get(akj)
    TheKeertanDropdownMenue=br.find_element_by_css_selector("#keert_drpdwn-selectized")
    TheKeertanDropdownMenue.send_keys(keertani)
    optionsContainer=br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-3.col-xs-12 > div > div.selectize-dropdown.single.selectpicker.select > div")
    optionsList=optionsContainer.find_elements_by_class_name("option") #taking all the ooptions from dropdown menu and put in list
    optionsList=[i.text for i in optionsList] #only the names are in this list as before there was other stuff in the list
    print(optionsList)
    for i in range(len(optionsList)):
        print(f'{i+1}) {optionsList[i]}')
    numForKerrtani=int(input("Type the number for the keertani you want: "))-1
    print(optionsList[numForKerrtani])
    TheKeertanDropdownMenue.send_keys(optionsList[numForKerrtani]) #type the exact keetani in the "search keertani"
    optionsContainer.find_element_by_class_name("option").click() #select that option
    br.find_element_by_css_selector("body > div.container > form > div > div > div > div.col-md-12.text-center.keer-top-but > input").click() #click search button
    print(br.current_url)
    allUrls.append(br.current_url)
        #br.get_screenshot_as_file("screenshot.png")

list="sant"
getKeertani(list)
'''
def getShabads():
    pass
def downloadShabads():
    pass
'''
