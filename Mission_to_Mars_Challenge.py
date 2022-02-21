#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# look for data with the content title
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# create new dataframe from the HTML table
# read_html() searches for and returns a list of tables; [0] tells pandas to pull the first table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# assign columns to dataframe
df.columns=['description', 'Mars', 'Earth']
# turn the description column into the dataframe's index
df.set_index('description', inplace=True)
df

# convert dataframe back into HTML code
df.to_html()

# ## D1: Scrape High-Resolution Mars' Hemisphere Images and Titles
# 
# ### Hemispheres

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

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()