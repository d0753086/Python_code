#!/usr/bin/env python3
# coding=utf-8
# -- coding: UTF-8 --
import sys
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request, Response,send_file
import io
from flask_cors import cross_origin
import MySQLdb
#import cv2
#import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib import font_manager

app = Flask(__name__)
#底下有加@cross_origin()的路由，CORS才算有打開

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    #即時資料
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="root",
                           passwd="",
                           db="testdb123",)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM real_time_information NATURAL JOIN location\
               WHERE real_time_information.SiteId = location.SiteId')
    #把抓到的資料打包成字典的格式，再整包轉成JSON
    rv = cursor.fetchall()
    payload = []
    newpayload = []
    content = {}
    seen = set()
    for result in rv:
        content = {'SiteId':result[0], 'AQI':result[1], 'CO':result[2], 'CO_8hr':result[3], 'NO':result[4], 'NO2':result[5], 'NOx':result[6], 'O3':result[7],'O3_8hr':result[8], 'PM10':result[9],'PM10_AVG':result[10], 'Pollutant':result[11], 'PublishTime':result[12], 'SO2':result[13], 'SO2_AVG':result[14], 'Status':result[15], 'WindDirec':result[16], 'WindSpeed':result[17], 'PM2_5':result[18], 'PM2_5_AVG':result[19], 'Latitude':result[20], 'Longitude':result[21], 'SiteName':result[22], 'County':result[23]}
        payload.append(content)
    
    for d in payload:
        x = d.get('County')
        if  x not in seen:
            seen.add(x)
            newpayload.append(d)
            
    return jsonify(newpayload)
#========================================================================================================
    
@app.route('/Publish/<publishtime>/SiteId/<SiteId>', methods=['GET'])
@cross_origin()
def find(publishtime, SiteId):
    
    #找某時某地的全部資料
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="root",
                           passwd="",
                           db="testdb123",)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Old_information NATURAL JOIN location\
               WHERE Old_information.SiteId = location.SiteId\
               AND Old_information.Monitor = '%s'\
               AND Old_information.SiteId = '%s'"% (publishtime,SiteId))
    #把抓到的資料打包成字典的格式，再整包轉成JSON
    rv1 = cursor.fetchall()
    payload = []
    content = {}
    for result in rv1:
        content = {'SiteId':result[0], 'AQI':result[1], 'CO':result[2], 'NO2':result[3], 'O3':result[4],'O3_8hr':result[5], 'Monitor':result[6], 'SO2':result[7], 'PM2_5':result[8], 'PM10':result[9], 'Latitude':result[10], 'Longitude':result[11], 'SiteName':result[12], 'County':result[13]}
        payload.append(content)
    
    return jsonify(payload)
#多打的
    
#========================================================================================================
    
@app.route('/<SiteId>/<start_time>/between/<end_time>/',methods=['GET'])
@cross_origin()
def during_time_draw(SiteId,start_time, end_time):
    #找時間區間的
    #取值url請打  ?資料名稱1 = 資料名稱1/?資料名稱2 = 資料名稱2，以此類推
    seen = set()
    if(request.args.get('CO')):
        CO = request.args.get('CO')
        seen.add(CO)
    if(request.args.get('AQI')):
        AQI = request.args.get('AQI')
        seen.add(AQI)
    if(request.args.get('NO2')):
        NO2 = request.args.get('NO2')
        seen.add(NO2)
    if(request.args.get('O3')):
        O3 = request.args.get('O3')
        seen.add(O3)
    if(request.args.get('O3_8hr')):
        O3_8hr = request.args.get('O3_8hr')
        seen.add(O3_8hr)
    if(request.args.get('SO2')):
        SO2 = request.args.get('SO2')
        seen.add(SO2)
    if(request.args.get('PM2_5')):
        PM2_5 = request.args.get('PM2_5')
        seen.add(PM2_5)
    if(request.args.get('PM10')):
        PM10 = request.args.get('PM10')
        seen.add(PM10) 
    
    total = ""
    x=0
    for i in seen:
        if(x==0):
            total = i
        else:
            total = total+","+i
        x = x+1
     
    #print(total) 測資 
    def draw(SQL):
        def wannadraw(data):
            plt.plot(df['Monitor'],df[data],'o-',label=str(data))
            for a,b in zip(df['Monitor'],df[data]):
                plt.text(a, b, '%.2f' % b, ha='center', va= 'bottom',fontsize=9)
                #中文字的路徑不一樣,要用要下載simhei.ttf字型並放入ttf資料夾
                #myfont = font_manager.FontProperties(fname='/Users/winston/opt/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf')
                
        conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
        conn.set_character_set('utf8')
        cursor=conn.cursor()
        cursor.execute(SQL)
        col = cursor.description
        date=cursor.fetchall()
        
        columns = pd.DataFrame(list(col))
        columns2 = list(columns[0])
        
        df = pd.DataFrame(list(date), columns=columns[0])
        
        plt.figure(figsize=(16,9))
        
        for i in columns2:
            if(i!='Monitor'):
                wannadraw(i)
                
        plt.xticks(df['Monitor']) 
        plt.xlabel('date')#,fontproperties=myfont)
        plt.legend(loc = "best", fontsize=20)
        #path要改成這個執行檔的檔案路徑
        #由於每次檔名都一樣會自動取代，不用特地刪除
        plt.savefig('picture.jpg')
        #path:要回傳的這張圖片的檔案路徑（相對路徑）
        '''
        path = "picture.jpg"
        print(path)
        return path
        測試
        '''
    
    SQL2 = "SELECT DISTINCT %s,Monitor FROM Old_information WHERE Monitor BETWEEN '%s' AND '%s' AND SiteId='%s'"%(total,start_time,end_time,SiteId)
    print(SQL2)
    draw(SQL2)
    
    #開檔寫入資料流，再傳送，採用MIMETYPE協定
    with open("picture.jpg", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/jpg'
        )

@app.route('/upload',methods=['GET'])
@cross_origin()
def page():
    with open("下載.jpg", 'rb') as bites:    
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/jpg'
        )
        
     # 傳送圖片的路由(舊)，測試用 
 
#========================================================================================================

@app.route('/<SiteId>/<start_time>/between/<end_time>/123',methods=['GET'])
@cross_origin()
def during_time_data(SiteId, start_time, end_time):
     #找時間區間(全部)的資料
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="root",
                           passwd="",
                           db="testdb123",)
    conn.set_character_set('utf8')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM old_information WHERE Monitor BETWEEN '%s' AND '%s' AND SiteId = '%s'" % (start_time, end_time, SiteId))
    
    
    rv1 = cursor.fetchall()
    payload = []
    content = {}
    for result in rv1:
         content = {'AQI':result[0], 'CO':result[1], 'Monitor':result[2], 'NO2':result[3], 'O3':result[4],'O3_8hr':result[5], 'PM10':result[6], 'PM2_5':result[7], 'SO2':result[8], 'SiteId':result[9]}
         payload.append(content)
    
    return jsonify(payload)

#========================================================================================================
    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3000)
    sys.exit()
