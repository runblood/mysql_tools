#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
################################################################################################################

### Insert插入类
class Insert:
    
    ### sql插入
    def sqlInsert(self, tablename, columnname):
        '''
            参数格式为：
            tablename = 'tablename',
            conditions = 'col1,col2,col3'
        '''

        ###初始化字段列表， 值列表
        vals = '';
        
        ### 获取获得
        for i in columnname.split(','):
            vals += '%s,'

        ###组装INSERT语句
        sqlInsert = """
            insert into %s (%s) values (%s)
            """ % (tablename, columnname, vals[:-1])

        return sqlInsert
