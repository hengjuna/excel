import time
from telnetlib import EC

import pandas as pd
import openpyxl
import os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver

from country_code import get_country_name


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.shipxy.com/")
    return driver
def get_real_country(mmsi_value, mydriver):
    global  dest
    try:
        # 查找输入框并输入 MMSI 值
        search_box = mydriver.find_element(By.ID, "txtKey")
        search_box.clear()
        search_box.send_keys(mmsi_value)

        # 查找并点击搜索按钮
        search_button = mydriver.find_element(By.ID, "searchBtn")  # 替换为实际的搜索按钮 ID
        search_button.click()
        # 等待搜索结果加载完成,根据网络调整时间
        time.sleep(1)
        WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.ID, "si_dest")))

        # 获取目的地信息
        dest = mydriver.find_element(By.ID, "si_dest").text
        if '>' in dest:
            countryCode = dest.split('>')[1].strip().split(' ')[0]
        elif ',' in dest:
            countryCode = dest.split(",")[1].strip().split(' ')[0]
        else:
            countryCode = dest.split(" ")[1].strip().split(' ')[0]

        # 根据国家代码获取国家名称
        countryName = get_country_name(countryCode)
        return countryName

    except NoSuchElementException:
        print(f"未找到元素：MMSI = {mmsi_value}")
    except TimeoutException:
        print(f"页面加载超时：MMSI = {mmsi_value}")
    except Exception as e:
        print(f"发生异常：MMSI = {mmsi_value}, 错误国家code：{str(dest)}")

    # 出现异常时返回默认值
    return "异常"

# 读取 Excel 文件
input_file = '铁矿_全球到港_分品种_20240506.xlsx'
df = pd.read_excel(input_file)

# 筛选出到货国为"未知"的行
unknown_rows = df[df['到货国'] == '未知']

#初始化浏览器
mydriver = init_driver()
count_sum = 0

# 对 '未知' 行的 '到货国' 列进行替换
for index, row in unknown_rows.iterrows():
    mmsi_value = row['MMSI']
    real_country = get_real_country(mmsi_value,mydriver)
    df.at[index, '到货国'] = real_country

    # 一定次数更新浏览器
    count_sum = count_sum + 1
    if(count_sum >= 10):
        mydriver.quit()
        mydriver = init_driver()
        count_sum = 0

# 另存为新文件，避免修改原文件
output_file = input_file + '_爬取未知到货国.xlsx'
df.to_excel(output_file, index=False)
mydriver.quit()