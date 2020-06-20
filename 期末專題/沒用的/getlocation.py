# -*- coding: utf-8 -*-
"""
Created on Tue May 26 19:43:11 2020

@author: owner
"""
import requests#, json;
url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
reqs = requests.get(url);
reqs.encoding="utf-8"
reqsjson = reqs.json()
for i in reqsjson:
    i['SiteId']=int(i['SiteId'])

import MySQLdb 
conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
conn.set_character_set('utf8')
cursor=conn.cursor() 
for i in reqsjson:
    SQL="INSERT INTO Location (SiteId,Latitude,Longitude,SiteName,County) VALUE"
    SQL=SQL+"('%d','%s','%s','%s','%s')"% (i['SiteId'],i['Latitude'],\
             i['Longitude'],i['SiteName'],i['County'])
    cursor.execute(SQL)

conn.commit()