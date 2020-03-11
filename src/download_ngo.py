import contextlib
import csv

import bs4
import lxml.html
import selenium.webdriver as webdriver

# from lxml import etree

CROME_DRIVER_PATH = 'C:/Users/DattatrayaTembare/chromedriver_win32/chromedriver.exe'

HOME_URL = 'https://ngodarpan.gov.in/index.php/home'
PAGE_URL = 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/6161/7/'
PER_PAGE = '?per_page=100'


def page_ngos(tree, xp) -> list:
    ngos_list = []
    for ngo in tree.xpath(xp):
        # print(f'table.text :: {etree.tostring(ngo)}')
        ngo_dict = {}
        ngo_dict['sr_no'] = ''.join(ngo.xpath('td[1]/text()')).strip()
        ngo_dict['name'] = ''.join(ngo.xpath('td[2]/a/text()')).strip()
        ngo_dict['id'] = ''.join(ngo.xpath('td[2]/a/@onclick')).strip()
        ngo_dict['city'] = ''.join(ngo.xpath('td[3]/text()')).strip()
        ngo_dict['address'] = ''.join(ngo.xpath('td[4]/text()')).strip().replace('\n', '')
        ngo_dict['work_sector'] = ''.join(ngo.xpath('td[5]/text()')).strip()
        ngos_list.append(ngo_dict)
    return ngos_list


def ngo_contact(tree, xp) -> dict:
    return {''.join(d.xpath('td[1]/text()')).strip(): ''.join(d.xpath('td[2]/text()')).strip() for d in tree.xpath(xp)}


def format_html(html_str):
    """
    format html page source, BeautifulSoup makes sure formatted output source is valid for parsing
    :param html_str: html page source string
    :return: formatted html
    """
    soup = bs4.BeautifulSoup(html_str, 'html5lib')
    return soup.prettify()


def write_info(ngo_list):
    keys = ngo_list[0].keys()
    with open('Delhi-NGOs.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ngo_list)
    print('Download successful!')


def execute():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    with contextlib.closing(webdriver.Chrome(CROME_DRIVER_PATH, options=options)) as driver:
        ngo_info = []
        for page in range(1, 63):
            print(f'Fetching page:  {page}')
            page_url = f'{PAGE_URL}{page}{PER_PAGE}'

            driver.get(page_url)
            f_html = format_html(driver.page_source)
            tree = lxml.html.fromstring(f_html)
            ngos_list = page_ngos(tree, '//*[@class="ibox-content"]/table/tbody/tr')

            for ngo in ngos_list:
                driver.execute_script(ngo.get('id'))  # 'show_ngo_info("165260");'
                driver.maximize_window()  # For maximizing window
                driver.implicitly_wait(30)  # gives an implicit wait for 30 seconds
                # print(driver.page_source)
                f_ngo = format_html(driver.page_source)
                ngo_tree = lxml.html.fromstring(f_ngo)
                contact = ngo_contact(ngo_tree, '//*[@id="printThis"]/div/div/table[8]/tbody/tr')
                ngo_details = {**ngo, **contact}
                ngo_info.append(ngo_details)
    # Write data to file
    write_info(ngo_info)


if __name__ == '__main__':
    execute()
