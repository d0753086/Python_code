# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:07:10 2020

@author: owner
"""
#!/bin/python3


import requests#, json;
url="http://opendata.epa.gov.tw/webapi/Data/ATM00679/?$orderby=MonitorDate%20desc&$skip=0&$top=1000&format=json"
reqs = requests.get(url);
reqs.encoding="utf-8"
reqsjson = reqs.json()
for i in reqsjson:
    i['AQI'] = int(i['AQI'])
    if(i['COSubIndex'] == ""):
        i['COSubIndex'] = 0
    i['COSubIndex'] = float(i['COSubIndex'])
        
    if(i['NO2SubIndex'] == ""):
        i['NO2SubIndex'] = 0
    i['NO2SubIndex'] = float(i['NO2SubIndex'])
    
    if(i['O38SubIndex'] == ""):
        i['O38SubIndex'] = 0
    i['O38SubIndex'] = float(i['O38SubIndex'])
    
    if(i['O3SubIndex'] == ""):
        i['O3SubIndex'] = 0
    i['O3SubIndex'] = float(i['O3SubIndex'])
    
    if(i['PM10SubIndex'] == ""):
        i['PM10SubIndex'] = 0
    i['PM10SubIndex'] = float(i['PM10SubIndex'])
    
    if(i['PM25SubIndex'] == ""):
        i['PM25SubIndex'] = 0
    i['PM25SubIndex'] = float(i['PM25SubIndex'])
    
    if(i['SO2SubIndex'] == ""):
        i['SO2SubIndex'] = 0
    i['SO2SubIndex'] = float(i['SO2SubIndex'])

import MySQLdb 
conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
conn.set_character_set('utf8')
cursor=conn.cursor() 

for i in reqsjson:
    #print(i["County"], i["SiteName"], i["PM2.5"])
    SQL="INSERT INTO old_information (AQI,CO,Monitor,NO2,O3_8hr,O3,PM10,PM2_5,SO2\
    ,SiteId)VALUE"
    SQL=SQL+"('%d','%.2f','%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%s')" % (i['AQI']\
             ,i['COSubIndex'],i['MonitorDate'],i['NO2SubIndex'],i['O38SubIndex']\
             ,i['O3SubIndex'],i['PM10SubIndex'],i['PM25SubIndex']\
             ,i['SO2SubIndex'],i['SiteId'])
    cursor.execute(SQL)

conn.commit() 