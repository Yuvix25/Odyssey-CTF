import os
import json
from selenium import webdriver
from utils import random_english_digits, PASSWORDS

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1280,720")
chrome_options.add_argument("--hide-scrollbars")

def get_webdriver():
    if os.path.isfile('./chromedriver.exe'):
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    else:
        chrome_options.binary_location = GOOGLE_CHROME_PATH
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    return driver
    

print("Selenium ready.")

def capture_url(url):
    driver = get_webdriver()
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return None
    
    httpd_url = url.replace('http://', 'https://')
    if httpd_url.startswith('https://127.0.0.1') or httpd_url.startswith('https://localhost') or httpd_url.startswith('https://0.0.0.0'):
        passwords_to_7 = {lvl:PASSWORDS[lvl] for lvl in PASSWORDS if lvl <= 'level7' and len(lvl) == 6}
        domain = httpd_url.split('/')[2].split(':')[0]
        # driver.add_cookie({'name': 'passwords', 'value': json.dumps(passwords_to_7), 'domain': domain})
        # driver.get(url)
    
    path = '/captures/' + random_english_digits(10) + '.png'
    res = driver.save_screenshot('.' + path)
    driver.close()
    return path