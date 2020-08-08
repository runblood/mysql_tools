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
使用范围：支持多IP下执行查询语句，且返回的结果支持过滤（支持是单列字段）
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql查询类
class Cls_Mysql_Query:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().mysql_query()
        self.util = Cls_Util()
        self.logging = Cls_Logging()

    ### 查询函数
    def __query(self):
        try:
            ### 获取IP文件数据
            ip_file = Cls_File(self.usage["ip_file"])
            ip_file_array = ip_file.read_by_line(delimiter='\n', comments='#')

            for ip_fd in ip_file_array:
                ### 初始化
                self.out = Cls_Out()

                ### 拆分IP列表中每行数据
                ip_fd_value = ip_fd[0].split(',')
               

                ### 打印列表信息
                print("\nHost: "+ ip_fd_value[0], \
                    "Port: "+ str(ip_fd_value[1]), "DB: "+ str(ip_fd_value[4]))

                ### 获取SQL语句列表
                sql_file = Cls_File(self.usage["sql_file"])
                sql_file.read_all_data()

                ### 开始循环IP列表，连接数据库
                self.mysql_db = Cls_Mysql(ip_fd_value[0], ip_fd_value[1], ip_fd_value[2], ip_fd_value[3], ip_fd_value[4])
                self.__mysql_result = self.mysql_db.query(sql_file.file_all_data)

                ### 判断执行结果
                if self.__mysql_result["code"] == 0:
                    ### 内容
                    result = self.__mysql_result["content"]

                    ### 标题
                    title = self.mysql_db.get_description()

                    ### 过滤信息
                    if self.usage["column_name"]:
                        ### 标题过滤
                        title = self.usage["column_name"].split(',')

                        ### 内容过滤
                        for c in title:
                            try:
                                ### 执行SQL，添加行
                                self.out.add_column(c.strip(), self.util.get_single_columnv(c.strip(), result, False))
                            except:
                                pass;
                    else:
                        ### 执行SQL，添加行
                        for c in title:
                            self.out.add_column(c, self.util.get_single_columnv(c, result, False))

                    ### 添加标题
                    self.out.add_title(title)
                else:
                    ### 执行SQL，添加行
                    self.out.add_row(["ERROR："+self.__mysql_result["content"]])

                ### 释放数据库资源
                self.mysql_db.close()

                ### 打印
                self.out.print()
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))

    ### 主函数
    def main(self):
        self.__query()

if __name__ == "__main__":
    Cls_Mysql_Query().main()
