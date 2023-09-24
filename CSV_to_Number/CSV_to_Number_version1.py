# 設定編碼格式為​​UTF-8
# coding=utf-8

import pandas as pd  # 導入pandas庫，用於資料處理
import time  # 導入time庫，用於時間相關操作
import csv  # 導入csv庫，用於CSV檔案操作
import datetime #導入datetime ，用於時間運算
DataSet = './CSV_DataSet/public_dataset.csv' #輸入CSV位置
SaveName = './Save_CSV/Output_CSV/Output_CSV_Version1.csv'  #輸出CSV位置

#紀錄開始時間
start_time = datetime.datetime.now()

# 建立一個空字典，用於儲存地址到郵遞區號的映射
dictionary = {}

# 從CSV檔案讀取數據，指定編碼格式為​​UTF-8
df = pd.read_csv(DataSet, encoding='utf-8')

# 在資料框中插入一個名為'zipcode'的資料列，並初始化為None，不允許重複值
df.insert(1, 'zipcode', None, allow_duplicates=False)

# 遍歷資料框中的每一行
for i in range(0, len(df)):
    # 建立查詢字串，將'縣市'、'鄉鎮市區'和'路名'拼接在一起
    query = df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]
    print('\n')
    # 如果查詢字串已經在字典中存在，將郵遞區號賦值給資料框中的'zipcode'列
    if query in dictionary.keys():
        df.loc[i, 'zipcode'] = dictionary[query]
        print(query + " the same as "+df['ID'][i]+'\n')
        print("Same number :" + str(df['zipcode'][i]))
    else:
        # 如果查詢字串不在字典中，建立一個新的郵遞區號並加入字典中
        zipcode = i
        dictionary[query] = zipcode
        # 列印ID和對應的郵遞區號
        print(str("ID = ") + df['ID'][i] + '; 郵遞區號 :' + str(dictionary[query]))
        # 將新的郵遞區號賦值給資料框中的'zipcode'列
        df.loc[i, 'zipcode'] = zipcode

# 刪除資料中不再需要的列，包括'縣市'、'鄉鎮市區'和'路名'
df.drop(columns=['縣市', '鄉鎮市區', '路名'], inplace=True)

# 建立一個新欄位'zipcode_success'，標記是否成功取得了郵遞區號
df['zipcode_success'] = df['zipcode'].notna()
# 紀錄結束時間
end_time = datetime.datetime.now()

# 計算運行時間
execution_time = (end_time - start_time).total_seconds() * 1000
print('\n')
print("程式運行時長：", execution_time, "ms",'\n')
# 保存CSV文件
df.to_csv(SaveName , index=False)  # index=False 表示不保存索引列
print("Save Successful!",'\n')
