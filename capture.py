import os
import json
from selenium import webdriver
from utils import random_english_digits, PASSWORDS

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1280,720")
chrome_options.add_argument("--hide-scrollbars")

if os.path.exists(GOOGLE_CHROME_PATH):
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
else:
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

print("Selenium ready.")

def capture_url(url):
    driver.get(url)
    
    httpd_url = url.replace('http://', 'https://')
    if httpd_url.startswith('https://127.0.0.1') or httpd_url.startswith('https://localhost'):
        driver.add_cookie({'name': 'passwords', 'value': json.dumps(PASSWORDS)})
        driver.get(url)
    
    path = '/captures/' + random_english_digits(10) + '.png'
    res = driver.save_screenshot('.' + path)
    return path