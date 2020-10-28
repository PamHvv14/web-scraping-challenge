from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re
import pymongo

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path)

def scrape():
    browser = init_browser()
    mars_dict ={}

    #NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.select_one('ul.item_list li.slide').find('div', class_= 'content_title').text
    news_teaser = soup.select_one('ul.item_list li.slide').find('div', class_='article_teaser_body').text

    #IMAGE
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    image_full=browser.find_by_id('full_image')
    image_full.click()
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url=soup.find('img', class_ = 'main_image')['src']
    featured_img_url = "https://www.jpl.nasa.gov" + img_url

    # TWEET
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather_tweet = soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text
    

    # FACTS
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_facts = tables[2]
    mars_facts.columns = ["Description", "Value"]
    mars_html_table = mars_facts.to_html()
    mars_html_table.replace('\n', '')
    
    #HEMISPHERES
    url5 ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_images = []
    products = soup.find('div', class_='collapsible results')
    hemispheres = products.find_all('div', class_='item')

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        url6 = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(url6)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_images.append({"title": title, "img_url": image_url})



    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_img_url": featured_img_url,
        "mars_weather": mars_weather,
        "mars_html_table": str(mars_html_table),
        "hemisphere_images": hemisphere_images
    }

    return mars_dict 