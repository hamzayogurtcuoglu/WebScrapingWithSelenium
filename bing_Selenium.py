from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time
import json
from urllib.request import urlopen, Request
import re
import threading

## BING SELENIIUM BOT 
##Seleniumla bing news deki haberlerin linklerini alan bot

start = time.time()

url_results_list = []

def bing_news_opener_proper(is_headless,query_word,driver_path):
    option = webdriver.ChromeOptions()
    option.add_argument("-icognito")
    if is_headless:
        option.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    browser.implicitly_wait(0.01)
    browser.get("https://www.bing.com/")

    search = browser.find_element_by_xpath("//input[starts-with(@class, 'b_searchbox')]")
    search.clear()
    search.send_keys(query_word)
    search.submit()
    try:
        newsButton =  browser.find_element_by_xpath("//a[text()='Haberler']")
    except:
        newsButton =  browser.find_element_by_xpath("//a[text()='News']")
    newsButton.click()

    element = browser.find_element_by_xpath("//*[text()='Most recent']")
    browser.execute_script("arguments[0].click();", element)
    return browser

def news_list_getter(browser):
    news_url_list= []
    inc = 1
    try:
        elements = browser.find_elements_by_xpath("//*[contains(@class, 'title')]")
        for element in elements:
            link = element.get_attribute("href")
            news_url_list.append((inc, link))
            inc += 1
    except():
        print("---------Exception----------")
    #browser.quit()
    return news_url_list

def URL_printer(url_list):
    inc = 1
    for index in range(len(url_list)):
        print(str(inc)+ ") " +  url_list[index][1])
        inc += 1

browser = google_news_opener_proper(False,'Aselsan',"/home/hamza/Desktop/chromedriver")
url_list = news_list_getter(browser)
URL_printer(url_list)
