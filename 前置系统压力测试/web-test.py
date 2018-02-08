#!/usr/bin/python
# -*-coding:utf-8-*-
#
#
import web
import time

urls = (
    '/index', 'index'
)

class index:
    def GET(self):
        print 'gogoogogo'
        time.sleep(3)
        return 'aaaa'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()