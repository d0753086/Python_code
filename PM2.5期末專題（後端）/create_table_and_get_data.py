# -*- coding: utf-8 -*-
"""
Created on Thu May 14 00:55:16 2020

@author: owner
"""

import MySQLdb,requests
conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
conn.set_character_set('utf8')
cursor=conn.cursor() 

SQL="CREATE TABLE Real_time_information (AQI int(3),CO float(2),CO_8hr float(1),\
NO float(2),NO2 float(2),NOx float(2),\
O3 float(2),O3_8hr float(2),PM10 float(2),PM10_AVG float(2),Pollutant char(10),\
PublishTime char(16),SO2 float(2),SO2_AVG int(2),SiteId char(3),\
Status char(16),WindDirec char(3),WindSpeed float(2),PM2_5 float(2),PM2_5_AVG float(3))"
cursor.execute(SQL)

SQL1="CREATE TABLE Old_information (AQI int(3),CO float(2),Monitor char(10),NO2 float(3),\
O3_8hr float(3),O3 float(3),PM10 float(3),PM2_5 float(3),SO2 float(2),SiteId char(3))"

cursor.execute(SQL1)

SQL2="CREATE TABLE Location (SiteId int(3),Latitude char(10),Longitude char(10),\
SiteName char(20),County char(10))"
cursor.execute(SQL2)

SQL3="CREATE TABLE AQI_Status (AQI int(3),Status char(16))"
cursor.execute(SQL3)

conn.commit()
print("create table complete!")
#------------------------------------------------------------GETOLDDATA
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

for i in reqsjson:
    SQL="INSERT INTO old_information (AQI,CO,Monitor,NO2,O3_8hr,O3,PM10,PM2_5,SO2\
    ,SiteId)VALUE"
    SQL=SQL+"('%d','%.2f','%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%s')" % (i['AQI']\
             ,i['COSubIndex'],i['MonitorDate'],i['NO2SubIndex'],i['O38SubIndex']\
             ,i['O3SubIndex'],i['PM10SubIndex'],i['PM25SubIndex']\
             ,i['SO2SubIndex'],i['SiteId'])
    cursor.execute(SQL)

conn.commit()
print("get old_data complete!")
#------------------------------------------------GETLOCATION
url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
reqs = requests.get(url);
reqs.encoding="utf-8"
reqsjson = reqs.json()
for i in reqsjson:
    i['SiteId']=int(i['SiteId'])
 
for i in reqsjson:
    SQL="INSERT INTO Location (SiteId,Latitude,Longitude,SiteName,County) VALUE"
    SQL=SQL+"('%d','%s','%s','%s','%s')"% (i['SiteId'],i['Latitude'],\
             i['Longitude'],i['SiteName'],i['County'])
    cursor.execute(SQL)

conn.commit()
print("get location complete!")
#--------------------------------------------------GETDATA

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
print("get realtime information complete!")
#-------------------------------------aqi

for i in range(51):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '良好')"%(i)
    cursor.execute(SQL)
for i in range(51,101):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '普通')"%(i)
    cursor.execute(SQL)
for i in range(101,151):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '對敏感族群不健康')"%(i)
    cursor.execute(SQL)
for i in range(151,201):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '對所有族群不健康')"%(i)
    cursor.execute(SQL)
for i in range(201,301):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '非常不健康')"%(i)
    cursor.execute(SQL)
for i in range(301,501):
    SQL="INSERT INTO AQI_Status (AQI, Status)\
         VALUES (%d, '危害')"%(i)
    cursor.execute(SQL)
conn.commit()
print("get aqi complete!")
#----------------------------------------------主鍵
SQL="ALTER TABLE real_time_information ADD PRIMARY KEY(PublishTime,SiteId)"
cursor.execute(SQL)
conn.commit()
SQL="ALTER TABLE old_information ADD PRIMARY KEY(Monitor,SiteId)"
cursor.execute(SQL)
conn.commit()
SQL="ALTER TABLE location ADD PRIMARY KEY(SiteId)"
cursor.execute(SQL)
conn.commit()
SQL="ALTER TABLE AQI_Status ADD PRIMARY KEY(AQI)"
cursor.execute(SQL)
conn.commit()
print("主鍵設定完成")

