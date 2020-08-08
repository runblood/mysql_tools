#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import pymysql
################################################################################################################

### Mysql连接类
class Cls_Mysql:
    
    ### 初始化
    def __init__(self, host, port, user, password, database='mysql', charset='utf8', \
        connect_timeout=3, cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_timeout= connect_timeout
        self.cursorclass = cursorclass

        ### 初始化
        self.__error = None
        self.__conn = None
        self.__cursor = None
        #self.__rows_affected = 0
       
        self.__init_conn()
        self.__init_cursor()

    ### 定义连接数据库
    def __init_conn(self):
        try:
            self.__conn = pymysql.connect(host=self.host, port=self.port, user=self.user, \
                password=self.password, database=self.database, charset=self.charset, \
                connect_timeout=self.connect_timeout, cursorclass=self.cursorclass)
        except Exception as e:
            self.__error = e

    ### 定义句柄
    def __init_cursor(self):
        if self.__conn:
            self.__cursor = self.__conn.cursor()

    ### 获取简化属性description
    def get_description(self):
        return [i[0].lower() for i in self.__cursor.description]

    ### 获取简化属性rowcount
    def get_rowcount(self):
        return self.__cursor.rowcount

    ### 获取所有数据
    def __get_allrows(self):
        return self.__cursor.fetchall()

    ### 获取部分数据
    def get_partrows(self, rows=1000):
        return self.__cursor.fetchmany(int(rows))

    ### 查询
    def query(self, sql, args=None, rows=None):
        """
            args:
                 单条: 
                     元祖: ('zhangsan', '2019-12-19 20:18:16', 'admin')
        """
        try:
            ### 先处理连接
            if self.__error:
                return {"code": 1, "content": str(self.__error)}

            ### 再执行SQL
            self.__cursor.execute(sql, args)

            ### 批量获取数据
            if rows:
                return {"code": 0}

            ### 获取全部数据
            return {"code": 0, "content": self.__get_allrows()}
        except Exception as e:
            self.close()
            return {"code": 1, "content": str(e)}

    ### 执行
    def execute(self, sql, args=None, multiple=False, commit_switch=True):
        """
            sql: INSERT INTO sys_area (name,update_time,update_by) VALUES (%s,%s,%s)
            args: 
                 单条:
                     元祖: ('zhangsan', '2019-12-19 20:18:16', 'admin')
                 批量:
                     第一种(二维列表): [('zhangsan', '2019-12-19 20:18:16', 'admin'), ('lisl', '2013-05-20 20:18:16', 'admin')]
                     第二种(列表套元祖): [['zhangsan', '2019-12-19 20:18:16', 'admin'], ['lisl', '2013-05-20 20:18:16', 'admin']]
            type: True多条，False单条
        """
        try:
            ### 先处理连接
            if self.__error:
                return {"code": 1, "content": str(self.__error)}

            ### 单条或多条执行逻辑
            if multiple:
                self.__cursor.executemany(sql, args)
            else:
                self.__cursor.execute(sql, args)
 
            ### 提交开关
            if commit_switch:
                self.commit()
 
            return {"code": 0, "content": self.__cursor.rowcount}
        except Exception as e:
            self.close()
            return {"code": 1, "content": str(e)}
          

    ### binlog开关
    def binlog_switch(self, option='ON'):
        self.__cursor.execute("set session sql_log_bin = " + option)

    ### 数据提交
    def commit(self):
        try:
            if self.__conn:
                self.__conn.commit()
                return {"code": 0, "content": "提交成功!"}

            return {"code": 1, "content": "提交失败!"} 
        except Exception as e:
            return {"code": 1, "content": str(e)}

    ### 数据回滚
    def rollback(self):
        try:
            if self.__conn:
                self.__conn.rollback()
                return {"code": 0, "content": "回滚成功!"}

            return {"code": 1, "content": "回滚失败!"}
        except Exception as e:
            return {"code": 1, "content": str(e)}

    ### 关闭连接、释放句柄
    def close(self):
        try:
            if self.__conn:
                self.__conn.close()
                self.__conn = None

            if self.__cursor:
                self.__cursor.close()
                self.__cursor = None
        except Exception as e:
            self.__conn = None
            self.__cursor = None
