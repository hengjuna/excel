from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

from country_code import get_country_name


def get_country(driver, code,i_value, ws, row_num):
    global dest

    try:

        time.sleep(0.2)

        search_box = driver.find_element(By.ID, "txtKey")
        search_box.clear()
        time.sleep(0.5)
        search_box.send_keys(code)



        search_box.send_keys(Keys.RETURN)
        time.sleep(0.5)
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        update_time = driver.find_element(By.ID, "si_lastTime").text
        ws.cell(row=row_num, column=22).value = update_time

        if(i_value == '未知'):
            dest = driver.find_element(By.ID, "si_dest").text
            if '>' in dest:
                countryCode = dest.split('>')[1].strip()
                if ' ' in countryCode:
                    countryCode = countryCode.split(' ')[0].strip()
            elif ',' in dest:
                countryCode = dest.split(",")[1]
            else:
                countryCode = dest.split(" ")[1]
            countryName = get_country_name(countryCode)
            ws.cell(row=row_num, column=9).value = countryName
            search_box.clear()

    except Exception as e:

        print("异常 " + str(code) + ' ' + dest + ' 行   ' + str(row_num))
        ws.cell(row=row_num, column=23).value = dest
        search_box.clear()

        return "异常"
