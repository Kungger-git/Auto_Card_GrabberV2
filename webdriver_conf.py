from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from card_grabber import identify_os, convert
import time, colorama, os


def find_driver(op, brs):
    os.chdir('/')
    drivers = {
        'Edge' : 'msedgedriver',
        'Chrome' : 'chromedriver',
        'Firefox' : 'geckodriver'
    }

    #windows
    if op == 'Windows':
        for root, dirs, files in os.walk(os.getcwd()):
            if '{}.exe'.format(drivers[brs]) in files:
                return os.path.join(root, '{}.exe'.format(drivers[brs]))

    elif op == 'Darwin' or op == 'Linux':
        for root, dirs, files in os.walk(os.getcwd()):
            if drivers[brs] in files:
                return os.path.join(root, drivers[brs])


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


def get_driver_options(browser):
    driver_options = {
        'Chrome': webdriver.ChromeOptions,
        'Edge': EdgeOptions,
        'Firefox': webdriver.FirefoxOptions
    }
    return driver_options[browser]()


def get_all_options(browser, options):
    if browser == 'Edge':
        options.use_chromium = True
        options.add_argument('headless')
        options.add_argument('disable-gpu')
    elif browser == 'Chrome' or browser == 'Firefox':
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')


def get_driver(select_browser, options):
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
            executable_path=identify_os(select_browser),
            options=options
        )
    finally:
        end = time.time()
        print(colorama.Fore.YELLOW,
              f'\n[*] Driver Found in: {convert(end-start)}', colorama.Style.RESET_ALL)
