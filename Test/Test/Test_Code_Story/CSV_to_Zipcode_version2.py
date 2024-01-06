# coding=utf-8
import pandas as pd
import requests
import urllib.parse
import time
import csv

dictionary = {}
my_list = []
df = pd.read_csv('./CSV_DataSet/public_dataset.csv',encoding='utf-8')
df.insert(1, 'zipcode', None, allow_duplicates=False)
for i in range(0, len(df)):
    query = df['縣市'][i] + df['鄉鎮市區'][i] + df['路名'][i]
    if query in dictionary.keys():
        df.loc[i, 'zipcode'] = dictionary[query]
    else:
        url = urllib.parse.quote(query)
        r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url)
        if r.status_code == 429:
            print(df['ID'][i + 1])
            break
        if r.json()['zipcode'] != "":
            zipcode = r.json()['zipcode']
            dictionary[query] = r.json()['zipcode']
            print(str("ID = ") + df['ID'][i]+'; 郵遞區號 :'+r.json()['zipcode'])
            print(len(r.json()['zipcode']))
            df.loc[i, 'zipcode'] = zipcode
            time.sleep(5)
        else:
            zipcode6 = r.json()['zipcode6']
            dictionary[query] = r.json()['zipcode6']
            print(str("ID = ") + df['ID'][i]+'; 郵遞區號 :'+r.json()['zipcode6'])
            print(len(r.json()['zipcode6']))
            df.loc[i, 'zipcode'] = zipcode6
            time.sleep(5)

            my_list.append(df["ID"][i] + query)
            print(my_list)

df.drop(columns=['縣市', '鄉鎮市區', '路名'], inplace=True)

# 添加一个新列标记是否成功获取了zipcode
df['zipcode_success'] = df['zipcode'].notna()

# 保存CSV文件
csv_filename = "errozipcode.csv"
with open(csv_filename, mode='w',encoding='utf-8' ,newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in my_list:
        writer.writerow([item])
df.to_csv("public_dataset_to.csv", index=False)  # index=False 表示不保存索引列

