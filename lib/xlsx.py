#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import xlsxwriter
################################################################################################################

### xlsx类
class Cls_Xlsx:

    ### 初始化
    def __init__(self, xlsx_name):
        '''
          新建xlsx文件
          constant_memory 减少内存中的数据量，以便写大文件
        '''
        self.__workbook = xlsxwriter.Workbook(xlsx_name)

    ### 新建sheet
    def add_worksheet(self, sheet_name='sheet1'):
        self.__worksheet = self.__workbook.add_worksheet(sheet_name)

    ### 设置标题
    def add_title(self, column_no, title, bold=False):
        if bold:
            self.__worksheet.write_row(column_no, title, bold)
        else:
            self.__worksheet.write_row(column_no, title)

    ### 插入数据
    def add_content(self, column_no, content):
        '''
          content: 格式为列表，如[1,2,3]
        '''
        self.__worksheet.write_column(column_no, content)

    ### 设置对齐方式
    def set_align(self, align='left'):
        self.__worksheet.set_align(align)

    ### 设置单元格背景颜色
    def set_fg_color(self, color='white'):
        self.__worksheet.set_fg_color(color)

    ### 设置列宽
    def set_column_wide(self, column_name, column_wide):
        self.__worksheet.set_column(column_name, column_wide)

    ### 通过数字获取xlsx序号
    def convertToTitle(self, n):
        """
        :type n: int
        :rtype: str
        """
        rStr = ""
        while n!=0:
            res = n%26
            if res == 0:
                res =26
                n -= 26
            rStr = chr(ord('A')+res-1) + rStr
            n = n//26
        return rStr

    ### xlsx保持并关闭
    def close(self):
        self.__workbook.close()
