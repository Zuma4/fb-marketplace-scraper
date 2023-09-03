from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd

# *_______________________________YOUR PART_______________________________* #

# How Many Times Do You Want The Page To Scroll?
scroll = 7

# Your Email To Log In
email = "haltshwezunfger@gmail.com"

# Your Password
password = "2227aaAa"

# What Marketplace You Want To Scrap? (Cars By Default)
marketplace = "https://web.facebook.com/marketplace/category/vehicles"

# Repeat Every How Much Minutes?
minutes = 10

# *_______________________________YOUR PART_______________________________* #

# ___CLASSES___
title_classes = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u"
price_classes = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u"
description_classes = "xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"
when_posted_and_location_classes = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa"
see_more_button_classes = "xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"
# _____END_____

# Infinite Loop That Repeats Every 10 Minutes
while True :
    try :

        # Using Virtual Browser
        driver = webdriver.Firefox()

        # Entering The Site
        driver.get("https://web.facebook.com/")

        # Automating Logging In Process
        email_field = driver.find_element(by=By.ID, value='email')
        password_field = driver.find_element(by=By.ID, value='pass')
        button = driver.find_element(by=By.NAME, value='login')

        email_field.send_keys(email)
        password_field.send_keys(password)
        button.click()
        time.sleep(2)

        # Entering The Marketplace
        driver.get(marketplace)

        # Scrolling 7 Times To The Bottom To Get More Elements
        # You Can Change How Many Times You Want The Driver To Scroll Thus Making The Page Load More Items
        while scroll != 0 :
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            scroll-=1

        # A Dictionary For Storing Information
        data_dict = {'title':[],'price':[], 'description':[], 'location':[],'when_posted':[], 'link':[]}

        # Parsing The Source Code
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        cars = soup.find('div', {'class':'x8gbvx8'}).find_all('div', {'class':'x1r8uery'})

        e = 0
        # Entering Each Item Link And Collecting Data
        for car in cars :
            # Getting Link And Storing It
            driver.get('https://web.facebook.com/' + car.find('a', {'class':'x1i10hfl'}).get('href'))
            data_dict['link'].append('https://web.facebook.com/' + car.find('a', {'class':'x1i10hfl'}).get('href'))

            # Checking If See More Button In Description Exists And Clicking It
            try :
                see_more_button = driver.find_element(by=By.XPATH, value=f'//div[@class="{see_more_button_classes}"]')
                see_more_button.click()
                time.sleep(2)
            except :
                pass

            # Getting Title And Storing
            title = driver.find_element(by=By.XPATH, value=f'//span[@class="{title_classes}"]').text.replace("[hidden information]",'')
            # Checking If The Element Is Available
            if title :
                data_dict['title'].append(title)
            else :
            # adding "Not Available" Otherwise
                data_dict['title'].append("Not Availabe")

            # Getting Price
            price = driver.find_element(by=By.XPATH, value=f'//span[@class="{price_classes}"]').text
            if price :
                data_dict['price'].append(price)
            else :
                data_dict['price'].append("Not Available")

            # Getting Description
            description = driver.find_element(by=By.XPATH, value=f'//div[@class="{description_classes}"]').text.replace("[hidden information]", '').replace('... See more', '')
            if description :
                data_dict['description'].append(description)
            else :
                data_dict['description'].append("Not Available")
            
            # Getting Location
            location = driver.find_element(by=By.XPATH, value=f'//span[@class="{when_posted_and_location_classes}"]').text
            if location :
                data_dict['location'].append(location[location.index('in'):].strip('in'))
            else :
                data_dict['location'].append("Not Available")

            # Getting When Posted
            when_posted = re.search("[^Listed ].* ago", driver.find_element(by=By.XPATH, value=f'//span[@class="{when_posted_and_location_classes}"]').text)
            if when_posted :
                data_dict['when_posted'].append(when_posted.group())
            else :
                data_dict['when_posted'].append("Not Available")

            if e != 10 :
                e += 1
            else :
                break

    finally :
        # Quiting The Browser
        driver.quit()

        dataFrame = pd.DataFrame({"Title": data_dict['title'], "Price": data_dict['price'], "Description": data_dict['description'],
                                "Location": data_dict['location'], "When_Posted":data_dict['when_posted'], "Link": data_dict['link']})
        
        print(dataFrame)
        
    dataFrame.to_csv('file.csv', sep=',', index=False, encoding='utf-8')
    time.sleep(minutes)
