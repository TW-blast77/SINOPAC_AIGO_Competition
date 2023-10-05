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

# 建立字典，用於儲存地址到編號的映射
city_code = {}  # 縣市編號字典
town_code = {}  # 鄉鎮市區編號字典
road_code = {}  # 路名編號字典

# 從CSV檔案讀取數據，指定編碼格式為​​UTF-8
df = pd.read_csv(DataSet, encoding='utf-8')

# 创建新的列 '編號' 并初始化为空字符串
df['編號'] = ''

# 初始化編號
current_city_code = 1
current_town_code = 1
current_road_code = 1

# 遍历数据框中的每一行
for i in range(0, len(df)):
    # 获取縣市、鄉鎮市區和路名的值
    city = df['縣市'][i]
    town = df['鄉鎮市區'][i]
    road = df['路名'][i]
    
    # 检查縣市是否在字典中，如果不在则为其分配一个唯一的編號
    if city not in city_code:
        city_code[city] = current_city_code
        current_city_code += 1
    
    # 检查鄉鎮市區是否在字典中，如果不在则为其分配一个唯一的編號
    if town not in town_code:
        town_code[town] = current_town_code
        current_town_code += 1
    
    # 检查路名是否在字典中，如果不在则为其分配一个唯一的編號
    if road not in road_code:
        road_code[road] = current_road_code
        current_road_code += 1

    # 将編號组合起来，形成一个字符串，并将其赋值给'編號'列
    combined_code = str(city_code[city]) + str(town_code[town]) + str(road_code[road])
    df.at[i, '編號'] = combined_code

# 将'編號'列添加到'縣市'、'鄉鎮市區'和'路名'列之前
df = df[['縣市', '鄉鎮市區', '路名', '編號']]

# 紀錄結束時間
end_time = datetime.datetime.now()

# 計算運行時間


# 保存CSV文件
df.to_csv(SaveName , index=False)  # index=False 表示不保存索引列
print("Save Successful!",'\n')
