#!/bin/bash

source bin/util.sh

port=$1

echo "获取到的port: $port"

python app.py --port $port
