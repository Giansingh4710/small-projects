from selenium import webdriver
import time
import urllib.request

options = webdriver.ChromeOptions()
options.headless = True
br = webdriver.Chrome('C:\\Users\\gians\\Desktop\\stuff\\chromedriver.exe',options=options)

facebookLinks=[
    "https://www.facebook.com/388765791243633/videos/825267938249859",
    "https://www.facebook.com/388765791243633/videos/270165670964426",
    "https://www.facebook.com/388765791243633/videos/1263586260684432",
    "https://www.facebook.com/388765791243633/videos/387404689097735",
    "https://www.facebook.com/388765791243633/videos/2736843553229652",
    "https://www.facebook.com/388765791243633/videos/778799682965214",
    "https://www.facebook.com/388765791243633/videos/780307126034844",
    "https://www.facebook.com/388765791243633/videos/997143157453387",
    "https://www.facebook.com/388765791243633/videos/689347551956816",
    "https://www.facebook.com/388765791243633/videos/649491149087258",]
count=0
for i in facebookLinks:
    time.sleep(2)
    br.get("https://www.getfvid.com/")
    time.sleep(1)
    br.find_element_by_css_selector("#form_download > div > input").send_keys(i) #sending link
    br.find_element_by_css_selector("#btn_submit").click()
    audioButton=br.find_element_by_css_selector("body > div.page-content > div > div > div.col-lg-10.col-md-10.col-centered > div > div:nth-child(3) > div > div.col-md-4.btns-download > p:nth-child(2) > a")
    url=audioButton.get_attribute("href")
    time.sleep(2)
    count+=1
    #urllib.request.urlretrieve(url,f'D:\\AkhandPaatDelih2020\\Part{count}.mp3')
    print(url)

