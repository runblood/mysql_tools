#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.file import Cls_File
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out
################################################################################################################

"""
使用范围：支持多IP下执行DML、DDL语句，且返回影响的行数；
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql执行类
class Cls_Mysql_Execute:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().mysql_execute()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

    ### 执行函数
    def __execute(self):
        try:
            ### 获取IP文件数据
            ip_file = Cls_File(self.usage["ip_file"])
            ip_file_array = ip_file.read_by_line(delimiter='\n', comments='#')

            ### 输出格式化、标题
            self.out.add_title(["IP", "Port", "Result"])

            ### 交互逻辑开始
            interactive_result = self.util.interactive('Are you sure to execute? [yes/no]: ') 
            if str(interactive_result) != 'yes':
                self.util.sys_exit()

            for ip_fd in ip_file_array:
                ### 拆分IP列表中每行数据
                ip_fd_value = ip_fd[0].split(',')

                ### 获取SQL语句列表
                sql_file = Cls_File(self.usage["sql_file"])
                sql_file.read_all_data()

                ### 开始循环IP列表，连接数据库
                self.mysql_db = Cls_Mysql(ip_fd_value[0], ip_fd_value[1], ip_fd_value[2], ip_fd_value[3], ip_fd_value[4])
                self.__mysql_result = self.mysql_db.execute(sql_file.file_all_data)

                ### 判断执行结果
                if self.__mysql_result["code"] == 0:
                    ### 执行SQL，添加行
                    self.out.add_row([ip_fd_value[0], ip_fd_value[1], "success, affect [" + \
                        str(self.__mysql_result["content"]) + "] line"])
                else:
                    ### 执行SQL，添加行
                    self.out.add_row([ip_fd_value[0], ip_fd_value[1], "ERROR：" + self.__mysql_result["content"]])

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
        self.__execute()

if __name__ == "__main__":
    Cls_Mysql_Execute().main()
