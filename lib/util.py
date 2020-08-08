#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
import sys, time, hashlib, re
################################################################################################################

### Util工具类
class Cls_Util:

    ### 日期转化
    def datetime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    ### 时间转化
    def time(self):
        return time.strftime("%H:%M:%S")

    ### 时间戳
    def timestamp(self):
        return time.strftime("%Y%m%d%H%M%S")

    ### 睡眠
    def sleep(self, t):
        time.sleep(t)

    ### 输入confirm
    def interactive(self, notice):
        return input(notice)

    ### 随机数
    def rand_str(self, num=12):
        seed = "qwertyuioplkjhgfdsazxcvbnm0987654321MNBVCXZASDFGHJKLPOIUYTREWQ-_"
        return ''.join(random.sample(seed, num))

    ### 大小格式化
    def sizeFormat(self, size, is_disk=False, precision=2):
        '''
        size format for human.
            byte      ---- (B)
            kilobyte  ---- (KB)
            megabyte  ---- (MB)
            gigabyte  ---- (GB)
            terabyte  ---- (TB)
            petabyte  ---- (PB)
            exabyte   ---- (EB)
            zettabyte ---- (ZB)
            yottabyte ---- (YB)
        '''
        formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        unit = 1000.0 if is_disk else 1024.0
        if not(isinstance(size, float) or isinstance(size, int)):
            raise TypeError('a float number or an integer number is required!')
        if size < 0:
            raise ValueError('number must be non-negative')
        for i in formats:
            size /= unit
            if size < unit:
                return f'{round(size, precision)}{i}'
        return f'{round(size, precision)}{i}'

    ### 判断字符串是否存在
    def charge_isexists_instr(self, str, match_str):
        if (str.find(match_str) == -1):
            return False

        return True

    ### 判断是否为list类型
    def isinstance_list(self, array):
        return [False, True][isinstance(array, list)]

    ### 合并2个list为dict
    def merge_list_to_dict(self, listA, listB):
        """
            listA: 作为key
            listB: 作为val
        """
        return dict(map(lambda x,y:[x,y],listA,listB))

    ### 合并2个dict为dict
    def merge_dict_to_dict(self, dictA={}, dictB={}):
        return dictB.update(dictA)

    ### list首字母变成大写
    def upperFirstLetter_list(self, list):
        n = 0
        for i in list:
            list[n] = i[0].upper()+i[1:]
            n += 1

        return list

    ### list平均等分划分
    def list_avg_partition(self, list_array, num):
         for i in range(0, len(list_array), num):
             yield list_array[i:i + num]

    ### 获取多tuple中指定index列的值
    def get_single_index_tuple(self, content, index):
        """
            v: [(a, b), (c, d)]
        """
        return [x[index] for x in content]

    ### tuple转化为list
    def tuple_to_list(self, content):
        return list(content)

    ### list转化为str
    def list_to_str(self, list, split_str, length=None):
        if length:
            string = ''.join(list)
            list = re.findall(r'.{'+str(length)+'}', string)
            list.append(string[(len(list)*length):])

        return split_str.join(list)

    ### 对比2个list之间的差值，左边为参照物
    def compare_list_diff(self, left_list, right_list):
        return [x for x in left_list if x not in right_list]

    ### list包dict转化所有的key为小写
    def changeUpperToLower(self, list_contain_dict):
        """
            list_contain_dict: [{"Aa":'1',"b":'2'},{"Aa":'3',"b":'4'}]
        """
        new_list=[];
        for x in list_contain_dict:
            new_dics={}
            for i,j in x.items():
                new_dics[i.lower()] = j
            new_list.append(new_dics)

        return new_list

    ### 获取列表字典中某一列
    def get_single_columnv(self, single_column_name, column_values, diff_case=True):
        if not diff_case:
             column_values = self.changeUpperToLower(column_values)
             single_column_name = single_column_name.lower()
        return [x[single_column_name] for x in column_values]

    ### 判断dict中是否存在每一/多个key和value
    def judge_isexists_indict(self, content, match_where, match_key):
        """
            content: [{"a": 1, "b": 2, "c": 3}, {"d": 3, "e": 4, "f": 5}]
            match_where: {"a": 1, "b": 2}
            match_key: {"c": 3}
        """
        ### 初始化
        match_value = "不存在"
        match = 0
        num = 0

        ### 开始查找匹配
        for i in content:
            for k1,v1 in i.items():
                for k2,v2 in match_where.items():
                    if k1 == k2 and v1 == v2:
                        num += 1

            ### 匹配match_where情况
            if num == len(match_where):
                ### 临时清空计数器
                num = 0

                ### 匹配某值是否存在，存在就取出值
                for k3,v3 in match_key.items():
                    if k3 in i.keys() and i[k3] == v3:
                        num += 1

                ### 匹配match_key情况
                if num == len(match_key):
                    match += 1
                match_value = i[k3]

            ### 临时清空计数器
            num = 0

        ### 合并判断是否存在某一/个key和value
        if match > 0:
            return (True, match_value)
        else:
            return (False, match_value)

    ### 字符串散列
    def md5_hexdigest(self, message):
        """
            输入：字符串进行md5后，再散列
            返回：十六进制数据字符串值
        """
        if not isinstance(message, str):
            message = str(message)

        message_md5 = hashlib.md5(message.encode("utf-8"))
        return message_md5.hexdigest()

    ### 清除字符串
    def clean_str(self, str):
        return str.strip().replace(" ", "_").replace(".", "").replace("\n", "")

    ### 清除字段
    def clean_sql_str(self, str):
        return str.replace("'", "\\'").replace("\n", "")

    ### 清楚空字符串
    def clear_space(self, str, position=None):
        if position == 'l':
            return str.lstrip()
        elif position == 'r':
            return str.rstrip()
        elif position == 'lr':
            return str.strip()
        else:
            return str.replace(" ", "")
 
    ### 匹配
    def match(self, regexp, line):
        return re.match(regexp, line)

    ### 杀死进程
    def kill_precursor_procs(procs):
        """
        procs - a set of processes
        """
        for proc in procs:
            if procs[proc] and psutil.pid_exists(procs[proc].pid):
                try:
                    procs[proc].kill()
                except:
                    # process no longer exists, no big deal.
                    pass

    ### 退出系统
    def sys_exit(self):
        sys.exit()
