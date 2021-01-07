#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:46:15 2020
Steam遊戲百大排行
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
    #百大排行
    options = Options()
    options.add_argument("--disable-notifications")
        
    url = "https://store.steampowered.com/stats/?l=tchinese"
    #chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    #chrome.get(url)
    response = requests.get(url)#欲加載之網頁
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    #設定完成，開始動作
    #json content:
        #{
            #id:
            #name:
            #url:
            #current_servers:
            #game_content:
        #}
    #========================================================
    
    results = soup.html.find_all("a", class_="gameLink") 
    content = {}
    payload = []
    servers = soup.html.find_all("span", class_="currentServers") #目前在線人數
    i=1  #loop variable
    time=0
    
    for result in results:
        browser = result.get('href')#去該遊戲的網址加載內容
        content_response = requests.get(browser)#欲加載之網頁
        game_content_soup = BeautifulSoup(content_response.content, "html.parser")
        Game_content = game_content_soup.html.find("div", class_="game_description_snippet")
        #這有問題FFF
        print(Game_content.text)
        content = {'Id':i,'name':result.text,'url':result.get('href'),'current_servers':servers[time].text,'Game_content':Game_content.text}
            #print(content)
        i = i+1
        time+=2
        payload.append(content)
    print(payload)
    return jsonify(payload)
    #輸出html的內容
<<<<<<< HEAD
=======

>>>>>>> 6140178a93505ac66c8d6c318669811d1eb20344
    #獲取json
    #整理資料
    #弄成json_return 
    #回傳給webpage
    #========================================================
@app.route('/Sales', methods=['GET'])
@cross_origin()
def sale():
    #顯示特惠通知
    options = Options()
    options.add_argument("--disable-notifications")
        
    url = "https://store.steampowered.com/search/?filter=topsellers&specials=1"
    #chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    #chrome.get(url)
    response = requests.get(url)#欲加載之網頁
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    #設定完成，開始動作
    Game_names = soup.html.find_all("span", class_="title") 
    discounts = soup.html.find_all("div", class_="col search_discount responsive_secondrow")
    prices = soup.html.find_all("div", class_="col search_price discounted responsive_secondrow")
    payload = []
    a = []
    origin_price = []  #原價
    discount_price = []  #特價
    content = {}
    i=0
    for result in prices:
            #特價的價格
            #print(result.text.split('NT'))
            a = result.text.split('NT')
            #print(a[2])  #第一格為原價第二格為特價
            a[0].replace(" ", "")
            a[1].replace(" ", "")
            a[2].replace(" ", "")
            origin_price.insert(i,a[1]) 
            discount_price.insert(i,a[2])
            print(discount_price[i])
            i+=1
    for time in range(0,50):
        #print(Game_names[time].text,discounts[time].text,origin_price[time],discount_price[time])
        a = discounts[time].text.split('\n')
        content = {'ID':time,'Game_name':Game_names[time].text,'discount':a[1],'origin_price':origin_price[time],'discount_price':discount_price[time].replace(" ","")}
        payload.append(content)

        #擷取優惠價格'''
<<<<<<< HEAD
    
    #print(payload)       
    return jsonify(payload)
    #每日特惠 https://store.steampowered.com/search/?filter=topsellers&specials=1
    
#========================================================
@app.route('/Game_content', methods=['GET'])
@cross_origin()
def get_content():
    #擷取遊戲內容
    payload = []
    return jsonify(payload)
#========================================================
@app.route('/News_content', methods=['GET'])
@cross_origin()
def get_news():
    
    payload = []
    
=======
>>>>>>> 6140178a93505ac66c8d6c318669811d1eb20344
    
    #print(payload)       
    return jsonify(payload)
    #每日特惠 https://store.steampowered.com/search/?filter=topsellers&specials=1
    
<<<<<<< HEAD
    
    
    
    
    
    
    
    
    
    
    
    
    
    return jsonify(payload)
#========================================================
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)
=======
#========================================================
@app.route('/Game_content', methods=['GET'])
@cross_origin()
def get_content():
    #擷取遊戲內容
    payload = []
    return jsonify(payload)
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)
>>>>>>> 6140178a93505ac66c8d6c318669811d1eb20344
