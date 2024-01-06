# Step 1: 匯入所需的模組
import sqlite3
import pandas as pd
from urllib.parse import unquote
import requests
import urllib.parse
import time
import csv

# Step 2: 定義資料庫檔案名稱
db_filename = "example.db"
csv_filename = "./Save_CSV/Output_CSV/Output_CSV_Version1.csv"
# Step 3: 創建資料表的函式
def create_zipcodes_table():
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

    # 關閉資料庫連接
    conn.close()

# Step 4: 處理地址資料的函式
def process_address_data(df):
    # 創建一個字典來儲存已經查詢過的地址與郵遞區號的對應關係
    dictionary = {}
    # 儲存錯誤的資料
    my_list = []
    counter = 0

    # 連接到 SQLite 資料庫
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # 迭代處理 DataFrame 的每一行
    for i in range(0, len(df)):
        counter += 1
        query = df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]

        # 檢查是否已經有查詢過這個地址，若有，直接取得郵遞區號
        if query in dictionary.keys():
            df.loc[i, 'zipcode'] = dictionary[query]
        else:
            # 將地址進行 URL 編碼，並發送查詢
            url = urllib.parse.quote(query)
            r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url)

            # 檢查 HTTP 狀態碼是否為 429（DDOS 防護）
            if r.status_code == 429:
                print(df['ID'][i + 1])
                break

            # 如果成功取得郵遞區號，則更新字典、資料庫，並顯示相關訊息
            if r.json().get('zipcode'):
                zipcode = r.json()['zipcode']
                dictionary[query] = r.json()['zipcode']

                cursor.execute('''
                    INSERT INTO zipcodes (city, district, road, zipcode)
                    VALUES (?, ?, ?, ?)
                ''', (df['縣市'][i], df['鄉鎮市區'][i], df['路名'][i], zipcode))

                conn.commit()

                print(f"""
    ------------------------------------------
    項目: {counter} 號
    request : http://zip5.5432.tw/zip5json.py?adrs={unquote(url)}
    目前地區為: {df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]}
    找尋到郵遞區號為: {(r.json()['zipcode'])}
    ------------------------------------------
    """)
                df.loc[i, 'zipcode'] = zipcode # !!! 將搜尋的zipcode取代原本的房屋地址 !!!
                time.sleep(2)
            else:
                # 如果查詢失敗，將錯誤資料加入列表
                my_list.append(df["ID"][i] + query)

    # 關閉資料庫連接
    conn.close()

    return df, my_list

# Step 5: 將資料寫入 CSV 檔案的函式
def write_to_csv(filename, data):
    with open(filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in data:
            writer.writerow([item])

# Step 6: 主程式
def main():
    # 創建資料表
    create_zipcodes_table()

    # 讀取 CSV 檔案
    df = pd.read_csv('./CSV_DataSet/public_dataset.csv')

    # !!!插入一列 'zipcode' 的空白欄位!!!
    df.insert(1, 'zipcode', None, allow_duplicates=False)

    # 處理地址資料
    df, error_list = process_address_data(df)

    # !!! 刪除不需要的欄位 !!!
    df.drop(columns=['縣市', '鄉鎮市區', '路名'], inplace=True)

    # 寫入 CSV 檔案
    write_to_csv(csv_filename, error_list)

    # 將 DataFrame 寫入新的 CSV 檔案
    df.to_csv("./Save_CSV/Output_CSV/Output_CSV_Version1.csv", index=False)

# Step 7: 程式進入點
if __name__ == "__main__":
    main()
