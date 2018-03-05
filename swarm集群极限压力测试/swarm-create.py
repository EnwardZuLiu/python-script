#! /usr/bin/python
# -*-coding:utf-8-*-

from __future__ import print_function

import threading
import os

class DockerCreateThread(threading.Thread):
    def init(self, name , id):
        self.thread_name = name
        self.thread_id = id
    def run(self):
        command = "docker -H :4000 run docker"
        os.system(command)

class DockerDeleteThread(threading.Thread):
    def init(self, name, id):
        self.thread_name = name
        self.thread_id = id
    def run(self):
        command = "docker -H :4000 rm -f aaaaaaa"
        os.system(command)
