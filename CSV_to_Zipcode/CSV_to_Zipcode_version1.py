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

for i in range(0,len(df)):
    query = df['縣市'][i]+df['鄉鎮市區'][i]+df['路名'][i]
    if query in dictionary.keys(): 
       df.loc[i,'zipcode'] = dictionary[query]
       
    else:
        url = urllib.parse.quote(query)
        r = requests.get("http://zip5.5432.tw/zip5json.py?adrs=" + url)
        if r.status_code == 429 :
            print(df['ID'][i+1])
            break
        if r.json()['zipcode'] != "" :
            zipcode =r.json()['zipcode'] #取出zipcode
            dictionary[query]=r.json()['zipcode']#存入 dictionary
            print(r.json()['zipcode'])
            print(len(r.json()['zipcode']))
            df.loc[i,'zipcode'] = zipcode #在DataFrame填入zipcode
            time.sleep(5)
        else:
            my_list.append(df["ID"][i]+query)
            
            
    
df.drop(columns = ['縣市','鄉鎮市區','路名'],inplace=True)
#print(df)
with open("csv_filename",mode= 'w') as file : 
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in my_list:
        writer.writerow([item])
df.to_csv("public_dataset_to.csv")