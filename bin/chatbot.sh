#!/bin/bash

source bin/util.sh
source bin/payment.sh

port=$(get_available_port)

echo "获取到的port: $port"

python app.py --port $port --host 0.0.0.0
