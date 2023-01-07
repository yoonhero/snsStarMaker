import pandas as pd
from crawler import PostCommentWriterCrawler
import random
import time

post_urls = pd.read_csv("./post.csv")
# print(post_urls.head())

post_write_crawler = PostCommentWriterCrawler("./chromedriver.exe")

for idx in range(len(post_urls)):
    row = post_urls.iloc[idx]
    t_url = row.url
    post_info = post_write_crawler.get_post_information(t_url)

    # time.sleep(2)

    # post_write_crawler.write_comment("It's awesome! Coolll.")

    # time.sleep(2)

    post_write_crawler.follow_writer(post_info["author"])
