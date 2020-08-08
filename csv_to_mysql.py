#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
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
使用范围：支持csv文件（必须是utf-8格式的文件）导入到mysql中
特别提醒：使用需谨慎。一切后果自负！
"""

### 导入Csv到Mysql类
class Cls_Csv_To_Mysql:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().csv_to_mysql()
        self.sqltext = Cls_SqlText()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()
        self.__config = config

        self.num = 0
        self.sqltext_conditions = ''

    ### 导入
    def __import(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["IP", "Port", "Result"])

            ### 获取目标端mysql信息
            ip_fd_value = str(self.usage["target_mysql"]).split(',')

            ### 开始循环IP列表，连接数据库
            self.mysql_db = Cls_Mysql(ip_fd_value[0], ip_fd_value[1], ip_fd_value[2], ip_fd_value[3], ip_fd_value[4])
            self.mysql_db.execute('SET NET_WRITE_TIMEOUT='+self.__config.net_write_timeout)

            ### 读取csv文件
            imp_file = Cls_File(self.usage["import_file"])
            impfile_data_array = imp_file.read_by_line(skiprows=int(self.usage["skip_line"]), \
                usecols=self.usage["usecols"]) 
            impfile_data_list = imp_file.file_data_chlist(impfile_data_array)

            # 组合sql
            self.sql = self.sqltext.sqlInsert(self.usage["table_name"], self.usage["column_name"])
            
            ### 按照insv_batch_size个数，进行分割
            self.sqltext_conditions = self.util.list_avg_partition(impfile_data_list, self.__config.insv_batch_size)
            for i in self.sqltext_conditions:
                ### 每隔insv_batch_size个元素，insert一次数据
                self.__mysql_result = self.mysql_db.execute(self.sql, i, True)

                ### 执行结果判断逻辑
                if self.__mysql_result["code"] == 1:
                    ### 获取结果，添加行
                    self.out.add_row([ip_fd_value[0], ip_fd_value[1], 'ERROR：'+str(self.__mysql_result["content"])])
                        
                    ### 释放数据库资源
                    self.mysql_db.close()

                    ### 退出
                    self.util.sys_exit()

            ### 获取结果，添加行
            self.out.add_row([ip_fd_value[0], ip_fd_value[1], '导入成功'])

            ### 释放数据库资源
            self.mysql_db.close()
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))
        finally:
            ### 输出
            self.out.print()
    
    ### 主函数
    def main(self):
        self.__import()

if __name__ == "__main__":
    Cls_Csv_To_Mysql().main()
