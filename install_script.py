import subprocess
import os
import urllib.request
import time

# 定義安裝路徑
INSTALL_PATH = "C:\\Python312"

# 下載 Python 安裝檔案
print("下載 Python 安裝檔案...")
python_installer_url = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
urllib.request.urlretrieve(python_installer_url, "python-3.12.1-amd64.exe")

# 安裝 Python
print("安裝 Python...")
subprocess.run(["python-3.12.1-amd64.exe", "/quiet", f"TargetDir={INSTALL_PATH}", "InstallAllUsers=1", "PrependPath=1"])
os.remove("python-3.12.1-amd64.exe")

# 設定環境變數
print("設定環境變數...")
subprocess.run(["setx", "PATH", f"%PATH%;{INSTALL_PATH};{INSTALL_PATH}\\Scripts", "/M"])

# 等待一些時間，確保 Python 安裝完成
time.sleep(10)

# 重新載入環境變數
subprocess.run(["refreshenv"])

# 安裝所需 Python 模組
print("安裝所需 Python 模組...")
subprocess.run(["pip", "install", "sqlite3", "pandas", "urllib", "requests"])

# 資料庫初始化
print("執行資料庫初始化...")
subprocess.run(["python", "database_setup.py"])

# 完成，等待用戶按下任意鍵
print("\n安裝完成！按下任意鍵以退出...")
input()
