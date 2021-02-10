#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:46:15 2020
一週天氣預報
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
    #一週天氣預報     
    options = Options()
    options.add_argument("--disable-notifications")
        
    url = "https://www.cwb.gov.tw/V8/C/W/week.html"
    #chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    #chrome.get(url)
    response = requests.get(url)#欲加載之網頁
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    #設定完成，開始動作
    
    '''
    不同的地方，day各有七天
    json content:
        {
             [
                {
                    country:xxx
                    sidedate:[
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },{
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        }                        
                            ]                   
                },
                {
                    country:xxx
                    sidedate:[
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },{
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        },
                        {
                            day:xxx,
                            status:xxx,
                            temp:xxx,
                            pic_url:xxxxxxxx
                        }                        
                            ]                   
                },...
            ]
        }'''
    #========================================================
    
    results = soup.html.find_all("a", class_="gameLink") 
    content = {}
    payload = []
    servers = soup.html.find_all("span", class_="currentServers") #目前在線人數
    i=1  #loop variable
    time=0
    
    for result in results:
        #browser = result.get('href')#去該遊戲的網址加載內容
        #content_response = requests.get(browser)#欲加載之網頁
        #game_content_soup = BeautifulSoup(content_response.content, "html.parser")
        #Game_content = game_content_soup.html.find("div", class_="game_description_snippet")
        #這有問題FFF
        #print(Game_content.text)
        content = {'Id':i,'name':result.text,'url':result.get('href'),'current_servers':servers[time].text}
            #print(content)
        i = i+1
        time+=2
        payload.append(content)
    print(payload)
    return jsonify(payload)
    #輸出html的內容

    #獲取json
    #整理資料
    #弄成json_return 
    #回傳給webpage
    #========================================================
@app.route('/day', methods=['GET'])
@cross_origin()
def day():
    '''
        找不同天數的星期名稱
        jsoncontent
        {
            day1:星期x,
            day2:星期x,
            day3:星期x,
            day4:星期x,
            day5:星期x,
            day6:星期x,
            day7:星期x,                  
        }
    '''

    options = Options()
    options.add_argument("--disable-notifications")
        
    url = "https://www.cwb.gov.tw/V8/C/W/week.html"
    #chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    #chrome.get(url)
    response = requests.get(url)#欲加載之網頁
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())
    #設定完成，開始動作
    days = soup.html.find_all("span", class_="heading_3") 
    print(days)
    content = {}
    '''
    content = {'day1':days}
  '''
    return jsonify(content)
#========================================================

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)

