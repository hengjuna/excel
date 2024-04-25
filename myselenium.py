from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

from country_code import get_country_name


def get_country(driver: object, code: object, ws: object, row_num: object) -> object:
    global dest

    try:

        time.sleep(1)

        search_box = driver.find_element(By.ID, "txtKey")
        search_box.clear()
        time.sleep(0.5)
        search_box.send_keys(code)


        time.sleep(0.5)
        search_box.send_keys(Keys.RETURN)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.5)

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

        return countryName
    except Exception as e:
        print("异常 " + str(code) + ' ' + dest)
        ws.cell(row=row_num, column=23).value = dest
        return "异常"
