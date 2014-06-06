#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jun 5, 2014
# @author Umut KIRGÖZ

import redis,time
from iprange import IPRange

r = redis.Redis(host = 'localhost', port = 6379, db = 8)

startTime = time.time()
ip = '212.101.96.1'
print '#'*80
print ip
print IPRange.get(ip, r)


endTime = time.time()
print 'Process Duration : %s seconds' %(endTime-startTime)