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

"""
 Google Newsden tarihe göre haber url çekip 
 haber çektikten sonra tek tek urllere girip 
 1) title 
 2) description 
 3) date
 4) url
"""

start = time.time()

url_results_list = []
def google_news_opener_proper(is_headless,query_word,driver_path):
    option = webdriver.ChromeOptions()
    option.add_argument("-icognito")
    if is_headless:
        option.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    browser.implicitly_wait(0.01)
    browser.get("https://www.google.com/")

    search = browser.find_element_by_xpath("//input[starts-with(@class, 'gLFyf gsfi')]")
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
def news_list_getter(browser, max_page_num):
    news_url_list= []
    inc = 1
    try:    
        #for page_number in range(2,max_page_num):
        elements = browser.find_elements_by_xpath("//*[contains(@class, 'title')]")
        for element in elements:
            link = element.get_attribute("href")
            news_url_list.append((inc, link))
            inc += 1
       # browser.find_element_by_xpath("//*[@aria-label='Page %s']" % page_number).click()
    except():
        print("---------Exception----------")
    browser.quit()
    return news_url_list


def URL_printer(url_list):
    inc = 1
    for index in range(len(url_list)):
        print(str(inc)+ ") " +  url_list[index][1])
        inc += 1


def finding_content_of_news(i, URLname):
    result_dict = dict()
    try:
        html = urlopen(URLname)
    except:
        req = Request(URLname, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)

    bsObj = BeautifulSoup(html.read(), features="lxml")

    try:
        if   bsObj.body.h1 != None:
            result_dict["haber_basliği"] = bsObj.body.h1.text.replace('\t','')
            result_dict["haber_basliği"] = result_dict["haber_basliği"].replace('\n','')

        elif bsObj.body.h2 != None:
            result_dict["haber_basliği"] = bsObj.body.h2.text.replace('\t','')
            result_dict["haber_basliği"] = result_dict["haber_basliği"].replace('\n','')
        else:
            result_dict["haber_basliği"] = ""

        if  bsObj.findAll("div", {"itemprop": "description"},text=True):
            matchResult = bsObj.findAll("div", {"itemprop": "description"},text=True)
            result_dict["haber_aciklama"] = matchResult[0][0].contents
        elif bsObj.body.h2 != None:
            result_dict["haber_aciklama"] = bsObj.body.h2.text.replace('\t','')
            result_dict["haber_aciklama"] = result_dict["haber_aciklama"].replace('\n', '')
        elif bsObj.body.h1 != None:
            result_dict["haber_aciklama"] = bsObj.body.h1.text.replace('\t','')
            result_dict["haber_aciklama"] = result_dict["haber_aciklama"].replace('\n', '')
        else:
            result_dict["haber_aciklama"] = "yok"

#Tarih çekme algoritması tüm sitelerde ortaktır
        regex_word = r'(\d+/\d+/\d+)'
        if re.search(regex_word, bsObj.body.text):
            matchResult = re.search(regex_word, bsObj.body.text)
            result_dict["haber_tarihi"] = matchResult.group(1)
        elif re.search(r'(\d+\.\d+\.\d+)', bsObj.body.text):
            matchResult = re.search(r'(\d+\.\d+\.\d+)', bsObj.body.text)
            result_dict["haber_tarihi"] = matchResult.group(1)
        elif re.search(r'(\d+ (Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık) +\d+)', bsObj.body.text):
            matchResult = re.search(r'(\d+ (Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık) +\d+)', bsObj.body.text)
            result_dict["haber_tarihi"] = matchResult.group(1)
        elif re.search(r'(\d+ [a-zA-Z]{1,7} +\d+)', bsObj.body.text):
            matchResult = re.search(r'(\d+ [a-zA-Z]{1,7} +\d+)', bsObj.body.text)
            result_dict["haber_tarihi"] = matchResult.group(1)
        elif re.search(r'(\d+-\d+-\d+)', bsObj.body.text):
            matchResult = re.search(r'(\d+-\d+-\d+)', bsObj.body.text)
            result_dict["haber_tarihi"] = matchResult.group(1)
        elif bsObj.body.time != None:
            result_dict["haber_tarihi"] = bsObj.body.time.text.replace('\t', '')
            result_dict["haber_tarihi"] = result_dict["haber_tarihi"].replace('\n', '')
        elif bsObj.body.span != None:
            result_dict["haber_tarihi"] = bsObj.body.span.text.replace('\t','')
            result_dict["haber_tarihi"] = result_dict["haber_tarihi"].replace('\n','')
        else:
            result_dict["haber_tarihi"] =  "yok"
        result_dict["haber_kaynagi"] = url_list[i][1]
        url_results_list.append(result_dict)
    except:
        print("+++++++++++++++++" + url_list[i][1])

def news_page_opener(url_list,news_number):

    threads = []
    for k in range(0,news_number,40):
        for i in range(40):
            t = threading.Thread(target=finding_content_of_news, name='thread{}'.format(i), args=(i+k,url_list[i+k][1]))
            threads.append(t)
            t.start()

        for i in threads:
            i.join()

def result_printer(url_results_list):
    for i in range(0,len(url_results_list)): #işlene bilen url sonucu kadar print eder
        print(str(i+1)+ "-) --------------------------------------------------------")
        print(url_results_list[i]["haber_basliği"])
        print(url_results_list[i]["haber_aciklama"])
        print(url_results_list[i]["haber_tarihi"])
        print(url_results_list[i]["haber_kaynagi"])

browser = google_news_opener_proper(False,'Aselsan',"/home/hamza/Desktop/chromedriver")
url_list = news_list_getter(browser, 9)
URL_printer(url_list)
news_page_opener(url_list,40)
result_printer(url_results_list)

end = time.time()

print('time is {}'.format(end - start))
