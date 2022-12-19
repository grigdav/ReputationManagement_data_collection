#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
import requests
from scrapy.http import TextResponse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.http import TextResponse
import pandas as pd
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re


# In[2]:


def get_response(URL: str, Headers):
    """
    This function takes URL as an input and provides response:
    - none is status code is not 200
    - scrapy TextResponse object otherwise
    """
    page = requests.get(URL, headers = Headers )
    if page.status_code == 200:
        response = TextResponse(body=page.text,url=page.url,encoding="utf-8")
    else:
        response = None
        print("wrong status code")
    return response


# # About hotel

# In[6]:


URL = 'https://www.tripadvisor.com/Hotel_Review-g293932-d23804505-Reviews-or10-Dave_Hotel_Yerevan-Yerevan.html#REVIEWS'


# In[7]:


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

Headers = {'User-Agent': user_agent}


# In[8]:


def hotel_info_scraper(URL : str, Headers = Headers):
    response = get_response(URL, Headers)
    title = response.css("h1::text").extract_first()
    num_views = response.css('span.qqniT::text').extract_first()
    adress = response.css('span.fHvkI.PTrfg::text').extract_first()
    overall_rating = response.css('span.uwJeR.P::text').extract_first()
    location_score = response.css("div.SSDgd > div.WdWxQ:nth-child(1) > span::text").extract()[1]
    cleanness_score = response.css("div.SSDgd > div.WdWxQ:nth-child(2) > span::text").extract()[1]
    service_score = response.css("div.SSDgd > div.WdWxQ:nth-child(3) > span::text").extract()[1]
    value_score = response.css("div.SSDgd > div.WdWxQ:nth-child(4) > span::text").extract()[1]
    data = {'title' : title, 'num_views' : num_views, "adress" : adress, 'overall_rating' : overall_rating,
           'location_score' : location_score , 'cleanness_score' : cleanness_score, 'service_score' : service_score,
           "value_score" : value_score}
    return data


# In[9]:


data = hotel_info_scraper(URL)


# In[10]:


data


# # comment scraper

# In[29]:


opts = Options()
opts.add_argument("--headless")
opts.add_argument("--disable-infobars")
opts.add_argument("start-maximized")
opts.add_argument("--disable-extensions")
opts.add_argument('--disable-notifications')
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
PATH = r"/Users/gevorgatanesyan/Downloads/chromedriver"


# In[30]:


def hotel_comment_scraper(URL : str):
    s = Service(PATH)
    browser = webdriver.Chrome(service=s, options=opts)
    browser.get(URL)
    
    time.sleep(4)
    browser.find_element(by=By.CSS_SELECTOR, value = "h2[class ='aFUwN Cj F1 b']").click()  
    
    time.sleep(2)
    
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight/4)")     

    time.sleep(4)
    
    try:
        time.sleep(5)
        browser.find_element(by=By.CSS_SELECTOR, value = 'ul[class = "LojWi w S4"] > li[class = "ui_radio XpoVm"]:nth-child(1)').click()
        time.sleep(5)
        browser.find_element(by=By.CSS_SELECTOR,value =  'ul[class = "LojWi w S4"] > li[class = "ui_radio XpoVm"]:nth-child(1)').click()
        time.sleep(5)
    except:
        try:
            browser.find_element(by=By.CSS_SELECTOR, value = 'ul[class = "LojWi w S4"] > li[class = "ui_radio XpoVm"]:nth-child(1)').click()       
        except:
            print('i')
            
    try:
        browser.find_element(by=By.CSS_SELECTOR,value =  "span.Ignyf._S.Z").click()
    except:
        pass
    
    

    comments = []
    rated = []
    locations = []
    contributions = []
    date_of_stay = []
    review_identical = []
    date_posted = []
    
    page = browser.page_source
    response = TextResponse(body = page,encoding="utf-8", url = URL)
    review_identical_css = response.css('div[class = "vTVDc"]')
    comment_css = response.css("q")
    location_css = response.css("div.MziKN ")
            
    comments.append([','.join(i) for i in  [i.css('span::text').extract() for i in comment_css]])
    rated.append([re.findall('\d', i)[0] for i in response.css("div[class ='Hlmiy F1'] > span").extract()])
    locations.append([i.css('span.RdTWF > span::text').extract() for i in location_css])
    contributions.append([i.css('span:nth-child(1) > span.yRNgz::text').extract_first() for i in location_css])
    date_of_stay.append(response.css("span[class = 'teHYY _R Me S4 H3']::text").extract())
    review_identical.append([i.css('div[class = "ZzICe Me f"] > div > span').extract() for i in review_identical_css])
    date_posted.append(response.css('div[class = "cRVSd"] > span::text').extract())
            
    
    
    while True:
        try:
            try:
                browser.find_element(by=By.CSS_SELECTOR,value =  "span.Ignyf._S.Z").click()
            except:
                pass
            time.sleep(5)
            browser.find_element(by=By.CSS_SELECTOR, value = "a[class ='ui_button nav next primary ']").click()  
            time.sleep(3)
            page = browser.page_source
            response = TextResponse(body = page,encoding="utf-8", url = URL)
            
            review_identical_css = response.css('div[class = "vTVDc"]')
            comment_css = response.css("q")
            location_css = response.css("div.MziKN ")
            
            comments.append([','.join(i) for i in  [i.css('span::text').extract() for i in comment_css]])
            rated.append([re.findall('\d', i)[0] for i in response.css("div[class ='Hlmiy F1'] > span").extract()])
            locations.append([i.css('span.RdTWF > span::text').extract() for i in location_css])
            contributions.append([i.css('span:nth-child(1) > span.yRNgz::text').extract_first() for i in location_css])
            date_of_stay.append(response.css("span[class = 'teHYY _R Me S4 H3']::text").extract())
            review_identical.append([i.css('div[class = "ZzICe Me f"] > div > span').extract() for i in review_identical_css])
            date_posted.append(response.css('div[class = "cRVSd"] > span::text').extract())
            
        except NoSuchElementException:
            break 

    
    data = {'comments':comments, 'rated':rated, 'locations':locations, 'contributions':contributions, 
           'date_of_stay':date_of_stay,'review_identical':review_identical, 'date_posted':date_posted }
    df = []
    for i in range(len(data['comments'])):
        df.append({k:v[i] for k,v in data.items()})
    data=pd.DataFrame(columns=['comments','rated','locations','contributions','date_of_stay','review_identical','date_posted'])
    for i in range(len(df)):
        data = data.append(pd.DataFrame(df[i]), ignore_index = True)
    
    return data


# In[31]:


abc = hotel_comment_scraper(URL = 'https://www.tripadvisor.com/Hotel_Review-g293932-d23804505-Reviews-Dave_Hotel_Yerevan-Yerevan.html')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




