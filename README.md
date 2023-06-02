# See README.org

# 测试环境启动

    make dev

# 正式环境启动

    PORT=19919 make prod

# docker build

    sudo docker build -t config-center . -f Containerfile

# docker run

    sudo docker run --rm -d --name config-center --network host config-center:latest

# Container文件修改

    1. 修改 port
