import os
import time
from selenium import webdriver
from utils import random_english_digits

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
    if url.startswith('https://127.'):
        time.sleep(0.7) # just so that it won't seem too fast
        return None
    
    driver = get_webdriver()
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return None
    
    path = '/captures/' + random_english_digits(10) + '.png'
    driver.save_screenshot('.' + path)
    driver.close()
    return path