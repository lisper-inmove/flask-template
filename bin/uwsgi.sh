#!/bin/bash

source bin/util.sh

port=$1

echo "获取到的port: $port"

`sysctl -w net.core.somaxconn=32768`

generate_ini () {
    cat > bin/server.ini <<-EOF
    [uwsgi]
    http = 0.0.0.0:${port}

    strict = true
    module = app
    callable = app
    processes = 4
    master = true
    threads = 1
    pidfile = bin/uwsgi.pid
    vacuum = true
    reload-mercy = 1
    worker-reload-mercy = 1
    listen = 4096
EOF
}

generate_ini

`uwsgi --gevent 4096 --gevent-early-monkey-patch bin/server.ini`
