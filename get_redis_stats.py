#!/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
__author__ ='runblood'

import datetime, time, sys
from optparse import OptionParser
from urlparse import urlparse
import redis
import signal

class RedisStat:
    def __init__(self):

        # get command line input
        parser = OptionParser()
        parser.add_option("--host", dest="host", help="host to connect to")
        parser.add_option("--port", dest="port", type=int, help="port to connect to")
        (options, args) = parser.parse_args()
    
    if options.host != None and options.port != None:
            # connect redis use connection pool
        pool = redis.ConnectionPool(host=options.host, port=options.port, db=0)
        conn = redis.Redis(connection_pool=pool)
        
        # define parameters
        self.conn = conn
        
        self.setSignalHandler()

        # print redis stats
            self.printStats()

    # back current time
    def curr_time(self):
    return datetime.datetime.now().strftime("%H:%M:%S")

    # sig do
    def setSignalHandler(self):
        def handler(signal, frame):
            print "Goodbye!"
            sys.exit()

        signal.signal(signal.SIGINT, handler)

    # redis stats function
    def printStats(self):
    data = []

    #间隔1秒打印一次
        sleep = 1

    # 计数
    ii = 0

        real_used_memory = 0
        real_used_memory_rss = 0
        real_fragment = 0
        real_conn = 0
        real_blocked_conn = 0
        real_qps = 0
        real_expired_keys = 0
        real_keyspace_hits = 0
        real_keyspace_misses = 0
    real_evicted_keys = 0
    real_bgsave_time_sec = 0
        real_InNet = 0
        real_NotNet = 0

    # just run forever until ctrl-c
    while True:

        # set previous values before overwriting
            last_used_memory       = real_used_memory
            last_used_memory_rss   = real_used_memory_rss
            last_fragment          = real_fragment
            last_conn              = real_conn
            last_blocked_conn      = real_blocked_conn
            last_qps               = real_qps
            last_expired_keys      = real_expired_keys
            last_keyspace_hits     = real_keyspace_hits
            last_keyspace_misses   = real_keyspace_misses
        last_evicted_keys      = real_evicted_keys
        last_bgsave_time_sec   = real_bgsave_time_sec
            last_InNet             = real_InNet
            last_OutNet            = real_NotNet

        # fetch the redis stats
        data = self.conn.info()

            real_used_memory       = str(round(data["used_memory"]/1024/1024, 2)) + 'M'
            real_used_memory_rss   = str(round(data["used_memory_rss"]/1024/1024, 2)) + 'M' 
            real_fragment          = data["mem_fragmentation_ratio"]
            real_conn              = data["connected_clients"]
            real_blocked_conn      = data["blocked_clients"]
            real_qps               = data["total_commands_processed"]
            real_expired_keys      = data["expired_keys"]
            real_keyspace_hits     = data["keyspace_hits"]
        real_evicted_keys      = data["evicted_keys"]
            real_keyspace_misses   = data["keyspace_misses"]
            real_bgsave_time_sec   = data["rdb_last_bgsave_time_sec"]
            real_InNet             = data["total_net_input_bytes"]
            real_OutNet            = data["total_net_output_bytes"]

            # head and data
         template="%8s%9s%13s%13s%6s%13s%8s%13s%9s%16s%12s%8s%8s"
        header = ('time', 'used_mem','used_mem_rss', 'mem_fra_rate', 'conn', \
               'blocked_conn', 'comm', 'expired_keys', 'del_keys', 'key_hits|misses', 'last_bgtime', 'InNet', 'OutNet')
        data = "self.curr_time(), real_used_memory, real_used_memory_rss, real_fragment, real_conn, \
                real_blocked_conn, int((real_qps - last_qps)/sleep), real_expired_keys, str(int((real_evicted_keys - last_evicted_keys)/sleep)), \
            str(int((real_keyspace_hits - last_keyspace_hits)/sleep)) + '|' + str(int((real_keyspace_misses - last_keyspace_misses)/sleep)), \
            str(int(real_bgsave_time_sec)), \
            str(round((real_InNet - last_InNet)/sleep/1024/1024,2)) + 'M', \
            str(round((real_OutNet - last_OutNet)/sleep/1024/1024,2)) + 'M'"

            #隔20行打印标题
            if (ii % 20 == 0):
                print template % header

            #打印数据
            print template % (eval(data))

            ii += 1   

            time.sleep(sleep)
    
if __name__ == "__main__":
    RedisStat()

