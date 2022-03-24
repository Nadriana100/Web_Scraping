
# import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
# import pymongo


# Scrape all functions 
def scrape_all():    # print("Scrape All reached")  -- just to check if is working Goal return a json can be load inMongoDB
    
    # Setup splinter  --- return json that has all sata, and loaded in MongoDB
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# Getting teh info from news web   # Get the info from News from Jupyter notebook
    news_title, news_paragraph = scrape_news(browser)   

# bulid a dictionary {} using the info from scrapes 

    marsData = {
    "News Title": news_title,
    "News Paragraph": news_paragraph,
    "Mars Image": scrape_mars_images(browser),
    "Mars Profile": scrape_mars_profile(browser),
    "Mars Hemispheres": srape_hemis(browser),
    "Last Updated": dt.datetime.now()
    }

 # Stop the webdriver 
    browser.quit()

    return marsData

######### Scrape NASA Mars News from Jupyter notebook
def scrape_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

#Dalay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    soup_mars = soup(html, "html.parser")

    # Title 
    news_title = soup_mars.find('div', class_="content_title")
    # Paragraph 
    news_p = soup_mars.find('div', class_="article_teaser_body").get_text

    return news_title, news_p

######### Scarpe JPL Mars Space Images - Featured Image
def scrape_mars_images(browser):
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)

# Image button
    full_image = browser.find_by_tag('button')[1]
    full_image.click()

# Parse the image 
    html = browser.html
    image_mars = soup(html, "html.parser")

    img_url_rel = image_mars.find('img', class_='fancybox-image').get('src')

# Base url to create an absolute url
    imag_url = f'https://spaceimages-mars.com/{img_url_rel}'

# Return the Imgage url

    return imag_url

######## Scrape MARS PLANET PROFILE 
def scrape_mars_profile(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    html = browser.html
    mars_facts = soup(html, "html.parser")

    # Find facts location

    profileLoc = mars_facts.find('div', class_="diagram mt-4")
    # getting the html code for the fact table
    profileTable = profileLoc.find('table')   

# create an empty string 

    profile = ""

    profile += str(profileTable)

    return profile
# Scrape Mars Hemispheres

def srape_hemis(browser):

    #base url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    #Create a list of the url 
    hemisphere_image_urls = []

    #loop
    for i in range (4):
        hemisphereInfo = {}

        # Find elements on each loop to avoid a stale element exception 
        browser.find_by_css('a.product-item img')[i].click()

        # Find the image 
        sample = browser.find_by_text('Sample').first
        hemisphereInfo['img_url']=sample['href']

        # Find the Hemisphere Title 
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text

        #Append into a list 
        hemisphere_image_urls.append(hemisphereInfo)

        # Navigate backwards 
        browser.back()

#return hemis. titles 



# Set up a flask app
if __name__ == "__main__":
    print(scrape_all)