# coding=utf-8
import sqlite3
import pandas as pd
from urllib.parse import unquote
import requests
import urllib.parse
import time
import csv

dictionary = {}
my_list = []
counter = 0
df = pd.read_csv('./CSV_DataSet/public_dataset.csv')
df.insert(1, 'zipcode', None, allow_duplicates=False)
csv_filename = "errozipcode.csv"
db_filename = "example.db"

# 連接到 SQLite 資料庫
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# 創建資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS zipcodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    district TEXT,
    road TEXT,
    zipcode TEXT
)
''')

# 提交更改
conn.commit()

for i in range(0, len(df)):
    counter += 1
    query = df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]

    if query in dictionary.keys():
        df.loc[i, 'zipcode'] = dictionary[query]
    else:
        url = urllib.parse.quote(query)
        r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url)#郵遞區號網址

        if r.status_code == 429: #被判斷為DDOS的話 輸出最後一次的Zipcode id
            print(df['ID'][i + 1])
            break

        if r.json()['zipcode'] != "":
            zipcode = r.json()['zipcode']
            dictionary[query] = r.json()['zipcode']
            # 將資料插入資料庫
            cursor.execute('''
                INSERT INTO zipcodes (city, district, road, zipcode)
                VALUES (?, ?, ?, ?)
            ''', (df['縣市'][i], df['鄉鎮市區'][i], df['路名'][i], zipcode))

            # 提交更改
            conn.commit()

            print(f"""
------------------------------------------
項目: {counter} 號
request : http://zip5.5432.tw/zip5json.py?adrs={unquote(url)}
目前地區為: {df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]}
找尋到郵遞區號為: {(r.json()['zipcode'])}
------------------------------------------
""")
            df.loc[i, 'zipcode'] = zipcode
            time.sleep(2)
        else:
            my_list.append(df["ID"][i] + query)

# 關閉資料庫連接
conn.close()

# 刪除不需要的欄位
df.drop(columns=['縣市', '鄉鎮市區', '路名'], inplace=True)

# 寫入 CSV 檔案
with open(csv_filename, mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in my_list:
        writer.writerow([item])

# 將 DataFrame 寫入新的 CSV 檔案
df.to_csv("./Save_CSV/Output_CSV/Output_CSV_Version1")

