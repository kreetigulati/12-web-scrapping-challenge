#!/usr/bin/env python
# coding: utf-8

# In[38]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd


# In[39]:
def scrape():

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News

    # In[70]:


    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')


    # In[71]:


    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')
    # Retrieve the latest news paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')
    print(news_title)
    news_p


    # In[72]:


    news_title = news_title[0].text
    news_p = news_p[0].text

    print(news_title)
    news_p


    # # JPL Mars Space Images - Featured Image

    # In[57]:


    # Mars Image to be scraped
    jpl_nasa_url = 'https://spaceimages-mars.com/'
    images_url = 'https://spaceimages-mars.com/'

    browser.visit(images_url)

    html = browser.html

    images_soup = bs(html, 'html.parser')


    # In[58]:


    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[1]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path
    print(featured_image_url)


    # # Mars Facts

    # In[59]:


    # Scrape Mars facts
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    tables


    # In[61]:


    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Description",1:"Mars",2:"Earth"},errors="raise")
    mars_fact.set_index("Description",inplace=True)
    mars_fact


    # In[62]:


    fact_table=mars_fact.to_html()
    fact_table


    # In[63]:


    fact_table.replace('\n','')
    print(fact_table)


    # # Mars Hemispheres

    # In[64]:


    # Scrape Mars hemisphere title and image
    url='https://marshemispheres.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')


    # In[65]:


    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]


    # In[66]:


    # Loop through each hemisphere item
    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=url+soup.find('li').a['href']
            
            
            if (title and image_src):
                
                # Print results
                print('-'*50)
                print(title)
                print(image_src)
                
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url': image_src
            }
            # console.log(hem_dict['image_url'])
            hemisphere_image_urls.append(hem_dict)
            
        except Exception as e:
            print(e)


    # In[67]:


    hemisphere_image_urls


    # In[73]:


    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":fact_table,
        "hemisphere_images":hemisphere_image_urls
    }


    # In[74]:


    return mars_dict