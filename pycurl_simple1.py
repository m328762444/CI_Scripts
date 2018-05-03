#!/usr/bin/env python
import os, sys
import time
import pycurl
url="http://www.baidu.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, url)
c.setopt(pycurl.CONNECTTIMEOUT, 5)
c.setopt(pycurl.TIMEOUT, 5)
c.setopt(pycurl.NOPROGRESS, 1)
c.setopt(pycurl.FORBID_REUSE, 1)
c.setopt(pycurl.MAXREDIRS, 1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT,30)

indexfile = open(os.path.dirname(os.path.realpath(__file__))+"/content.txt", "wb")
c.setopt(pycurl.WRITEHEADER, indexfile)
c.setopt(pycurl.WRITEDATA, indexfile)
try:
	c.perform()
except Exception,e:
	print "connection error: " + str(e)
	indexfile.close()
	c.close()
	sys.exit()
NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)

print "HTTP STATUS: " + str(HTTP_CODE)
print "DNS time:  ms " + str(NAMELOOKUP_TIME*1000)
print "start connect time:  ms " + str(CONNECT_TIME*1000)
print "prepare tranfer time:  ms " + str(PRETRANSFER_TIME*1000)
print "start tranfer time:  ms " + str(STARTTRANSFER_TIME*1000)
print "tranfer end time:  ms " + str(TOTAL_TIME*1000)
print "data file size: byte/s " + str(SIZE_DOWNLOAD)
print "HTTP head size: byte "+ str(HEADER_SIZE)
print "average download speend:  bytes/s " + str(SPEED_DOWNLOAD)
indexfile.close()
c.close()

