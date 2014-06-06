#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jun 5, 2014
# @author Umut KIRGÖZ

import socket,struct

class IPRange(object):
    _indexPrefix = 'iprange-indexes'
    _infoPrefix = 'iprange-info'
    _hitKey = 'iprange-hits'
    
    def __init__(self,rangeMin,rangeMax,rangeDesc,rangeCountry):
        self.rangeMin = rangeMin
        self.rangeMinNum = self.ip2long(rangeMin)
        self.rangeMax = rangeMax
        self.rangeMaxNum = self.ip2long(rangeMax)
        self.rangeDesc = rangeDesc
        self.rangeCountry = rangeCountry
        
        self.key = "%s-%s" %(self.rangeMinNum,self.rangeMaxNum)
        
    def __str__(self):
        """
        textual representation
        """
        return "IPRange: %s" % self.__dict__
    
    def save(self,redisConn):
        """
        Save an IP range to redis
        @param redisConn a redis connectino or pipeline
        """        
        redisConn.zadd(self._indexPrefix, self.key, self.rangeMaxNum)
        
        key = "%s-%s" %(self._infoPrefix,self.key)
        redisConn.hmset(key,{'rangeMin':self.rangeMin,'rangeMax':self.rangeMax,'rangeDesc':self.rangeDesc,'rangeCountry':self.rangeCountry})
        
    @staticmethod
    def get(ip, redisConn):
        """
        Get a range and all its data by ip
        """
        
        ipnum = IPRange.ip2long(ip)

        #get the location record from redis
        record = redisConn.zrangebyscore(IPRange._indexPrefix, ipnum ,'+inf', 0, 1, True)
        
        if not record:
            #not found? k! 
            rangeKey = 'not_found'           
            result = None
        else:
            try:   
                rangeKey = record[0][0]          
                key = "%s-%s" %(IPRange._infoPrefix,rangeKey)
                
                (rngMin,rngMax) = record[0][0].split('-')
                rngMin = int(rngMin)
                rngMax = int(rngMax)
                
                #address not in any range
                if not rngMin <= ipnum <= rngMax:            
                    rangeKey = 'not_in_any_range'
                    result = None
                else:            
                    result = redisConn.hgetall(key)
            except IndexError:
                rangeKey = 'unknown'
                result = None
        
        IPRange.hit(rangeKey,redisConn)
        
        return result
    
    @staticmethod   
    def hit(key,redisConn):
        return redisConn.hincrby(IPRange._hitKey,key,1)
        
    
    @staticmethod
    def ip2long(ip):
        """
        Convert an IP string to long
        """
        ip_packed = socket.inet_aton(ip)
        return struct.unpack("!L", ip_packed)[0]
        
        