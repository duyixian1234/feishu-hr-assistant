FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt
RUN set -xe \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

COPY ./ /code
WORKDIR /code
EXPOSE 8080
CMD ["sh","./run-web.sh"]
