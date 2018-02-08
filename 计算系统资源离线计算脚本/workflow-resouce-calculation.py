#!/usr/bin/python
# -*-coding:utf-8-*-
#
#

import MySQLdb
import fire
# from enum import Enum
import time, datetime
# import csv

'''
用来离线计算Workflow的资源使用情况

1 获取到 workflow 的运行时间
2 将 workflow 按照每2分钟划分区域
3 搜索出该workflow所有的的监控指标
4 将监控指标按时间归类到各个区域
5 将各个区域内的相同监控指标进行相加，得到总的监控指标

'''

def getDBcon(hostIp, userName, password, dbName):
    '''连接数据库
    '''
    connect = MySQLdb.connect(
        host=hostIp, user=userName, passwd=password, db=dbName)
    return connect


def selectQuery(sql, connect):
    '''执行sql语句
    '''
    print '查询数据库数据，该SQL语句为：' + str(sql)
    cur = connect.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def run(workflow_id, env='PUBLISH'):
    if workflow_id is None:
        print 'workflow_id 为None，直接返回。'
        return
    if env is None:
        print '运行环境为None，直接返回'
        return
    if env == 'DEV':
        print '获取开发环境数据库链接'
        connect = getDBcon('192.168.0.1', 'test',
                           'test', 'test')
    if env == 'RTM':
        connect = getDBcon('192.168.0.1', 'test',
                           'test', 'test')
    if env == 'PUBLISH':
        print '获取生产环境数据库链接'
        connect = getDBcon('192.168.0.1', 'test',
                           'test', 'test')
    if connect is None:
        print '运行环境为只能是 DEV,RTM,PUBLISH 其中的一个，不可以为其他值'
        return

    WORKFLOW_SQL = 'SELECT t.create_time, t.update_time FROM t_workflow t WHERE t.id = %s' % workflow_id
    rows = selectQuery(WORKFLOW_SQL, connect)
    time_array = []
    start = time.mktime(rows[0][0].timetuple()) # 获取秒级时间戳
    end = time.mktime(rows[0][1].timetuple()) # 获取秒级时间戳

    # 每两分钟一个时刻，将所有的时间存放到数组中
    tmp = start
    while tmp < end:
        time_array.append(tmp)
        tmp = tmp + 120
    time_array.append(end)

    # 将时间戳按照时间段来分类
    result_array = []
    i = 1
    for me_time in time_array:
        tmp_object = {}
        tmp_object['start_time'] = me_time
        tmp_object['end_time'] = me_time + 120
        tmp_object['index'] = i
        tmp_object['metra'] = []
        i = i + 1
        result_array.append(tmp_object)

    METRA_SQL = "SELECT m.`metric_name`, d.`create_time`, d.`value` FROM t_metric m, t_metric_data d WHERE m.`id` = d.`metric_id` AND m.`metric_name` IN ('ramUsage', 'cpuPercent') AND m.`container_id` IN (SELECT c.`container_id` FROM t_task t, t_container c WHERE t.`workflow_id` = %s AND t.`task_uuid` = c.`task_uuid`)" % workflow_id
    
    #将所有的监控指标按照创建时间放到指定的时间段里面
    rows1 = selectQuery(METRA_SQL, connect)
    for row in rows1:
        timetuple = time.mktime(row[1].timetuple())
        for tmp_object in result_array:
            if timetuple > tmp_object['start_time'] and timetuple <= tmp_object['end_time']:
                tmp_object['metra'].append(row)

    # 计算每一个时间段里面的所有的监控指标
    for row in result_array:
        metras = row['metra']
        ram = 0
        cpu = 0
        for metra in metras:
            if metra[0] == 'ramUsage':
                ram = ram + metra[2]
            if metra[0] == 'cpuPercent':
                cpu = cpu + metra[2]
        row['ram'] = ram
        row['cpu'] = cpu
        row['start_time'] = datetime.datetime.fromtimestamp(row['start_time'])
        row['end_time'] = datetime.datetime.fromtimestamp(row['end_time'])
        row['metra'] = None
        # print row
    # csvFile3 = open(path, 'w', newline='') 
    print 'index\tstart_time\tend_time\tram\tcpu'    
    for row in result_array:
        print '%s\t%s\t%s\t%s\t%s' % (row['index'], row['start_time'], row['end_time'], row['ram'], row['cpu'])

def __main__():
    fire.Fire(run)


if __name__ == "__main__":
    __main__()
