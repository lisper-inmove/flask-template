#!/bin/bash

if [ ! -f gproto/api.proto ];then
   echo "未找到文件 gproto/api.proto，服务启动失败"
   exit -1
fi

source bin/util.sh

port=$(get_available_port)

python gapp.py --port $port
