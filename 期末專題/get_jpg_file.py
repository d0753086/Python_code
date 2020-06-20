# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 11:00:08 2020

@author: Joe
"""

import requests

SERVER_IP = "127.0.0.1"
API_SERVER = "http://" + SERVER_IP + ":3000"
DOWNLOAD_IMAGE_API = "/upload"

try:
    #例外處理，類似IF-ELSE
    
    downloadImageInfoResponse = requests.get(
        API_SERVER + DOWNLOAD_IMAGE_API)

    if downloadImageInfoResponse.status_code == 200:
        with open('下載.jpg', 'wb') as getFile:
            getFile.write(downloadImageInfoResponse.content)
except Exception as err:
    
    #發生意外錯誤，列印出錯誤訊息
    print('Other error occurred %s' % {err})