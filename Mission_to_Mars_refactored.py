# 1. Set-up
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# 2. Scrape 'MARS Planet News'
def mars_news():
   url = 'https://redplanetscience.com/'
   browser.visit(url)
   browser.is_element_present_by_css('div.list_text', wait_time=1)
   html = browser.html
   news_soup = soup(html, 'html.parser')
   slide_elem = news_soup.select_one('div.list_text')
   slide_elem.find('div', class_='content_title')
   news_title = slide_elem.find('div', class_='content_title').get_text()
   news_title
   news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   news_p

# 3. Scrape 'Jet Propulsion Laboratory'
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

# 4. Scrape Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html()

# 5. End session
browser.quit()