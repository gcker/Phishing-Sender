#!/usr/bin/python3
#coding=utf-8

'''
Created on 2020年2月4日
@author: Gcker

Phishing sender封装了swaks，使人们批量发送邮件变得更简单
'''

import re
import base64
import os
import time
import threading
from config import logger
from config import args
from config import errMsg
from queue import Queue
from tqdm import tqdm

SENDCOUNT = 0

class Sender(threading.Thread):
    def __init__(self, threadNum, que, lock):
        threading.Thread.__init__(self)
        self._threadNum = threadNum
        self._threadLock = lock
        self._que = que
        self._fromMail = args.fromMail
        self._eml = args.eml
        self._mode = args.mode
        self._smtpUser = args.username
        self._smtpPass = args.password
        self._smtpServer = args.server
        self._sendCount = 0
        self._sendCmd = ''

        # 处理发件人字符串
        base64FirstName = base64.b64encode(self._fromMail.split('@')[0].encode('utf-8')).decode('utf-8')
        self._fromMail = f'=?gb18030?B?{base64FirstName}?=<{self._fromMail}>'

        return 0

    def run(self):
        while not self._que.empty():
            addressee = self._que.get()
            self.send(addressee)

            self._threadLock.acquire()
            global SENDCOUNT
            SENDCOUNT += 1
            logger.info(f'Sent to: {addressee} successful')
            self._threadLock.release()
        return 0
        

    def send(self, addressee):
        # 获取邮件主题
        content = ''
        with open(self._eml, 'r') as f:
            content = f.read()

        # 修改邮件文本中的收件人
        b64Str = base64.b64encode(addressee.split('@')[0].encode('utf-8')).decode('utf-8')
        to = 'To: "=?gb18030?B?' + b64Str + '?=" <' + addressee + '>\n'
        content = re.sub(r'(To: ).*?\n', to, content, count=1)
        
        with open('tmp/%d.eml' % self._threadNum, 'w') as f:
            f.write(content)

        # 构造swask命令发送邮件
        if self._mode == 'lan': # 局域网模式发送
            self._sendCmd = f'swaks --hide-all --server {self._smtpServer} --data tmp/{self._threadNum}.eml  --h-from "{self._fromMail}" --from xx@smtp2go.com --to {addressee}'
        elif self._mode == 'wan': # 互联网模式发送
            self._sendCmd = f'swaks --hide-all --from hr@test.com --h-From "{self._fromMail}" --data tmp/{self._threadNum}.eml --to {addressee}'
        elif self._mode == 'proxy': # 代理模式发送
            self._sendCmd = f'swaks --hide-all --server {self._smtpServer} --data tmp/{self._threadNum}.eml  --h-from "{self._fromMail}" --from xx@smtp2go.com -au {self._smtpUser} -ap {self._smtpPass} --to {addressee}'
        os.system(self._sendCmd + f'; echo $? > tmp/{self._threadNum}.recode')

        # 检测swaks返回的错误
        with open(f'tmp/{self._threadNum}.recode', 'r') as f:
            recode = f.read().strip()
            # print(f'错误代码：{recode}')
            if recode != '0':
                try:
                    logger.error(f'{errMsg[recode]} 请运行命令:{self._sendCmd} 自行排错')
                except Exception:
                    logger.error(f'未知错误，请运行命令:{self._sendCmd} 自行排错')

        return 0

def main():
    try:
        que = Queue()
        addresseeList = []

        # tmp目录用于放临时文件
        if not os.path.exists('tmp/'):
            os.mkdir('tmp')

        # 检测收件人是否有多个
        patt = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        if (re.match(patt, args.toMail)) is None:
            # 队列载入邮箱列表
            with open(args.toMail, 'r') as f:
                addresseeList = [addressee.strip() for addressee in f.readlines()]
            for addressee in addresseeList:
                if (re.match(patt, addressee)):
                    que.put(addressee)
                else:
                    logger.error(f'错误邮箱格式：{addressee}')
                    continue  
        else:
            # 队列载入单个邮箱
            que.put(args.toMail)

        # 启动线程
        lock = threading.Lock()
        threadCount = args.thread # 线程数量
        threadList = []
        logger.info('启动线程数：%d' % threadCount)
        for i in range(threadCount):
            threadList.append(Sender(i, que, lock))
        for t in threadList:
            t.start()
        for t in threadList:
            t.join()
    except Exception as e:
        logger.error(e)
    
    logger.info(f'Complete! Total: {SENDCOUNT}')
    print()

    return 0

if __name__ == '__main__':
        main()