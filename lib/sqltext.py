#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from .sql.insert import Insert
################################################################################################################

### 用法类
class Cls_SqlText:

    ### 初始化
    def __init__(self):
        self.__insert = Insert()

    ### Sql插入
    def sqlInsert(self, tablename, columnname):
        return self.__insert.sqlInsert(tablename, columnname)
