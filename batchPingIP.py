# -*- coding: utf-8 -*-

#********************************************************
#*** Author      : lion
#*** Create Date : 2017/09/18
#*** Modify Date : NA
#*** Function    : Batch check ip can reachable or not
#********************************************************

import sys
import re
import subprocess
import threading
import time
import platform

ip = raw_input('Please iput a random ip:')

if len(ip.split('.')) != 4 or not re.match(r'\d+.\d+.\d+.\d+', ip):
    print("Invalid ip")
    sys.exit(1)

ip_segment = '.'.join(ip.split('.')[:-1])
ping_result = []


def check_alive(ip):
    if platform.system() == 'Windows':
        ping_cmd = 'ping -n 1 -w 4 %s' % (ip,)
    else:
        ping_cmd = 'ping -c 1 -W 2 %s' % (ip,)
    p = subprocess.Popen(ping_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p.stdout.read()
    regex = re.findall(r'100', result)
    regex2 = re.findall(r'TTL ',result)
    if len(regex) == 0 and len(regex2) == 0:
        ping_result.append("%s Success" % (ip,))
    else:
        ping_result.append("%s Fail" % (ip,))

if __name__ == "__main__":
    threads = []
    num = 0
    for i in range(256):
        ping_ip = '.'.join([ip_segment, str(i)])
        t1 = threading.Thread(target=check_alive, args=(ping_ip,))
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
        num = num + 1
        if num % 50 == 0:
            time.sleep(2)
    for t in threads:
        t.join()
    for i in sorted(ping_result, key = lambda x:int(x.split(' ')[0].split('.')[3])):
        print(i)
    print('Execute End!')
    raw_input('Press enter key to exit')
