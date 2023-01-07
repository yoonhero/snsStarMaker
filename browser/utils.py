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
    def __init__(self, driver_path="./chromedriver.exe"):
        self.driver = webdriver.Chrome(driver_path)
        self.action = ActionChains(self.driver)

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

    def get_post_page_urls(self):
        post_urls = {"tag": [], "url": []}

        tags = ["penguin", "pingu", "cuteanimals",
                "cutepuppy", "antarctica", "antarcticaphotography"]
        # tag = random.choice(tags)

        for tag in tags:
            previous_scroll_y_offset = 0
            t_url = f"{INSTAGRAM_TAG}/{tag}"
            print(f"Target URL: {t_url}")

            self.driver.get(t_url)

            time.sleep(4)

            for _ in range(200):
                try:
                    images_grid = self.driver.find_element(By.XPATH,
                                                           "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div")

                    images = images_grid.find_elements(
                        By.CSS_SELECTOR, "a.x1i10hfl")

                    for im in images:
                        post_url = im.get_attribute("href")

                        if post_url in post_urls["url"]:
                            print("It is already existed")
                            continue

                        print(post_url)
                        post_urls["tag"].append(tag)
                        post_urls["url"].append(post_url)

                    # Scroll to target element
                    t_element = images[-1]
                    self.action.move_to_element(t_element).perform()

                    current_scroll_y_offset = self.driver.execute_script(
                        'return window.pageYOffset;')

                    if previous_scroll_y_offset == current_scroll_y_offset:
                        self.driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        continue

                    previous_scroll_y_offset = current_scroll_y_offset
                    time.sleep(0.1)

                except StaleElementReferenceException:
                    pass

        return post_urls

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    browser = Browser("../chromedriver.exe")
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
