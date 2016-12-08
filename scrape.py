from lxml import etree
import requests
from lxml import html
from tabulate import tabulate
import re
import json


def init():
    global _dealtable
    global _deals
    _dealtable = []
    _deals = []
    extract_deal_details_json()
    # get_tabular_data()


def extractdetailsfrom(deal, xpathdef):
    innertree = html.fromstring(etree.tostring(deal))
    result = innertree.xpath(xpathdef)
    if not result:
        return ''
    return result[0]


def extract_urls(start_url):
    request_endpoints = [start_url]
    response = requests.get(start_url)
    tree = html.fromstring(response.content)
    request_other = tree.xpath('//*[@id="deals-container"]/footer/ul/li/a/@href')
    request_endpoints.extend(request_other)
    formatted_requests = [re.sub(r'^\/\/',r'http://',x) for x in request_endpoints]
    return formatted_requests


def extract_deals(formatted_requests):
    global _deals
    for r in formatted_requests:
        res = requests.get(r)
        tree = html.fromstring(res.content)
        _deals.extend(tree.xpath('//*[@id="deals"]/section[@class="deal row"]'))


def extract_deal_details():
    global _dealtable
    global _deals
    urls = extract_urls('http://dealsofamerica.com')
    extract_deals(urls)
    for deal in _deals:
        dealrow = []
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                        'header/a/text()'))
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/text()'))
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/a/text()'))
        _dealtable.append(dealrow)

def extract_deal_details_json():
    global _dealtable
    global _deals
    urls = extract_urls('http://dealsofamerica.com')
    extract_deals(urls)
    for deal in _deals:
        dealrow = []
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                        'header/a/text()'))
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/text()'))
        dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/a/text()'))
        _dealtable.append(dealrow)


def get_tabular_data():
    global _dealtable
    print tabulate(_dealtable, headers=['description', 'price', 'company'])


def get_json_data():
    init()
    return json.dumps(_dealtable)

if __name__ == '__main__':
    init()
