from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
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
    news_title = soup.find('div', class_= 'content_title').text
    news_teaser = soup.find('div', class_='article_teaser_body').text

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
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    # FACTS
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_img_url": featured_img_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict