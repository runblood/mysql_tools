#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import pymysql
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.file import Cls_File
from lib.sqltext import Cls_SqlText
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out

import conf.config as config
################################################################################################################

"""
使用范围：支持源端到目标端任何sql级别的数据同步，但目标端只支持一个表；
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql到Mysql迁移类
class Cls_Mysql_To_Mysql:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().migrate()
        self.sqltext = Cls_SqlText()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        self.__config = config
        self.__num = 0
        self.__count = 0

        ### 获取源端、目标端mysql信息, 表名
        self.__source = str(self.usage["source"]).split(',')
        self.__target = str(self.usage["target"]).split(',')

    ### 添加行
    def __add_row(self, result):
        self.out.add_row([self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
            self.__target[0]+':'+str(self.__target[1])+'/'+self.__target[4], self.util.datetime(), result])        

    ### 主函数
    def __migrate(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["Source", "Target", "Datetime", "Result"])

            ### 获取SQL语句列表
            sql_file = Cls_File(self.usage["sql_file"])
            sql_file.read_all_data()

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4], cursorclass=pymysql.cursors.SSCursor)
            self.__source_mysql_db.execute('SET NET_READ_TIMEOUT='+self.__config.net_read_timeout)
            self.__source_mysql_result = self.__source_mysql_db.query(sql_file.file_all_data)

            ### 判断执行结果
            if self.__source_mysql_result["code"] == 0:
                ### 连接目标端
                self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], self.__target[3], \
                    self.__target[4])

                ### 按照insv_batch_size个数，进行分割
                self.__source_allrows_len = len(list(self.util.list_avg_partition(self.__source_mysql_result["content"], \
                    self.__config.insv_batch_size)))

                ### 组合sqltext conditions
                self.sql = self.sqltext.sqlInsert(self.usage["target_table_name"], self.usage["target_column_name"])

                ### 提交数据
                for i in self.util.list_avg_partition(self.__source_mysql_result["content"], self.__config.insv_batch_size):
                    self.__num += 1
                    self.__count += 1
                    self.__target_mysql_result = self.__target_mysql_db.execute(self.sql, i, True, False)

                    ### 判断执行结果
                    if self.__target_mysql_result["code"] == 0:
                        ### 控制提交频率
                        if (self.__num * self.__config.insv_batch_size) >= self.__config.commit_batch_size or\
                            self.__count == self.__source_allrows_len:
                            ### 目标端提交
                            self.__commit_result = self.__target_mysql_db.commit()

                            ### 提交结果判断
                            if self.__commit_result["code"] ==0:
                                ### 添加行
                                self.__add_row("迁移"+str(self.__num * self.__config.insv_batch_size - \
                                    (self.__config.insv_batch_size - len(i))) + "行成功!")

                                ### 清零
                                self.__num = 0
                            else:
                                self.__add_row("提交时："+str(self.__num * self.__config.insv_batch_size - \
                                    (self.__config.insv_batch_size - len(i))) + "行失败!，原因是："+self.__commit_result["content"])

                                ### 退出
                                self.util.sys_exit()
                    else:
                        self.__add_row("提交："+str(self.__num * self.__config.insv_batch_size - \
                            (self.__config.insv_batch_size - len(i))) + "行失败!，原因是："+self.__target_mysql_result["content"])
                        self.util.sys_exit()
            else:
                ### 添加行
                self.out.add_row([ip_fd_value[0], ip_fd_value[1], "ERROR："+self.__mysql_result["content"]])

            ### 释放数据库资源
            self.__source_mysql_db.close()
            self.__target_mysql_db.close()
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))
        finally:
            ### 输出
            self.out.print()

    ### 主函数
    def main(self):
        self.__migrate()

if __name__ == "__main__":
    Cls_Mysql_To_Mysql().main()
