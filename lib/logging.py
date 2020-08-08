#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2020 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
from lib.util import Cls_Util
import logging
################################################################################################################

### Logging工具类
class Cls_Logging:

    ### 初始化
    def __init__(self):
        self.util = Cls_Util()
        self.__logging()

    ### 日志结构定义
    def __logging(self):
        ### 初始化日志格式
        log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        date_format = self.util.datetime()
        logging.basicConfig(level=logging.DEBUG,
                            format=log_format,
                            datefmt=date_format,
                            #filename= 'error.log', #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                            filemode='w')

    ### info记录
    def loggingInfo(self, info):
        logging.info(info)

    ### warning记录
    def loggingWarning(self, warning):
        logging.warning(warning)

    ### error记录
    def loggingError(self, error):
        logging.error(error)

    ### debug记录
    def loggingDebug(self, debug):
        logging.debug(debug)

    ### critical记录
    def loggingCritical(self, critical):
        logging.debug(critical)
