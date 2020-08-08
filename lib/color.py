#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from colorama import init, Fore, Back, Style
################################################################################################################

### 输出类
class Cls_Color:

    ### 初始化
    def __init__(self):
        """
            Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
            Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
            Style: DIM, NORMAL, BRIGHT, RESET_ALL
        """
        init(autoreset=True) # 初始化，并且设置颜色设置自动恢复

    ### 字体红色
    def fore_red(self, content):
        return Fore.RED + content
