from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome("./chromedriver.exe")

driver.get("https://www.instagram.com")

print(driver.title)

time.sleep(2)

driver.close()