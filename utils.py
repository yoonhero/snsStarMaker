from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import pandas

from constants import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_HOME, INSTAGRAM_TAG

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')


class Browser():
    def __init__(self, crawler_path="./chromedriver.exe"):
        self.driver = webdriver.Chrome(crawler_path)
        self.action = ActionChains(self.driver)
    
    def init_browser(self):
        self.home()

        # Waiting For Loading Browser Contents
        time.sleep(2)

        self.login()

        time.sleep(2)

    def home(self):
        self.driver.get(INSTAGRAM_HOME)

    def login(self):
        try:
            username_input = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
            username_input.send_keys(INSTAGRAM_USERNAME)

            password_input = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
            password_input.send_keys(INSTAGRAM_PASSWORD)

            form_button = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button"
            )
            form_button.click()

            time.sleep(1)

            return True
        except:
            return False

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    browser = Browser("./chromedriver.exe")
    browser.home()

    # Waiting For Loading Browser Contents
    time.sleep(2)

    browser.login()

    time.sleep(2)

    # post_urls_dict = browser.get_post_page_urls()

    # post_url_dataframe = pandas.DataFrame(post_urls_dict)

    # print(post_url_dataframe.head())

    # print(f"Total Post Crawled: {len(post_url_dataframe)}")

    # post_url_dataframe.to_csv("post.csv")

    time.sleep(10)

    browser.quit()
