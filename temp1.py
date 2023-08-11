import pandas as pd 
import requests
from bs4 import BeautifulSoup
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
import time



user_url = "https://www.dongchedi.com/user/690907766332752"
driver = webdriver.Chrome()
driver.get(user_url)

while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    if driver.find_elements(By.XPATH, """//div[contains(text(),"没有更多了")]"""):
        break

xpath = "//section//a[contains(@href,'ugc/article') and not(contains(@href, '#comment'))]"
xpath2 = "//section//a[contains(@href, '/video/') and not(contains(@href, '#comment'))]"

ele = driver.find_elements(By.XPATH, xpath2)
res = [e.get_attribute("href") for e in ele]
print(set(res))
print(len(set(res)))
