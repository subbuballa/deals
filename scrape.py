# from bs4 import BeautifulSoup
from lxml import etree
import requests
from lxml import html
# import lxml
from tabulate import tabulate


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


response = requests.get('http://dealsofamerica.com')
tree = html.fromstring(response.content)
deals = tree.xpath('//*[@id="deals"]/section[@class="deal row"]')
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
