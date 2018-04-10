#!/usr/bin/env python

import re
import time
import dryscrape
import sys
from BeautifulSoup import BeautifulSoup
from webkit_server import InvalidResponseError

URLprefix = 'http://www.cool-proxy.net/proxies/http_proxy_list/page:'
URLpostfix = '/sort:score/direction:desc'
pages = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14' ]
PORTS = [ ]
yport = 0
dryscrape.start_xvfb()
session = dryscrape.Session()
session.set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
session.set_timeout('100')

for page in pages:
    URL = URLprefix + page + URLpostfix

    try:        
        session.visit(URL)
    except InvalidResponseError:
        print >> sys.stderr, 'page timeout... going to next page'
        
    HTML=session.body()
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
    COUNTER = 0
    for IP in IPs:
        print "%s:%s" % (IP, PORTS[COUNTER])
        COUNTER += 1
    del PORTS[0:]
    time.sleep(40)
