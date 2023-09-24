# coding=utf-8
import pandas as pd
from pandas import Series, DataFrame
import requests
import urllib.parse
import time

df = pd.read_csv('../CSV_DataSet/public_dataset.csv')
df.insert(1, 'zipcode', None, allow_duplicates=False)

for i in range(0,len(df)):
    query = df['縣市'][i]+df['鄉鎮市區'][i]+df['路名'][i]
    url = urllib.parse.quote(query)
    r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url)
    zipcode =r.json()['zipcode']
    print(r.json()['zipcode'])
    df.loc[i,'zipcode'] = zipcode
    time.sleep(2)

df.drop(columns = ['縣市','鄉鎮 市區','路名'],inplace=True)
print(df)

df.to_csv("public_dataset_tocsv")