from selenium import webdriver
from msedge.selenium_tools import Edge
from card_grabber import identify_os, convert
import time, colorama, os


def log_finder(driver_browser):
    log_files = {
        'Chrome': 'chromedriver.log',
        'Edge': 'msedgedriver.log',
        'Firefox': 'geckodriver.log'
    }
    for root, dirs, files in os.walk(os.getcwd()):
        if log_files[driver_browser] in files:
            return os.path.join(root, log_files[driver_browser])
        else:
            if not os.path.exists('logs/'):
                os.makedirs('logs/')
            with open(f'logs/{log_files[driver_browser]}', 'a') as f:
                pass


def get_driver(select_browser):
    try:
        colorama.init()
        start = time.time()
        webdriver_browsers = {
            'Chrome': webdriver.Chrome,
            'Edge': Edge,
            'Firefox': webdriver.Firefox
        }
        return webdriver_browsers[select_browser](
            service_log_path=log_finder(select_browser),
            executable_path=identify_os(select_browser)
        )
    finally:
        end = time.time()
        print(colorama.Fore.YELLOW,
              f'\n[*] Driver Found in: {convert(end-start)}', colorama.Style.RESET_ALL)
