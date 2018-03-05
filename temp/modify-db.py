#! /usr/bin/python
# -*-coding:utf-8-*-

import MySQLdb
import json

update_sql = ""
select_sql = "SELECT * FROM t_task t WHERE t.`workflow_id` IN (925, 955, 967, 968)"

def getConnection(hostIp, username, password, dbName):
    dbConnection = MySQLdb.connect(host=hostIp, user=username, passwd=password, db=dbName)
    return dbConnection

def run():
    conn = getConnection('10.19.1.250', 'cloud', '123.bmk', 'biocloud_compute')
    cursor = conn.cursor()
    cursor.execute(select_sql)
    rows = cursor.fetchall()
    print rows


