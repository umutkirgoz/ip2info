#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jun 5, 2014
# @author Umut KIRGÖZ

import redis,time
from ip2info import IPInfo

r = redis.Redis(host = 'localhost', port = 6379, db = 8)

startTime = time.time()
ip = '194.27.203.11'
print '#'*80
print ip
print IPInfo.get(ip, r)


endTime = time.time()
print 'Process Duration : %s seconds' %(endTime-startTime)