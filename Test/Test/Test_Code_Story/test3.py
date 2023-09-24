# coding=utf-8
import pandas as pd
from pandas import Series, DataFrame
import requests
import urllib.parse
import time
import csv
dictionary = {}
my_list = []
df = pd.read_csv('./CSV_DataSet/public_dataset.csv')
df.insert(1, 'zipcode', None, allow_duplicates=False)
csv_filename = "errozipcode.csv"

for i in range(47,57):
    query = df['縣市'][i]+df['鄉鎮市區'][i]+df['路名'][i]
    if query in dictionary.keys(): 
       df.loc[i,'zipcode'] = dictionary[query]
       
    else:
        url = urllib.parse.quote(query)
        r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url )
        if r.status_code == 429 :
            print(df['ID'][i+1])
            break
        if(len(r.json()['zipcode']) == 0):
            print("erro")
        else:
            print(r.json()['zipcode'])
            print(len(r.json()['zipcode']))
        
        time.sleep(4)
   
df.drop(columns = ['縣市','鄉鎮市區','路名'],inplace=True)
with open("csv_filename",mode= 'w') as file : 
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in my_list:
        writer.writerow([item])
