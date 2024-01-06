# 下載此Project 
請在**git bash** 中執行，下載此專案。
## Step 1 :切換至指定專案目錄
```bash
cd **在此填入您的目錄位置**
```
```git
git clone https://github.com/TW-blast77/SINOPAC_AIGO_Competition.git
```
# **SINOPAC_AIGO_Competition**
此項目旨在存放和處理CSV資料集，包含以下目錄和功能：

- **CSV_DataSet**：存放測試資料集的目錄。

- **CSV_to_Number**：包含將CSV檔案中的鄉鎮縣市名稱轉換為數字編碼的程式碼。

- **CSV_to_Zipcode**：包含將CSV檔案中的鄉鎮縣市名稱轉換為郵遞區號的程式碼。

- **Save_CSV**：用於存放輸出的.CSV檔案的目錄。

- **Test**：包含專案的測試程序和歷史資料。
# !! 環境設置 !! (請先執行環境測試檔案)
請在cmd包中執行，安裝python基本環境以及python模組。
```bash
python install_script.py
```
# 用法
### **1. 在 _*CSV_DataSet*_ 目錄中存放測試資料集。**
### **2. 使用 *CSV_to_Number* 目錄中的程式碼將CSV檔案中的鄉鎮縣市名稱轉換為數位編碼。**
### **3. 使用 *CSV_to_Zipcode* 目錄中的程式碼將CSV檔案中的鄉鎮縣市名稱轉換為郵遞區號。**
### **4. 輸出的CSV檔案將會保存在 *Save_CSV* 目錄中。**

# 程式範例
以下是如何使用該項目的範例：

## Step 1 將CSV檔案中的鄉鎮縣市名稱轉換為郵遞區號
```bash
python CSV_to_Zipcode/convert_to_zipcode.py
```
## Step 2將CSV檔案中的鄉鎮縣市名稱轉換為數位編碼
```bash
python CSV_to_Number/convert_to_number.py
```
# HTML不動產資料

## Step 3開啟HTML資料夾中的 Property_HTML
```bash
Property_HTML.html
```
# 版本歷史

- **1.0.0** (Taiwan UTC +8 China Standard Time，2023-10-05 06:59 AM)：首次發布。
- **1.1.0** (Taiwan UTC +8 China Standard Time，2023-10-05 06:48 AM)：二次發布。
- **1.2.0** (Taiwan UTC +8 China Standard Time，2024-01-02 10:23 AM)：三次發布。
- **1.3.0** (Taiwan UTC +8 China Standard Time，2024-01-03 02:01 PM)：四次發布。
- **1.4.0** (Taiwan UTC +8 China Standard Time，2024-01-05 05:05 PM)：五次發布。
- **1.4.1** (Taiwan UTC +8 China Standard Time，2024-01-06 06:00 PM)：六次發布。
# 作者
作者：[Blast77]
