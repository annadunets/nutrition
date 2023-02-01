import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from time import sleep


def load_page(product_name):

    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    # chrome_service = Service('/usr/lib/chromium-browser/chromedriver')
    chrome_service = Service('/usr/bin/chromedriver')


    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Opening Sainsbury's website
    driver.get("https://www.sainsburys.co.uk")

    # Finding the search field by id
    search_input = driver.find_element(By.ID, 'term')
    
    # Sending input text to search field
    search_input.send_keys(product_name)

    # Pressing enter to search input text
    search_input.send_keys(Keys.ENTER)
    sleep(5)

    product_input = driver.find_element(By.CLASS_NAME, 'pt__link')

    product_input.send_keys(Keys.ENTER)
    sleep(5)

    nutrition_input = driver.find_element(By.CLASS_NAME, "nutritionTable")
    result = text_parser(nutrition_input.text)
    driver.quit()
    return result


def text_parser(text):
    nutrition_arr = ['Fat', 'Carbohydrate', 'Protein']
    result_arr = []
    for el in nutrition_arr:
        pattern = el + "[\s<]*([0-9.]+)"
        search = re.search(pattern, text)
        result_arr.append(search.group(1))
    return result_arr







