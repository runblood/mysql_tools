#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out
################################################################################################################

"""
使用范围：
    1、对比源单表和目标单表结构是否一致, 对比多表使用逗号分隔，为空或不传参数table_name将会对比连接源库和目标库
       之间，所有表的结构是否一致（源库为参照）
    2、查询源单表表结构, 查询多表使用逗号分隔，为空或不传参数table_name将会接源库所有表
    3、同步源端表结构到目标端，同步多表使用逗号分隔，为空或不传参数table_name将会接源库所有表（源库为参照）
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql结构对比类
class Cls_Mysql_Structure:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().structure()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        ### 获取源端mysql信息, 表名
        self.__source = str(self.usage["source"]).split(',')

    ### 添加行
    def __add_row(self, tablename=None, result=None):
        if self.usage["suboptions_name"] == 'query_structure':
            self.out.add_row([self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
                tablename, result])
        else:
            self.out.add_row([self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
                self.__target[0]+':'+str(self.__target[1])+'/'+self.__target[4], tablename, result])

    ### 执行数据
    def __execute_data(self, mysql_db, sqltext, error_header):
        execute_rt = mysql_db.execute(sqltext)
        if execute_rt["code"] == 1:
            #if self.usage["force"] and execute_rt["content"].split(",")[0][1:] == '1050':
            #    print(1)
            self.__add_row(self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
                error_header + str(execute_rt["content"]))

            ### 退出
            self.util.sys_exit()

    ### 结构对比
    def __structure_compare(self):
        try:
            ### 获取标端mysql信息, 表名
            self.__target = str(self.usage["target"]).split(',')

            ### 输出格式化、标题
            self.out.add_title(["source", "target", "tablename", "Result"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], \
                self.__source[3], self.__source[4])
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], \
                self.__target[3], self.__target[4])

            ### 获取表名, 未定义表名，就依照对比源端所有表
            if self.usage["table_name"]:
                tablename = str(self.usage["table_name"]).split(',')
            else:
                self.__source_mysql_result = self.__source_mysql_db.query("show tables")
                if self.__source_mysql_result["code"] == 1:
                    self.__add_row(result="获取源端所有表ERROR：" + self.__source_mysql_result["content"])

                    ### 退出
                    self.util.sys_exit()

                tablename = self.util.get_single_columnv('Tables_in_'+self.__source[4], self.__source_mysql_result["content"])

            ### 开始循环表
            for i in tablename:
                self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], \
                    self.__target[3], self.__target[4])
                ### 源端和目标端都查询表
                self.__source_table = self.__source_mysql_db.query("show create table " + i)
                self.__target_table = self.__target_mysql_db.query("show create table " + i)

                ### 执行结果判断
                if self.__source_table["code"] == 1:
                    self.__add_row(i, self.__source_table["content"])
                elif self.__target_table["code"] == 1:
                    self.__add_row(i, result=self.__target_table["content"])
                else:
                    ### 对源端和目标的表结构进行散列后，对比
                    if self.util.md5_hexdigest(self.util.get_single_columnv('Create Table', self.__source_table["content"])) == \
                        self.util.md5_hexdigest(self.util.get_single_columnv('Create Table', self.__target_table["content"])):
                        self.__add_row(i, "一致")
                    else:
                        self.__add_row(i, "不一致")

            ### 释放数据库资源
            self.__source_mysql_db.close()
            self.__target_mysql_db.close()
        except Exception as e:
            print(e)
        finally:
            ### 输出
            self.out.print()

    ### 查询结构
    def __query_structure(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["source", "tablename", "Result"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], \
                self.__source[3], self.__source[4])

            ### 获取表名, 未定义表名，就依照对比源端所有表
            if self.usage["table_name"]:
                tablename = str(self.usage["table_name"]).split(',')
            else:
                self.__source_mysql_result = self.__source_mysql_db.query("show tables")
                if self.__source_mysql_result["code"] == 1:
                    self.__add_row(result="获取源端所有表ERROR：" + self.__source_mysql_result["content"])

                    ### 退出
                    self.util.sys_exit()

                tablename = self.util.get_single_columnv('Tables_in_'+self.__source[4], self.__source_mysql_result["content"])

            ### 开始循环表
            for i in tablename:
                ### 源端和目标端都查询表
                self.__source_table = self.__source_mysql_db.query("show create table " + i)

                ### 执行结果判断
                if self.__source_table["code"] == 1:
                    self.__add_row(result="获取源端表结构ERROR：" + self.__source_table["content"])

                    ### 退出
                    self.util.sys_exit()
                self.__add_row(i, self.__source_table["content"][0]["Create Table"])

            ### 释放数据库资源
            self.out.all_column_align()
            self.__source_mysql_db.close()
        except Exception as e:
            print(e)
        finally:
            ### 输出
            self.out.print()

    ### 同步对比
    def __sync_structure(self):
        try:
            ### 获取标端mysql信息, 表名
            self.__target = str(self.usage["target"]).split(',')

            ### 输出格式化、标题
            self.out.add_title(["source", "target", "tablename", "Result"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], \
                self.__source[3], self.__source[4])
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], \
                self.__target[3], self.__target[4])

            ### 获取表名, 未定义表名，就依照对比源端所有表
            if self.usage["table_name"]:
                tablename = str(self.usage["table_name"]).split(',')
            else:
                self.__source_mysql_result = self.__source_mysql_db.query("show tables")
                if self.__source_mysql_result["code"] == 1:
                    self.__add_row(result="获取源端所有表ERROR：" + self.__source_mysql_result["content"])

                    ### 退出
                    self.util.sys_exit()

                tablename = self.util.get_single_columnv('Tables_in_'+self.__source[4], self.__source_mysql_result["content"])

            ### 开始循环表
            for i in tablename:
                ### 源端和目标端都查询表
                self.__source_table = self.__source_mysql_db.query("show create table " + i)

                ### 执行结果判断
                if self.__source_table["code"] == 1:
                    print(1)
                    self.__add_row(i, self.__source_table["content"])
                else:
                    self.__execute_data(self.__target_mysql_db, self.__source_table["content"][0]["Create Table"], '目标端执行异常：')
                    self.__add_row(i, 'success')

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
        if self.usage["suboptions_name"] == 'structure_compare':
            self.__structure_compare()
        elif self.usage["suboptions_name"] == 'query_structure':
            self.__query_structure()
        elif self.usage["suboptions_name"] == 'sync_structure':
            self.__sync_structure()

if __name__ == "__main__":
    Cls_Mysql_Structure().main()
