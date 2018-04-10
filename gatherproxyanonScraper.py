#!/usr/bin/env python

import re
import time
import dryscrape
from BeautifulSoup import BeautifulSoup

URL = 'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous'
gpPageClick = [ ]

def getIPports(HTML):
    PORTS = [ ]
    COUNTER = 0
    ipCOUNTER = 0
    yport = 0

    soup = BeautifulSoup(HTML)
    IPs = soup.findAll('td', text=re.compile('[0-9]{1,3}(\.[0-9]{1,3}){3}'))
    PORTs = soup.findAll('td', text=re.compile('[0-9]{1,5}'))
    #print "PORTs: %s" % PORTs

    for port in PORTs:
        if yport == 1:
            PORTS.append(port)
        if re.search('gp.dep', port):
            yport = 1
        else: 
            yport = 0

    for ip in IPs:
        if ipCOUNTER % 2 == 1:
            print "%s:%s" % (ip, PORTS[COUNTER]) 
            COUNTER += 1
        ipCOUNTER += 1
dryscrape.start_xvfb()
session = dryscrape.Session()
session.set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
session.set_timeout('100')
session.visit(URL)

ShowFullListButton = session.at_xpath('//input[@value="Show Full List"]')
ShowFullListButton.click()
HTML = session.body()
getIPports(HTML)
soup = BeautifulSoup(HTML)
onClicks = soup.findAll('a', onclick=re.compile('gp.pageClick\([0-9]{1,2}\)'))

for clickables in onClicks:
    page = clickables.getText()
    gpPageClick.append('gp.pageClick(' + page + ');')

for pageClick in gpPageClick:
    time.sleep(26)
    NextPage = session.at_xpath('//a[@onclick="%s"]' % pageClick)
    NextPage.click()
    HTML = session.body()
    getIPports(HTML)
