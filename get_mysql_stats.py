#!/usr/bin/env python
#coding=utf-8
from __future__ import division
from optparse import OptionParser
import time
import sys
import os
import MySQLdb

# 获得客户端信息函数
def get_cli_options():
    parser = OptionParser(usage="usage: python %prog [options]", description="""This script prints MySQL TPS QPS""")

    parser.add_option("-H", "--host",
                      dest="host",
                      default="127.0.0.1",
                      metavar="HOST",
                      help="mysql host")
    parser.add_option("-P", "--port",
                      dest="port",
                      default=3306,
                      metavar="PORT",
                      help="mysql port")
    
    parser.add_option("-u", "--user",
                      dest="user",
                      default='root',
                      metavar="USER",
                      help="mysql user")

    parser.add_option("-p", "--password",
                      dest="password",
                      default='',
                      metavar="PASSWORD",
                      help="mysql password")

    parser.add_option("-I", "--interval",
                      dest="interval",
                      default=1,
                      metavar="interval",
                      help="default 1")
    (options, args) = parser.parse_args()

    return options

# 处理大小
def get_size(size, fre):
    size_tmp = size/fre

    if size_tmp >= 1073741824:
        result_size = str(round(size_tmp/1024/1024/1024,1)) + 'G'
    elif size_tmp >= 1048576 and size_tmp < 1073741824:
        result_size = str(int(size_tmp/1024/1024)) + 'M'
    elif size_tmp >= 1024 and size < 1048576:
        result_size = str(int(size_tmp/1024)) + 'k'
    else:
        result_size = str(int(size_tmp)) + 'b'

    return result_size

# 主函数
def main() :
    options = get_cli_options()
    try: 
      conn = MySQLdb.connect(host=options.host,port=int(options.port),user=options.user,passwd=options.password, charset='utf8')
    except  MySQLdb.Error,e:
      print "Error %d:%s"%(e.args[0],e.args[1])
      exit(1)
    cursor=conn.cursor()
    conn.autocommit(True)
    count=0
    mystat1={}
    mystat2={}
    sql = "show global status where Variable_name in ('Com_commit','Com_delete','Com_insert','Com_select','Com_update',\
                                                      'Innodb_buffer_pool_read_requests','Innodb_buffer_pool_reads','Threads_running',\
                                                      'Threads_connected','Threads_cached','Threads_created','Com_replace',\
						      'Innodb_deadlocks','Innodb_row_lock_current_waits','Innodb_row_lock_waits',\
						      'Open_tables','Open_files','Innodb_data_pending_fsyncs','Innodb_data_pending_reads',\
						      'Innodb_data_pending_writes','Slow_queries',\
						      'Bytes_received','Bytes_sent');"
    # 头部信息
    template = "%8s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%6s%4s%12s%8s%8s%11s%10s%10s%9s%6s%7s" 
    header   = ('time', 'sel', 'ins', 'upd', 'del', 'rpl', 'tps', 'cre', 'run', 'con', 'cac', 'hit', \
		'dlk', 'i_clk|i_tlk', 'open_ct', 'open_cf', 'i_data_pfs', 'i_data_pr', 'i_data_pw', 'slow_num', 'netIn', 'netOut')
    print template % header

    while True:
       try :
          cursor.execute(sql)
          results1 = cursor.fetchall()
          mystat1=dict(results1)
          diff =int(options.interval) 
          time.sleep(diff)
          cursor.execute(sql)
          results2 = cursor.fetchall()
          mystat2=dict(results2)

          Com_diff = int((int(mystat2['Com_commit'])  - int(mystat1['Com_commit'])) / diff)
          del_diff = int((int(mystat2['Com_delete'])  - int(mystat1['Com_delete'])) / diff)
          ins_diff = int((int(mystat2['Com_insert'])  - int(mystat1['Com_insert'])) / diff)
          sel_diff = int((int(mystat2['Com_select'])  - int(mystat1['Com_select'])) / diff)
          rep_diff = int((int(mystat2['Com_replace']) - int(mystat1['Com_replace'])) /diff)
          upd_diff = int((int(mystat2['Com_update'])  - int(mystat1['Com_update'])) / diff)
          hit_diff = float(mystat2['Innodb_buffer_pool_read_requests'])-float(mystat2['Innodb_buffer_pool_reads'])
          hit_buff = round(hit_diff/float(mystat2['Innodb_buffer_pool_read_requests'])*100,2)
          thr_run  = int(mystat2['Threads_running'])
          thr_cre  = int((int(mystat2['Threads_created'])  - int(mystat1['Threads_created'])) / diff)
          thr_cac  = int(mystat2['Threads_cached'])
          thr_con  = int(mystat2['Threads_connected'])
          qps      = sel_diff
          tps      = del_diff+ins_diff+upd_diff+rep_diff
	  dead_lk  = int(mystat2['Innodb_deadlocks'])
          inno_clk = int(mystat2['Innodb_row_lock_current_waits'])
          inno_tlk = int(mystat2['Innodb_row_lock_waits'])
	  open_ct  = int(mystat2['Open_tables'])
	  open_cf  = int(mystat2['Open_files'])
          i_data_pfs = int(mystat2['Innodb_data_pending_fsyncs'])
          i_data_pr = int(mystat2['Innodb_data_pending_reads'])
          i_data_pw = int(mystat2['Innodb_data_pending_writes'])
	  slow_num = int((int(mystat2['Slow_queries'])  - int(mystat1['Slow_queries'])) / diff)
	  netIn    = get_size((int(mystat2['Bytes_received']) - int(mystat1['Bytes_received'])), diff)
	  netOut   = get_size((int(mystat2['Bytes_sent'])   - int(mystat1['Bytes_sent'])), diff)
          dt       = time.strftime('%H:%M:%S',time.localtime(time.time())) 
	  
	  # 开始打印
          datastr  = (dt,qps,ins_diff,upd_diff,del_diff,rep_diff,tps,thr_cre,thr_run,thr_con,thr_cac,hit_buff,\
		     dead_lk,str(inno_clk) + '|' + str(inno_tlk),open_ct,open_cf,i_data_pfs,i_data_pr,i_data_pw,slow_num,netIn,netOut)

          count=count+1
          if (count % 20 == 0):
              print template % header
          
	  print template % datastr

       except KeyboardInterrupt :
          print "exit .."
          sys.exit()
  
if __name__ == '__main__':
   main()
