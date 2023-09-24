# 設定編碼格式為​​UTF-8
# coding=utf-8

import pandas as pd  # 導入pandas庫，用於資料處理
import requests  # 匯入requests庫，用於進行HTTP請求
import urllib.parse  # 導入urllib函式庫，用於網址編碼
import time  # 導入time庫，用於時間相關操作
import csv  # 導入csv庫，用於CSV檔案操作

# 建立一個空字典，用於儲存地址到郵遞區號的映射
dictionary = {}

# 建立一個空列表，用於儲存額外的資料（目前沒有使用到）
my_list = []

# 從CSV檔案讀取數據，指定編碼格式為​​UTF-8
df = pd.read_csv('./CSV_DataSet/public_dataset.csv', encoding='utf-8')

# 在資料框中插入一個名為'zipcode'的資料列，並初始化為None，不允許重複值
df.insert(1, 'zipcode', None, allow_duplicates=False)

# 遍歷資料框中的每一行
for i in range(0, len(df)):
    # 建立查詢字串，將'縣市'、'鄉鎮市區'和'路名'拼接在一起
    query = df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]
    
    # 如果查詢字串已經在字典中存在，將郵遞區號賦值給資料框中的'zipcode'列
    if query in dictionary.keys():
        df.loc[i, 'zipcode'] = dictionary[query]
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

# 列印整個字典，顯示地址到郵遞區號的映射
print(dictionary)

# 保存CSV文件
csv_filename = "errozipcode.csv"
with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in my_list:
        writer.writerow([item])
df.to_csv("public_dataset_to.csv", index=False)  # index=False 表示不保存索引列
