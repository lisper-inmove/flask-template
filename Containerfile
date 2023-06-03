FROM python

WORKDIR /app

COPY require.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r require.txt
ENV PORT=19993
ENV R_ENABLE_REPLICA=true

COPY . .

CMD ["make", "uwsgi"]
