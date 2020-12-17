#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:41:13 2020

@author: ivan
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import pytesseract
from PIL import Image

print("上車地點是:")
start = input()
print("下車地點是:")
end = input()
print("乘車日期是?格式為2020/xx月/xx日")
whatdate = input()
print("時段是?格式為00:00開始每隔三小時,中間加逗號")
interval = input()
print(start+end+whatdate)
options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("http://www.ebus.com.tw/")
time.sleep(3)
close = chrome.find_element_by_xpath('/html/body/div[4]/div/a[1]')
close.click()


chrome.switch_to_frame(0)
chrome.switch_to_frame(0)

ticket = chrome.find_element_by_xpath('/html/body/table/tbody/tr[1]/td/table/tbody/tr/td[1]/a/img')
ticket.click()

net = chrome.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/a[1]')
net.click()

windows = chrome.window_handles
chrome.switch_to_window(windows[-1])

agree = chrome.find_element_by_name('Agreement')
agree.click()
#========================================================================以下為訂購資料填寫
name = chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
name.send_keys('林伯桎')

ID_number = chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input')
ID_number.send_keys('R124906335')

Phone_number = chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/input')
Phone_number.send_keys('0983088160')

select_start = Select(chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[5]/td[2]/select'))

select_start.select_by_visible_text(start)

select_end = Select(chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[6]/td[2]/select'))

select_end.select_by_visible_text(end)


date = Select(chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[7]/td[2]/select'))
date.select_by_value(whatdate)

time_interval = Select(chrome.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[8]/td[2]/select'))
time_interval.select_by_value(interval)

image = Image.open(r'https://www.ebus.com.tw/NetOrder/CheckImageCode.aspx')
code = pytesseract.image_to_string(image)
print(code)

































