#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2020 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from lib.mysql import Cls_Mysql
from lib.usage import Cls_Usage
from lib.file import Cls_File
from lib.util import Cls_Util
from lib.logging import Cls_Logging
from lib.out import Cls_Out

import conf.config as config
################################################################################################################

"""
使用范围：支持源端到目标端任何sql级别的对比
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql对比类
class Cls_Mysql_Compare:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().compare()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        self.__config = config

        ### 中间值保持
        self.__error = []
        self.__presult = []

        ### 获取源端、目标端mysql信息, 表名
        self.__source = str(self.usage["source"]).split(',')
        self.__target = str(self.usage["target"]).split(',')

    ### 部分对比子函数
    def __part_compare(self, source_part, target_part):
        for s in source_part:
            if s not in target_part and s not in self.__error:
               self.__error.append(s)
            else:
               continue
        for l in target_part:
            if l not in source_part:
               self.__presult.append(l)
        for x in self.__error:
            if x in target_part or x in self.__presult:
               self.__error.remove(x)
            else:
               pass

    ### 输出差值
    def __out_diff(self):
        replstr = "replace into x.x values "
        for i in self.__error:
            head = '("'
            end = '")'
            var_col = []
            for key, val in i.items():
               var_col.append(str(val))
            strvar = '","'.join(var_col)
            c_v = head + strvar + end
            insertsql = replstr + c_v.replace('"None"', 'NULL')
            self.out.add_row([insertsql])

    ### 主函数
    def __compare(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["Compare_result[源端作为参考，目标和源端不一致的]"])

            ### 获取SQL语句列表
            sql_file = Cls_File(self.usage["sql_file"])
            sql_file.read_all_data()

            ### 连接源端、目标端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4])
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], self.__target[3], \
                self.__target[4])
            self.__source_mysql_result = self.__source_mysql_db.query(sql_file.file_all_data, None, self.usage["batch_size"])
            self.__target_mysql_result = self.__target_mysql_db.query(sql_file.file_all_data, None, self.usage["batch_size"])

            ### 判断执行结果
            if self.__source_mysql_result["code"] == 0:
                ### 捆绑式循环获取
                source_part_result = self.__source_mysql_db.get_partrows(self.usage["batch_size"])
                while source_part_result:
                    target_part_result = self.__target_mysql_db.get_partrows(self.usage["batch_size"])
                    source_md5_hexdigest = self.util.md5_hexdigest(source_part_result)
                    target_md5_hexdigest = self.util.md5_hexdigest(target_part_result)
                    if source_md5_hexdigest != target_md5_hexdigest:
                        self.__part_compare(source_part_result, target_part_result)

                    source_md5_hexdigest = []
                    target_md5_hexdigest = []
                    source_part_result = self.__source_mysql_db.get_partrows(self.usage["batch_size"])

                ### 输出差值
                self.__out_diff()
            else:
                ### 添加行
                self.out.add_row(["ERROR："+self.__mysql_result["content"]])

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
        self.__compare()

if __name__ == "__main__":
    Cls_Mysql_Compare().main()
