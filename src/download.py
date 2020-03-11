import csv
import json

import bs4
import lxml.html
import requests
from selenium import webdriver

SITE_URL = 'https://ngodarpan.gov.in/index.php/search/'
SEARCH_URL = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/search_index_new/0'
CONTENT_URL = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info'
CSRF_URL = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf'
CONTENT_URL_1 ='https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info'


# Get access URLs from config file
# configs = Config()
# utils = Utils()
# a_config = configs.access_config['bony']
# a_urls = a_config['access-url']
# in_p_val = '04542BHM7'

def format_html(html_str):
    """
    format html page source, BeautifulSoup makes sure formatted output source is valid for parsing
    :param html_str: html page source string
    :return: formatted html
    """
    soup = bs4.BeautifulSoup(html_str, 'html5lib')
    return soup.prettify()


def xpath_result(res, xp):
    f_html = format_html(res.text)
    tree = lxml.html.fromstring(f_html)
    return tree.xpath(xp)[0]


def page_ngos(s, tree) -> list:
    ngos_list = []
    form_data = {"id": "165260", "csrf_test_name": ""}
    for ngo in tree.xpath('//*[@id="example"]/tbody/tr'):
        # print(f'table.text :: {etree.tostring(ngo)}')
        ngo_dict = {}
        ngo_dict['sr_no'] = ''.join(ngo.xpath('td[1]/text()')).strip()
        ngo_dict['name'] = ''.join(ngo.xpath('td[2]/a/text()')).strip()
        id = ''.join(ngo.xpath('td[2]/a/@onclick')).strip().replace("show_ngo_info('", "").replace("')", "")
        ngo_dict['city'] = ''.join(ngo.xpath('td[3]/text()')).strip()
        ngo_dict['address'] = ''.join(ngo.xpath('td[4]/text()')).strip().replace('\n', '')
        ngo_dict['work_sector'] = ''.join(ngo.xpath('td[5]/text()')).strip()

        form_data['id'] = id
        gres = s.get(CSRF_URL)
        # token = json.loads(gres.text).get('csrf_token')
        form_data['csrf_test_name'] = json.loads(gres.text).get('csrf_token')
        _res = s.post(CONTENT_URL_1, data=form_data)
        print(_res.text)
    return ngos_list


def extract():
    # Session will be closed at the end of 'with' block
    with requests.Session() as s:
        # 1. Page one, pull all states
        res = s.get(SITE_URL)
        # print(f'Page Details:::: {res1.status_code}, {res1.cookies.get_dict()}, {res1.headers}, {res1.text}')
        # csrf_key = xpath_result(res, '//*[@id="csrf_test_name"]/@value')
        states = xpath_result(res, '//*[@id="state_search_search"]')
        states_dict = {state.attrib['value']: state.text.strip() for state in states}

        # 2. Page two, pull state specific ngos from all pages
        form_data = {"state_search": "0", "district_search": "", "sector_search": "null", "ngo_type_search": "null",
                     "ngo_name_search": "", "unique_id_search": "", "view_type": "detail_view", "csrf_test_name": ""}
        for num, state_name in states_dict.items():
            print(f'********{state_name}********')
            if num != '':
                state_ngos_list = []

                form_data['state_search'] = num
                gres = s.get(CSRF_URL)
                form_data['csrf_test_name'] = json.loads(gres.text).get('csrf_token')
                res1 = s.post(f'{SEARCH_URL}0', data=form_data)
                # print(f'Page Details:::: {res1.status_code}, {res1.cookies.get_dict()}, {res1.headers}, {res1.text}')
                tree = lxml.html.fromstring(format_html(res1.text))
                state_ngos = ''.join(tree.xpath('//*[@class="pagination"]/b/span/text()')).strip().split()[-1]
                print(state_ngos)
                # Add first page ngos to state ngo list
                state_ngos_list.extend(page_ngos(s, tree))
                # Add remaining pages ngos to state ngo list
                for page in range(10, int(state_ngos), 10):
                    gres = s.get(CSRF_URL)
                    form_data['csrf_test_name'] = json.loads(gres.text).get('csrf_token')
                    _res = s.post(f'{SEARCH_URL}{page}', data=form_data)
                    _tree = lxml.html.fromstring(format_html(_res.text))
                    state_ngos_list.extend(page_ngos(s, _tree))

                keys = state_ngos_list[0].keys()
                with open(f'{state_name}-{state_ngos}.csv', 'w') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(state_ngos_list)


# extract()
