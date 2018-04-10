#!/usr/bin/env python

import re
import time
import dryscrape
from BeautifulSoup import BeautifulSoup

URL = 'http://free-proxy-list.net/anonymous-proxy.html'
PORTS = [ ]

def getIPports(HTML):
    yport = 0
    COUNTER = 0

    soup = BeautifulSoup(HTML)
    
    IPs = soup.findAll('td', text=re.compile('[0-9]{1,3}(\.[0-9]{1,3}){3}'))
    PORTs = soup.findAll('td', text=re.compile('[0-9]{1,5}'))
    
    for port in PORTs:
        if yport == 1:
            PORTS.append(port) 
        if re.search('[0-9]{1,3}(\.[0-9]{1,3}){3}', port):
            yport = 1
        else:
            yport = 0

    for ip in IPs:
        print "%s:%s" % (ip, PORTS[COUNTER])
        COUNTER += 1

    del PORTS[0:]
dryscrape.start_xvfb()
session = dryscrape.Session()
session.set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
session.set_timeout('100')
session.visit(URL)
HTML = session.body()
getIPports(HTML)
time.sleep(5)

for x in range(4):  
    NextButton = session.at_xpath('//a[@id="proxylisttable_next"]')
    NextButton.click()
    HTML = session.body()
    getIPports(HTML)
    time.sleep(5)
