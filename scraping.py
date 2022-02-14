from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_p = mars_news(browser)
    hemispheres = mars_hemispheres(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        'hemispheres': hemispheres
    }
    browser.quit()
    return data

def mars_news(browser):
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts():
    try:
        df = pd.read_html(
            'https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    items = hemisphere_soup.find_all('div', class_="item")
    hemisphere_urls = []
    try:
        for item in items:
            hemisphere_rel = item.a['href']
            hemisphere_url = f'https://marshemispheres.com/{hemisphere_rel}'
            hemisphere_urls.append(hemisphere_url)
    except AttributeError:
        return None
    img_urls = []
    titles = []
    try:
        for hemisphere_url in hemisphere_urls:
            browser.visit(hemisphere_url)
            html = browser.html
            imgs_soup = soup(html, 'html.parser')
            img_rel = imgs_soup.find('img', class_='wide-image').get('src')
            img_url = f'https://marshemispheres.com/{img_rel}'
            img_urls.append(img_url)
            title = imgs_soup.find('h2', class_='title').get_text()
            titles.append(title)
    except AttributeError:
        return None
    hemispheres = [{'image': i, 'caption': t} for i, t in zip(img_urls, titles)]
    return hemispheres

if __name__ == "__main__":
    print(scrape_all())