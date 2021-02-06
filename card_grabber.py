from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import webdriver_conf, colorama, insert_credentials, platform, time, random, sys


def identify_os(browser):
    os = platform.system()
    return webdriver_conf.find_driver(os, browser)


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


def main(driver):
    driver.get(
        'https://cardgenerator.io/mastercard-credit-card-generator/'
    )
    print('\nTo stop.. Just hit CTRL+C\n\n')
    while True:
        try:
            countrySearch = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="personCountryInput"]'))
            )
            countrySearch.click()

            country_container = [
                f'//*[@id="personCountryInput"]/option[{i}]' for i in range(2, 241)
            ]

            random_country = random.choice(country_container)
            try:
                country = WebDriverWait(driver, 0).until(
                    EC.presence_of_element_located(
                        (By.XPATH, random_country))
                )
                print(colorama.Fore.GREEN,
                    f'\nSelected Country: {country.text}',
                    colorama.Style.RESET_ALL)
                country.click()
            except Exception as err:
                print(colorama.Fore.RED,
                    f'[!!] There was an error in the try block: {err}',
                    colorama.Style.RESET_ALL)
            finally:
                    pass

            generate_card = driver.find_element_by_xpath(
                '//*[@id="masterCard_select_id"]'
            )
            generate_card.click()

            for rem in range(34, 0, -1):
                sys.stdout.write('\r')
                sys.stdout.write('{:2d} seconds remaining.'.format(rem))
                sys.stdout.flush()
                time.sleep(1)

            container = []
            card_number = driver.find_element_by_xpath('//*[@id="card_number_id"]').text
            name = driver.find_element_by_xpath('//*[@id="card_name_id"]').text
            address = driver.find_element_by_xpath('//*[@id="card_address_id"]').text
            country = driver.find_element_by_xpath('//*[@id="card_country_id"]').text
            cvv = driver.find_element_by_xpath('//*[@id="card_cvv_id"]').text
            exp = driver.find_element_by_xpath('//*[@id="card_exp_id"]').text
            container.extend((card_number, name, address, country, cvv, exp))

            sys.stdout.write("\rComplete!            \n")
            print(f"""
                    Card Number: {card_number}

                    Name: {name}

                    Address: {address}

                    Country: {country}

                    CVV: {cvv}

                    EXP: {exp}
                    """)
            # Inserting the collected Information to the database
            insert_credentials.insertData(insert_credentials.connect_db(), container)
        except WebDriverException as err:
            print(colorama.Fore.RED,
                '[!!] WebDriver Failed To Function!', err,
                colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    brs = ['Chrome', 'Edge', 'Firefox']
    for i in range(len(brs)):
        print(f'{brs[i]}\n\n')

    select = str(input('Select A Browser: '))
    if select == 'q':
        quit()
    try:
        # Connecting to the database
        insert_credentials.check_connection()
        if select in brs:
            options = webdriver_conf.get_driver_options(select)
            webdriver_conf.get_all_options(select, options)
            browser = webdriver_conf.get_driver(select, options)

            start = time.time()
            main(browser)
            end = time.time()
            print(colorama.Fore.YELLOW,
                  f'\n[*] Program took: {convert(end-start)}', colorama.Style.RESET_ALL)
        else:
            raise ValueError('\n\n[!!] Bruh')
    except WebDriverException as err:
        print(colorama.Fore.RED,
              f'[!!] No WebDriver Found For: {select}', err,
              colorama.Style.RESET_ALL)
    print('\n\n')
