# get_mysql_stats

限制：
5.7及以上的不支持，后期再支持

帮助
# python get_mysql_stats.py --help
Usage: python get_mysql_stats.py [options]

This script prints MySQL TPS QPS

Options:
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  mysql host
  -P PORT, --port=PORT  mysql port
  -u USER, --user=USER  mysql user
  -p PASSWORD, --password=PASSWORD
                        mysql password
  -I interval, --interval=interval
                        default 1
                        
例子：
# python get_mysql_stats.py --host=xxxxxxxx --port=xxx --user=xxx --password=xxx
    time  sel  ins  upd  del  rpl  tps  cre  run  con  cac   hit dlk i_clk|i_tlk open_ct open_cf i_data_pfs i_data_pr i_data_pw slow_num netIn netOut
18:47:13    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   799b
18:47:14    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
18:47:15    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
18:47:16    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
18:47:17    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
18:47:18    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
18:47:19    0    0    0    0    0    0    0    2    2    0 99.89   0         0|4     144      35          0         0         0        0  652b   753b
