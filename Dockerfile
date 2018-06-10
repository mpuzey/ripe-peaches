FROM python:3.6-alpine
MAINTAINER Matthew Puzey "mpuzey1@outlook.com"

RUN mkdir -p   /tmdb
COPY app /ripe-peaches/app
COPY main.py /ripe-peaches/main.py
COPY config.py /ripe-peaches/config.py
COPY requirements.txt /ripe-peaches/requirements.txt


WORKDIR /ripe-peaches
RUN apk add --update \
    py-pip

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "main.py"]
