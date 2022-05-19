from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

class EngineModel(object):

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--incognito')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.url = ''
        self.FILENAME = ''

    def get_info(self, args, **kwargs):
        pass

    def dispose(self):
        self.browser.close()
        self.browser.quit()
