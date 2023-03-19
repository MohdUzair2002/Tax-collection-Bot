import csv
import shutil
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver as webdr
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
import socket
import random
from datetime import datetime
import time
import logging

# PIN,Tax Sale ?,From Year - To Year (Scav Sale Only),Status ?,Status Document Number ?,Date,Comment,Tax Year,Status ?,Forfeit,Date,1st Installment Tax Balance,2nd Installment Tax Balance,Type,Warrant Year ?




SLEEP_A = 0
SLEEP_B = 0

# hey dre... Path for Edge driver:  



BAN_SLEEP_TIME = 30
dt = datetime.now()
date=dt.strftime("%d")+'-'+dt.strftime("%m")+'-'+str(dt.year)

CSV_FILE = 'PIN_scraper.csv'
#Defining the log file name
logging.basicConfig(filename="logfilename_"+date+".log", level=logging.ERROR)

# Parameters for POST request
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded'
}
URL = 'https://taxdelinquent.cookcountyclerkil.gov/'
CSV_HEADER = ['PIN', 'Tax Sale ?', 'From Year - To Year (Scav Sale Only)', 'Status1 ?',
              'Status Document Number ?', 'Date', 'Comment', 'Tax Year', 'Status2 ?', 'Forfeit Date',
              '1st Installment Tax Balance', '2nd Installment Tax Balance', 'Type', 'Warrant Year ?']

errors = (socket.error, ConnectionError)


