#!/usr/bin/python
# -*-coding:utf-8-*-
#
#

import urllib
import urllib2
import threading
import traceback
import random

class MyThread(threading.Thread):
    '''
    '''
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = thread_name
    def run(self):
        while True:
            try:
                req1 = urllib.urlopen('http://localhost:8090/index')
                print str(self.thread_id) + "访问结果为" + str(req1.read())
            except Exception, e:
                print "访问服务器异常" + traceback.print_exc()


for i in range(1, 10000, 1):
    myThread = MyThread(i, "Thread-" + str(i))
    myThread.start()

