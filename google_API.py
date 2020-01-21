#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time
import json
from urllib.request import urlopen

## Google API News
## Sadece news URL çekmektedir.

def google_news(topic):
    linkList = []
    query = topic
    searchEngineKey = ""
    Authentication = ""
    z = 1
    for y in range(0,100,10):
        r = requests.get('https://www.googleapis.com/customsearch/v1?',
        params={"key": Authentication,"cx": searchEngineKey,"q":query,"start" : y+1,"lr":"lang_tr"})
        response = r.json()
        for i in range(10):
            try:
                linkList.append(response["items"][i]["link"])
            except:
                pass
    for index in range(0,len(linkList)):
        print(str(z) + "-) " + linkList[index])
        z +=1

google_news("Aselsan")  #Haberi istenen başlık buraya yazınız.
