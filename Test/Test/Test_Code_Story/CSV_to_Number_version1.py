# 設定編碼格式為UTF-8
# coding=utf-8

import pandas as pd  # 導入pandas庫，用於資料處理
import time  # 導入time庫，用於時間相關操作
import csv  # 導入csv庫，用於CSV檔案操作
import datetime #導入datetime ，用於時間運算

DataSet = './CSV_DataSet/AOI.csv' #輸入CSV位置
SaveName = './Save_CSV/Output_CSV/Output_AOI-CSV_Version1.csv'  #輸出CSV位置
#紀錄開始時間
start_time = datetime.datetime.now()

df = pd.read_csv(DataSet, encoding='utf-8')

for i in range(0, len(df)):
    dataset = df['KWH'][i]
    if dataset > 2.0195:
        
        print(df.loc[i, ['captureTime', 'KW_A', 'KW_B', 'KW_C', 'KWH']])
# 紀錄結束時間
end_time = datetime.datetime.now()
print("Save Successful!", '\n')
print(end_time)
