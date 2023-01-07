from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


INSTAGRAM_HOME = "https://www.instagram.com"
INSTAGRAM_TAG = "https://www.instagram.com/explore/tags"


PAGE_LOADING_TIME = 4
