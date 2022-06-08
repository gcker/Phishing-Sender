#!/usr/bin/python3
#coding=utf-8

from loguru import logger
import sys
import argparse
import os
import re

# 日志配置
## 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
          '[<level>{level: <5}</level>] ' \
          '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
          '<level>{message}</level>'
## 日志文件记录格式
logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
          '[<level>{level: <5}</level>] ' \
          '<cyan>{process.name}({process.id})</cyan>:' \
          '<cyan>{thread.name: <10}({thread.id: <5})</cyan> | ' \
          '<blue>{module}</blue>.<blue>{function}</blue>:' \
          '<blue>{line}</blue> - <level>{message}</level>'

logger.remove()
logger.add(sys.stderr, format=stdout_fmt)
logger.add('log/sender-{time}.log', format=logfile_fmt)

# 错误代码定义
errMsg = {
    '0' : '没有发生错误', 
    '1' : '错误解析命令行选项', 
    '2' : '连接到远程服务器时出错', 
    '3' : '未知的连接类型', 
    '4' : '以“管道”的连接类型运行时，写入或读取子进程的致命问题', 
    '5' : '在以“管道”的连接类型运行时，子进程意外死亡。 这可能意味着用--pipe指定的程序不存在。', 
    '6' : '连接意外关闭。', 
    '10' : '先决条件中的错误（所需的模块不可用）', 
    '21' : '从服务器读取初始banner时出错', 
    '22' : 'HELO交易中的错误', '23' : 'MAIL交易中的错误', 
    '24' : '不接受RCPT', '25' : '服务器向DATA请求返回了错误', 
    '26' : '服务器不接受邮件跟踪数据', 
    '27' : '正常会话退出请求后服务器返回错误', 
    '28' : 'AUTH交易中的错误', 
    '29' : 'TLS交易中的错误', 
    '30' : '请求/要求PRDR，但未发布', 
    '32' : 'TLS协商后EHLO中的错误', 
    '33' : 'XCLIENT交易中的错误', 
    '34' : 'XCLIENT之后EHLO中的错误', 
    '35' : 'PROXY选项处理中的错误', 
    '36' : '发送PROXY banner时出错'
}

# 参数配置
parse = argparse.ArgumentParser(description='Phishing sender')
parse.add_argument('--fromMail', '-f', type=str, required=True, help='specify a sender')
parse.add_argument('--toMail', '-to', type=str, required=True, help='specify a recipient email or file')
parse.add_argument('--eml', '-e', type=str, required=True, help='specify the eml file')
parse.add_argument('--mode', '-m', type=str, required=True, choices=['lan', 'wan', 'proxy'], help='use send mode')
parse.add_argument('--username', '-u', type=str, help='specify SMTP sender username')
parse.add_argument('--password', '-p', type=str, help='specify SMTP sender password')
parse.add_argument('--server', '-s', type=str, help='specify SMTP server')
parse.add_argument('--thread', '-t', type=int, default=5, help='specify thread (default: 5)')
args = parse.parse_args()

## 参数检测
if (args.mode == 'lan'):    # 内网发件
    if (args.server is None):
        logger.error('使用lan模式发件需要指定-s参数的值')
        exit(0)
elif (args.mode == 'proxy'):
    if ((args.username is None) or (args.password is None) or (args.server is None)):
        logger.error('使用proxy模式发件需要指定-u、-p和-s参数的值')
        exit(0)
elif (not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', args.toMail)) and (not os.path.exists(args.toMail)):
    logger.error('指定的收件人列表文件不存在')
    exit(0)
elif (not os.path.exists(args.eml)):
    logger.error('指定的邮件正文文件不存在')
    exit(0)