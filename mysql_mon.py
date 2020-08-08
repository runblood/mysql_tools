#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import sys
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out
################################################################################################################

"""
使用范围：查询数据库监控性能信息
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql监控类
class Cls_Mysql_Mon:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().mon()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        self.__num = 1

        ### 获取源端mysql信息
        self.__source = str(self.usage["source"]).split(',')

    ### 打印输出
    def __printInnodbStatus(self, regexp, line, p_k=None, num=1, p_type=None, format=False, title=None, title_num=False):
        m = self.util.match(regexp, line)
        if m:
            ### 添加行
            if title:
                if title_num:
                    self.out.add_row(["", title+ " "+ m.group(1)])
                else:
                    self.out.add_row([title, ""])
            else:
                size = m.group(num)
                if format:
                    size = self.util.sizeFormat(int(m.group(num)))

                if p_type:
                    self.out.add_row(["", str(p_k) + " ["+size+"] " + p_type])
                else:
                    self.out.add_row(["", str(p_k) + " ["+size+"]"])

    ### innodb监控状态
    def __collectInnodbStatus(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["Title", "Content"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4])
            innodb_status = self.__source_mysql_db.query("SHOW ENGINE INNODB STATUS")
            ### 连接异常判断 
            if innodb_status["code"] == 1:
                self.logging.loggingError(innodb_status["content"])

                ### 退出
                self.util.sys_exit()

            ### 进入主逻辑
            for line in innodb_status["content"][0]["Status"].split("\n"):
                # SEMAPHORES
                self.__printInnodbStatus("SEMAPHORES", line, title="SEMAPHORES['信号量']")
                self.__printInnodbStatus("OS WAIT ARRAY INFO: reservation count (\d+)", line, \
                    "innodb.oswait_array.reservation_count[全局等待数组信息(当数据组创建后预留的计数)]")
                self.__printInnodbStatus("OS WAIT ARRAY INFO: signal count (\d+)", line, \
                    "innodb.oswait_array.signal_count[收到的通知次数]")
                self.__printInnodbStatus("RW-shared spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.spin_waits", p_type=" type=rw-shared")
                self.__printInnodbStatus("RW-shared spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.round", 2, " type=rw-shared")
                self.__printInnodbStatus("RW-shared spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.os_waits", 3, " type=rw-shared")
                self.__printInnodbStatus("RW-excl spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.spin_waits", p_type=" type=rw-exclusive")
                self.__printInnodbStatus("RW-excl spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.rounds", 2, " type=rw-exclusive")
                self.__printInnodbStatus("RW-excl spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.os_waits", 3, " type=rw-exclusive")
                self.__printInnodbStatus("RW-sx spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.spin_waits", p_type=" type=mutex")
                self.__printInnodbStatus("RW-sx spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.rounds", 2, " type=mutex")
                self.__printInnodbStatus("RW-sx spins (\d+), rounds (\d+), OS waits (\d+)", line, \
                    "innodb.locks.os_waits", 3, " type=mutex")

                self.__printInnodbStatus("TRANSACTION", line, title="TRANSACTION['事务']")
                self.__printInnodbStatus("History list length (\d+)", line, \
                    "innodb.history_list_length[回滚段未清理的事务数]")

                self.__printInnodbStatus("INSERT BUFFER AND ADAPTIVE HASH INDEX", line, \
                    title="INSERT BUFFER AND ADAPTIVE HASH INDEX['自适应HASH索引']")
                self.__printInnodbStatus("Ibuf: size (\d+), free list len (\d+), seg size (\d+), (\d+) merges", line, \
                    "innodb.ibuf.size")
                self.__printInnodbStatus("Ibuf: size (\d+), free list len (\d+), seg size (\d+), (\d+) merges", line, \
                    "innodb.ibuf.free_list_len", 2)
                self.__printInnodbStatus("Ibuf: size (\d+), free list len (\d+), seg size (\d+), (\d+) merges", line, \
                    "innodb.ibuf.seg_size", 3)
                self.__printInnodbStatus("Ibuf: size (\d+), free list len (\d+), seg size (\d+), (\d+) merges", line, \
                    "innodb.ibuf.merges", 4)
                self.__printInnodbStatus("insert (\d+), delete mark (\d+), delete (\d+)", line, \
                    "innodb.ibuf.inserts")
                self.__printInnodbStatus("insert (\d+), delete mark (\d+), delete (\d+)", line, \
                    "innodb.ibuf.delete_mark", 2)
                self.__printInnodbStatus("insert (\d+), delete mark (\d+), delete (\d+)", line, \
                    "innodb.ibuf.delete", 3)

                self.__printInnodbStatus("LOG", line, title="LOG['日志']")
                self.__printInnodbStatus("Log sequence number (\d+)", line, \
                    "Log sequence number[系统最大的LSN号]")
                self.__printInnodbStatus("Log flushed up to   (\d+)", line, \
                    "Log flushed up to[当前已经写入redo日志文件的LSN]")
                self.__printInnodbStatus("Pages flushed up to (\d+)", line, \
                    "Pages flushed up to[已经将更改写入脏页的lsn号]")
                self.__printInnodbStatus("Last checkpoint at  (\d+)", line, \
                    "Last checkpoint at[checkpoint位置]")

                self.__printInnodbStatus("BUFFER POOL AND MEMORY", line, title="BUFFER POOL AND MEMORY['BUFFER POOL']")
                self.__printInnodbStatus("Total large memory allocated (\d+)", line, \
                    "Total large memory allocated[分配内存总字节数]", format=True)
                self.__printInnodbStatus("Dictionary memory allocated (\d+)", line, \
                    "Dictionary memory allocated[数据字典占用的字节数]", format=True)
                self.__printInnodbStatus("Buffer pool size   (\d+)", line, \
                    "Buffer pool size[缓存池中总页数]")
                self.__printInnodbStatus("Free buffers       (\d+)", line, \
                    "Free buffers[缓存池剩余总页数]")
                self.__printInnodbStatus("Database pages     (\d+)", line, \
                    "Database pages[缓冲池LRU链条总页数]")
                self.__printInnodbStatus("Old database pages (\d+)", line, \
                    "Old database pages[缓冲池LRU链条中的冷链条总页数]")
                self.__printInnodbStatus("Modified db pages  (\d+)", line, \
                    "Modified db pages[脏链条总页数]")
                self.__printInnodbStatus("Pending reads      (\d+)", line, \
                    "Pending reads[在检查点期间要刷新的缓冲池页数]")

                self.__printInnodbStatus("---BUFFER POOL (\d+)", line, title="------[实例]BUFFER POOL", title_num=True)

                self.__printInnodbStatus("ROW OPERATIONS", line, title="ROW OPERATIONS['行操作']")
                self.__printInnodbStatus("\d+ queries inside InnoDB, (\d+) queries in queue", line, \
                    "innodb.queries_queued")
                self.__printInnodbStatus("(\d+) read views open inside InnoDB", line, \
                    "innodb.opened_read_views")
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))
        finally:
            ### 输出
            self.out.print()

    ### global状态
    def __collectGlobalStatus(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["time", "qps", "ins", "upd", "del", "rep", "tps", "thr_run", "thr_con", "thr_cac", \
                "hit_buf", "lock_c|t", "o_table|file", "p_fsyncs|reads|writes", "netIn", "netOut"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4])

            ### sqltext
            sqltext = "show global status where Variable_name in ('Com_commit','Com_delete','Com_insert',\
                'Com_select','Com_update','Innodb_buffer_pool_read_requests','Innodb_buffer_pool_reads',\
                'Threads_running','Threads_connected','Threads_cached','Threads_created',\
                'Com_replace','Innodb_row_lock_current_waits','Innodb_row_lock_waits',\
                'Open_tables','Open_files','Innodb_data_pending_fsyncs','Innodb_data_pending_reads',\
                'Innodb_data_pending_writes','Slow_queries','Bytes_received','Bytes_sent')"
            ### 初次赋值
            last_global_status = self.__source_mysql_db.query(sqltext)["content"]

            ### 循环输出
            while True:
                ### 睡眠
                self.util.sleep(1)

                ### 上次值获取
                last_global_status_rt = self.util.merge_list_to_dict(self.util.get_single_columnv("Variable_name", last_global_status), \
                    self.util.get_single_columnv("Value", last_global_status))

                ### 再次获取
                now_global_status = self.__source_mysql_db.query(sqltext)["content"]
                now_global_status_rt = self.util.merge_list_to_dict(self.util.get_single_columnv("Variable_name", now_global_status), \
                    self.util.get_single_columnv("Value", now_global_status))
                
                ### 进入主逻辑
                time = self.util.time()
                qps = int(now_global_status_rt["Com_select"]) - int(last_global_status_rt["Com_select"])
                ins = int(now_global_status_rt["Com_insert"]) - int(last_global_status_rt["Com_insert"])
                upd = int(now_global_status_rt["Com_update"]) - int(last_global_status_rt["Com_update"])
                dle = int(now_global_status_rt["Com_delete"]) - int(last_global_status_rt["Com_delete"])
                rep = int(now_global_status_rt["Com_replace"]) - int(last_global_status_rt["Com_replace"])
                tps = ins + upd + dle + rep
                thr_run = int(now_global_status_rt["Threads_running"])
                thr_con = int(now_global_status_rt["Threads_connected"])
                thr_cac = int(now_global_status_rt["Threads_cached"])
                hit_diff = float(now_global_status_rt['Innodb_buffer_pool_read_requests'])-float(now_global_status_rt['Innodb_buffer_pool_reads'])
                hit_buf = round(hit_diff/float(now_global_status_rt['Innodb_buffer_pool_read_requests'])*100,2)
                lock_c = now_global_status_rt["Innodb_row_lock_current_waits"]
                lock_t = now_global_status_rt['Innodb_row_lock_waits']
                open_table  = now_global_status_rt['Open_tables']
                open_file  = now_global_status_rt['Open_files']
                p_fsyncs = now_global_status_rt['Innodb_data_pending_fsyncs']
                p_reads = now_global_status_rt['Innodb_data_pending_reads']
                p_writes = now_global_status_rt['Innodb_data_pending_writes']
                netIn = self.util.sizeFormat(int(now_global_status_rt["Bytes_received"]) - int(last_global_status_rt["Bytes_received"]))
                netOut = self.util.sizeFormat(int(now_global_status_rt["Bytes_sent"]) - int(last_global_status_rt["Bytes_sent"]))

                self.out.add_row([time, qps, ins, upd, dle, rep, tps, thr_run, thr_con, thr_cac, hit_buf, \
                    lock_c + "|" + lock_t, open_table + "|" + open_file, p_fsyncs + "|" + p_reads + "|" + p_writes, netIn, netOut])

                ### 再次赋值
                last_global_status = now_global_status

                ### 累加计数器
                self.__num += 1

                ### 循环10次，就输出和清理
                if self.__num == 10:
                    ### 输出
                    self.out.print()
                    self.out.clear_row()

                    ### 清空
                    self.__num = 1
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))

    ### 主函数
    def main(self):
        if self.usage["suboptions_name"] == "innodb_status":
            self.__collectInnodbStatus()
        elif self.usage["suboptions_name"] == "global_status":
            self.__collectGlobalStatus()

if __name__ == "__main__":
    Cls_Mysql_Mon().main()
