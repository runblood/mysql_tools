# mysql_tools

![pypi](https://img.shields.io/pypi/v/mysql_tools.svg?style=flat)

## Introduction

Daily operation and maintenance tools of MySQL

## Features

- Support Mysql to MySQL database, table and condition level synchronization
- Support MySQL remote query and remote execution
- Support MySQL table level data comparison
- Support the import of CSV files into mysql
- Support MySQL export to CSV file
- Support MySQL any input parameter comparison
- Support MySQL structure simple comparison
- Support MySQL show engine InnoDB status important information output
- Support MySQL user table authority query and synchronization

## Requirements

- [Python](https://www.python.org/downloads/) >= 3.6
- [numpy](https://pypi.org/project/numpy/) >= 1.17.4
- [prettytable](https://pypi.org/project/PrettyTable/) >= 0.7.2
- [xlrd](https://pypi.org/project/xlrd/) >= 1.2.0
- colorama >= 0.4.3
...

## Usage

### Config file

[`ip_list.txt`]

Connection information used to connect to the local / remote DB, for example：
```
10.x.x.1,port,user,pasword,db
10.x.x.2,port,user,pasword,db
```

[`sql_list.txt`]

Used to save the execution of a query or command, for example：

```
select * from test;
```

### usage Detailed

### 1、Remote query data
```
$ python mysql_query.py --help
usage: mysql_query.py [-h] -i IP_FILE -s SQL_FILE [-c COLUMN_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -i IP_FILE, --ip_file IP_FILE
                        ip list file
  -s SQL_FILE, --sql_file SQL_FILE
                        query sql
  -c COLUMN_NAME, --column_name COLUMN_NAME
                        column name
```

## Support this project

- Just click a star!
- Join wechat group to communicate!
- donation!

## WeChat Pay

<img width="200" src="https://github.com/runblood/mysql_tools/blob/master/images/wechatpay.jpeg">

## ThanksTo

Powerful Python IDE [Pycharm](https://www.jetbrains.com/pycharm/?from=mysql_tools) 

## License

This project is licensed under the Apache-2.0 License.
