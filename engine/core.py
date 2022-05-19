from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class EngineModel(object):

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        self.browser = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=options)
        self.url = ''
        self.FILENAME = ''

    def get_info(self, args, **kwargs):
        pass

    def dispose(self):
        self.browser.close()
        self.browser.quit()
