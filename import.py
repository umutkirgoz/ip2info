#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jun 5, 2014
# @author Umut KIRGÖZ

import redis
from iprange import IPRange

r = redis.Redis(host = 'localhost', port = 6379, db = 8)

r.flushdb()

pipe = r.pipeline()

filename = 'ripe.csv'
counter = 0
for line in open(filename):
    x = line.strip().split('|')
    
    rangeMin = x[0]
    rangeMax = x[1]
    rangeDesc = x[2]
    rangeCountry = x[3]
    
    if rangeMin.count('.') != 3 or rangeMax.count('.') != 3:
        print "Cannot Import: %s" %(line)
        continue
    
    print "%s--%s--%s---%s" %(rangeMin,rangeMax,rangeDesc,rangeCountry)
    range = IPRange(rangeMin,rangeMax,rangeDesc,rangeCountry)
    range.save(pipe)
    
    counter += 1
    if counter % 1000 == 0:
        pipe.execute()
        
    #if counter == 1000:
        #exit()
    
    
    

