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
    1、query_parameter: 查找对应端参数信息
    2、compare_parameter: 对比源端和目标端参数是否一致（源库为参照），如果要对比部分参数，请用逗号分开；
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql参数对比类
class Cls_Mysql_Paramter:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().parameter()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        ### 获取源端mysql信息, 表名
        self.__source = str(self.usage["source"]).split(',')

    ### 查询参数
    def __query_parameter(self):
        try:
            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], \
                self.__source[3], self.__source[4])

            ### 开始批量获取参数
            clear_p = self.util.clear_space(self.usage["parameters"])
            srt = self.__source_mysql_db.query("show variables where variable_name in (\""+ \
                clear_p.replace(",", "\",\"") +"\")")

            ### 连接异常判断
            if srt["code"] == 1:
                self.logging.loggingError(srt["content"])

                ### 退出
                self.util.sys_exit()

            ### 进入主逻辑
            single_sp = self.util.get_single_columnv('Variable_name', srt["content"])
            diff_sp = self.util.compare_list_diff(clear_p.split(','), single_sp)
            for line in srt["content"]:
                self.out.add_row([line["Variable_name"], line["Value"]])

            ### 追加差集
            for diff_line in diff_sp:
                self.out.add_row([diff_line, "not_find"])

            ### 释放数据库资源
            self.__source_mysql_db.close()
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))
        finally:
            ### 输出
            self.out.print()

    ### 参数对比
    def __paramter_compare(self):
        try:
            ### 获取目标端mysql信息, 表名
            self.__target = str(self.usage["target"]).split(',')

            ### 输出格式化、标题
            self.out.add_title(["Parameters", "Source_value", "Target_value", "Compare_Result"])

            ### 连接源端、目标端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], \
                self.__source[3], self.__source[4])
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], \
                self.__target[3], self.__target[4])

            ### 开始批量获取参数
            clear_p = self.util.clear_space(self.usage["parameters"])
            srt = self.__source_mysql_db.query("show variables where variable_name in (\""+ \
                clear_p.replace(",", "\",\"") +"\")")
            trt = self.__target_mysql_db.query("show variables where variable_name in (\""+ \
                clear_p.replace(",", "\",\"") +"\")")

            ### 连接异常判断
            if srt["code"] == 1:
                self.logging.loggingError(srt["content"])

                ### 退出
                self.util.sys_exit()
            if trt["code"] == 1:
                self.logging.loggingError(trt["content"])

                ### 退出
                self.util.sys_exit()

            ### 进入主逻辑
            self.__s_list = []
            self.__t_list = []
            for line in clear_p.split(","):
                for s_line in srt["content"]:
                    if s_line["Variable_name"] == line:
                        self.__s_list.append(s_line["Value"])

                for t_line in trt["content"]:
                    if t_line["Variable_name"] == line:
                        self.__t_list.append(t_line["Value"])

                if len(self.__s_list) > 0 and len(self.__t_list) > 0:
                    if self.__s_list[0] == self.__t_list[0]:
                        self.__result = "一致"
                    else:
                        self.__result = "不一致"
                    self.out.add_row([line, self.__s_list[0], self.__t_list[0], self.__result])
                elif len(self.__s_list) > 0 and len(self.__t_list) == 0:
                    self.out.add_row([line, self.__s_list[0], "not_find", "不一致"])
                elif len(self.__s_list) == 0 and len(self.__t_list) > 0:
                    self.out.add_row([line, "not_find", self.__t_list[0], "不一致"])
                else:
                    self.out.add_row([line, "not_find", "not_find", "不一致"])

                self.__s_list = []
                self.__t_list = []
                
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
        if self.usage["suboptions_name"] == 'query_parameter':
            self.__query_parameter()
        elif self.usage["suboptions_name"] == 'parameter_compare':
            self.__paramter_compare()

if __name__ == "__main__":
    Cls_Mysql_Paramter().main()
