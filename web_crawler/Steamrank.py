#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:46:15 2020
音樂推薦排行榜
@author: ivan
"""
import sys
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from flask import Flask, jsonify, request, Response,send_file
from flask_cors import cross_origin
import time
import requests
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    #json content:
        #{
            #id:
            #name:
            #url:
        #}
        
    options = Options()
    options.add_argument("--disable-notifications")
    
    url = "https://store.steampowered.com/stats/?l=tchinese"
    #chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    #chrome.get(url)
    response = requests.get(url)#欲加載之網頁
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    #設定完成，開始動作
    #========================================================
    
    results = soup.html.find_all("a", class_="gameLink") 
    content = {}
    payload = []
    i=1  #loop variable
    
    
    for result in results:
        content = {'Id':i,'name':result.text,'url':result.get('href')}
        #print(content)
        i = i+1
        payload.append(content)
    print(payload)
    return jsonify(payload)
    #輸出html的內容
    #定義網址
    
    #爬取網ｔ
    #獲取json
    #整理資料
    #弄成json_return 
    #回傳給webpage
    
    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)
    sys.exit()