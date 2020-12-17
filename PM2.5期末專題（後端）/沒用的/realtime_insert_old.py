#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:05:04 2020

@author: winston
"""

import pandas as pd
import MySQLdb


conn = MySQLdb.connect(host='localhost', user='root', passwd='', 
                       db='testdb123', charset='utf8')

cursor = conn.cursor()

sql = 'SELECT * FROM real_time_information;'
cursor.execute(sql)

# 獲取資料庫列表資訊
col = cursor.description

# 獲取全部查詢信息
re = cursor.fetchall()
# 獲取一行資料
#re = cursor.fetchone()

# 獲取的資料預設為tuple，將columns轉換成DataFrame
columns = pd.DataFrame(list(col))
# 將資料轉換成DataFrame，並匹配columns
df = pd.DataFrame(list(re), columns=columns[0])
#將SiteId設為index，方便等下利用SiteId選取資料
df = df.set_index('SiteId')

sql2 = 'SELECT DISTINCT SiteId FROM real_time_information;'
cursor.execute(sql2)
re2 = cursor.fetchall()
st = list(re2)

def transform(i):
    #依照SiteId選取資料
    temp = pd.DataFrame(df.loc[i])
    
    #將SiteId歸位，因為SiteId當index的話，無法區別資料
    #（例如選取基隆市的資料，假如資料有兩筆，但SiteId都為1，無法區分）
    temp = temp.reset_index()
    #計算好的資料
    willinsert = dict()
    
    for k in temp.columns:
        
        sum = float(0)
        for j in temp.index: 
            #選取格式為int或的float的資料並個別加總起來
            if(temp[k].dtypes == float or temp[k].dtypes == int):
                sum = sum + float(temp[k].loc[j])
            #PublishTime改成Monitor,只保留年月日
            if(k == 'PublishTime'):
                willinsert['Monitor'] = temp[k].loc[j][:10]
            else:
                willinsert[k] = temp[k].loc[j]
        if(sum != float(0)):
            #依照資料有多少筆取平均
            sum = sum/(len(temp.index))
            #只顯示到小數點後第二位
            willinsert[k] = round(sum,2)
    
    print(willinsert)
    print()
    
for i in st:        
    transform(i)






















