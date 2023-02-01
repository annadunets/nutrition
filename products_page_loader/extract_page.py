import re
import config_local as config
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def load_page(product_name):
    driver = create_driver()
     # Open Sainsbury's website
    driver.get(config.WEBSITE)
    submit_search_form(driver, product_name)
    sleep(5)
    load_product_page(driver)
    sleep(5)
    nutrition_table_text = fetch_nutrition_table(driver)
    driver.quit()
    nutrition_array = text_parser(nutrition_table_text)
    return nutrition_array


def create_driver():
    # create a driver for Chrome website
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    chrome_service = Service('/usr/bin/chromedriver')
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

def submit_search_form(driver, product_name):
    # Find the search field by id
    search_input = driver.find_element(By.ID, 'term')
    # Send input text to search field
    search_input.send_keys(product_name)
    # Press enter to search input text
    search_input.send_keys(Keys.ENTER)

def load_product_page(driver):
    product_input = driver.find_element(By.CLASS_NAME, 'pt__link')
    product_input.send_keys(Keys.ENTER)


def fetch_nutrition_table(driver):
    nutrition_input = driver.find_element(By.CLASS_NAME, "nutritionTable")
    return nutrition_input.text

def text_parser(text):
    nutrition_arr = ['Fat', 'Carbohydrate', 'Protein']
    result_arr = {}
    for el in nutrition_arr:
        pattern = el + "[\s<]*([0-9.]+)"
        search = re.search(pattern, text)
        result_arr[el] = float(search.group(1))

    return result_arr







