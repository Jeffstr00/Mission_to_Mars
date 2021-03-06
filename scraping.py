#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemi_images(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemi_image": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# ### Mars News Title + Paragraph

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:
        # create new dataframe from the HTML table
        # read_html() searches for and returns a list of tables; [0] tells pandas to pull the first table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    # use BaseException as a catchall for any built-in exceptions and wono't handle any user-defined exceptions; using it because we're using Pandas' read_html() function to pull data instead of scraping with BeautifulSoup/Splinter
    except BaseException:
        return None

    # assign columns to dataframe
    df.columns=['Description', 'Mars', 'Earth']
    # turn the description column into the dataframe's index
    df.set_index('Description', inplace=True)

    # convert dataframe back into HTML code, add bootstrap
    return df.to_html()


# ### Mars Hemispheres Images

def hemi_images(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # create for loop to iterate through the different hemispheres
    for i in range(4):
        # create dictionary for each hemisphere to hold url + title
        hemispheres = {}
        # find and click link to each 'i' hemisphere
        browser.find_by_css('a.product-item h3')[i].click()
        
        # find the url to the full-sized image
        sample_elem = browser.links.find_by_text('Sample').first
        # extract its href
        image_url = sample_elem['href']
        #print(image_url)
        # add this hemisphere's url to its dictionary
        hemispheres['url'] = image_url

        # find the hemisphere's image title
        title = browser.find_by_css('h2.title').text
        #print(title)
        # add this hemisphere's title to its dictionary
        hemispheres['title'] = title
        # append the hemisphere_image_urls list to include the current hemisphere's image url/title
        hemisphere_image_urls.append(hemispheres)
        
        # return to previous page
        browser.back()

    # return a list of dictionaries featuring each hemisphere's image url/title; close browser
    return hemisphere_image_urls