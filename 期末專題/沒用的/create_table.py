# -*- coding: utf-8 -*-
"""
Created on Thu May 14 00:55:16 2020

@author: owner
"""

import MySQLdb 
conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
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

conn.commit()