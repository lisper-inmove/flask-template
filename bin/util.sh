#!/bin/bash

# 项目名称
export APPNAME=demo
# 是否开启终端显示日志
export LOGGER_ENABLE_CONSOLE=true
# 是否开启syslog日志
export LOGGER_ENABLE_SYSLOG=false
# syslog日志服务器地址
export LOGGER_SYSLOG_HOST=logger.server
# syslog日志服务端口
export LOGGER_SYSLOG_PORT=514
# syslog日志设备
export LOGGER_SYSLOG_FACILITY=local7
# 服务启动环境
export RUNTIME_ENVIRONMENT=test

# For local test
# MongoDB数据库ip
export MONGODB_SERVER_ADDRESS=127.0.0.1
# MongoDB数据库端口
export MONGODB_PORT=27018

# For k8s
export R_MONGODB_SERVER_ADDRESS="mongodb-replica-0.mongodb-replica-headless.mongodb.svc.cluster.local"
export R_MONGODB_PORT=27017
export R_MONGODB_USER_NAME=root
export R_MONGODB_ROOT_PASSWORD=335f07030aaaa2f1f58a8796549b70a9
export R_MONGODB_REPLICA_SET=rs0
export R_MONGODB_MIN_POOL_SIZE=8
export R_MONGODB_MAX_POOL_SIZE=512
export R_MONGODB_REPLICA_SET_NUMBER=3


function get_available_port() {
    port=6003
    while true
    do
        declare -i flag
        flag=`lsof -i:$port | wc -l`
        if [ $((flag)) -eq 0 ];then
           break
        else
           ((port++))
        fi
    done
    echo $((port+0))
}
