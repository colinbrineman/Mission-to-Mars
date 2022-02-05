# 1. Set-up
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
# Set executable path and browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# 2. Scrape 'MARS Planet News'
# Visit site
url = 'https://redplanetscience.com'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)
# Parse html
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
# Use parent element to find 1st "a" tag & save it as "news_title"
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
# Use the parent element to find paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# 3. Scrape 'Jet Propulsion Laboratory'
# Visit site
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Find & click full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# Parse html
html = browser.html
img_soup = soup(html, 'html.parser')
# Find relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# Use base URL to create absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# 4. Scrape Mars Facts
# Scrape table with Pandas
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Format DataFrame
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df
# Convert DataFrame back into html-ready code
df.to_html()

# End session
browser.quit()