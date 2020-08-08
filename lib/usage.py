#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import argparse
################################################################################################################

### 用法类
class Cls_Usage:

    ### 初始化
    def __init__(self):
        try:
            ### 创建最上层解析器
            self.__parser = argparse.ArgumentParser()
        except Exception as e:
            return None

    ### mysql_query用法类
    def mysql_query(self):
        self.__parser.add_argument('-i', '--ip_file', help='ip list file', required=True)
        self.__parser.add_argument('-s', '--sql_file', help='query sql', required=True)
        self.__parser.add_argument('-c', '--column_name', help='column name')

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### mysql_execute用法类
    def mysql_execute(self):
        self.__parser.add_argument('-i', '--ip_file', help='ip list file', required=True)
        self.__parser.add_argument('-s', '--sql_file', help='dml sql', required=True)
        self.__parser.add_argument('-c', '--column_name', help='column name')

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### mysql_to_excel用法类
    def mysql_to_excel(self):
        self.__parser.add_argument('-sm', '--source_mysql', help='source mysql\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-s', '--sql_file', help='sql list file', required=True)
        self.__parser.add_argument('-t', '--export_file', help='Export file name', required=True)

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### csv_to_mysql用法类
    def csv_to_mysql(self):
        self.__parser.add_argument('-tm', '--target_mysql', help='target mysql\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-f', '--import_file', help='csv file, must utf-8', required=True)
        self.__parser.add_argument('-t', '--table_name', help='db table name', required=True)
        self.__parser.add_argument('-c', '--column_name', help='column name. must: string type, comma separated', required=True)
        self.__parser.add_argument('-s', '--skip_line', help='skip csv file, not skipped by default', default=0)
        self.__parser.add_argument('-uc', '--usecols', help='Some columns, primitive types, eg: (0, 2)')

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### migrate用法类
    def migrate(self):
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-sl', '--sql_file', help='sql list file', required=True)
        self.__parser.add_argument('-ttn', '--target_table_name', help='target db tablename', required=True)
        self.__parser.add_argument('-tcn', '--target_column_name', help='target column name. muster: string type, comma separated', required=True)
        self.__parser.add_argument('-b', '--batch_size', help='batch size, default value 1000', default=1000)

        #self.__parser.add_argument('-d', '--delete', help='Delete data that has been synchronized from the source db', default='N')

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### structure用法类
    def structure(self):
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__sub_parser = self.__parser.add_subparsers(title='suboptions', help='additional help', dest='suboptions_name')
        self.__sub_parser.required = True

        ### structure_compare用法类
        self.__structure_compare_parser = self.__sub_parser.add_parser('structure_compare', help='structure compare')
        self.__structure_compare_parser.set_defaults(func=self.__structure_compare()) # 将函数structure_compare子解析器bar绑定

        ### query_structure用法类
        self.__query_structure_parser = self.__sub_parser.add_parser('query_structure', help='query structure')
        self.__query_structure_parser.set_defaults(func=self.__query_structure()) # 将函数query_structure子解析器bar绑定

        ### sync_structure用法类
        self.__sync_structure_parser = self.__sub_parser.add_parser('sync_structure', help='sync structure')
        self.__sync_structure_parser.set_defaults(func=self.__sync_structure()) # 将函数sync_structure子解析器bar绑定

        ### namespace转换
        return vars(self.__parser.parse_args())
    def __structure_compare(self):
        self.__structure_compare_parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
        self.__structure_compare_parser.add_argument('-tn', '--table_name', help='compare single table, \
            \nMultiple tables separated by ","\nBlank or not fill in all forms')
    def __query_structure(self):
        self.__query_structure_parser.add_argument('-tn', '--table_name', help='query single table structure, \
            \nMultiple tables separated by ","\nBlank or not fill in all forms')
    def __sync_structure(self):
        self.__sync_structure_parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
        self.__sync_structure_parser.add_argument('-tn', '--table_name', help='compare single table, \
            \nMultiple tables separated by ","\nBlank or not fill in all forms')

    ### user用法类
    def user(self):
        ### 必须项
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
        self.__sub_parser = self.__parser.add_subparsers(title='suboptions', help='additional help', dest='suboptions_name')
        self.__sub_parser.required = True

        ### 创建子解析器'showuser'
        self.__showuser_parser = self.__sub_parser.add_parser('showuser', help='show user')
        self.__showuser_parser.set_defaults(func=self.__showuser()) # 将函数showuser与子解析器bar绑定

        ### 创建子解析器'syncpriv'
        self.__showuser_parser = self.__sub_parser.add_parser('syncpriv', help='sync privileges')
        self.__showuser_parser.set_defaults(func=self.__syncpriv()) # 将函数syncpriv与子解析器bar绑定

        ### namespace转换
        return vars(self.__parser.parse_args())
    def __showuser(self):
        pass;
    def __syncpriv(self):
        self.__showuser_parser.add_argument('-ac', '--account', help='user and host, format must be: user@host, \ndefault all account')

    ### compare用法类
    def compare(self):
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-sl', '--sql_file', help='sql list file', required=True)
        self.__parser.add_argument('-b', '--batch_size', help='batch size, default value 1000', default=1000)

        ### namespace转换
        return vars(self.__parser.parse_args())

    ### mon监控类
    def mon(self):
         ### 必须项
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__sub_parser = self.__parser.add_subparsers(title='suboptions', help='additional help', dest='suboptions_name')
        self.__sub_parser.required = True

        ### 创建子解析器'innodb_status'
        self.__innodb_status_parser = self.__sub_parser.add_parser('innodb_status', help='show engine innodb status')
        self.__innodb_status_parser.set_defaults(func=self.__innodb_status()) # 将函数innodb_status与子解析器bar绑定

        ### 创建子解析器'global_status'
        self.__global_status_parser = self.__sub_parser.add_parser('global_status', help='global status, tps、qps...')
        self.__global_status_parser.set_defaults(func=self.__global_status()) # 将函数global_status与子解析器bar绑定

        ### namespace转换
        return vars(self.__parser.parse_args())
    def __innodb_status(self):
        pass;
    def __global_status(self):
        pass;

    ### parameter参数类
    def parameter(self):
        ### 必须项
        self.__parser.add_argument('-s', '--source', help='source db\
            \nformat: ip,port,user,password,database', required=True)
        self.__parser.add_argument('-p', '--parameters', help='parameters name,\
            \nMultiple tables separated by ","\nBlank or not fill in all forms', required=True)
        self.__sub_parser = self.__parser.add_subparsers(title='suboptions', help='additional help', dest='suboptions_name')
        self.__sub_parser.required = True

        ### 创建子解析器'query_parameter'
        self.__query_parameter_parser = self.__sub_parser.add_parser('query_parameter', help='query parameter')
        self.__query_parameter_parser.set_defaults(func=self.__query_parameter()) # 将函数query_parameter子解析器bar绑定

        ### 创建子解析器'parameter_compare'
        self.__parameter_compare_parser = self.__sub_parser.add_parser('parameter_compare', help='compare parameter')
        self.__parameter_compare_parser.set_defaults(func=self.__parameter_compare()) # 将函数parameter_compare子解析器bar绑定

        ### namespace转换
        return vars(self.__parser.parse_args())
    def __query_parameter(self):
        pass;
    def __parameter_compare(self):
        self.__parameter_compare_parser.add_argument('-t', '--target', help='target db\
            \nformat: ip,port,user,password,database', required=True)
