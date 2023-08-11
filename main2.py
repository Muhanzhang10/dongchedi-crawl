import time
import os 
import pandas as pd
import requests  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re, datetime
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=False, default=428)
    args = parser.parse_args()
    return args 


def get_response(html_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari'
    }
    response = requests.get(url=html_url, headers=headers)
    return response


def save(img_url, file_path):
    img_content = get_response(img_url).content
    with open(file_path, mode='wb') as f:
        f.write(img_content)
    return 


def save_images(image_urls, file_path):
    for i in range(len(image_urls)):
        save(image_urls[i], file_path+ f"/{str(i)}.jpeg")
    return 

def main(num):
    """
    顺序为: 用户名、标题、发文时间、文章内容、url
    """
    f = open(f"url/url{num}.txt", 'r')

    users = []
    topics = []
    dates = []
    contents = []
    urls = []
    image_urls = []

    for line in f:
        
        url = line[:-1]
        
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        user = ''
        user_xpath = [f"//p//a[contains(@href, '/user/')]", "//a[contains(@href, '/user/') and contains(@class,'active-link-text')]"]
        for u in user_xpath:
            try:
                user = driver.find_element(By.XPATH, u).text
                if not user:
                    continue 
                break 
            except:
                continue
        
        topic = ''
        topic_xpath = ["//h1", "//div[contains(@class,'award')]//p[contains(@class,'line-1')]"]
        for t in topic_xpath:
            try:
                topic = driver.find_element(By.XPATH, t).text
                if not topic:
                    continue 
                break
            except:
                continue
            
        date = ''
        date_xpath = ["//div[contains(@class, 'user')]//p", "//span[contains(@class, 'time')]"]
        for d in date_xpath:
            try:
                date = driver.find_element(By.XPATH, d).text 
                if not date:
                    continue

                date_ = re.search('\d{4}-\d{2}-\d{2}', date)
                if not date_:
                    date_ = re.search('\d{2}-\d{2}', date)
                    
                date = date_.group()
                break 
            except:
                continue
            
        content = ''
        content_xpath = ["//p[contains(@class, 'article-content')]//span", "//div[contains(@class, 'article-content')]//p", "//section[contains(@id, 'article')]//div//p", "//section[contains(@id, 'article')]//p//span", "//section[contains(@id, 'article')]//p"]  
        for c in content_xpath:
            try:
                content_ = driver.find_elements(By.XPATH, c)
                if not content_:
                    continue 

                content = '\n'.join([i.text for i in content_])
                break 
            except:
                continue
            
        
        image = '' 
        try:
            image_path = f"img/{topic}"
            os.mkdir(image_path)
        except:
            pass 
        image_xpath = ["//div[contains(@class, 'image-list')]//div[contains(@class, 'img-wrapper')]//img", "//section[contains(@id, 'article')]//div//div//img"]
        for i in image_xpath:
            try:
                image_ = driver.find_elements(By.XPATH, i)
                if not image_:
                    continue 
                image_urls_ = [im.get_attribute("src") for im in image_]
                save_images(image_urls_, image_path)
                image = ' '.join(image_urls_)
            except:
                continue 
            
        users.append(user); topics.append(topic); dates.append(date); contents.append(content); urls.append(url); image_urls.append(image)


    df = pd.DataFrame()
    df["users"] = users 
    df["topics"] = topics
    df["dates"] = dates
    df["contents"] = contents
    df["urls"] = urls
    df["image_urls"] = image_urls
    df.to_excel(f"res/res{num}.xlsx", index=False)
    return 


if __name__ == '__main__':
    args = arg_parse()
    start = args.start
    end = args.end
    print(start, end)
    for i in range(start, end):
        num = "0" * (3 - len(str(i))) + str(i) 
        print(num)
        main(num)