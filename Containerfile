FROM python

WORKDIR /app

COPY require.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r require.txt
ENV PORT=3001

COPY . .

CMD ["make", "uwsgi"]
