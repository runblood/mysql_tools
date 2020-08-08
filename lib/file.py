#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import numpy as np
from .util import Cls_Util
import conf.config as config
################################################################################################################

class Cls_File:

    ### 初始化
    def __init__(self, file):
        self.file = file
        self.util = Cls_Util()

    ### 获取文件行数
    def file_clines(self):
        return len(open(self.file,'rU').readlines())

    ### 按照行读取文件
    def read_by_line(self, dtype=bytes, delimiter=config.separator, comments=None, skiprows=0, unpack=False, usecols=None, encoding='utf-8'):
        '''
            dtype : str,int,float默认
            delimiter: 分隔符
            unpack: True 列组合，False 行组合
            usecols: 例如'0,3,5' 代表只读0,3,5这3列数据
            comments: 跳过以comments参数开头的行
        ''' 
        ### 筛选出某些列
        if usecols:
            usecols=self.str_to_tuple(usecols)

        self.file_data_array = np.loadtxt(self.file, dtype=dtype, delimiter=delimiter, comments=comments, \
            unpack=unpack, skiprows=skiprows, usecols=usecols, encoding=encoding).astype(str)  #将文件中数据加载到data数组里

        ### 判断结果为几维数组
        # 0 字符串，1为1维数组，2为2维数组，N为N为数组
        if self.file_data_array.ndim == 0:
            self.file_data_array = [[str(self.file_data_array)]]
        elif self.file_data_array.ndim == 1:
            ''' 1维转化为2维'''
            self.file_data_array.resize((len(self.file_data_array), 1))

        return self.file_data_array

    ### str转化为元祖
    def str_to_tuple(self, str):
        self.__tuple_result = ()
        for i in str:
            if i != ',':
                self.__tuple_result = self.__tuple_result + (int(i),)

        return self.__tuple_result

    ### 多维数组转化为List
    def file_data_chlist(self, file_data_array):
        self.__file_data_result = []; self.__file_data_result_tmp = []
        for i in file_data_array:
            for j in range(len(i)):
                self.__file_data_result_tmp.append(i[j])
            self.__file_data_result.append(self.__file_data_result_tmp)

            ### 清空
            self.__file_data_result_tmp = []
        return self.__file_data_result

    ### 读取整个文件
    def read_all_data(self):
        try:
            with open(self.file, "r", encoding='utf8') as file:
                self.file_all_data_tmp = file.read().splitlines()

            ### 将list转化为str
            self.file_all_data = "".join(self.file_all_data_tmp)
        except:
            self.file_all_data = ""
        finally:
            file.close()
