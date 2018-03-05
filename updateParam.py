#! /usr/bin/python
# -*-coding:utf-8-*-

import MySQLdb
import argparse
import json

devDbConfig = ('10.3.128.42', 'test_pre', 'test_pre.123', 'biocloud_compute')

hgDbConfig = ('10.2.12.1', 'cloud', 'cloud.123.bmk', 'biocloud_compute')

yzDbConfig = ('10.50.1.250', 'cloud', '123.bmk', 'biocloud_compute')

rtmDbConfig = ('10.3.129.50', 'rtm_cloud', '123.rtm_cloud..bmk', 'biocloud_compute')

databaseConfig = dict()
databaseConfig['dev'] = devDbConfig
databaseConfig['hg'] = hgDbConfig
databaseConfig['yz'] = yzDbConfig
databaseConfig['rtm'] = rtmDbConfig

querySql = "select parameter_value from t_task_parameter where param_name='%s' and workflow_id=%s"

updateSql = "update t_task_parameter set parameter_value = '%s' where param_name='%s' and workflow_id=%s" 

def getConnection(hostIp, username, password, dbName):
    dbConnection = MySQLdb.connect(host=hostIp, user=username, passwd=password, db=dbName)
    return dbConnection

def executeSql(dbConnection, sql):
    dbCursor = dbConnection.cursor()
    dbCursor.execute(sql)
    rows = dbCursor.fetchall()
    return rows

def closeConnect(dbConnection):
    dbConnection.close()

if __name__ == '__main__':
    argParse = argparse.ArgumentParser(description="该脚本用于生产修改参数和新增参数")
    argParse.add_argument("-enviroment", dest="enviroment", help="需要修改的workflowId", default="dev")
    argParse.add_argument("-workflowId", dest="workflowId", help="需要修改的workflowId")
    argParse.add_argument("-paramName", dest="paramName", help="需要修改的参数名称")
    argParse.add_argument("-value", dest="value", help="修改的参数值")
    args = argParse.parse_args()
    argsDict = args.__dict__
    enviroment = argsDict.get("enviroment")
    workflowId = argsDict.get("workflowId")
    paramName = argsDict.get("paramName")
    value = argsDict.get("value")
    dbConfig = databaseConfig.get(enviroment)
    dbConnection = getConnection(dbConfig[0], dbConfig[1], dbConfig[2], dbConfig[3])
    queryParamSql = querySql%(paramName,workflowId)
    rows = executeSql(dbConnection, queryParamSql)
    if len(rows) is 0:
        print 'workflowId:%s和paramName:%s组合查找不到对应的数据,请检查输入参数是否正确'%(workflowId, paramName)
        closeConnect(dbConnection)
    elif len(rows) is not 1:
        print 'workflowId:%s和paramName:%s组合查到多条数据,数据错误,请联系开发检查'%(workflowId, paramName)
        closeConnect(dbConnection)
    else:
        paramValue = rows[0][0]
        print '请确认需要修改的参数值为: ', paramValue
        paramValueJson = json.loads(paramValue)
        paramValueJson['value']['value'] = value
        paramValueString = json.dumps(paramValueJson)
        print '请确认修改后的参数值为: ', paramValueString
        updateParamSql = updateSql%(paramValueString, paramName, workflowId)
        rows = executeSql(dbConnection, updateParamSql)
        dbConnection.commit()
        print '更新成功...'
        closeConnect(dbConnection)