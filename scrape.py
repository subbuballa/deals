# from bs4 import BeautifulSoup
from lxml import etree
import requests
from lxml import html
# import lxml
from tabulate import tabulate
import re


def extractdetailsfrom(deal, xpathdef):
    innertree = html.fromstring(etree.tostring(deal))
    result = innertree.xpath(xpathdef)
    if not result:
        return ''
    # print type(result[0]) is lxml.html.HtmlElement
    # print type(result[1]) is lxml.html.HtmlElement
    # print etree.tostring(result[0])
    return result[0]
    # return BeautifulSoup(etree.tostring(result)).prettify()


request_endpoints = ['http://dealsofamerica.com']
response = requests.get('http://dealsofamerica.com')
tree = html.fromstring(response.content)
request_other = tree.xpath('//*[@id="deals-container"]/footer/ul/li/a/@href')
request_endpoints.extend(request_other)
# print request_endpoints
formatted_requests = [re.sub(r'^\/\/',r'http://',x) for x in request_endpoints]
deals=[]
for r in formatted_requests:
    res = requests.get(r)
    tree = html.fromstring(res.content)
    deals.extend(tree.xpath('//*[@id="deals"]/section[@class="deal row"]'))
# print deals
# print len(deals)
dealtable = []
for deal in deals:
    dealrow = []
    dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/a/text()'))
    dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/text()'))
    dealrow.append(extractdetailsfrom(deal, '//*[@class="deal row"]/section/'
                                      'header/span/a/text()'))
    dealtable.append(dealrow)
print tabulate(dealtable, headers=['description', 'price', 'company'])
