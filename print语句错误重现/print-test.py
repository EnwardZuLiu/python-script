#!/usr/bin/python
# -*-coding:utf-8-*-
#
#

import threading
import sys
import json

def getData():
    me = dict()
    for i in range(1, 10000, 1):
        me['kldsjp233op2vp0392vm0309-jnvp=' + str(i)] = 'sdjkfhkasfknsjkvnkahefklw--0293054iijdvo=-q-=23tioj4g0493ig=32ikvpo3mvpi3=-o=-43-kv-3k4g-93o=-4to2=kv-30i=-t0o2=3kfgp3ke-o2=9to30-2eig0jv0-23i=2o-3jgp4j3-ti=-i=vk2-3kgv-43j' +str(i) 
    return me

class TestThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = thread_name
    def run(self):
        while True:
            encode_argus = json.dumps(getData())
            print str(self.thread_id) + "------------" + encode_argus
            sys.stdout.flush()

for j in range(1, 100, 1):
    thread1 = TestThread(j, 'Thread-' + str(j))
    thread1.start()