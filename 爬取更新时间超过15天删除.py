import time

import pandas as pd
import openpyxl
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.shipxy.com/")
    return driver

def get_update_time(mmsi_value,mydriver):
    try:
        search_box = mydriver.find_element(By.ID, "txtKey")
        search_box.clear()
        search_box.send_keys(mmsi_value)

        # 查找并点击搜索按钮
        search_button = mydriver.find_element(By.ID, "searchBtn")  # 替换为实际的搜索按钮 ID
        search_button.click()
        # 等待搜索结果加载完成,根据网络调整时间
        time.sleep(1)
        update_time_element = WebDriverWait(mydriver, 10).until(
            EC.presence_of_element_located((By.ID, "si_lastTime"))  # 替换为实际的更新时间元素 ID
        )

        update_time_str = update_time_element.text
        return update_time_str
    except Exception:
        print(f"未找到更新时间元素,MMSI = {mmsi_value}")
        return None

# 读取 Excel 文件
input_file = '铁矿_全球到港_分品种_20240506.xlsx'
df = pd.read_excel(input_file)

# 初始化浏览器
mydriver = init_driver()
count_sum = 0

# 添加更新时间列
df['更新时间'] = ""

# 获取更新时间并填充到数据框中
for index, row in df.iterrows():
    mmsi_value = row['MMSI']
    update_time = get_update_time(mmsi_value,mydriver)
    if update_time:
        df.at[index, '更新时间'] = update_time
    count_sum += 1
    if(count_sum >= 10):
        mydriver.quit()
        mydriver = init_driver()
        count_sum = 0

# 计算当前时间
current_time = datetime.now()

# 删除更新时间超过15天的行
days_threshold = 15
df['更新时间'] = pd.to_datetime(df['更新时间'], errors='coerce')  # 将更新时间列转换为日期时间对象
df = df.dropna(subset=['更新时间'])  # 删除无效日期时间行
df = df[(current_time - df['更新时间']) <= timedelta(days=days_threshold)]

# 另存为新文件，避免修改原文件
output_file = input_file + '_获取更新时间超过15删除后.xlsx'
df.to_excel(output_file, index=False)

# 关闭浏览器
mydriver.quit()
