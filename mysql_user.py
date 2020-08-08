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
    1、showuser: 查询源库用户及用户权限, 对比源库和目标库用户是否一致、权限是否一致；
    2、syncpriv: 对比目标库和源库不一致的权限，从源端拷贝目标端没有的权限权限；
特别提醒：使用需谨慎。一切后果自负！
"""

### Mysql用户类
class Cls_Mysql_User:

    ### 初始化
    def __init__(self):
        self.usage = Cls_Usage().user()
        self.util = Cls_Util()
        self.logging = Cls_Logging()
        self.out = Cls_Out()

        ### 获取源端、目标端mysql信息, 表名
        self.__source = str(self.usage["source"]).split(',')
        self.__target = str(self.usage["target"]).split(',')

        ### 初始化
        self.__diff = "一致"
        self.__no_diff = "不一致"

    ### 添加行
    def __add_row(self, user_host=None, type=None, source=None, target=None, result=None):
        self.out.add_row([user_host, type, source, target, result])

    ### 相关子指标判断
    def __child_charge(self, header, type, source, content, match_where, match_key):
        jii = self.util.judge_isexists_indict(content, match_where, match_key)
        if jii[0]:
            self.__add_row(header, type, source, source, self.__diff)
        else:
            self.__add_row(header, type, source, jii[1], self.__no_diff)

    ### 查询数据
    def __get_data(self, mysql_db, sqltext, error_header):
        query_rt = mysql_db.query(sqltext)
        if query_rt["code"] == 1:
            self.__add_row(source=self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
                target=self.__target[0]+':'+str(self.__target[1])+'/'+self.__target[4], \
                result = error_header + str(query_rt["content"]))

            ### 退出
            self.util.sys_exit()

        return query_rt["content"]

    ### 执行数据
    def __execute_data(self, mysql_db, sqltext, error_header):
        execute_rt = mysql_db.execute(sqltext)
        if execute_rt["code"] == 1:
            self.__add_row(source=self.__source[0]+':'+str(self.__source[1])+'/'+self.__source[4], \
                target=self.__target[0]+':'+str(self.__target[1])+'/'+self.__target[4], \
                result = error_header + str(execute_rt["content"]))

            ### 退出
            self.util.sys_exit()

        return execute_rt["content"]

    ### 显示用户
    def __showuser(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["User_Host", "Type", "Source", "Target", "Compare_Result"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4])
            ### 连接源端
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], self.__target[3], \
                self.__target[4])

            # 先判断出目标端是否有源端的用户差异
            """
                开始输出`user\host`, `max_questions`, `max_updates`, `max_connections`, `max_user_connections`, \
                `plugin`, `authentication_string`, `password_expired`, `password_lifetime`, `account_locked`
            """
            compare_sqltext = 'select `user`, `host`, max_questions, max_updates, max_connections, max_user_connections, \
                `plugin`, authentication_string, password_expired, password_lifetime, account_locked from mysql.`user`'
            source_rt = self.__get_data(self.__source_mysql_db, compare_sqltext, '源端出现异常：')
            target_rt = self.__get_data(self.__target_mysql_db, compare_sqltext, '目标端出现异常：')

            for uh in source_rt:
                ### 1、`用户/组`处理
                self.__child_charge(uh["user"]+'@'+uh["host"], "user_host", uh["user"]+'@'+uh["host"], \
                    target_rt, {"user": uh["user"], "host": uh["host"]}, \
                    {"user": uh["user"], "host": uh["host"]})

                ### 2、`max_questions_per_hour`判断
                self.__child_charge('', "max_questions_per_hour", uh["max_questions"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"max_questions": uh["max_questions"]})

                ### 3、`max_updates_per_hour`判断
                self.__child_charge('', "max_updates_per_hour", uh["max_updates"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"max_updates": uh["max_updates"]})

                ### 4、`max_connections_per_hour`判断
                self.__child_charge('', "max_connections_per_hour", uh["max_connections"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"max_connections": uh["max_connections"]})

                ### 5、`max_user_connections`判断
                self.__child_charge('', "max_user_connections", uh["max_user_connections"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"max_user_connections": uh["max_user_connections"]})

                ### 6、`plugin`判断
                self.__child_charge('', "plugin", uh["plugin"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"plugin": uh["plugin"]})

                ### 7、`authentication_string`判断
                self.__child_charge('', "authentication_string", uh["authentication_string"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"authentication_string": uh["authentication_string"]})

                ### 8、`password_expired`判断
                self.__child_charge('', "password_expired", uh["password_expired"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"password_expired": uh["password_expired"]})

                ### 9、`password_lifetime`判断     
                self.__child_charge('', "password_lifetime", uh["password_lifetime"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"password_lifetime": uh["password_lifetime"]})

                ### 10、`account_locked`判断     
                self.__child_charge('', "account_locked", uh["account_locked"], target_rt, \
                    {"user": uh["user"], "host": uh["host"]}, {"account_locked": uh["account_locked"]})

                ### 11、`privileges`判断
                ### 11.1 获取源端和目标端权限
                get_privileges_sqltext = 'show grants for `' + uh["user"]+'`@`'+uh["host"] + '`;'
                source_priv = self.__get_data(self.__source_mysql_db, get_privileges_sqltext, '源端查询权限异常：')
                target_priv = self.__get_data(self.__target_mysql_db, get_privileges_sqltext, '目标查询权限异常：')
                ### 11.2 对比端和目标端权限
                if len(self.util.compare_list_diff(source_priv, target_priv)) == 0 and \
                    len(self.util.compare_list_diff(target_priv, source_priv)) == 0:
                    self.__add_row('', "privileges", self.util.list_to_str(self.util.get_single_columnv('Grants for ' + \
                        uh["user"]+'@'+uh["host"], source_priv), '\n', 30), \
                        self.util.list_to_str(self.util.get_single_columnv('Grants for ' + \
                        uh["user"]+'@'+uh["host"], target_priv), '\n', 30), self.__diff)
                else:
                    self.__add_row('', "privileges", self.util.list_to_str(self.util.get_single_columnv('Grants for ' + \
                        uh["user"]+'@'+uh["host"], source_priv), '\n', 30), \
                        self.util.list_to_str(self.util.get_single_columnv('Grants for ' + \
                        uh["user"]+'@'+uh["host"], target_priv), '\n', 30), self.__no_diff)

            ### 释放数据库资源
            self.__source_mysql_db.close()
            self.__target_mysql_db.close()
        except Exception as e:
            print(e)
        finally:
            ### 输出
            self.out.print()

    ### 同步权限
    def __syncpriv(self):
        try:
            ### 输出格式化、标题
            self.out.add_title(["User_Host", "Content", "Source", "Target", "Copy_Result"])

            ### 连接源端
            self.__source_mysql_db = Cls_Mysql(self.__source[0], self.__source[1], self.__source[2], self.__source[3], \
                self.__source[4])
            ### 连接源端
            self.__target_mysql_db = Cls_Mysql(self.__target[0], self.__target[1], self.__target[2], self.__target[3], \
                self.__target[4])

            # 先查源端用户信息
            """
                开始输出`user\host`, `max_questions`, `max_updates`, `max_connections`, `max_user_connections`, \
                `plugin`, `authentication_string`, `password_expired`, `password_lifetime`, `account_locked`
            """
            sqltext = 'select `user`, `host`, max_questions, max_updates, max_connections, max_user_connections, \
                `plugin`, authentication_string, password_expired, password_lifetime, account_locked from mysql.`user`'
            if self.usage["account"]:
                sqltext = sqltext + " where concat(`user`, '@', `host`) = '" + self.usage["account"] + "'"
            source_rt = self.__get_data(self.__source_mysql_db, sqltext, '源端出现异常：')

            for uh in source_rt:
                ### 禁止同步root@localhost权限
                if not (uh["user"] == "root" and uh["host"] == "localhost"):
                    ### 先判断是否有用户，没有先创建，否则跳过
                    isexists_user = "select count(1) as total from mysql.user " + " where concat(`user`, '@', `host`) = '" + \
                        self.usage["account"] + "'"
                    charge_user = self.__get_data(self.__target_mysql_db, isexists_user, '目标端查询用户是否存在出现异常；')
                    if charge_user[0]["total"] == 0:
                        sqltext = 'create user `'+uh["user"]+'`@`'+uh["host"]+'`'
                        self.__execute_data(self.__target_mysql_db, sqltext, '目标端创建用户异常：')
                        self.__add_row(uh["user"] + '@' + uh["host"], 'create user', '', '', 'success')

                    ### 1、`max_questions_per_hour`判断
                    sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` WITH MAX_QUERIES_PER_HOUR ' + str(uh["max_questions"]);
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步max_questions_per_hour异常：')
                    self.__add_row(uh["user"] + '@' + uh["host"], 'max_questions_per_hour', '', '', 'success')
                    
                    ### 2、`max_updates_per_hour`判断
                    sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` WITH MAX_UPDATES_PER_HOUR ' + str(uh["max_updates"]);
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步max_updates_per_hour异常：')
                    self.__add_row('', 'max_updates_per_hour', '', '', 'success')
                    
                    ### 3、`max_connections_per_hour`判断
                    sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` WITH MAX_CONNECTIONS_PER_HOUR ' + str(uh["max_connections"]);
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步max_connections_per_hour异常：')
                    self.__add_row('', 'max_connections_per_hour', '', '', 'success')
                    
                    ### 4、`max_user_connections`判断
                    sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` WITH MAX_USER_CONNECTIONS ' + str(uh["max_user_connections"]);
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步max_user_connections异常：')
                    self.__add_row('', 'max_user_connections', '', '', 'success')
                    
                    ### 5、`password_expired`和`password_lifetime`判断
                    if str(uh["password_expired"]) == 'Y':
                        sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` PASSWORD EXPIRE';
                    else:
                        password_lifetime = str(uh["password_lifetime"])
                        if str(uh["password_lifetime"]) == 'None':
                            password_lifetime = 'null'
                    
                        sqltext = 'UPDATE mysql.user set password_lifetime=' + password_lifetime + \
                            ' where user=\''+uh["user"]+'\' and host=\''+uh["host"]+'\'';
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步password_expired和password_lifetime异常：')
                    self.__add_row('', 'password_expired+password_lifetime', '', '', 'success')
                    
                    ### 6、`account_locked`判断
                    if str(uh["account_locked"]) == 'Y':
                        sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` ACCOUNT LOCK';
                    else:
                        sqltext = 'ALTER USER `'+uh["user"]+'`@`'+uh["host"]+'` ACCOUNT UNLOCK';
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步account_locked异常：')
                    self.__add_row('', 'account_locked', '', '', 'success')
                    
                    ### 7、`plugin`从源端到目标端
                    ### 7.1 获取源端权限
                    get_privileges_sqltext = 'show grants for `' + uh["user"]+'`@`'+uh["host"] + '`;'
                    source_priv = self.__get_data(self.__source_mysql_db, get_privileges_sqltext, '源端查询权限异常：')
                    ### 7.2 拷贝权限到目标端
                    for cp in source_priv:
                        ### `WITH GRANT OPTION"`重新组合
                        grant_sqltext = cp['Grants for '+uh["user"]+'@'+uh["host"]]+' identified with '+ uh["plugin"]
                        if self.util.charge_isexists_instr(cp['Grants for '+uh["user"]+'@'+uh["host"]], 'WITH GRANT OPTION'):
                            grant_sqltext = grant_sqltext.replace('WITH GRANT OPTION', '') + ' WITH GRANT OPTION'
                        self.__get_data(self.__target_mysql_db, grant_sqltext, '目标执行权限异常：')
                        self.__add_row('', 'plugin+privileges', '' ,'', 'success')
                    
                    ### 8、同步权限
                    sqltext = 'UPDATE mysql.user SET authentication_string = \''+uh["authentication_string"]+\
                              '\' where user=\''+uh["user"]+'\' and host=\''+uh["host"]+'\'';
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端同步authentication_string异常：')
                    self.__add_row('', 'authentication_string', '', '', 'success')
                    
                    ### 9、刷新权限
                    sqltext = 'flush privileges'
                    self.__execute_data(self.__target_mysql_db, sqltext, '目标端刷新权限异常：')
                    self.__add_row('', 'flush privileges', '', '', 'success')
                else:
                    self.__add_row(uh["user"] + '@' + uh["host"], 'plugin+privileges', '', '', '不允许同步这个账号')
        except Exception as e:
            ### 错误输出
            self.logging.loggingError(str(e))
        finally:
            ### 输出
            self.out.print()

    ### 主函数
    def main(self):
        if self.usage["suboptions_name"] == 'showuser':
            self.__showuser()
        elif self.usage["suboptions_name"] == 'syncpriv':
            self.__syncpriv()

if __name__ == "__main__":
    Cls_Mysql_User().main()
