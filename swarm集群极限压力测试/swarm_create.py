#! /usr/bin/python
# -*-coding:utf-8-*-

'''
用来测试swarm集群大量创建删除容器的极限
'''

from __future__ import print_function

import threading
import os
import time
from functools import wraps

def logger(name):
    """日志装饰器
    在某一些方法上加入注解，方便打印该方法的执行时间以及相关日志打印信息
    :param name: 步骤名
    :return: 方法
    """
    def logger_decorator(func):
        """装饰器
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """内部方法
            """
            print('[%s] 开始运行，方法名为 [%s.%s] ......' % (name, func.__module__, func.__name__))
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print('[%s] 正常运行结束了，花费的时间为： %f sec' % (name, end - start))
            return result
        return wrapper
    return logger_decorator


class DockerCreateThread(threading.Thread):
    '''创建一个DokcerCreate线程类
    '''
    def __init__(self, thread_name, thread_id):
        '''构造方法
        '''
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id

    def run(self):
        i = 0
        while True:
            i = i + 1
            start = time.time()
            command = "docker -H :4000 run --name=liuzm_test_" + str(self.thread_id) + str(i) +\
            " hub.bmkcloud.lan/tools_drawtools /bin/sh -c \"sleep 1\""
            ret = os.system(command)
            end = time.time()
            print('[%s] - return is %s, create docker time is: %f' % (self.thread_name, str(ret), (end - start)))

class DockerDeleteThread(threading.Thread):
    '''创建一个DockerDelete线程类
    '''
    def __init__(self):
        '''构造方法
        '''
        threading.Thread.__init__(self)

    def run(self):
        while True:
            start = time.time()
            time.sleep(30)
            command = "docker -H :4000 ps -a | grep liuzm_test | awk '{print $1}'| xargs docker -H :4000 rm -f"
            os.system(command)
            end = time.time()
            print('delete docker time is: %f' % (end - start))

for i in range(1, 10, 1):
    create_thread = DockerCreateThread('create_thread-' + str(i), i)
    create_thread.start()

delete_thread = DockerDeleteThread()
delete_thread.start()