# 1 - get input (loop thorugh csv rows)
def get_pins(csv_file):
    with open(csv_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        pins = [pin[0] for pin in csvreader]
        return pins  # -> list


# 2 - get page (token) then post data for specified pin
def get_taxes(pin):
    done = False

    while not done:
        try:
            # Get session TOKEN
            # RANDOM OwnerType
            rnd_sleep = random.randint(SLEEP_A, SLEEP_B)
            # print("BEBUG: sleepin for {0}".format(rnd_sleep))
            #time.sleep(rnd_sleep)

            browser.get(URL)

            s = requests.Session()
            a = s.get(URL)

            if a.status_code == 200:
                # print(pin, "200 ok!")
                pass

            elif a.status_code == 403:
                print('Your IP has been blocked by the website. Sleeping for {0} secs.'.format(BAN_SLEEP_TIME))
                time.sleep(BAN_SLEEP_TIME)
                continue

            #soup = BeautifulSoup(browser.page_source, 'html.parser')
            #token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')

            #data = {
            #    '__RequestVerificationToken': token,
            #    'Pin': pin
            #}

            print(pin)

            # RANDOM SLEEP
            #rnd_sleep = random.randint(SLEEP_A, SLEEP_B)
            # print("BEBUG: sleepin for {0}".format(rnd_sleep))
            #time.sleep(rnd_sleep)

            #Finding input element using xpath & clearing the data in input tab
            pin_input = browser.find_element_by_xpath("//input[@name='Pin']")
            pin_input.clear()
            #Passing the respective value
            pin_input.send_keys(pin)
            pin_input.send_keys(Keys.RETURN)

            #Using random sleep value
            #print("DEBUG: sleepin for {0}".format(rnd_sleep)
            rnd_sleep = random.randint(SLEEP_A, SLEEP_B)
            print("DEBUG: sleepin for {0}".format(rnd_sleep) )
            time.sleep(rnd_sleep)

            #Getting Current url to check the response code
            current_url = browser.current_url


            # Send POST request
            #b = s.post(URL, headers=HEADERS, data=data)
            b = s.get(current_url)

            if b.status_code == 200:
            # print(pin, "200 ok!")
                done = True

            elif b.status_code == 403:
                print('Your IP has been blocked by the website. Sleeping for {0} secs.'.format(BAN_SLEEP_TIME))
                time.sleep(BAN_SLEEP_TIME)
        except errors as e:
            print('Error {}. Sleeping for {0} secs.'.format(e, BAN_SLEEP_TIME))
            logging.exception('Error {}. Sleeping for {0} secs.'.format(e, BAN_SLEEP_TIME))
            time.sleep(BAN_SLEEP_TIME)

        #browser element is parsed and returned in order to scrap data
        b = browser.page_source
    return b  # -> html response


# 3 - html parse response
def loop_td_rows(table, td_index, fix=False):
    # Func to extract data from table, fix toggle for unclosed html tag
    data = []
    tr = table.find_all('tr')
    for row in tr:
        if fix:
            data.append(row.find_all('td')[td_index].text.strip().split('\n')[0])
        else:
            data.append(row.find_all('td')[td_index].text.strip())
    return data


def l_to_csv(l):
    # list concat func
    return ';'.join(l)


def parse_data(response):
    #tax_soup = BeautifulSoup(response.content, 'html.parser')
    tax_soup = BeautifulSoup(response, 'html.parser')
    # check taxes
    no_taxes = tax_soup.find('div', {'class': 'validation-summary-errors text-danger'})
    if no_taxes is not None:
        message = no_taxes.ul.li.text
        dict_data = {
            'PIN': pin,
            'Tax Sale ?': message,
            'From Year - To Year (Scav Sale Only)': '',
            'Status1 ?': '',
            'Status Document Number ?': '',
            'Date': '',
            'Comment': '',
            'Tax Year': '',
            'Status2 ?': '',
            'Forfeit Date': '',
            '1st Installment Tax Balance': '',
            '2nd Installment Tax Balance': '',
            'Type': '',
            'Warrant Year ?': ''
        }
    else:
        try:
            first_table = \
            tax_soup.find_all('table', {'class': 'table-filter table table-condensed table-hover table-striped'})[
                0].tbody
            """FIRST TABLE"""
            tax_sale = loop_td_rows(first_table, 0)
            from_y_to_y = loop_td_rows(first_table, 1)
            status1 = loop_td_rows(first_table, 2)
            status_doc = loop_td_rows(first_table, 3)
            date = loop_td_rows(first_table, 4)
            comment = loop_td_rows(first_table, 5)

            try:
                second_table = \
                tax_soup.find_all('table', {'class': 'table-filter table table-condensed table-hover table-striped'})[
                    1].tbody
                """SECOND TABLE"""
                tax_t = loop_td_rows(second_table, 0)
                status2 = loop_td_rows(second_table, 1)
                forfeit_date = loop_td_rows(second_table, 2)
                first_inst = loop_td_rows(second_table, 3, fix=True)  # the html had an error, closing td missing.
                second_inst = loop_td_rows(second_table, 4)
                backtax = loop_td_rows(second_table, 5)
                warrant_y = loop_td_rows(second_table, 6)
            except IndexError:
                tax_t = ''
                status2 = ''
                forfeit_date = ''
                first_inst = ''
                second_inst = ''
                backtax = ''
                warrant_y = ''

            # build dict of structured data (bs4)
            dict_data = {
                'PIN': pin,
                'Tax Sale ?': l_to_csv(tax_sale),
                'From Year - To Year (Scav Sale Only)': l_to_csv(from_y_to_y),
                'Status1 ?': l_to_csv(status1),
                'Status Document Number ?': l_to_csv(status_doc),
                'Date': l_to_csv(date),
                'Comment': l_to_csv(comment),
                'Tax Year': l_to_csv(tax_t),
                'Status2 ?': l_to_csv(status2),
                'Forfeit Date': l_to_csv(forfeit_date),
                '1st Installment Tax Balance': l_to_csv(first_inst),
                '2nd Installment Tax Balance': l_to_csv(second_inst),
                'Type': l_to_csv(backtax),
                'Warrant Year ?': l_to_csv(warrant_y)
            }
        except Exception as error:
            dict_data = {
                'PIN': pin,
                'Tax Sale ?': error,
                'From Year - To Year (Scav Sale Only)': '',
                'Status1 ?': '',
                'Status Document Number ?': '',
                'Date': '',
                'Comment': '',
                'Tax Year': '',
                'Status2 ?': '',
                'Forfeit Date': '',
                '1st Installment Tax Balance': '',
                '2nd Installment Tax Balance': '',
                'Type': '',
                'Warrant Year ?': ''
            }
    return dict_data


# 5 - dump to csv (append)
def dump_to_csv(csv_file, d_data):
    fieldnames = CSV_HEADER
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(csv_file, 'r', newline='') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, lineterminator='\n', delimiter=',')
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames, lineterminator='\n', delimiter=',')
        for row in reader:
            if row['PIN'] == d_data['PIN']:
                row = d_data
            writer.writerow(row)
    shutil.move(tempfile.name, csv_file)


if __name__ == "__main__":
    """TESTING"""
    # pin = '25-08-201-032-0000'
    # for i in range(10000):
    #     taxes_response = get_taxes(pin)
    #     print(taxes_response.status_code)
    #     taxes_data = parse_data(taxes_response)
    #     print(taxes_data['Tax Sale ?'])

    """PRODUCTION"""

# hey dre... Path for Edge driver:  c:\program files\python37\

    pins = get_pins(CSV_FILE)
    print(pins)
    terminate = 0
    try:
        browser = webdr.Chrome()
    except Exception as arguments:
        print("Error in loading Chrome Webdriver\nCheck the log file")
        logging.exception("Failed to open chrome")
        terminate = 1
    if terminate == 0:
        for pin in pins:
            # time.sleep(3)
            if pin == 'PIN':
                pass
            else:
                print("{0}, {1}".format(pin, pins.index(pin) + 1))
                taxes_response = get_taxes(pin)
                taxes_data = parse_data(taxes_response)
                dump_to_csv(CSV_FILE, taxes_data)
        browser.close()
    print("Completed...")