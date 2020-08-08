#!/usr/local/bin/python3.6
#-*- coding: utf-8 -*-
#Author WangJiang@2019 15810438848 634615288@qq.com
#All rights reserved

################################################################################################################
################################################################################################################

### excel 2003硬限制65536行
xlsx_limit = 65536

### csv/txt默认分隔符
separator = ','

### 读写超时(s)
net_read_timeout = '3600'
net_write_timeout = '3600'

### 捆绑插入值大小(就是insert 时带values多少个)
insv_batch_size = 5

### 捆绑提交频率值
commit_batch_size = 1000
