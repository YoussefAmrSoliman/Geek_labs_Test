from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver  
from datetime import datetime , timedelta
import time 
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 

# INPUTS
Ticker = input("insert Ticker:")
time_interval = int(input("minutes:"))  #minutes
n = int(input("number off accounts to scrape:"))
links=[]


occ_num = 0
for i in range(n):
    links.append(input("insert link:"))
browser = webdriver.Chrome() 
for i in range(n):
    posts = []
    browser.get(links[i])
    screen_height = browser.execute_script("return window.screen.height;")
    
    # web driver to load html dynamicly
    for j in range(0,15):
        time.sleep(2)
        browser.execute_script(f"window.scrollBy(0,{screen_height *1})","")
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        date = soup.findAll(class_="css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21") # Selecting all of the anchors with titles
        text = soup.findAll(class_="css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim")
        post = [(date[i].time['datetime'],text[i].text,text[i]['id']) for i in range(len(date))]
        for k in range(len(post)):
            f = True
            for l in range(len(posts)):
                if posts[l][2] == post[k][2]:
                    f = False
            if f == True:    
                posts.append(post[k])
        
        j+=1 

    # Posts in the time interval    
    posts_in_time = []
    for i in range(len(posts)):
        posttime = datetime.strptime(posts[i][0], '%Y-%m-%dT%H:%M:%S.000Z')
        timedif=int((datetime.now()-posttime) / timedelta(minutes=1))
        
        if timedif < time_interval:
            posts_in_time.append(posts[i])   
    
    # number of occurances of the ticker
    for i in range(len(posts_in_time)):
        b=[m.start() for m in re.finditer("\{}".format(Ticker), posts_in_time[i][1])]
        #print(len(b))
        occ_num = occ_num + len(b)
print("{} was mentioned {} times in the last {} minutes".format(Ticker, occ_num, time_interval))