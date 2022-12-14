#!/usr/bin/env python
# coding: utf-8

# In[51]:


import time
import requests
import numpy as np
import pandas as pd
from scrapy.http import TextResponse
import re
import scrapy
from itertools import chain
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import math
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


# # Scraping main info from individual pages

# In[59]:


url = 'https://www.booking.com/hotel/am/best-western-congress.html'
PATH = r"C:/Users/Gigabyte/Downloads/chromedriver_win32/chromedriver.exe"


# In[39]:


def main_info_scraper(url):
    page = requests.get(url)
    response = TextResponse(body=page.text,url=url,encoding="utf-8")
    name = response.css('h2[class="d2fee87262 pp-header__title"]::text').extract()
    address=response.css('p[id=showMap2]>span:nth-of-type(1)::text').extract()
    new_address = []
    for i in address:
        new_address.append(i.replace("\n", ""))
    hotel_overall_rating=response.css('div[data-testid=review-score-component]>div:nth-of-type(1)::text').extract()
    reviews = response.css('div[data-testid=review-score-component]>div:nth-of-type(2)>span:nth-of-type(2)::text').extract()
    new_reviews = []
    for i in reviews:
        new_reviews.append(i.replace("\xa0", ""))
    new_reviews_final=[]
    for i in new_reviews:
        new_reviews_final.append(i.replace("·", ""))
    new_reviews_final=new_reviews_final[1]
    main_info_dict={'hotel_name':name,'address':new_address,'hotel_overall_rating':hotel_overall_rating,'number_of_reviews':new_reviews_final,'hotel_url':url}
    hotel_main_info = pd.DataFrame(main_info_dict)
    return hotel_main_info


# In[40]:


hotel_main_info = main_info_scraper(url)


# In[41]:


hotel_main_info


# # Scraping info about rooms

# In[48]:


def room_info_scraper(url,PATH):
    browser = webdriver.Chrome(PATH)
    browser.get(url)
    page = browser.page_source
    response = TextResponse(body = page, encoding = "utf-8", url = url)
    c = browser.find_elements(By.CSS_SELECTOR, "section[class='roomstable'] > div[class='d46673fe81 cdefac0453 c6aefe00bc c135d5bf2d'] >div > div >a > span")
    listik = [i.text for i in c]
    all_dict=[]
    for i in range(2,len(listik)+2):
        browser.find_element(By.CSS_SELECTOR, "section[class='roomstable'] > div[class='d46673fe81 cdefac0453 c6aefe00bc c135d5bf2d']:nth-of-type({}) >div > div >a > span".format(i)).click()
        time.sleep(3)
        page = browser.page_source
        response = TextResponse(body = page, encoding = "utf-8", url = url)
        facilities_main = response.css('span[class = " bui-badge bui-badge--outline room_highlight_badge--without_borders"]::text').extract()
        extra_facilities = response.css('li[class = "hprt-lightbox-list__item js-lightbox-facility"]>span::Text').extract()
        dict_fact={'room_name':listik[i-2],'hotel_main_fac':facilities_main,'hotel_extra_fac':extra_facilities}
        all_dict.append(dict_fact)
        browser.find_element(By.CSS_SELECTOR, "a[class='lightbox_close_button']").click()
        browser.refresh()
        time.sleep(3)
    data_about_rooms=pd.DataFrame(all_dict)
    return data_about_rooms


# In[49]:


room_info = room_info_scraper(url)


# In[50]:


room_info


# # Scraping reviews

# In[84]:


#Final function
review_rate = []
date = []
reviewer = []
review = []
reviewer_country = []
reviewer_roomtype = []
reviewer_nights = []
traveler = []
review_positive = []
review_negative = []
def review_scraper(url):
    browser = webdriver.Chrome(PATH)
    browser.get(url) 
    browser.find_element("css selector", 'button[data-testid="fr-read-all-reviews"]').click() 
    time.sleep(4)
    browser.find_element("css selector", 'span[class="bui-input-select"]>select[id="review_sort"]>option[value="f_recent_desc"]').click() 
    time.sleep(2)
    while True:
        try:
            browser_new= browser.page_source
            test2=Selector(text = browser_new).css('div.bui-grid__column-9.c-review-block__right')
            for i in test2:
                review_rate.append(i.css('div[class="bui-review-score__badge"]::text').extract())
            
            for i in test2:
                date.append(i.css('span[class="c-review-block__date"]::text').extract())
            
            for i in test2:
                review.append(i.css('div[class="bui-grid__column-11"] >h3:nth-child(1)::text').extract())
            test3=Selector(text = browser_new).css('div.bui-grid__column-3.c-review-block__left')
           
            for i in test3:
                reviewer.append(i.css('span[class="bui-avatar-block__title"]::text').extract())
           
            for i in test3:
                reviewer_country.append(i.css('span[class="bui-avatar-block__subtitle"]::text').extract())
            
            for i in test3:
                reviewer_roomtype.append(i.css('li[class="bui-list__item review-block__room-info--disabled"]>a>div[class="bui-list__body"]::text').extract())  
           
            for i in test3:
                reviewer_nights.append(i.css('ul[class="bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date"]>li[class="bui-list__item"]>div[class="bui-list__body"]::text').extract())
            
            for i in test3:
                traveler.append(i.css('ul[class="bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row"]>li[class="bui-list__item"]>div[class="bui-list__body"]::text').extract())
            
            for i in test2:
                review_positive.append(i.css('p.c-review__inner.c-review__inner--ltr > span.c-review__body.c-review__body--original::text').extract())
           
            for i in test2:
                review_negative.append(i.css('div.c-review > div:nth_child(2)>p.c-review__inner.c-review__inner--ltr > span.c-review__body.c-review__body--original::text').extract())
            
            browser.find_element("xpath",'//a[@class="pagenext"]').click()
            time.sleep(5)
            
        except:
            break
            
    return(review_rate,date,reviewer,review ,reviewer_country ,reviewer_roomtype,reviewer_nights ,traveler ,review_positive,review_negative )


# In[85]:


reviews=review_scraper(url)


# In[90]:


def review_preprocessing(reviews):
    data_final=pd.DataFrame(list(zip(reviews[0],reviews[1],reviews[2],reviews[3],reviews[4],reviews[5],reviews[6],reviews[7],reviews[8],reviews[9])),columns=['individual_rating','review_date','reviewer_name','main_review','country','room_type','number_of_stayed_nights','traveler_type','positive_subreview','negative_subreview'])
    listik = data_final.columns.to_list()
    for i in listik:
        data_final[i]=data_final[i].str[0]
    remove_list=['review_date','main_review','room_type','number_of_stayed_nights','traveler_type']
    for i in remove_list:
        data_final[i]=data_final[i].str.replace('\n','')
    data_final['review_date']=data_final['review_date'].str.replace('Reviewed: ','')
    data_final['main_review']=data_final['main_review'].str.replace(' ','')
    data_final['number_of_stayed_nights']=data_final['number_of_stayed_nights'].str.split(' ',expand=True)[0]
    return data_final


# In[91]:


data = review_preprocessing(reviews)


# In[92]:


data


# In[ ]:





# In[ ]:




