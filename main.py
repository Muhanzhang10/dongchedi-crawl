import pandas as pd 
import requests
from bs4 import BeautifulSoup
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


df = pd.read_csv("懂车帝观测账号.csv")

f = open("url.txt", "a")

for index, row in df.iterrows():
    print(index)
    if index < 62:
        continue
    
    user_url = row["url"].split('/')[-3:]
    user_url.insert(2, 'wenzhang')
    user_url = 'https://' + '/'.join(user_url)

    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(user_url)

    count = 0
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        if driver.find_elements(By.XPATH, """//div[contains(text(),"没有更多了")]"""):
            break
        if count % 100:
            time.sleep(2)
        count += 1
        
    
    xpath = "//a[contains(@href,'/article/') and not(contains(@href, '#comment'))]"
    ele = driver.find_elements(By.XPATH, xpath)
    
    res = list(set([e.get_attribute("href") for e in ele]))
    for r in res:
        print(r)
        f.write(r)
        f.write('\n')

    time.sleep(1)
    driver.quit()
    
f.close()
    






