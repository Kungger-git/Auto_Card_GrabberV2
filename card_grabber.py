from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import webdriver_conf, colorama, os, platform, time, random, countries


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


def identify_os(browser):
    return find_driver(platform.system(), browser)


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


def main(driver):
    driver.get(
        'https://cardgenerator.io/mastercard-credit-card-generator/'
    )
    try:
        countrySearch = WebDriverWait(driver, 0).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="personCountryInput"]'))
        )
        countrySearch.click()

        random_country = random.choice(countries.country_container)
        try:
            get_country = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located(
                    (By.XPATH, random_country))
            )
            print(colorama.Fore.GREEN,
                  f'\nSelected Country: {get_country.text}',
                  colorama.Style.RESET_ALL)
            get_country.click()
        finally:
                pass

        generate_card = driver.find_element_by_xpath(
            '//*[@id="masterCard_select_id"]'
        )
        generate_card.click()

        time.sleep(34)
        card_number = driver.find_element_by_xpath('//*[@id="card_number_id"]').text
        name = driver.find_element_by_xpath('//*[@id="card_name_id"]').text
        address = driver.find_element_by_xpath('//*[@id="card_address_id"]').text
        country = driver.find_element_by_xpath('//*[@id="card_country_id"]').text
        cvv = driver.find_element_by_xpath('//*[@id="card_cvv_id"]').text
        exp = driver.find_element_by_xpath('//*[@id="card_exp_id"]').text

        print(f"""
                Card Number: {card_number}

                Name: {name}

                Address: {address}

                Country: {country}

                CVV: {cvv}

                EXP: {exp}
                """)
    except WebDriverException as err:
        print(colorama.Fore.RED,
              '[!!] WebDriver Failed To Function!', err,
              colorama.Style.RESET_ALL)
    finally:
       driver.quit()


if __name__ == '__main__':
    colorama.init()
    brs = ['Chrome', 'Edge', 'Firefox']
    for i in range(len(brs)):
        print(f'{brs[i]}\n\n')

    select = str(input('Select A Browser: '))
    if select == 'q':
        quit()
    try:
        if select in brs:
            browser = webdriver_conf.get_driver(select)

            start = time.time()
            main(browser)
            end = time.time()
            print(colorama.Fore.YELLOW,
                  f'\n[*] Program took: {convert(end-start)}', colorama.Style.RESET_ALL)
        else:
            raise ValueError(colorama.Fore.RED,
                             '\n\n[!!] Bruh', colorama.Style.RESET_ALL)
    except WebDriverException as err:
        print(colorama.Fore.RED,
              f'[!!] No WebDriver Found For: {select}', err,
              colorama.Style.RESET_ALL)
    print('\n\n')
