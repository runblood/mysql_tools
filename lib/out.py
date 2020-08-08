#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import prettytable as pt
################################################################################################################

### 输出类
class Cls_Out:

    ### 初始化
    def __init__(self, padding_width=1):
        self.tb = pt.PrettyTable()
        self.tb.padding_width = padding_width

    ### 横向割线
    def hrules(self, type=pt.ALL):
        self.tb.hrules = type # 横向割线，可以是：FRAME，ALL，NONE

    ### 纵向割线
    def vrules(self, type=pt.ALL):
        self.tb.vrules = type # 纵向割线，可以是：FRAME，ALL，NONE

    ### 添加标题函数
    def add_title(self, title):
        ### 添加标题
        self.tb.field_names = title

    ### 添加行函数
    def add_row(self, row_content):
        ### 添加行内容
        self.tb.add_row(row_content)

    ### 清空行内容函数
    def clear_row(self):
        ### 清空所有行内容
        self.tb.clear_rows()

    ### 单列水平对齐方式函数
    def column_align(self, column_name, align_type='l'):
        self.tb.align[column_name] = align_type

    ### 全部水平对齐方式函数
    def all_column_align(self, align_type='l'):
        self.tb.align = align_type

    ### 添加列函数
    def add_column(self, column_name, column_content):
        ### 添加列内容
        self.tb.add_column(column_name, column_content)

    ### 单列垂直对齐方式函数
    def column_valign(self, column_name, valign_type='l'):
        self.tb.valign[column_name] = valign_type

    ### 全部垂直对齐方式函数
    def all_column_valign(self, valign_type='b'):
        self.tb.valign = valign_type

    ### 清空标题和行内容函数
    def clear_all(self):
        ### 清空标题和所有行内容
        self.tb.clear()

    ### 打印结果
    def print(self):
        self.hrules()
        self.vrules()
        self.all_column_align()
        self.all_column_valign()

        print(self.tb)
