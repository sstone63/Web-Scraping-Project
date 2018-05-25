from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def scrape():

    #connect to chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #store url variable and use browser to visit page
    articles_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(articles_url)

    #scrape page for article titles and paragraphs
    html = browser.html
    soup = bs(html, "html.parser")

    article_list = soup.find("ul", class_="item_list")

    article_title = article_list.find("div", class_="content_title").text
    paragraph = article_list.find("div", class_="article_teaser_body").text

    
    
    #gather featured image url
    image_page_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_page_url)

    html = browser.html
    soup = bs(html, "html.parser")

    image_div = soup.find("article", class_="carousel_item")

    featured_image_url = "https://www.jpl.nasa.gov" + image_div.a["data-fancybox-href"]

    #scrape mars weather tweets
    tweets_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweets_url)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #scrape mars facts with pandas
    facts_url = "https://space-facts.com/mars/"

    mars_table = pd.read_html(facts_url)

    mars_df = pd.DataFrame(mars_table[0])

    mars_df = mars_df.rename(columns={0: "Description", 1: "Value"})

    mars_df = mars_df.set_index("Description")

    #convert dataframe table to html string
    mars_table = mars_df.to_html()

    mars_df.to_html("mars_table.html")

    #scrape astropedia for mars hemisphere images
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_titles_href = []
    hemisphere_image_urls = []
    hemisphere_titles_unedit = []

    hemisphere_title_scrape = soup.find_all("h3")

    for title in hemisphere_title_scrape:
        title = title.text.strip()
        hemisphere_titles_unedit.append(title)
        title = title.replace(" Hemisphere ", " ")
        title = title.replace(" ", "_")
        title = title.lower()
        hemisphere_titles_href.append(title)

    #scrape for hemisphere images
    count = 0

    for title in hemisphere_titles_href:
        hemisphere_url = ("https://astrogeology.usgs.gov/search/map/Mars/Viking/" + title)
        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, "html.parser")
        image_element = soup.find("img", class_="wide-image")    
        image_url = "https://astrogeology.usgs.gov" + image_element["src"]    
        title = title.replace("_", " ")

        image_dict = {}
        image_dict["title"] = hemisphere_titles_unedit[count]
        image_dict["img_url"] = image_url
    
        hemisphere_image_urls.append(image_dict)

        count += 1

    # create final dictionary       
    mars_dict = {
    "id": 1,
    "article_title": article_title,
    "article_desc": paragraph,
    "featured_image_url": featured_image_url,
    "mars_weather": mars_weather,
    "mars_table": mars_table,
    "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_dict

scrape()

