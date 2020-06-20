# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:34:19 2020

@author: owner
"""

import os,datetime,time,MySQLdb
readtime=datetime.datetime.today()
import requests
#-----------------------------------------------------------
def avg(date):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='',db='testdb123', charset='utf8')
    cursor = conn.cursor()

    #抓取SiteId
    sql = 'SELECT DISTINCT SiteId FROM real_time_information;'
    cursor.execute(sql)
    sitere = cursor.fetchall()
    num1=cursor.rowcount
    
    #需要做運算的資料
    col = ['AQI','CO','NO2','O3_8hr','O3','PM10','PM2_5','SO2']
    conn = MySQLdb.connect(host='localhost', user='root', passwd='',db='testdb123', charset='utf8')
    cursor = conn.cursor()
    
    for i in range(num1):
        #將要insert的資料
        willinsert = dict()
        for j in col:
            
            sql2="SELECT {data} FROM real_time_information WHERE PublishTime LIKE '{date}%' AND SiteId = '{site}'".format(data=j,date=date,site=sitere[i][0])
            print(sql2)
            cursor.execute(sql2)
            
            re = cursor.fetchall()
            num=cursor.rowcount
            conn.commit()
            
            sum=float()
            for k in range(num):
                sum=sum+re[k][0]
                
            sum = sum/num
                
            willinsert[j] = round(sum,2)
        willinsert['SiteId'] = sitere[i][0]
        willinsert['Monitor'] = date
        print(willinsert)
        
        #insert運算好的資料
        SQL="INSERT INTO Old_information (AQI,CO,Monitor,NO2,\
        O3_8hr,O3,PM10,PM2_5,SO2,SiteId)VALUE"
        SQL=SQL+"('%.2f','%.2f','%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%s')"\
        %(willinsert['AQI'],willinsert['CO'],willinsert['Monitor'],willinsert['NO2'],\
          willinsert['O3_8hr'],willinsert['O3'],willinsert['PM10'],willinsert['PM2_5'],\
          willinsert['SO2'],willinsert['SiteId'])
        cursor.execute(SQL)
        conn.commit()

#-----------------------------------------------------------------
while(1):
    time.sleep(3600)
    executetime=datetime.datetime.today()
    print(readtime)
    print(executetime)
    #--------------------------------新的一天執行更新
    if(executetime.day!=readtime.day):
        print("A NEW DAY")
        #------------------------------計算插在這裡
        
        date="%d-%02d-%02d"%(readtime.year,readtime.month,readtime.day)
        avg(date)
        #----------------------------------------------刪除即時資料
        conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
        conn.set_character_set('utf8')
        cursor=conn.cursor()
        SQL="DELETE FROM Real_time_information WHERE PublishTime LIKE '%d-%02d-%02d%%';"%(int(readtime.year),int(readtime.month),int(readtime.day))
        print(SQL)
        cursor.execute(SQL)
        conn.commit()
        #-------------------------------刪除時間超過一個月
        conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
        conn.set_character_set('utf8')
        cursor=conn.cursor()
        SQL="SELECT DISTINCT Monitor FROM old_information"
        cursor.execute(SQL)
        num=cursor.rowcount
        date=cursor.fetchall()
        conn.commit()
        
        for i in range(num):
            setdate=datetime.datetime(int(date[i][0][0:4]),int(date[i][0][5:7]),\
                              int(date[i][0][8:10])) #抓時間放入datetime
            if((executetime-setdate).days>=31):
                conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
                conn.set_character_set('utf8')
                cursor=conn.cursor()
                print("%s"% (date[i][0]))
                SQL="DELETE FROM old_information WHERE Monitor = '%s'"%(date[i][0])
                cursor.execute(SQL)
                conn.commit()
        #------------------------------------------------------------
        print('delete compelete!')
        del SQL,conn,cursor,num,i,date
        #------------------------------------隔一小時更新一次
    if((executetime-readtime).seconds>=3600):
        
        print("資料載入中")
        url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
        reqs = requests.get(url);
        reqs.encoding="utf-8"
        reqsjson = reqs.json()
        print('資料載入完成')
          #------------------------------------將資料轉型
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
            #-----------------------------------匯入資料
        print("匯入資料中")
        conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
        conn.set_character_set('utf8')
        cursor=conn.cursor() 
        for i in reqsjson:
            if(i['Status']=="設備維護"):
                continue;
            else:
                
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
        print("匯入完成")
        del i,SQL,cursor,conn,url,reqs,reqsjson
        readtime=datetime.datetime.today()
        #--------------------------------------------------------------
os.system("PAUSE")