# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:07:10 2020

@author: owner
"""
#!/bin/python3

import requests#, json;
url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
reqs = requests.get(url);
reqs.encoding="utf-8"
reqsjson = reqs.json()

#格式為LIST

for i in reqsjson:
    if(i['AQI']=="-" or i['AQI']==""):
        i['AQI']=0
    i['AQI']=int(i['AQI'])
    
    if(i['CO']=="-" or i['CO']==""):
        i['CO']=0
    i['CO']=float(i['CO'])
        
    if(i['CO_8hr']=="-" or i['CO_8hr']==""):
        i['CO_8hr']=0
    i['CO_8hr']=float(i['CO_8hr'])
    
    if(i['NO']=="-" or i['NO']==""):
        i['NO']=0
    i['NO']=float(i['NO'])
    
    if(i['NO2']=="-" or i['NO2']==""):
        i['NO2']=0
    i['NO2']=float(i['NO2'])
    
    if(i['NOx']=="-" or i['NOx']==""):
        i['NOx']=0
    i['NOx']=float(i['NOx'])
    
    if(i['O3']=="-" or i['O3']==""):
        i['O3']=0
    i['O3']=float(i['O3'])
    
    if(i['O3_8hr']=="-" or i['O3_8hr']==""):
        i['O3_8hr']=0
    i['O3_8hr']=float(i['O3_8hr'])
    
    if(i['PM10']=="-" or i['PM10']==""):
        i['PM10']=0
    i['PM10']=float(i['PM10'])
    
    if(i['PM10_AVG']=="-" or i['PM10_AVG']==""):
        i['PM10_AVG']=0
    i['PM10_AVG']=float(i['PM10_AVG'])
    
    if(i['PM2.5']=='ND'):
        i['PM2.5']='1'
    if(i['PM2.5']=="-" or i['PM2.5']==""):
        i['PM2.5']=0
    i['PM2.5']=float(i['PM2.5'])
       
    if(i['PM2.5_AVG']=="-" or i['PM2.5_AVG']==""):
        i['PM2.5_AVG']=0
    i['PM2.5_AVG']=float(i['PM2.5_AVG'])
    
    if(i['SO2']=="-" or i['SO2']==""):
        i['SO2']=0
    i['SO2']=float(i['SO2'])
    
    if(i['SO2_AVG']=="-" or i['SO2_AVG']==""):
        i['SO2_AVG']=0
    i['SO2_AVG']=float(i['SO2_AVG'])
    
    if(i['WindSpeed']=="-" or i['WindSpeed']==""):
        i['WindSpeed']=0
    i['WindSpeed']=float(i['WindSpeed'])

del i

import MySQLdb 
conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
conn.set_character_set('utf8')
cursor=conn.cursor() 
for i in reqsjson:
    SQL="INSERT INTO Real_time_information (AQI,CO,CO_8hr,NO,\
    NO2,NOx,O3,O3_8hr,PM10,PM10_AVG,PM2_5,PM2_5_AVG,Pollutant,PublishTime,\
    SO2,SO2_AVG,SiteId,Status,WindDirec,WindSpeed)VALUE"
    SQL=SQL+"('%d','%.2f','%.1f','%.1f','%1f','%.1f','%d','%d','%d','%d','%d',\
    '%d','%s','%s','%.1f','%d','%s','%s','%s','%d')" \
    %(i['AQI'],i['CO'],i['CO_8hr'],\
    i['NO'],i['NO2'],i['NOx'],i['O3'],i['O3_8hr'],i['PM10'],\
    i['PM10_AVG'],i['PM2.5'],i['PM2.5_AVG'],\
    i['Pollutant'],i['PublishTime'],i['SO2'],i['SO2_AVG'],i['SiteId'],\
    i['Status'],i['WindDirec'],i['WindSpeed'])
    cursor.execute(SQL)

conn.commit()