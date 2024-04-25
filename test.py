import openpyxl
import os

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

import daogang
import myselenium

# Load the Excel file


file_path = '/Users/minggong/PycharmProjects/pythonProject/铁矿_全球海漂_分品种_20240422.xlsx'

if "到港" in os.path.basename(file_path):
    daogang.daogang(file_path)
if "海漂" not in os.path.basename(file_path):
    pass
else:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.shipxy.com/")

    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    # Create a new Excel file to save the modified rows
    new_file_path = file_path + "_modified.xlsx"
    # 创建新的工作簿作为模板的副本
    new_wb = openpyxl.Workbook()
    new_ws = new_wb.active



    # Iterate over rows
    for row_num in range(2, ws.max_row + 1):
        # Get values from columns H and M
        i_value = ws.cell(row=row_num, column=9).value
        p_value = ws.cell(row=row_num, column=16).value

        # Check if values are the same
        if i_value == p_value:
            # Delete the row
            ws.delete_rows(row_num, 1)
        else:
            # Check if the I column value is unknown
            if i_value == '未知':
                # Get the A column value
                a_value = ws.cell(row=row_num, column=1).value

                country = myselenium.get_country(driver,a_value,ws,row_num);
                print(country),
                # Get the ship information fromship_info = response.json()

                # Update the I and M columns with the ship information

                ws.cell(row=row_num, column=9).value = country
                # 将整行数据追加到新工作表中
                new_row_values = [cell.value for cell in ws[row_num]]
                new_ws.append(new_row_values)
    # Save the changes to the original file
    wb.save(file_path + "_update.xlsx")

    new_wb.save(new_file_path)
    driver.quit()
