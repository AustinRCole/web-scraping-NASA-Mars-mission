import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time


def init_browser():
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    story_title = soup.find('div', class_="content_title").text.strip()

    story_paragraph = soup.find('div',class_="rollover_description_inner").text.strip()

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url2)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')

    mars_image = soup2.find('img',class_='thumb')
    mars_image_url = 'https://www.jpl.nasa.gov' + mars_image['src']

    url3 = 'https://space-facts.com/mars/'

    table = pd.read_html(url3)[0].to_html()

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    browser.click_link_by_partial_text('Hemisphere')
    browser.click_link_by_partial_text('Sample')

    for x in range(4):
    
        html2 = browser.html
    
        soup = BeautifulSoup(html2, 'html.parser')
        images = soup.find_all('img', class_='thumb')
    
        index = 0
        limit = 4
    
        browser.back()
        browser.find_link_by_partial_text('Hemisphere')[x].click()
        browser.click_link_by_partial_text('Sample')
    
        hemisphere_urls = []

        for image in images:
            src = image['src']
            hemisphere_urls.append(f'https://astrogeology.usgs.gov{src}')
            index += 1
            if index == limit:
                break
    
    time.sleep(1)

    browser.quit()

    mars_data = {
        'title': story_title,
        'paragraph': story_paragraph,
        'primary_image': mars_image_url,
        'table': table,
        'pics': hemisphere_urls
    }

    return mars_data
