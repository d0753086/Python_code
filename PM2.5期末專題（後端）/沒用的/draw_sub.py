# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 23:41:23 2020

@author: owner
"""
import pandas as pd
import matplotlib.pyplot as plt
import MySQLdb
#from matplotlib import font_manager

def draw(SQL):
    

    def wannadraw(data):
        plt.plot(df['Monitor'],df[data])

#myfont = font_manager.FontProperties(fname='/Users/winston/opt/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf')

    conn=MySQLdb.connect(host="localhost",user="root", passwd="",db="testdb123")
    conn.set_character_set('utf8')
    cursor=conn.cursor() 
    #SQL="SELECT * FROM old_information WHERE Monitor BETWEEN '2020-05-19' AND '2020-06-03' AND SiteId = '1'"
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
    plt.xlabel("Monitor" ''',fontproperties=myfont''')
    plt.ylabel('AQI' ''',fontproperties=myfont''')
    plt.savefig('匯出的圖片.jpg')
    path = "#你這個執行檔的路徑，檔案會存在這"
    return path
#    img = cv2.imread('匯出的圖片', 1)
#path = 'Desktop/python'
#cv2.imwrite(os.path.join(path, 'waka.png'), img)
 #   cv2.waitKey(0)