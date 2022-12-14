#!/usr/bin/env python
# coding: utf-8

# In[38]:


from selenium import webdriver
from scrapy.http import TextResponse
import re
import scrapy
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date


# In[21]:


def sraper(url):
    driver = webdriver.Chrome()
    driver.get(url)
    for i in range(1500):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script(f"window.scrollTo(document.body.scrollHeight,{100*i});")
        time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page = driver.page_source
    response = TextResponse(body = page, encoding = 'utf-8', url = url)
    review_block = response.css("div[jsname = 'Pa5DKe'] > div[class = 'Svr5cf bKhjM']" )
    read_more=[i.css("a.VOZjLd::Text").extract() for i in review_block]
    name=[i.css(".DHIhE::Text").extract() for i in review_block]
    dates=[i.css(".iUtr1::Text").extract() for i in review_block]
    reviews=[i.css("div[jsname='NwoMSd']>div[class='STQFb eoY5cb']>div[class='K7oBsc']>div>span::text").extract() for i in review_block]
    reviews_full=[i.css("div[class='kVathc']>div[class='STQFb eoY5cb']>div[class='K7oBsc']>div>span::text").extract() for i in review_block]
    ratings=[i.css(".GDWaad::text").extract() for i in review_block]
    review=[["".join(i)] for i in reviews]
    review_full=[["".join(i)] for i in reviews_full]
    trip_type_rate=[i.css("div[class='X4nL7d']>div>span:nth-of-type(2)::text").extract() for i in review_block]
    rating_rsl=[i.css("div>div[class='dA5Vzb']>span:nth-of-type(2)::text").extract() for i in review_block]
    hotel_name=response.css("span[class='Pvd8ed ZSxxwc']>div[class='nCqM5e']::text").extract()
    review_data = pd.DataFrame(
    {'name': name,
     'stars': ratings,
     'reviewshort': review,
     'review_full':review_full,
     'dates': dates,
    'read_more':read_more,
    'traveler_type':trip_type_rate,
    'rating_rsl':rating_rsl})
    return(review_data,hotel_name)
    


# In[58]:


review_data=sraper('https://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htlshttps://www.google.com/travel/hotels/paris%20hotel%20armenia/entity/CgoIvoXG1_T8hbVLEAE/reviews?q=paris%20hotel%20armenia&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4718358%2C4723331%2C4731329%2C4757164%2C4814050%2C4861688%2C4864715%2C4874190%2C4886082%2C4886480%2C4890098%2C4893075%2C4902277%2C4903082%2C4903556%2C4905351%2C4905600%2C4906050%2C4912819%2C4916863%2C4919757%2C4920622&hl=en-AM&gl=am&ssta=1&grf=EmQKLAgOEigSJnIkKiIKBwjmDxAMGBMSBwjmDxAMGBQgADAeQMoCSgcI5g8QDBgOCjQIDBIwEi6yASsSKQonCiUweDQwNmFiY2ZjMGEzZWZhNWY6MHg0YjZhMTdlNzRhZjE4MmJl&rp=EL6Fxtf0_IW1SxC-hcbX9PyFtUs4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiotLnbxPj7AhUAAAAAHQAAAAAQAw&utm_campaign=sharing&utm_medium=link&utm_source=htls')


# In[59]:


def preprocessing(review_data):
    scraped_data=review_data[0]
    scraped_data['hotel_name']=[review_data[1] for i in scraped_data.iterrows()]
    scraped_data[['room_rate', 'service_rate','location_rate']]=pd.DataFrame(scraped_data['rating_rsl'].to_list(), index= scraped_data.index)
    columns = scraped_data.columns.to_list()
    for i in columns:
        scraped_data[i]=scraped_data[i].str[0]
    scraped_data.replace('', np.nan, inplace=True)
    scraped_data.review_full = np.where(scraped_data.review_full.isnull(), scraped_data.reviewshort, scraped_data.review_full)
    scraped_data['dates']=scraped_data['dates'].str.replace('on','')
    matching_dict={"year":["years","year"],"months":["mths","mth"],"weeks":["weeks","week"],"days":["days","day"]}
    scraped_data.dates=scraped_data.dates.apply(lambda x: x.replace('a ','1 '))
    scraped_data.dates=scraped_data.dates.apply(lambda x: relativedelta(years=int(x.split()[0]))                          if (x.split()[1] in matching_dict['year'])                          else relativedelta(months=int(x.split()[0]))                          if (x.split()[1] in matching_dict['months'])                          else relativedelta(weeks=int(x.split()[0]))                          if (x.split()[1] in matching_dict['weeks'])                          else relativedelta(days=int(x.split()[0]))                         if (x.split()[1] in matching_dict['days'])                        
                        else x)
    scraped_data.dates=scraped_data.dates.apply(lambda x: date.today()-x)
    scraped_data=scraped_data[scraped_data['read_more'].isna()]
    scraped_data=scraped_data.drop(['reviewshort','read_more','rating_rsl'],1)
    scraped_data=scraped_data[~scraped_data['name'].isna()]
    return(scraped_data)
    
    
    


# In[ ]:


scraped_data․to_excel('google_reviews.xlsx')

