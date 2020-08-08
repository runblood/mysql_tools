#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import pymysql
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.file import Cls_File
from lib.xlsx import Cls_Xlsx
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out

import conf.config as config
################################################################################################################

"""
使用范围：支持mysql导出数据到csv、txt、xlsx等（保持结果变化下后缀即可~~），但只支持<65535行（excel硬限制）
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql导出到Excel类
class Cls_Mysql_to_Excel:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().mysql_to_excel()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()
        self.__config = config

        self.__mysql_desc = []
        self.__mysql_data = []
        self.__mysql_rowcount = 0

    ### 导出函数
    def __export(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["IP", "Port", "Result"])

            ### 获取源端mysql信息
            ip_fd_value = str(self.usage["source_mysql"]).split(',')

            ### 获取SQL语句列表
            sql_file = Cls_File(self.usage["sql_file"])
            sql_file.read_all_data()

            ### 开始获取IP信息，连接数据库
            self.mysql_db = Cls_Mysql(ip_fd_value[0], ip_fd_value[1], ip_fd_value[2], ip_fd_value[3], \
                ip_fd_value[4], cursorclass=pymysql.cursors.SSCursor)
            self.mysql_db.execute('SET NET_READ_TIMEOUT='+self.__config.net_read_timeout)
            self.__mysql_result = self.mysql_db.query(sql_file.file_all_data)

            ### 判断执行结果
            if self.__mysql_result["code"] == 0:
                file_name = ip_fd_value[0] + '_'+ ip_fd_value[1] + '_' + self.util.timestamp()  + \
                    '_' +self.usage["export_file"]

                ### 执行SQL，添加xlsx文件、内容等
                self.workbook = Cls_Xlsx(file_name)
                self.workbook.add_worksheet()

                ### 添加sheet标题
                sheet_title = self.mysql_db.get_description()
                sheet_content = self.__mysql_result["content"]
                self.workbook.add_title('A1', sheet_title)

                ### 添加sheet内容
                for d in range(0, len(sheet_title)):
                    self.workbook.add_content(self.workbook.convertToTitle(d+1)+'2', \
                        self.util.get_single_index_tuple(sheet_content, d))
                self.workbook.close()

                ### 执行SQL，添加行
                self.out.add_row([ip_fd_value[0], ip_fd_value[1], file_name])
            else:
                ### 执行SQL，添加行
                self.out.add_row([ip_fd_value[0], ip_fd_value[1], "ERROR："+self.__mysql_result["content"]])

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
        self.__export()

if __name__ == "__main__":
    Cls_Mysql_to_Excel().main()
