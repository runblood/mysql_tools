# mysql_tools

![pypi](https://img.shields.io/pypi/v/synch.svg?style=flat)

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

## 依赖

- Python >= 2.7
- colorama >= 0.4.3
- numpy >= 1.17.4
- prettytable >= 0.7.2
- xlrd >= 1.2.0
...

## Usage

### conf/ip_list.txt

Connection information used to connect to the local / remote dB, for example：
10.x.x.1,port,user,pasword,db
10.x.x.2,port,user,pasword,db

### conf/sql_list.txt

Used to save the execution of a query or command, for example：

select * from test;

### usage method

eg：
$ python mysql_query.py --help

## Support this project

- Just click a star!
- Join wechat group to communicate!
- donation!

## WeChat Pay

<img width="200" src="https://github.com/runblood/mysql_tools/blob/master/images/wechatpay.jpeg"/>

## ThanksTo

Powerful Python IDE [Pycharm](https://www.jetbrains.com/pycharm/?from=synch) 

## License

This project is licensed under the Apache-2.0 License.
