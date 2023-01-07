from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import random
import pandas
import time

from utils import Browser
from constants import INSTAGRAM_TAG, PAGE_LOADING_TIME


class PostUrlCrawler(Browser):
    def __init__(self, crawler_path):
        super(PostUrlCrawler, self).__init__(crawler_path)

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

            time.sleep(PAGE_LOADING_TIME)

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


class PostCommentWriterCrawler(Browser):
    def __init__(self, crawler_path):
        super(PostCommentWriterCrawler, self).__init__(crawler_path)

        self.init_browser()

    def get_post_information(self, post_url):
        # Author, Post Description
        post_information = {}

        self.driver.get(post_url)

        time.sleep(PAGE_LOADING_TIME)

        post_card_element = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div")

        post_author = post_card_element.find_element(
            By.CSS_SELECTOR, "a.x1i10hfl")
        author_link = post_author.get_attribute("href")
        # author_link = f"https://www.instagram.com{temp_link}"

        post_information["author"] = author_link

        post_description = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span")
        description = post_description.text

        post_information["description"] = description

        time.sleep(0.2)

        self.like_post(post_card_element)

        return post_information

    def like_post(self, post_element):
        like_btn_container = post_element.find_element(
            By.CSS_SELECTOR, "section._aamu")
        like_btn = like_btn_container.find_element(
            By.CSS_SELECTOR, "button._abl-")
        like_btn.click()
        
        time.sleep(0.5)

    def write_comment(self, comment):
        # to_comment_page_btn = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[2]/button")
        # to_comment_page_btn.click()

        commentArea = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea")
        commentArea.click()
        commentArea = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea")
        commentArea.send_keys(comment)
        time.sleep(1)

        form_btn = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/div[2]/div")
        form_btn.click()

        print("Post My Comment!")

        time.sleep(4)

    def follow_writer(self, user_link):
        self.driver.get(user_link)

        time.sleep(PAGE_LOADING_TIME)

        follow_btn = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button")

        # If I already followed this person  we don't need to click again
        try:
            t = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div[1]").text
            print(t)
        except:
            t = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button/div/div").text
            print(t)

            if t == "팔로우":
                follow_btn.click()


if __name__ == "__main__":
    t_url = "https://www.instagram.com/p/Cm8O5v2oMA7/"

    post_write_crawler = PostCommentWriterCrawler("./chromedriver.exe")

    post_info = post_write_crawler.get_post_information(t_url)

    print(post_info)

    # time.sleep(2)

    # post_write_crawler.write_comment("It's Awesome!")

    # time.sleep(2)

    post_write_crawler.follow_writer(post_info["author"])
