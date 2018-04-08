#!/usr/bin/python
# -*-coding:utf-8-*-
#
#

import Queue
import threading
import time

class ThreadPoolManage(object):
    '''线程池管理类
    '''
    def __init__(self, core_num, max_num):
        self.core_num = core_num
        self.max_num = max_num
        self.__worker_list = []
        self.__task_queue = Queue.Queue()
        self.__thread_num = 0
        self.__init_worker()
    
    def __init_worker(self):
        '''初始化核心线程数
        '''
        for i in range(self.core_num):
            self.__thread_num = self.__thread_num + 1
            self.__worker_list.append(Worker(self.__task_queue, 'aync-thread-worker-%s' % str(self.__thread_num)))

    def put_task(self, func, *args):
        '''向队列中存放任务
        '''
        self.__task_queue.put((func, list(args)))

class Worker(threading.Thread):
    '''工作线程
    '''
    def __init__(self, task_queue, thread_name):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.thread_name = thread_name
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.task_queue.get()
                do(args)
                # self.task_queue.task_done()
            except Exception as e:
                print '运行任务出现异常：%s' % e
def run(n):
    print n
    time.sleep(n[0])
    

if __name__ == '__main__':
    tpm = ThreadPoolManage(2, 10)
    tpm.put_task(run, 1)
    tpm.put_task(run, 2)
    tpm.put_task(run, 3)
    tpm.put_task(run, 4)
    tpm.put_task(run, 5)
    tpm.put_task(run, 6)
    tpm.put_task(run, 7)
    tpm.put_task(run, 8)
    tpm.put_task(run, 9)
    tpm.put_task(run, 10)
    tpm.put_task(run, 11)
    tpm.put_task(run, 12)
    print 'all put'


