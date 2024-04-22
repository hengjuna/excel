from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

from country_code import get_country_name


def get_country(driver,code):
    global dest
    try:

        driver.get("https://www.shipxy.com/")
        time.sleep(1)

        search_box = driver.find_element(By.ID, "txtKey")
        search_box.send_keys(code)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)
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
    except Exception:
        print("异常 " + str(code) + ' ' + dest)
        return "异常"
