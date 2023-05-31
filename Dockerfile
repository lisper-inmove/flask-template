FROM python:3.10-slim

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install --yes --no-install-recommends libjemalloc2 protobuf-compiler
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2 MALLOC_CONF='background_thread:true,dirty_decay_ms:0,muzzy_decay_ms:0'
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV PYTHONPATH=/app

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN cd /app && protoc -I. --python_out=. proto/**/*.proto
RUN cd /app && protoc -I. --python_out=. api/*.proto

EXPOSE 6003