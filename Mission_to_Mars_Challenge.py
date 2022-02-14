# 1 Initial steps

# 1.1 Import dependencies
from bs4 import BeautifulSoup as soup
from html5print import HTMLBeautifier
import pandas as pd
from pprint import pprint
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# 1.2 Initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# 2 Web scraping

# 2.1 News article
url = 'https://redplanetscience.com'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# 2.1.1 Title
news_title = slide_elem.find('div', class_='content_title').get_text()
print(news_title)

# 2.1.2 Paragraph
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
print(news_p)

# 2.2 Surface image
url = 'https://spaceimages-mars.com/'
browser.visit(url)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
html = browser.html
img_soup = soup(html, 'html.parser')
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url = f'{url}{img_url_rel}'
print(img_url)

# 2.3 Facts table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
print(HTMLBeautifier.beautify(df.to_html()))

# 2.4 Hemisphere images
url = 'https://marshemispheres.com/'
browser.visit(url)
html = browser.html
hemisphere_soup = soup(html, 'html.parser')
items = hemisphere_soup.find_all('div', class_="item")
hemisphere_urls = []
for item in items:
    hemisphere_rel = item.a['href']
    hemisphere_url = f'https://marshemispheres.com/{hemisphere_rel}'
    hemisphere_urls.append(hemisphere_url)
img_urls = []
titles = []
for hemisphere_url in hemisphere_urls:
    browser.visit(hemisphere_url)
    html = browser.html
    imgs_soup = soup(html, 'html.parser')
    img_rel = imgs_soup.find('img', class_='wide-image').get('src')
    img_url = f'https://marshemispheres.com/{img_rel}'
    img_urls.append(img_url)
    title = imgs_soup.find('h2', class_='title').get_text()
    titles.append(title)
hemispheres = [{'image': i, 'caption': t} for i, t in zip(img_urls, titles)]
pprint(hemispheres)

# 3 Quit browser
browser.quit()