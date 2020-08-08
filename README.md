#### get_mysql_stats【mysql的性能监控】

```
#### 1 帮助
```
#### python get_mysql_stats.py --help

Usage: python get_mysql_stats.py [options]  
 
This script prints MySQL TPS QPS  

Options:  
　-h,　--help　　　　　　show this help message and exit  
　-H HOST,　--host=HOST　mysql host  
　-P PORT,　--port=PORT　mysql port  
　-u USER,　--user=USER　mysql user  
　-p PASSWORD,　--password=PASSWORD  
　　　　　　　　　　　　　 mysql password  
　-I　interval,　--interval=interval  
　　　　　　　　　　　　　 default 1         
```
#### 1 例子：
```
#### python get_mysql_stats.py --host=xxxxxxxx --port=xxx --user=xxx --password=xxx
采集信息列表：  
　1）time：时间  
　2）sel：qps  
　3）ins：插入  
　4）upd：更新  
　5）del：删除    
　6）rpl：替换  
　7）tps：tps  
　8）cre：进程创建数  
　9）run：进程运行数  
　10）con：链接数  
　11）cac：缓存  
　12）hit：命中率  
　13）dlk：死锁  
　14）i_clk：innodb当前等待数  
　15）i_tlk：innodb总等待数  
　16）open_ct：打开表数  
　17）open_cf：打开文件数  
　18）i_data_pfs：innodb当前挂起 fsync() 操作的数量  
　19）i_data_pr：innodb当前挂起的读操作数  
　20）i_data_pw：inndo当前挂起的写操作数  
　21）slow_num：慢日志数  
　22）netIn：网卡输入  
　23）netOut网卡输出

### 2. get_redis_stats【redis的性能监控】
使用方法和get_mysql_stats一样
